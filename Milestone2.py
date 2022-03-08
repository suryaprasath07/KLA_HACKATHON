import threading

import yaml
import time
import csv
from datetime import datetime

logFile = open("logFile.txt", "w")
count_dit = 0

def time_function(function_name, sleep_time,fun_name):
    print((str(datetime.now())+";" + function_name + " Executing TimeFunction("+ fun_name +","+str(sleep_time)+")"))
    logFile.write((str(datetime.now())+";" + function_name + " Executing TimeFunction("+ fun_name +","+str(sleep_time)+")\n"))
    time.sleep(sleep_time)
    logFile.write(str(datetime.now()) + ";" + function_name + " Exit\n")

def data_load(function_name,File_name,fun_name=""):
    var = 0
    print((str(datetime.now()) + ";" + function_name + " Executing DataLoad(" + File_name + ")"))
    logFile.write((str(datetime.now()) + ";" + function_name + " Executing DataLoad(" + File_name + ")\n"))
    file = open(File_name)
    csvReader = csv.reader(file)
    file = next(csvReader)
    for row in csvReader:
        var+=1
    logFile.write((str(datetime.now()) + ";" + function_name + " Exit\n"))
    print((str(datetime.now()) + ";" + function_name + " Exit\n"))
    return var

def helper(flow_name, data):
    if data["Type"] == 'Flow':
        if data["Execution"] == "Sequential":
            seq_activities(flow_name, data["Activities"])
        if data["Execution"] == "Concurrent":
            conc_activities(flow_name,data["Activities"])

def task_activities(flowname, functioninput, input1,FUNCTION):
    global count_dit
    if(FUNCTION=="TIME_FUNCTION"):
        time_function(flowname, int(input1),functioninput)
    elif(FUNCTION=="DATA_LOAD"):
        count_dit = data_load(flowname,input1,functioninput)
        print(count_dit)

def seq_activities(flowname, data):
    tempdata = list(data.values())
    flowtaskname = list(data.keys())
    global count_dit

    for temp, flow in zip(tempdata, flowtaskname):
        flowprint = flowname + "." + flow
        print(str(datetime.now()) + ";" + flowprint + " Entry")
        logFile.write(str(datetime.now()) + ";" + flowprint + " Entry\n")
        if temp["Type"] == "Task":
            if temp["Function"] == "TimeFunction":
                if "Condition" in temp:
                    key = temp["Condition"][temp["Condition"].index("(")+1:temp["Condition"].index(")")]
                    condn = temp["Condition"].split()[-2]
                    val = int(temp["Condition"].split()[-1])

                    res = count_dit
                    if(condn==">" and res>val):
                        task_activities(flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],
                                        "TIME_FUNCTION")
                    elif(condn=="<" and res<val):
                        task_activities(flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],
                                        "TIME_FUNCTION")
                    else:
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Skipped\n")
                else:
                    print("TIME FUNCTION==>",flowprint)
                    task_activities(flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],"TIME_FUNCTION")

            if temp["Function"] == "DataLoad":
                if "Condition" in temp:
                    key = temp["Condition"][temp["Condition"].index("(")+1:temp["Condition"].index(")")]
                    condn = temp["Condition"].split()[-2]
                    val = int(temp["Condition"].split()[-1])
                    res = count_dit
                    if(condn==">" and res>val):
                        task_activities(flowprint,"", temp["Inputs"]["Filename"],
                                        "DATA_LOAD")

                    elif(condn=="<" and res<val):
                        task_activities(flowprint, "", temp["Inputs"]["Filename"],
                                        "DATA_LOAD")
                    else:
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Skipped\n")
                else:
                    task_activities(flowprint,"", temp["Inputs"]["Filename"],"DATA_LOAD")

        if temp["Type"] == "Flow":
            helper(flowprint, temp)
            logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")

def conc_activities(flowname,data):
    global count_dit
    tempdata = list(data.values())
    flowtaskname = list(data.keys())
    Thread_arr = []
    flow_arr = []
    Thread_flowArr = []
    dataThread_arr = []

    for temp, flow in zip(tempdata, flowtaskname):
        flowprint = flowname + "." + flow
        print(str(datetime.now()) + ";" + flowprint + " Entry")
        logFile.write(str(datetime.now()) + ";" + flowprint + " Entry\n")
        if temp["Type"] == "Task":

            if temp["Function"] == "TimeFunction":
                if "Condition" in temp:
                    key = temp["Condition"][temp["Condition"].index("(") + 1:temp["Condition"].index(")")]
                    condn = temp["Condition"].split()[-2]
                    val = int(temp["Condition"].split()[-1])

                    print(val,count_dit)

                    res = count_dit
                    if (condn == ">" and res > val):
                        Thread1 = threading.Thread(target=task_activities, args=(
                            flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],"TIME_FUNCTION",))
                        Thread1.start()
                        Thread_arr.append(Thread1)

                    elif (condn == "<" and res < val):
                        Thread1 = threading.Thread(target=task_activities, args=(
                            flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],"TIME_FUNCTION",))
                        Thread1.start()
                        Thread_arr.append(Thread1)
                    else:
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Skipped\n")
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")
                else:
                    Thread1 = threading.Thread(target=task_activities, args=(
                        flowprint, temp["Inputs"]["FunctionInput"], temp["Inputs"]["ExecutionTime"],"TIME_FUNCTION",))
                    Thread1.start()
                    Thread_arr.append(Thread1)
                # logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")
            if temp["Function"] == "DataLoad":

                if "Condition" in temp:
                    key = temp["Condition"][temp["Condition"].index("(") + 1:temp["Condition"].index(")")]
                    condn = temp["Condition"].split()[-2]
                    val = int(temp["Condition"].split()[-1])

                    res = count_dit

                    if (condn == ">" and res > val):
                        Thread1 = threading.Thread(target=data_load, args=(
                        flowprint,temp["Inputs"]["Filename"], "",))
                        Thread1.start()
                        Thread_arr.append(Thread1)
                        dataThread_arr.append(Thread1)

                    elif (condn == "<" and res < val):
                        Thread1 = threading.Thread(target=data_load, args=(
                        flowprint, temp["Inputs"]["Filename"], "",))
                        Thread1.start()
                        Thread_arr.append(Thread1)
                        dataThread_arr.append(Thread1)
                    else:
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Skipped\n")
                        logFile.write(str(datetime.now()) + ";" + flowprint + " Exit\n")
                else:
                    Thread1 = threading.Thread(target=data_load, args=(flowprint, temp["Inputs"]["Filename"],))
                    Thread1.start()
                    Thread_arr.append(Thread1)
                    dataThread_arr.append(Thread1)

        if temp["Type"] == "Flow":
            Thread1 = threading.Thread(target=helper, args=(flowprint, temp,))
            Thread1.start()
            Thread_flowArr.append(Thread1)
            flow_arr.append(flowprint)

    for thread in Thread_arr:
        thread.join()

    for thread in dataThread_arr:
        thread.join()

    for thread,flow in zip(Thread_flowArr,flow_arr):
        thread.join()
        logFile.write(str(datetime.now()) + ";" + flow + " Exit\n")

if __name__=="__main__":
    with open("Milestone2A.yaml", "r") as file:
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