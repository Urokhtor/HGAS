<<<<<<< HEAD
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

#import matplotlib as mpl
from matplotlib import use
# Use Agg backend so rendering graphs can be done without a window system such as X.
#mpl.use("Agg", warn = False)
use("Agg", warn = False)
import matplotlib.pyplot as plt
from datetime import datetime
from Constants import SENSOR_TYPE_DEFAULT, SENSOR_TYPE_TEMPERATURE, SENSOR_TYPE_DHT11, SENSOR_TYPE_SR04, PLOT_DAY, PLOT_WEEK

class Plot:
    
    def __init__(self, parent):
        self.__name__ = "Plot"
        self.parent = parent
        self.folder = "Plots/"
    
    def generateSensorDailyPlot(self, sensorID):
        """
            Takes the ID of one sensor and then generates the daily data plot if it's found.
            
            Returns True if the plot was generated successfully and False if it failed.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + "generateSensorDailyPlot")
        
        files = self.parent.logging.getFiles()
        
        # Perhaps optimise this so that we only need to get that one file. Get the sensor object and
        # generate the file name out of that information since it's always the same.
        for file in files:
            if file.find(sensorID) != -1:
                self.parent.deviceManager.getSensorById(sensorID)
                try:
                    self.generateDay(self.parent.logging.getSensorFileData(file, PLOT_DAY), file.split(".csv")[0], sensor)
                    return True
                    
                except Exception as e:
                    self.parent.logging.logEvent("GenerateSensorDailyPlots ecountered an error: " + str(e) + ", sensor: " + sensor["name"], "red")
                    return False
                    
    def generateSensorWeeklyPlot(self, sensorID):
        """
            Takes the ID of one sensor and then generates the weekly data plot if it's found
            
            Returns True if the plot was generated successfully and False if it failed.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + "generateSensorWeeklyPlot")
        
        files = self.parent.logging.getFiles()
        
        # Perhaps optimise this so that we only need to get that one file. Get the sensor object and
        # generate the file name out of that information since it's always the same.
        for file in files:
            if file.find(sensorID) != -1:
                self.parent.deviceManager.getSensorById(sensorID)
                try:
                    self.generateWeek(self.parent.logging.getSensorFileData(file, PLOT_WEEK), file.split(".csv")[0], sensor)
                    return True
                    
                except Exception as e:
                    self.parent.logging.logEvent("GenerateSensorWeeklyPlots ecountered an error: " + str(e) + ", sensor: " + sensor["name"], "red")
                    return False

    def generateDailyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating daily plots for each of the
            sensors.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "generateDailyPlots")
        
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
                
            try:
                id = file.split("_")[0]
            except Exception as e:
                self.parent.logging.logEvent("Plot error: Misnamed file, error message: " + str(e), "red")
                continue
            
            # Perhaps we should use the deviceManager instead to get the sensor.
            for sensor in self.parent.deviceManager.getSensors():
                if sensor["id"] == int(id):
                    try:
                        # Fetch the logging data, parse it so that only 24 hours worth of data is left and pass the data
                        # to generateDay which generates the plot for daily data.
                        self.generateDay(self.parent.logging.getSensorFileData(file, PLOT_DAY), file.split(".csv")[0], sensor)
                        
                    except Exception as e:
                        self.parent.logging.logEvent("Generate daily plots error: " + str(e) + ", file: " + file, "red")
                    
                    break
                    
    def generateWeeklyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating weekly plots for each of the
            sensors.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "generateWeeklyPlots")
        
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
                
            try:
                id = file.split("_")[0]
            
            except Exception as e:
                self.parent.logging.logEvent("Plot error: Misnamed file, error message: " + str(e), "red")
                continue
                
            # Perhaps we should use the deviceManager instead to get the sensor.
            for sensor in self.parent.deviceManager.getSensors():
                if sensor["id"] == int(id):
                    try:
                        # Fetch the logging data, parse it so that only week's worth of data is left and pass the data
                        # to generateDay which generates the plot for weekly data.
                        self.generateWeek(self.parent.logging.getSensorFileData(file, PLOT_WEEK), file.split(".csv")[0], sensor)
                    
                    except Exception as e:
                        self.parent.logging.logEvent("Generate weekly plots error: " + str(e) + ", file: " + file, "red")
                        
                    break
                    
    def generateDay(self, data, file, sensor):
        self.parent.logging.logDebug(self.__name__ + "." + "generateDay")
        
        currTime = data[0][0]
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        
        x = []
        y = [] # Y axis.
        
        total = 0
        index = 0
        
        # Map the y- and x-axis values to lists.
        for time, measurement in data:
            yTmp = measurement
            
            # Do a little adjustment to smoothen the graph (sensors aren't absolute).
            if index > 0 and index < (len(data)-1):
                lastReading = data[index-1][1]
                nextReading = data[index+1][1]
                yTmp = (yTmp + lastReading + nextReading)/3

            y.append(yTmp)
            
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
             
            total += yTmp
            index += 1

            x.append(time)
        
        # Determine how mux additional y axis space there needs to be.
        delta = yMax - yMin
        maxBoundary = yMax
        minBoundary = yMin
        
        if delta == 0: delta = 2
        
        yMax += delta * 0.2
        yMin -= delta * 0.2
        
        plt.figure()
        plt.plot(x, y) # Draw the actual plot.
        plt.grid(True) # Draw grids to help reading the plot.
        plt.suptitle("Last 24 h")
        plt.title(sensor["name"])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if sensor["type"] == SENSOR_TYPE_DEFAULT:
            type = "Hygrometer reading"
        elif sensor["type"] == SENSOR_TYPE_DHT11:
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif sensor["type"] == SENSOR_TYPE_TEMPERATURE:
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif sensor["type"] == SENSOR_TYPE_SR04:
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        lista = [] # x-axis location
        timeObject = datetime.fromtimestamp(currTime)
        closestHourOffset = timeObject.minute * 60 + timeObject.second 
        lastReading = currTime - closestHourOffset
        lastHour = timeObject.hour
        tmpHours = []
        lista.append(lastReading)
        tmpHours.append(lastHour)
        
        for i in range(0, 11):
            lastReading -= 120*60 # Calculate the previous hour's position.
            lista.append(lastReading) # Append it.
            
            lastHour -= 2 # We want to draw the hours with 2 hour interval, i.e. 0, 2, 4, 6...
            
            # Handle day change.
            if lastHour == -1:
                lastHour = 23
            
            elif lastHour == -2:
                lastHour = 22
            
            # Add hour value which is mapped to the same index as the corresponding x-axis value
            # that we added to lista.
            tmpHours.append(lastHour)
            
        plt.ylabel(type) # Sensor's type goes here.
        plt.xlabel("Time")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction") # Text inside the plot area telling some info.
        plt.xticks(lista, tmpHours) # Set x axis and give its elements time names.
        location = (self.folder + "day-" + file).replace(" ", "")
        plt.savefig(location, transparent=True) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
        
    def generateWeek(self, data, file, sensor):
        self.parent.logging.logDebug(self.__name__ + "." + "generateWeek")
        
        currTime = data[0][0]
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        x = []
        y = [] # Y axis.
        total = 0
        index = 0
        
        # Map the y- and x-axis values to lists.
        for time, measurement in data:
            yTmp = measurement
            
            # Do a little adjustment to smoothen the graph (sensors aren't absolute).
            if index > 0 and index < (len(data)-1):
                lastReading = data[index-1][1]
                nextReading = data[index+1][1]
                yTmp = (yTmp + lastReading + nextReading)/3

            y.append(yTmp)
            
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
             
            total += yTmp
            index += 1

            x.append(time)
        
        # Determine how mux additional y axis space there needs to be.
        delta = yMax - yMin
        maxBoundary = yMax
        minBoundary = yMin
        
        if delta == 0: delta = 2
        
        yMax += delta * 0.4
        yMin -= delta * 0.4
        
        plt.figure()
        plt.plot(x, y) # Draw the actual plot.
        plt.grid(True) # Draw grids to help reading the plot.
        plt.suptitle("Last 7 days")
        plt.title(sensor["name"])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if sensor["type"] == SENSOR_TYPE_DEFAULT:
            type = "Hygrometer reading"
        elif sensor["type"] == SENSOR_TYPE_DHT11:
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif sensor["type"] == SENSOR_TYPE_TEMPERATURE:
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif sensor["type"] == SENSOR_TYPE_SR04:
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        timeObject = datetime.fromtimestamp(currTime)
        lastDay = timeObject.day
        currMonth = timeObject.month
        closestDayOffset = timeObject.hour * 60 * 60 + timeObject.minute * 60 + timeObject.second
        lastReading = currTime - closestDayOffset
        interval = 86400
        tmpDays = []
        lista = []
        lista.append(lastReading)
        tmpDays.append(lastDay)
        
        for i in range(0, 6):
            lastReading -= interval
            lista.append(lastReading)
            
            lastDay -= 1
            
            if lastDay <= 0:
                if currMonth-1 in [1, 3, 5, 7, 8, 10, 23]: lastDay = 31
                elif  currMonth-1 in [4, 6, 9, 11]: lastDay = 30
                else: lastDay = 28
                
            tmpDays.append(lastDay)
            
        plt.ylabel(type)
        plt.xlabel("Day")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction")
        plt.xticks(lista, tmpDays) # Set x axis and give its elements time names.
        location = (self.folder + "week-" + file).replace(" ", "")
        plt.savefig(location, transparent=True) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
