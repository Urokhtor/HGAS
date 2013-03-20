from Connection import Connection
from threading import Thread
from time import strftime
from time import sleep

class Scheduler:
    """
        The scheduler handles executing timed tasks, such as operating pumps and lights and
        reading sensor data.
    """
    
    def __init__(self):
        self.running = True
        self.taskManager = TaskManager()
        
        self.updateThread = Thread(target=self.update)
        self.updateThread.start()
    
    def initialize(self):
        """
            In the beginning check through tasks and find the task event that needs to be executed
            the soonest.
        """
        
        self.taskManager.findNextTask()
    
    def terminate(self):
        self.running = False
    
    def update(self):
        """
            Checks the current time and compares it to the next task time that is in queue, if we've
            reached it, executes the task(s) and finds a next one.
        """
        
        while self.running:
            currentTime = strftime("%H %M %S").split(" ")
            currentTimeInt = int(currentTime[0])*60*60 + int(currentTime[1])*60 + int(currentTime[2])

            # Reset the task manager around midnight, otherwise tasks won't execute again.
            if currentTimeInt == 0:
                self.taskManager.resetTasks()
                
            if currentTimeInt >= self.taskManager.getNextTaskTime() and not self.taskManager.getNextTaskIsExecuted():
                self.taskManager.executeNextTask()
                self.taskManager.findNextTask()
                
            sleep(1)
        
class TaskManager:
    """
        Handles routines for adding, removing, accessing and executing tasks.
    """
    
    def __init__(self):
        self.tasks = [] # List for all the stored tasks
        self.nextTask = [] # Copies of the task(s) that need to be executed next.
        self.nextTaskTime = 0 # At which time the next task(s) need to be executed.
        self.nextTaskIsExecuted = False # Without this the scheduler goes mad if it has already executed all the tasks for the day.
    
    def addTask(self, task):
        if self.hasTask(task.getName()):
            return False
            
        self.tasks.append(task)
        self.findNextTask()
        return True
    
    def getTask(self, name):
        for task in self.tasks:
            if task.getName() == name:
                return task
    
    def hasTask(self, name):
        for task in self.tasks:
            if task.getName() == name:
                return True
                
        return False
    
    def removeTask(self, name):
        if not self.hasTask(name):
            return False
            
        for task in self.tasks:
            if task.getName() == name:
                self.tasks.remove(task)
                return True
    
    def executeNextTask(self):
        for task in self.nextTask:
            if not task.getEventIsExecuted(self.nextTaskTime):
                task.executeCallBack()
                task.markEventExecuted(self.nextTaskTime)
        self.nextTaskIsExecuted = True
    
    def findNextTask(self):
        """
            After executing last task(s) search for ones scheduled next.
        """
        
        self.emptyNextTaskList()
        self.nextTaskTime = 0
        self.nextTaskIsExecuted = False
        currentTime = strftime("%H %M %S").split(" ")
        currentTimeInt = int(currentTime[0])*60*60 + int(currentTime[1])*60 + int(currentTime[2])
        
        for task in self.tasks:
            events = task.getScheduledEvents()
            
            for time, executed in events.items():
                taskTimeInt = time
                
                if len(self.nextTask) == 0 and not executed:
                    self.nextTask.append(task)
                    self.nextTaskTime = taskTimeInt
                    continue
                    
                elif taskTimeInt > currentTimeInt and taskTimeInt < self.nextTaskTime and not executed:
                    self.emptyNextTaskList()
                    self.nextTask.append(task)
                    self.nextTaskTime = taskTimeInt
                    continue
                
                elif taskTimeInt >= currentTimeInt and taskTimeInt == self.nextTaskTime and not executed:
                    self.nextTask.append(task)
                    continue
            
        if len(self.nextTask) == 0:
            self.nextTaskIsExecuted = True
        
    def resetTasks(self):
        """
            Loop through all tasks and set all scheduled events as not-executed.
        """
        
        for task in self.tasks:
            events = task.getScheduledEvents()
            
            for time in events:
                task.scheduledEvents[time] = False
        
        self.findNextTask()
        
    def emptyNextTaskList(self):
        self.nextTask[:] = []
        
    def getNextTaskTime(self):
        return self.nextTaskTime
        
    def getNextTaskIsExecuted(self):
        return self.nextTaskIsExecuted
    
class Task:
    
    def __init__(self, name, action, port, callBack = None):
        self.name = name
        self.action = action
        self.port = port
        self.callBack = callBack
        self.scheduledEvents = {}
    
    def getName(self):
        return self.name
    
    def getAction(self):
        return self.action
    
    def getPort(self):
        return self.port
        
    def executeCallBack(self):
        if self.callBack != None: self.callBack(self.action)
    
    def getScheduledEvents(self):
        return self.scheduledEvents
        
    def addScheduledEvent(self, time):
        currentTime = strftime("%H %M %S").split(" ")
        currentTimeInt = int(currentTime[0])*60*60 + int(currentTime[1])*60 + int(currentTime[2])
        
        if time > currentTimeInt: self.scheduledEvents[time] = False
        else: self.scheduledEvents[time] = True
    
    def removeScheduledEvent(self, time):
        del self.scheduledEvents[time]
    
    def removeAllScheduledEvents(self):
        self.scheduledEvents[:] = []
        
    def markEventExecuted(self, time):
        self.scheduledEvents[time] = True
        
    def getEventIsExecuted(self, time):
        return self.scheduledEvents[time]