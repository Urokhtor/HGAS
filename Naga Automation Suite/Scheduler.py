"""
    Naga Automation Suite - an automation system for home gardens
    Copyright (C) 2013  Jere Teittinen
    
    Author: Jere Teittinen <j.teittinen@luukku.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from threading import Thread, RLock
from time import strftime, sleep
from datetime import datetime
from queue import Queue
import traceback

class Scheduler:
    """
        The scheduler handles executing timed tasks, such as operating pumps and lights and
        reading sensor data.
    """
    
    def __init__(self):
        self.running = True
        self.midnightReset = False
        self.taskManager = TaskManager()
        
        self.updateThread = None
    
    def initialize(self):
        """
            Initialize the scheduler by starting the thread.
        """
        
        self.updateThread = Thread(target=self.update).start()
        #self.taskManager.findNextTask()
    
    def terminate(self):
        self.running = False
    
    def update(self):
        """
            Checks the current time and compares it to the next task time that is in queue, if we've
            reached it, executes the task(s) and finds a next one.
        """
        
        while self.running:
            try:
                currTime = datetime.now().time()
                currentTimeSeconds = currTime.hour*60*60 + currTime.minute*60 + currTime.second

                # Reset the task manager around midnight, otherwise tasks won't execute again.
                if currentTimeSeconds < 60 and not self.midnightReset:
                    self.taskManager.resetTasks()
                    self.taskManager.findNextTask(currTime)
                    self.midnightReset = True
                    
                if currentTimeSeconds >= self.taskManager.getNextTaskTime() and not self.taskManager.getNextTaskIsExecuted():
                    # Reset midnightReset if we're past the first minute of the day so that the task resetting
                    # will work after the next midnight.
                    if self.midnightReset and currentTimeSeconds > 60:
                        self.midnightReset = False
                        
                    self.taskManager.executeNextTask()
                    self.taskManager.findNextTask(currTime)
                    
            except Exception as e:
                print("Scheduler error: " + str(e))
                traceback.print_exc()
                continue
                
            sleep(0.1)
        
class TaskManager:
    """
        Handles routines for adding, removing, accessing and executing tasks.
    """
    
    def __init__(self):
        self.tasks = [] # List for all the stored tasks
        self.nextTask = [] # Copies of the task(s) that need to be executed next.
        self.nextTaskQueue = Queue()
        self.nextTaskTime = 0 # At which time the next task(s) need to be executed.
        self.nextTaskIsExecuted = False # Without this the scheduler goes mad if it has already executed all the tasks for the day.
    
    def addTask(self, task):
        """
            Adds a new task and then checks which task(s) needs to be executed next. Returns false if task
            already exists.
        """
        
        if self.hasTask(task.getName()):
            return False
            
        self.tasks.append(task)
        self.findNextTask()
        return True
    
    def getTask(self, name):
        """
            Finds and returns task with given name. If task with that name can't be found, returns None.
        """
        
        for task in self.tasks:
            if task.getName() == name:
                return task
        
        return None
    
    def hasTask(self, name):
        """
            Returns true if task with given name exists. Returns false if it doesn't exist.
        """
        
        for task in self.tasks:
            if task.getName() == name:
                return True
                
        return False
    
    def removeTask(self, name):
        """
            Removes task with given name, finds next task(s) to be executed and returns true. Returns
            false if task can't be found.
        """
        
        if not self.hasTask(name):
            return False
            
        for task in self.tasks:
            if task.getName() == name:
                self.tasks.remove(task)
                self.findNextTask()
                return True
    
    def executeNextTask(self):
        """
            Executes tasks in next task queue and marks the event executed. Also handles removing temporary
            tasks if all their events have been executed.
        """
        
        while not self.nextTaskQueue.empty():
            task = self.nextTaskQueue.get()
            
            # Skip task if current time can't be found but task is scheduled for some reason.
            if not self.nextTaskTime in task.getScheduledEvents():
                continue
            
            # If task's current event isn't executed yet, try to execute the callback function.
            if not task.getEventIsExecuted(self.nextTaskTime):
                try:
                    task.executeCallBack()
                except Exception as e:
                    raise RuntimeError(str(e))
                
                # Mark event executed so it won't be executed a second time.
                task.markEventExecuted(self.nextTaskTime)
                
                # If task is temporary and all of its events have been executed, remove it.
                if task.getAllEventsExecuted() and not task.isPermanent():
                    self.tasks.remove(task)
                    continue
        
        # Tells scheduler that all tasks are executed if set to true. Prevents tasks from executing after all
        # of their daily events have been executed. If findNextTask() find tasks who have events left to be
        # executed, this flag is set to false.
        self.nextTaskIsExecuted = True
    
    def findNextTask(self, currTime = None):
        """
            After executing last task(s) search for ones to be scheduled next.
        """
        
        self.emptyNextTaskList()
        self.nextTaskTime = 0
        self.nextTaskIsExecuted = False
        
        if currTime == None:
            currTime = datetime.now().time()
            
        currentTimeSeconds = currTime.hour*60*60 + currTime.minute*60 + currTime.second
        
        for task in self.tasks:
            events = task.getScheduledEvents()
            
            for time, executed in events.items():
                taskTimeInt = time
                
                if len(self.nextTask) == 0 and not executed:
                    self.nextTask.append(task)
                    self.nextTaskTime = taskTimeInt
                    continue
                    
                elif taskTimeInt > currentTimeSeconds and taskTimeInt < self.nextTaskTime and not executed:
                    self.emptyNextTaskList()
                    self.nextTask.append(task)
                    self.nextTaskTime = taskTimeInt
                    continue
                
                elif taskTimeInt >= currentTimeSeconds and taskTimeInt == self.nextTaskTime and not executed:
                    self.nextTask.append(task)
                    continue
        
        # All of current day's task events have been executed, this flag prevents scheduler from trying to
        # execute tasks anymore during that day.
        if len(self.nextTask) == 0:
            self.nextTaskIsExecuted = True
        
        # This routine is quite ineffective, but in normal conditions there won't be too many tasks in the system
        # so it's OK. It fills the nextTaskQueue one by one, taking into account task's priority. Executing first
        # the task(s) with lowest priority.
        for task in self.nextTask[:]:
            if task.getPriority() == 0:
                self.nextTaskQueue.put(task)
                self.nextTask.remove(task)
                
        for task in self.nextTask[:]:
            if task.getPriority() == 1:
                self.nextTaskQueue.put(task)
                self.nextTask.remove(task)
                
        for task in self.nextTask[:]:
            if task.getPriority() == 2:
                self.nextTaskQueue.put(task)
                self.nextTask.remove(task)   
                
        for task in self.nextTask[:]:
            if task.getPriority() == 3:
                self.nextTaskQueue.put(task)
                self.nextTask.remove(task)
        
    def resetTasks(self):
        """
            Loop through all tasks and set all scheduled events as not-executed. Should be called at midnight.
        """
        
        for task in self.tasks:
            if not task.isPermanent():
                continue
                
            events = task.getScheduledEvents()
            
            for time in events:
                task.scheduledEvents[time] = False
        
    def emptyNextTaskList(self):
        """
            Empty the list so there won't be anything left in the list when new nextTask(s) are added.
        """
        
        self.nextTask[:] = []
        
    def getNextTaskTime(self):
        """
            Tells the time at which next task(s) need to be executed.
        """
        
        return self.nextTaskTime
        
    def getNextTaskIsExecuted(self):
        """
            Mainly tells the scheduler whether all the current day's tasks have been executed so it won't
            try to execute them anymore.
        """
        
        return self.nextTaskIsExecuted
    
class Task:
    
    def __init__(self, name, action, priority, callBack = None, _isPermanent = True):
        self.name = name
        self.action = action
        self.priority = priority
        self.callBack = callBack
        self._isPermanent = _isPermanent
        self.scheduledEvents = {}
        self.mutex = RLock()
    
    def getName(self):
        """
            Returns the name of the task.
        """
        
        return self.name
    
    def getAction(self):
        """
            The action to be passed as a parameter to the callback function. It can be for example a protocol
            message to be passed to send().
        """
        
        return self.action
    
    def getPriority(self):
        """
            Returns the priority set to this task. Lower value means it needs to be executed more urgently.
            Currently priorities 0-3 are supported. Tasks added by the user should use priority 1.
        """
        
        return self.priority
        
    def executeCallBack(self):
        """
            Executes the callback function registered for this task.
        """
        
        self.mutex.acquire()
        if self.callBack is not None:
            try:
                self.callBack(self.action)
            except Exception as e:
                raise RuntimeError("Scheduler task " + self.name + " encountered an exception: " + str(e))
                
        self.mutex.release()
    
    def isPermanent(self):
        """
            Returns whether the task is permanent or temporary. Temporary tasks are removed after all their
            events have been executed.
        """
        
        return self._isPermanent
        
    def getScheduledEvents(self):
        """
            Returns the scheduled event times at chich the task will be executed.
        """
        
        return self.scheduledEvents
        
    def addScheduledEvent(self, time):
        """
            Adds a new scheduled event to the task a checks if it should've been executed yet or not, then
            sets that value to keep the scheduler happy.
        """
        
        currentTime = strftime("%H %M %S").split(" ")
        currentTimeInt = int(currentTime[0])*60*60 + int(currentTime[1])*60 + int(currentTime[2])
        
        self.mutex.acquire()
        if time > currentTimeInt: self.scheduledEvents[time] = False
        else: self.scheduledEvents[time] = True
        self.mutex.release()
    
    def removeScheduledEvent(self, time):
        """
            Removes one scheduled event.
        """
        
        # This really should be made safer so we don't accidentally try to remove a time that doesn't exist.
        self.mutex.acquire()
        del self.scheduledEvents[time]
        self.mutex.release()
    
    def removeAllScheduledEvents(self):
        """
            Clears the scheduled events list.
        """
        
        self.mutex.acquire()
        self.scheduledEvents.clear()
        self.mutex.release()
        
    def markEventExecuted(self, time):
        """
            Marks event with given time executed.
        """
        
        # This too should be made safer by implementing some functionality that checks whether the given
        # time exists. However currently this is done in the task manager so it works right.
        self.mutex.acquire()
        self.scheduledEvents[time] = True
        self.mutex.release()
        
    def getAllEventsExecuted(self):
        """
            Return false is all events have not been executed yet, return true in the other case.
        """
        
        flag = True
        self.mutex.acquire()
        for time in self.scheduledEvents.keys():
            if self.scheduledEvents[time] is False:
                flag = False
        
        self.mutex.release()
        return flag
        
    def getEventIsExecuted(self, time):
        """
            Returns whether the event with given time is executed on current day.
        """
        
        return self.scheduledEvents[time]

    def scheduleByEvents(self, events):
        for time in events:
            try:
                hour, minute = time.split(":")
                if int(hour) > 23 or int(hour) < 0 or int(minute) > 60 or int(minute) < 0:
                    self.parent.logging.logEvent("Task error: Scheduled time " + time + " is not valid in task " + self.name, "red")
                    continue

                else:
                    taskTime = int(hour)*60*60 + int(minute)*60
                    self.addScheduledEvent(taskTime)

            except:
                self.parent.logging.logEvent("Task error: Scheduled time " + time + " is not valid in task " + self.name, "red")
                continue

    def scheduleByInterval(self, interval):
        time = 0
        # UPDATE THESE TO USE A MANAGER
        timeInterval = interval*60

        while time < 86400:
            self.addScheduledEvent(time)
            time += timeInterval