# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
import numpy as np
import pandas as pd


class ganttChart:

    # Fields
    chart = pd.DataFrame()
    timeElapsed = 0
    idleTime = 0

    # Methods
    def addTask(self, taskName, arrivalTime, startTime, endTime, status):
        if startTime > self.timeElapsed: # Filling the gap for idle wait
            self.idleTime += startTime - self.timeElapsed
            timeElapsed = startTime
        elif startTime < self.timeElapsed:
            print("[addTask] Input arguments are conflicting with the existing schedule.")
            return False
        self.chart = pd.concat([self.chart,
                                pd.DataFrame(columns=["Task", "Arrival Time", "Start Time", "End Time", "Status"],
                                             data=[[taskName, arrivalTime, startTime, endTime, status]])],
                               axis=0)
        self.timeElapsed += endTime - startTime
        print("[addTask] Task "+str(taskName)+" with status "+str(status)+" added to the list successfully.")
        return True

    def turnaroundTimeTask(self, taskName):
        subchart = self.chart.loc[self.chart["Task"] == taskName]
        if len(subchart) == 0:
            print("[turnaroundTime] No such task exists.")
            return -1
        tt = subchart["End Time"].max() - subchart["Arrival Time"].unique().item()
        return tt

    def turnaroundTime(self):
        if len(self.chart) == 0:
            print("[turnaroundTime] No tasks found in schedule.")
            return -1
        listTT = [self.turnaroundTimeTask(taskName) for taskName in self.chart["Task"].unique()]
        tt = sum(listTT) / len(self.chart["Task"].unique())
        return tt

    def waitingTimeTask(self, taskName):
        subchart = self.chart.loc[self.chart["Task"] == taskName]
        if len(subchart) == 0:
            print("[waitingTime] No such task exists.")
            return -1
        wt =  subchart["Start Time"].min() - subchart["Arrival Time"].unique().item()
        for i in range(len(subchart)-1):
            wt += subchart["Start Time"].iloc[i+1] - subchart["End Time"].iloc[i]
        return wt

    def waitingTime(self):
        if len(self.chart) == 0:
            print("[waitingTime] No tasks found in schedule.")
            return -1
        listWT = [self.waitingTimeTask(taskName) for taskName in self.chart["Task"].unique()]
        wt = sum(listWT) / len(self.chart["Task"].unique())
        return wt

    def throughput(self):
        if len(self.chart) == 0:
            print("[throughput] No tasks found in schedule.")
            return -1
        t = len(self.chart["Task"].unique()) / (self.chart["End Time"].max() - self.chart["Start Time"].min())
        return t

    # Constructor(s)
    def __init__(self):
        chart = pd.DataFrame(columns=["Task", "Arrival Time", "Start Time", "End Time", "Status"])

    # String Override(s)
    def __str__(self):
        print("Text temporary.")

def FCFS(inputDF):
    inputDF.sort_values(by=["Arrival Time","Priority"], ascending=[True, True], inplace=True)
    scheduleFCFS = ganttChart()
    for i in range(len(inputDF)):
        scheduleFCFS.addTask(inputDF["Process ID"].iloc[i].item(),
                             inputDF["Arrival Time"].iloc[i].item(),
                             scheduleFCFS.timeElapsed,
                             scheduleFCFS.timeElapsed + inputDF["Burst Time"].iloc[i].item(),
                             "Complete")

    print(scheduleFCFS.chart)
    print("Time within the schedule is " + str(scheduleFCFS.timeElapsed))
    print("Total idle time within the schedule is " + str(scheduleFCFS.idleTime))
    print("Avg Turnaround Time for processes within the schedule is " + str(scheduleFCFS.turnaroundTime()))
    print("Avg Waiting Time for processes within the schedule is " + str(scheduleFCFS.waitingTime()))
    print("Throughput for processes within the schedule is " + str(scheduleFCFS.throughput()))

    return scheduleFCFS

