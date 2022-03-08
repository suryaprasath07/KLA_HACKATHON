import threading

import yaml
import time
from datetime import datetime

logFile = open("logFile1B.txt", "w")

def time_function(function_name, sleep_time,fun_name):
    print((str(datetime.now())+";" + function_name + " Executing TimeFunction("+ fun_name +","+str(sleep_time)+")"))
    logFile.write((str(datetime.now())+";" + function_name + " Executing TimeFunction("+ fun_name +","+str(sleep_time)+")\n"))
    time.sleep(sleep_time)
    logFile.write(str(datetime.now()) + ";" + function_name + " Exit\n")


def helper(flow_name, data):
    if data["Type"] == 'Flow':
        if data["Execution"] == "Sequential":
            seq_activities(flow_name, data["Activities"])
        if data["Execution"] == "Concurrent":
            conc_activities(flow_name,data["Activities"])

def task_activities(flowname, functioninput, exectime):
    sdata = flowname
    time_function(sdata, int(exectime),functioninput)

def seq_activities(flowname, data):
    tempdata = list(data.values())
    flowtaskname = list(data.keys())

    for temp, flow in zip(tempdata, flowtaskname):
        flowprint = flowname + "." + flow
        print(str(datetime.now()) + ";" + flowprint + " Entry")
        logFile.write(str(datetime.now()) + ";" + flowprint + " Entry\n")
        if temp["Type"] == "Task":
            if temp["Function"] == "TimeFunction":
                task_activities(flowprint,temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"])
        if temp["Type"] == "Flow":
            helper(flowprint, temp)
            logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")

def conc_activities(flowname,data):
    tempdata = list(data.values())
    flowtaskname = list(data.keys())
    Thread_arr = []
    flow_arr = []
    Thread_flowArr = []
    for temp, flow in zip(tempdata, flowtaskname):
        flowprint = flowname + "." + flow
        print(str(datetime.now()) + ";" + flowprint + " Entry")
        logFile.write(str(datetime.now()) + ";" + flowprint + " Entry\n")
        if temp["Type"] == "Task":
            if temp["Function"] == "TimeFunction":
                Thread1 = threading.Thread(target=task_activities,args=(flowprint,temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],))
                Thread1.start()
                Thread_arr.append(Thread1)
                # logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")
        if temp["Type"] == "Flow":
            Thread1 = threading.Thread(target=helper, args=(flowprint, temp,))
            Thread1.start()
            Thread_flowArr.append(Thread1)
            flow_arr.append(flowprint)

    for thread in Thread_arr:
        thread.join()

    for thread,flow in zip(Thread_flowArr,flow_arr):
        thread.join()
        logFile.write(str(datetime.now()) + ";" + flow + " Exit\n")

if __name__=="__main__":
    with open("Dataset/Milestone1/Milestone1B.yaml", "r") as file:
        try:
            yamlData = yaml.safe_load(file)
            task_name = list(yamlData.keys())[0]
            task_details = list(yamlData.values())[0]
            logFile.write(str(datetime.now()) + ";" + str(task_name) + " Entry\n")
            print(str(datetime.now()) + ";" + str(task_name) + " Entry")
            helper(task_name, task_details)
            print(str(datetime.now()) + ";" + str(task_name) + " Exit")
            logFile.write(str(datetime.now()) + ";" + str(task_name) + " Exit")
        except yaml.YAMLError as exc:
            print(exc)
