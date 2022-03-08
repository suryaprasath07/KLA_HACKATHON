import yaml
import time
from datetime import datetime

logFile = open("logFile.txt", "w")

def time_function(function_name, sleep_time,fun_name):
    logFile.write((str(datetime.now())+";" + function_name + " Executing TimeFunction("+ fun_name +","+str(sleep_time)+")\n"))
    time.sleep(sleep_time)

def helper(flow_name, data):
    if data["Type"] == 'Flow':
        if data["Execution"] == "Sequential":
            seq_activities(flow_name, data["Activities"])


def task_activities(flowname, functioninput, exectime):
    sdata = flowname
    time_function(sdata, int(exectime),functioninput)


def seq_activities(flowname, data):

    tempdata = list(data.values())
    flowtaskname = list(data.keys())

    for temp, flow in zip(tempdata, flowtaskname):
        flowprint = flowname + "." + j
        logFile.write(str(datetime.now()) + ";" + flowprint + " Entry\n")
        if temp["Type"] == "Task":
            if temp["Function"] == "TimeFunction":
                task_activities(flowprint,temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"])
                logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")
        if temp["Type"] == "Flow":
            helper(flowprint, temp)
            logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")

with open("Dataset/Milestone1/Milestone1A.yaml", "r") as file:
    try:
        yamlData = yaml.safe_load(file)
        task_name = list(yamlData.keys())[0]
        task_details = list(yamlData.values())[0]
        logFile.write(str(datetime.now()) + ";" + str(task_name) + " Entry\n")
        helper(task_name, task_details)
        logFile.write(str(datetime.now()) + ";" + str(task_name) + " Exit")
        print(str(datetime.now()) + ";" + str(task_name) + " Exit")
    except yaml.YAMLError as exc:
        print(exc)