def Preemptive(inputDF, sortOrder):
    inputDF["Remaining Time"] = inputDF["Burst Time"].copy()

    schedulePre = ganttChart()
    timeCursor = 0
    evalTimeList = sorted(list(inputDF["Arrival Time"].unique()))
    for i in range(len(evalTimeList)-1):
        currEvalTime = evalTimeList[i]
        nextEvalTime = evalTimeList[i+1]
        availableTime = nextEvalTime - currEvalTime
        if timeCursor < currEvalTime: timeCursor = currEvalTime # Checking for an adding idle wait, if not then both should already be equal
        while availableTime != 0:
            inputDF.sort_values(by=sortOrder, ascending=[False, False, False], inplace=True) # Sorting is applied in reverse just like a stack works
            processStack = list(inputDF.loc[(inputDF["Remaining Time"] != 0) & (inputDF["Arrival Time"] <= currEvalTime), "Process ID"].unique())
            if len(processStack) == 0: break
            else: processName = processStack.pop()
            if timeCursor < inputDF.loc[inputDF["Process ID"] == processName, "Arrival Time"].item(): # Checking for and adding idle wait
                timeCursor = inputDF.loc[inputDF["Process ID"] == processName, "Arrival Time"].item()
            if inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item() <= availableTime:
                schedulePre.addTask(inputDF.loc[inputDF["Process ID"] == processName, "Process ID"].item(),
                                    inputDF.loc[inputDF["Process ID"] == processName, "Arrival Time"].item(),
                                    timeCursor, #schedulePre.timeElapsed,
                                    timeCursor + inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item(), #schedulePre.timeElapsed + inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item(),
                                    "Complete")
                # Below order is important
                availableTime -= inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item()
                timeCursor += inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item()
                inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"] = 0
            else:
                schedulePre.addTask(inputDF.loc[inputDF["Process ID"] == processName, "Process ID"].item(),
                                    inputDF.loc[inputDF["Process ID"] == processName, "Arrival Time"].item(),
                                    timeCursor, #schedulePre.timeElapsed,
                                    timeCursor + availableTime, #schedulePre.timeElapsed + availableTime,
                                    "Partial")
                # Below order is important
                inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"] = (
                        inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item() - availableTime)
                timeCursor += availableTime
                availableTime = 0
                #processStack.insert(0, processName)
    timeCursor = nextEvalTime # Manually initializing the final segment
    while True: # Leftover processes, no wait involved here
        inputDF.sort_values(by=sortOrder, ascending=[False, False, False], inplace=True) # Sorting is applied in reverse just like a stack works
        processStack2 = list(inputDF.loc[(inputDF["Remaining Time"] != 0), "Process ID"].unique())
        if len(processStack2) == 0: break
        else: processName = processStack2.pop()
        schedulePre.addTask(inputDF.loc[inputDF["Process ID"] == processName, "Process ID"].item(),
                            inputDF.loc[inputDF["Process ID"] == processName, "Arrival Time"].item(),
                            timeCursor, #schedulePre.timeElapsed,
                            timeCursor + inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item(), #schedulePre.timeElapsed + inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item(),
                            "Complete")
        #Below order is important
        timeCursor += inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"].item()
        inputDF.loc[inputDF["Process ID"] == processName, "Remaining Time"] = 0

    print(schedulePre.chart)
    print("Time within the schedule is " + str(schedulePre.timeElapsed))
    print("Total idle time within the schedule is " + str(schedulePre.idleTime))
    print("Avg Turnaround Time for processes within the schedule is " + str(schedulePre.turnaroundTime()))
    print("Avg Waiting Time for processes within the schedule is " + str(schedulePre.waitingTime()))
    print("Throughput for processes within the schedule is " + str(schedulePre.throughput()))

    return schedulePre

def SJF(inputDataFrame) : return Preemptive(inputDataFrame, ["Remaining Time", "Priority", "Arrival Time"])

