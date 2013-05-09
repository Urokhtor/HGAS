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

import matplotlib as mpl
# Use Agg backend so rendering graphs can be done without a window system such as X.
mpl.use("Agg", warn = False)
import matplotlib.pyplot as plt
from time import strftime

class Plot:
    
    def __init__(self, parent):
        self.parent = parent
        self.folder = "Plots/"

    def generateDailyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating daily plots for each of the
            sensors.
        """
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
            
            try:
                # Fetch the logging data, parse it so that only 24 hours worth of data is left and pass the data
                # to generateDay which generates the plot for daily data.
                self.generateDay(self.generateDayData(self.parent.logging.getFileData(file)), file.split(".csv")[0])
                
            except Exception as e:
                self.parent.logging.logEvent("Generate daily plots error: " + str(e), "red")
                
    def generateWeeklyPlots(self, params):
        """
            Fetches the sensor logging files and loops through them, generating weekly plots for each of the
            sensors.
        """
        
        files = self.parent.logging.getFiles()
         
        for file in files:
            if file == "eventlog.csv":
                continue

            if file.find("test") != -1:
                continue
            
            try:
                # Fetch the logging data, parse it so that only week's worth of data is left and pass the data
                # to generateDay which generates the plot for weekly data.
                self.generateWeek(self.generateWeekData(self.parent.logging.getFileData(file)), file.split(".csv")[0])
            
            except Exception as e:
                self.parent.logging.logEvent("Generate weekly plots error: " + str(e), "red")
                
    def generateDay(self, data, file):
        currTime = data[0][1].split(":", 3)
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        # X axis. Times stored here should be minutes, first element being that last/current minute.
        # Meaning if 3.3. 19:00 was the starting point of our data and 4.3. 19:00 was the end point,
        # then the last element of x should be 0 minutes (starting point of logging) and first element
        # the end point of logging (~1440 minutes).
        x = []
        y = [] # Y axis.
        previousTime = int(currTime[0])*60 + int(currTime[1]) # Time in minutes of the last element.
        i = 1440# - int(currTime[1]) # The current minute value.
        total = 0
        index = 0
        
        for day, time, measurement in data:
            yTmp = float(measurement.replace("\n", ""))
            
            if not index == 0 and index < (len(data)-1):
                lastReading = float(data[index-1][2].replace("\n", ""))
                nextReading = float(data[index+1][2].replace("\n", ""))
                yTmp = (yTmp + lastReading + nextReading)/3

            y.append(yTmp)
            
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
             
            total += yTmp
            index += 1
            
            tmpTime = time.split(":")
            currHour = int(tmpTime[0])

            x.append(i)
            
            # Time of the current set of data.
            lineTime = time.split(":")
            lineCurrTime = int(lineTime[0])*60 + int(lineTime[1])
            
            if previousTime - lineCurrTime != 0:
                # If this is triggered then the day of the read data has changed (i.e. from 4.3. to 3.3.)
                # which makes normally determining the time interval impossible, so let's just use the
                # last interval between measurements.
                if lineCurrTime > previousTime:
                    i -= (1440 - lineCurrTime) + previousTime
                    previousTime = lineCurrTime
                    continue
                    
                i -= previousTime - lineCurrTime 
                previousTime = lineCurrTime
        
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
        plt.title(file.split("-")[0])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        # The type of sensor ends the sensor logging data file name. Check the type and choose an appropriate
        # title for the y axis.
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if file.endswith("hygrometer"):
            type = "Hygrometer reading"
        elif file.endswith("humidity"):
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif file.endswith("temp"):
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif file.endswith("ultrasound"):
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        lista = []
        lastReading = x[0] - int(currTime[1])
        lastHour = int(data[0][1].split(":", 1)[0])
        tmpHours = []
        
        for i in range(0, 12):
            lista.append(lastReading)
            lastReading -= 120
            
            tmpHours.append(lastHour)
            lastHour -= 2
            
            if lastHour == -1:
                lastHour = 23
            
            elif lastHour == -2:
                lastHour = 22
            
        plt.ylabel(type)
        plt.xlabel("Time")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction")
        plt.xticks(lista, tmpHours) # Set x axis and give its elements time names.
        location = (self.folder + "day-" + file).replace(" ", "")
        plt.savefig(location) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
        
    def generateDayData(self, data):
        """
            Generates a list of data for last 24 h of logging.
            Argument taken is all logging data.
        """
        
        currDay = data[0][0].split(".")
        currTime = data[0][1].split(":")
        startTime = int(currTime[0])*60 + int(currTime[1]) # Time in minutes of the first element.
        previousTime = startTime
        holder = [] # Read the data we need into this holder.
        
        # Data is read in descending order (newest measurement first). If newest measurement was taken
        # for example at 19:00, then the last measurement we need is 19:00 the day before. dayChanged
        # keeps track of the day the measurement was taken when compared to the newest one. This tells
        # the loop that is day has changed and the current line's time is less than 19:00, then we've
        # got everything we need and we sould return holder.
        dayChanged =  False
        holder.append(data[0]) # Fill holder with one element so dayChange works.
        
        for line in data[1:]:
            lineTime = line[1].split(":")
            lineCurrTime = int(lineTime[0])*60 + int(lineTime[1]) # Time in minutes of the current element.
            lineCurrDay = line[0].split(".")
            
            if lineCurrTime == previousTime: continue
            
            # Check if day has changed and updates dayChanged. If we notice that day offset from starting point
            # is at least 2 days, we know there has been a break in logging and we should break from the loop
            # and return the collected data.
            if int(currDay[0]) != int(lineCurrDay[0]) and not dayChanged:
                if int(currDay[0]) > int(lineCurrDay[0]):
                    dayChanged = True
                    
                elif int(lineCurrDay[1]) in [1, 3, 5, 7, 8, 10, 23]:
                    if int(lineCurrDay[0]) == 31: dayChanged = True
                    else: break
                    
                elif int(lineCurrDay[1]) in [4, 6, 9, 11]:
                    if int(lineCurrDay[0]) == 30: dayChanged = True
                    else: break
                    
                else:
                    if int(lineCurrDay[0]) == 28: dayChanged = True
                    else: break
                
            # Happens when for example, if startTime is 19:00 and current line's time is 00:00.
            # Then we know the day is changed because lines are in descending time order.
            if lineCurrTime >= startTime and dayChanged == False: dayChanged = True
            
            # If day is changed and line's time is below for example 19:00, we know that we've already
            # found that 24 h of loggin data we were looking for so return.
            if dayChanged and lineCurrTime <= startTime:
                return holder
            
            # Add the current line to the holder container.
            holder.append(line)
            previousTime = lineCurrTime
        
        return holder
        
    def generateWeek(self, data, file):
        currTime = data[0][1].split(":")
        
        type = "" # What type of sensor it is.
        yMax = -9999 # Used to set max boundary for the generated plot. Max sensor value in the data set.
        yMin = 9999 # Used to set min boundary for the generated plot. Min sensor value in the data set.
        x = []
        y = [] # Y axis.
        previousDay, previousMonth, previousYear = data[0][0].split(".")
        previousDay = int(previousDay)
        previousMonth = int(previousMonth)
        previousYear = int(previousYear)
        previousTime = int(currTime[0])*60 + int(currTime[1]) # Time in minutes of the last element.
        i = 10080# - int(currTime[0])*60 + int(currTime[1])# The current minute value.
        total = 0
        
        for day, time, measurement in data:
            yTmp = float(measurement.replace("\n", ""))
            if yTmp > yMax: yMax = yTmp
            if yTmp < yMin: yMin = yTmp
            y.append(yTmp)
            total += yTmp
            
            tmpTime = time.split(":")
            currHour = int(tmpTime[0])
            currDay = int(day.split(".", 1)[0])

            x.append(i)
            
            # Time of the current set of data.
            lineTime = time.split(":")
            lineCurrTime = int(lineTime[0])*60 + int(lineTime[1])
            lineCurrDay, lineCurrMonth, lineCurrYear = day.split(".")
            lineCurrDay = int(lineCurrDay)
            lineCurrMonth = int(lineCurrMonth)
            lineCurrYear = int(lineCurrYear)
            
            if previousTime - lineCurrTime != 0:
                # If this is triggered then the day of the read data has changed (i.e. from 4.3. to 3.3.)
                # which makes normally determining the time interval impossible, so let's just use the
                # last interval between measurements.
                if lineCurrTime > previousTime or lineCurrDay != previousDay:
                    if lineCurrDay > previousDay:
                        if lineCurrMonth in [1, 3, 5, 7, 8, 10, 23]: previousDay += 31
                        elif lineCurrMonth in [4, 6, 9, 11]: previousDay += 30
                        else: previousDay += 28

                    i -= (previousDay - lineCurrDay) * 1440 - lineCurrTime + previousTime
                    previousTime = lineCurrTime
                    previousDay = lineCurrDay
                    continue
                    
                i -= previousTime - lineCurrTime 
                previousTime = lineCurrTime
                previousDay = lineCurrDay

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
        plt.title(file.split("-")[0])
        plt.axis([x[len(x)-1], x[0], yMin, yMax])
        
        # The type of sensor ends the sensor logging data file name. Check the type and choose an appropriate
        # title for the y axis.
        xAxisText = "Average: " + str(round(total/len(y), 1))
        
        if file.endswith("hygrometer"):
            type = "Hygrometer reading"
        elif file.endswith("humidity"):
            type = "Humidity %"
            xAxisText += " %, min: " + str(round(minBoundary, 1)) + " %, max: " + str(round(maxBoundary, 1)) + " %"
        elif file.endswith("temp"):
            type = "Temperature C"
            xAxisText += " C, min: " + str(round(minBoundary, 1)) + " C, max: " + str(round(maxBoundary, 1)) + " C"
        elif file.endswith("ultrasound"):
            type = "Distance cm"
            xAxisText += " cm, min: " + str(round(minBoundary, 1)) + " cm, max: " + str(round(maxBoundary, 1)) + " cm"

        lastReading = x[0] - int(currTime[0])*60 + int(currTime[1])
        interval = int(x[0]/7)
        lastDay = int(data[0][0].split(".", 1)[0])
        currMonth = int(data[0][0].split(".", 2)[1])
        tmpDays = []
        lista = []
        
        for i in range(0, 7):
            lista.append(lastReading)
            lastReading -= interval
            
            tmpDays.append(lastDay)
            lastDay -= 1
            
            if lastDay <= 0:
                if currMonth-1 in [1, 3, 5, 7, 8, 10, 23]: lastDay = 31
                elif  currMonth-1 in [4, 6, 9, 11]: lastDay = 30
                else: lastDay = 28
            
            
        plt.ylabel(type)
        plt.xlabel("Day")
        plt.annotate(xAxisText, xy=(0.03, 0.94), xycoords="axes fraction")
        plt.xticks(lista, tmpDays) # Set x axis and give its elements time names.
        location = (self.folder + "week-" + file).replace(" ", "")
        plt.savefig(location) # Save the plot with the file name of the sensor.
        plt.clf() # Close figure so this figure's dataset won't show up in the next one.
        plt.close()
        
    
    def generateWeekData(self, data):
        """
            Generates hourly data for the week plot. Takes measurements for each hours and then calculates
            an average value for the time.
        """
        
        currTime = data[0][1].split(":", 3)
        startTime = int(currTime[0])*60 + int(currTime[1]) # Time in minutes of the first element.
        previousDay = int(data[0][0].split(".", 1)[0])
        previousTime = startTime
        previousHour = int(currTime[0])
        daysToGo = 8
        measurementsInCurrentHour = 0
        averageMeasurementHolder = 0
        holder = [] # Read the data we need into this holder.
        holder.append(data[0]) # Fill holder with one element so dayChange works.
        
        for line in data[1:]:
            lineTime = line[1].split(":")
            lineCurrTime = int(lineTime[0])*60 + int(lineTime[1]) # Time in minutes of the current element.
            lineDay = line[0].split(".")[0]
            
            if lineCurrTime == previousTime: continue
            
            if lineDay != previousDay:
                daysToGo -= 1
                previousDay = lineDay
            
            # If day is changed and line's time is below for example 19:00, we know that we've already
            # found that 24 h of loggin data we were looking for so return.
            if daysToGo < 1 and lineCurrTime <= startTime:
                return holder
            
            measurementsInCurrentHour += 1
            averageMeasurementHolder += float(line[2].replace("\n", ""))
            
            # Add the current line to the holder container.
            if previousHour != int(lineTime[0]):
                day, hour, measurement = line
                measurement = str(round(averageMeasurementHolder / measurementsInCurrentHour, 2))
                holder.append((day, hour, measurement))
                previousHour = int(lineTime[0])
                measurementsInCurrentHour = 0
                averageMeasurementHolder = 0
                measurementsInCurrentHour += 1
                averageMeasurementHolder += float(line[2].replace("\n", ""))
            
            previousTime = lineCurrTime
        
        return holder