=======
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

#import matplotlib as mpl
from matplotlib import use
# Use Agg backend so rendering graphs can be done without a window system such as X.
#mpl.use("Agg", warn = False)
use("Agg", warn = False)
import matplotlib.pyplot as plt
from datetime import datetime
from Constants import SENSOR_TYPE_DEFAULT, SENSOR_TYPE_TEMPERATURE, SENSOR_TYPE_DHT11, SENSOR_TYPE_SR04, PLOT_DAY, PLOT_WEEK

class Plot:
    
    def __init__(self, parent):
        self.__name__ = "Plot"
        self.parent = parent
        self.folder = "Plots/"
    
    def generateSensorDailyPlot(self, sensorID):
        """
            Takes the ID of one sensor and then generates the daily data plot if it's found.
            
            Returns True if the plot was generated successfully and False if it failed.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + "generateSensorDailyPlot")
        
        files = self.parent.logging.getFiles()
        
        # Perhaps optimise this so that we only need to get that one file. Get the sensor object and
        # generate the file name out of that information since it's always the same.
        for file in files:
            if file.find(sensorID) != -1:
                self.parent.deviceManager.getSensorById(sensorID)
                try:
                    self.generateDay(self.parent.logging.getSensorFileData(file, PLOT_DAY), file.split(".csv")[0], sensor)
                    return True
                    
                except Exception as e:
                    self.parent.logging.logEvent("GenerateSensorDailyPlots ecountered an error: " + str(e) + ", sensor: " + sensor["name"], "red")
                    return False
                    
    def generateSensorWeeklyPlot(self, sensorID):
        """
            Takes the ID of one sensor and then generates the weekly data plot if it's found
            
            Returns True if the plot was generated successfully and False if it failed.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + "generateSensorWeeklyPlot")
        
        files = self.parent.logging.getFiles()
        
        # Perhaps optimise this so that we only need to get that one file. Get the sensor object and
        # generate the file name out of that information since it's always the same.
        for file in files:
            if file.find(sensorID) != -1:
                self.parent.deviceManager.getSensorById(sensorID)
                try:
                    self.generateWeek(self.parent.logging.getSensorFileData(file, PLOT_WEEK), file.split(".csv")[0], sensor)
                    return True
                    
                except Exception as e:
                    self.parent.logging.logEvent("GenerateSensorWeeklyPlots ecountered an error: " + str(e) + ", sensor: " + sensor["name"], "red")
                    return False

    def generateDailyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating daily plots for each of the
            sensors.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "generateDailyPlots")
        
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
                
            try:
                id = file.split("_")[0]
            except Exception as e:
                self.parent.logging.logEvent("Plot error: Misnamed file, error message: " + str(e), "red")
                continue
            
            # Perhaps we should use the deviceManager instead to get the sensor.
            for sensor in self.parent.deviceManager.getSensors():
                if sensor["id"] == int(id):
                    try:
                        # Fetch the logging data, parse it so that only 24 hours worth of data is left and pass the data
                        # to generateDay which generates the plot for daily data.
                        self.generateDay(self.parent.logging.getSensorFileData(file, PLOT_DAY), file.split(".csv")[0], sensor)
                        
                    except Exception as e:
                        self.parent.logging.logEvent("Generate daily plots error: " + str(e) + ", file: " + file, "red")
                    
                    break
                    
    def generateWeeklyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating weekly plots for each of the
            sensors.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "generateWeeklyPlots")
        
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
                
            try:
                id = file.split("_")[0]
            
            except Exception as e:
                self.parent.logging.logEvent("Plot error: Misnamed file, error message: " + str(e), "red")
                continue
                
            # Perhaps we should use the deviceManager instead to get the sensor.
            for sensor in self.parent.deviceManager.getSensors():
                if sensor["id"] == int(id):
                    try:
                        # Fetch the logging data, parse it so that only week's worth of data is left and pass the data
                        # to generateDay which generates the plot for weekly data.
                        self.generateWeek(self.parent.logging.getSensorFileData(file, PLOT_WEEK), file.split(".csv")[0], sensor)
                    
                    except Exception as e:
                        self.parent.logging.logEvent("Generate weekly plots error: " + str(e) + ", file: " + file, "red")
                        
                    break
                    
    def generateDay(self, data, file, sensor):
        self.parent.logging.logDebug(self.__name__ + "." + "generateDay")
        
        currTime = data[0][0]
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        
        x = []
        y = [] # Y axis.
        
        total = 0
        index = 0
        
        # Map the y- and x-axis values to lists.
        for time, measurement in data:
            yTmp = measurement
            
            # Do a little adjustment to smoothen the graph (sensors aren't absolute).
            if index > 0 and index < (len(data)-1):
                lastReading = data[index-1][1]
                nextReading = data[index+1][1]
                yTmp = (yTmp + lastReading + nextReading)/3

            y.append(yTmp)
            
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
             
            total += yTmp
            index += 1

            x.append(time)
        
        # Determine how mux additional y axis space there needs to be.
        delta = yMax - yMin
        maxBoundary = yMax
        minBoundary = yMin
        
        if delta == 0: delta = 2
        
        yMax += delta * 0.2
        yMin -= delta * 0.2
        
        plt.figure()
        plt.plot(x, y) # Draw the actual plot.
        plt.grid(True) # Draw grids to help reading the plot.
        plt.suptitle("Last 24 h")
        plt.title(sensor["name"])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if sensor["type"] == SENSOR_TYPE_DEFAULT:
            type = "Hygrometer reading"
        elif sensor["type"] == SENSOR_TYPE_DHT11:
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif sensor["type"] == SENSOR_TYPE_TEMPERATURE:
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif sensor["type"] == SENSOR_TYPE_SR04:
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        lista = [] # x-axis location
        timeObject = datetime.fromtimestamp(currTime)
        closestHourOffset = timeObject.minute * 60 + timeObject.second 
        lastReading = currTime - closestHourOffset
        lastHour = timeObject.hour
        tmpHours = []
        lista.append(lastReading)
        tmpHours.append(lastHour)
        
        for i in range(0, 11):
            lastReading -= 120*60 # Calculate the previous hour's position.
            lista.append(lastReading) # Append it.
            
            lastHour -= 2 # We want to draw the hours with 2 hour interval, i.e. 0, 2, 4, 6...
            
            # Handle day change.
            if lastHour == -1:
                lastHour = 23
            
            elif lastHour == -2:
                lastHour = 22
            
            # Add hour value which is mapped to the same index as the corresponding x-axis value
            # that we added to lista.
            tmpHours.append(lastHour)
            
        plt.ylabel(type) # Sensor's type goes here.
        plt.xlabel("Time")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction") # Text inside the plot area telling some info.
        plt.xticks(lista, tmpHours) # Set x axis and give its elements time names.
        location = (self.folder + "day-" + file).replace(" ", "")
        plt.savefig(location, transparent=True) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
        
    def generateWeek(self, data, file, sensor):
        self.parent.logging.logDebug(self.__name__ + "." + "generateWeek")
        
        currTime = data[0][0]
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        x = []
        y = [] # Y axis.
        total = 0
        index = 0
        
        # Map the y- and x-axis values to lists.
        for time, measurement in data:
            yTmp = measurement
            
            # Do a little adjustment to smoothen the graph (sensors aren't absolute).
            if index > 0 and index < (len(data)-1):
                lastReading = data[index-1][1]
                nextReading = data[index+1][1]
                yTmp = (yTmp + lastReading + nextReading)/3

            y.append(yTmp)
            
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
             
            total += yTmp
            index += 1

            x.append(time)
        
        # Determine how mux additional y axis space there needs to be.
        delta = yMax - yMin
        maxBoundary = yMax
        minBoundary = yMin
        
        if delta == 0: delta = 2
        
        yMax += delta * 0.4
        yMin -= delta * 0.4
        
        plt.figure()
        plt.plot(x, y) # Draw the actual plot.
        plt.grid(True) # Draw grids to help reading the plot.
        plt.suptitle("Last 7 days")
        plt.title(sensor["name"])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if sensor["type"] == SENSOR_TYPE_DEFAULT:
            type = "Hygrometer reading"
        elif sensor["type"] == SENSOR_TYPE_DHT11:
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif sensor["type"] == SENSOR_TYPE_TEMPERATURE:
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif sensor["type"] == SENSOR_TYPE_SR04:
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        timeObject = datetime.fromtimestamp(currTime)
        lastDay = timeObject.day
        currMonth = timeObject.month
        closestDayOffset = timeObject.hour * 60 * 60 + timeObject.minute * 60 + timeObject.second
        lastReading = currTime - closestDayOffset
        interval = 86400
        tmpDays = []
        lista = []
        lista.append(lastReading)
        tmpDays.append(lastDay)
        
        for i in range(0, 6):
            lastReading -= interval
            lista.append(lastReading)
            
            lastDay -= 1
            
            if lastDay <= 0:
                if currMonth-1 in [1, 3, 5, 7, 8, 10, 23]: lastDay = 31
                elif  currMonth-1 in [4, 6, 9, 11]: lastDay = 30
                else: lastDay = 28
                
            tmpDays.append(lastDay)
            
        plt.ylabel(type)
        plt.xlabel("Day")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction")
        plt.xticks(lista, tmpDays) # Set x axis and give its elements time names.
        location = (self.folder + "week-" + file).replace(" ", "")
        plt.savefig(location, transparent=True) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
>>>>>>> cbd3bf5dabe3e29b4f5be216a7b15ab66f6732ef