def PS(inputDataFrame) : return Preemptive(inputDataFrame, ["Priority", "Remaining Time", "Arrival Time"])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    filePath = sys.argv[1]
    if os.path.exists(os.path.join(os.getcwd(), filePath)):
        inputDataFrame = pd.read_csv(filePath, sep=',', header=None,
                                     names=["Process ID", "Arrival Time", "Burst Time", "Priority"])
    else:
        print("No input file found! ")
        input("Press ENTER to exit.")
        exit()

    print(inputDataFrame)

    if not os.path.exists(os.path.join(os.getcwd(), "out")): os.mkdir("out")

    print("FCFS:")
    FCFS(inputDataFrame)
    print("SJF:")
    scheduleSJF = SJF(inputDataFrame)
    scheduleSJF.chart.to_csv("out/scheduleSJF_chart.csv", index=False)
    print("PS:")
    schedulePS = PS(inputDataFrame)
    schedulePS.chart.to_csv("out/schedulePS_chart.csv", index=False)

    """
    testSchedule = ganttChart() # FCFS Output Exemplified
    testSchedule.addTask(1, 0, 0, 3, "Complete")
    testSchedule.addTask(2, 2, 3, 7, "Complete")
    testSchedule.addTask(3, 3, 7, 8, "Complete")
    testSchedule.addTask(4, 8, 8, 11, "Complete")
    testSchedule.addTask(5, 10, 11, 15, "Complete")

    print(testSchedule.chart)
    print("Time within the schedule is "+str(testSchedule.timeElapsed))
    print("Total idle time within the schedule is " + str(testSchedule.idleTime))
    print("Avg Turnaround Time for processes within the schedule is "+str(testSchedule.turnaroundTime()))
    print("Avg Waiting Time for processes within the schedule is "+str(testSchedule.waitingTime()))
    print("Throughput for processes within the schedule is "+str(testSchedule.throughput()))

    testSchedule2 = ganttChart() # SJF Output Exemplified
    testSchedule2.addTask(1, 0, 0, 2, "Partial")
    testSchedule2.addTask(1, 0, 2, 3, "Complete")
    testSchedule2.addTask(3, 3, 3, 4, "Complete")
    testSchedule2.addTask(2, 2, 4, 8, "Complete")
    testSchedule2.addTask(4, 8, 8, 10, "Partial")
    testSchedule2.addTask(4, 8, 10, 11, "Complete")
    testSchedule2.addTask(5, 10, 11, 15, "Complete")

    print(testSchedule2.chart)
    print("Time within the schedule is "+str(testSchedule2.timeElapsed))
    print("Total idle time within the schedule is " + str(testSchedule2.idleTime))
    print("Avg Turnaround Time for processes within the schedule is "+str(testSchedule2.turnaroundTime()))
    print("Avg Waiting Time for processes within the schedule is "+str(testSchedule2.waitingTime()))
    print("Throughput for processes within the schedule is "+str(testSchedule2.throughput()))

    testSchedule3 = ganttChart()  # Priority Output Exemplified
    testSchedule3.addTask(1, 0, 0, 2, "Partial")
    testSchedule3.addTask(2, 2, 2, 3, "Partial")
    testSchedule3.addTask(2, 2, 3, 6, "Complete")
    testSchedule3.addTask(1, 0, 6, 7, "Complete")
    testSchedule3.addTask(3, 3, 7, 8, "Complete")
    testSchedule3.addTask(4, 8, 8, 10, "Partial")
    testSchedule3.addTask(5, 10, 10, 14, "Complete")
    testSchedule3.addTask(4, 8, 14, 15, "Complete")

    print(testSchedule3.chart)
    print("Time within the schedule is " + str(testSchedule3.timeElapsed))
    print("Total idle time within the schedule is " + str(testSchedule3.idleTime))
    print("Avg Turnaround Time for processes within the schedule is " + str(testSchedule3.turnaroundTime()))
    print("Avg Waiting Time for processes within the schedule is " + str(testSchedule3.waitingTime()))
    print("Throughput for processes within the schedule is " + str(testSchedule3.throughput()))
    """

    input("Press ENTER to exit.")
    print_hi("Bye!")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
