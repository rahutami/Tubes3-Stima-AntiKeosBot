from app.library.checker import *
from app.library.util import *

# # DONE: fixed processing error still add new object to taskList and increment availID
# # TODO: fitur2 masih pada belom kelar bro
# # * ini kalo mau nambah2in langsung kesini aja harusnya udah langsung bisa kepake di websitenya

def tambahTask(line, id, taskList):
    newTask = extractTaskFromLine(line, id)
    message = convertTaskToMessage(newTask)
    
    if(message == ""):
        message = "Perintah tidak dapat dikenali"
    else:
        message = "[TASK BERHASIL DICATAT]\n" + message
    
    if newTask != -1:
        taskList.append(newTask)
        return(message, id+1, taskList)
    else:
        return(message, id, taskList)

def daftarTask(line, taskList):
    (startDate, endDate) = extractDateStartDateEnd(line)
    kataPenting = searchKataPenting(line)

    if(kataPenting != None):
        kataPenting = kataPenting.group(0)
    else:
        kataPenting = ""

    message = ""
    for task in taskList:
        if(isQualified(task, kataPenting, startDate, endDate)):
            message += convertTaskToMessage(task) + "\n"

    if(message == ""):
        return "Tidak ada"
    else:
        return "[Daftar Deadline]\n" + message

def filterBasedOnKataPenting(line, taskList):
    (indexStart, indexEnd) = searchKeywords(line.lower(), "tugas")

    if(indexStart != -1):
        keyword = "Tugas"
        kataPenting = ["tubes", "tucil"]
    else:
        kataPentingObj = searchKataPenting(line.lower())
        if kataPentingObj != None:
            kataPenting = [kataPentingObj.group(0)]
            keyword = kataPentingObj.group(0).capitalize()
        else:
            return taskList, keyword
    
    newTaskList = []

    for task in taskList:
        for kata in kataPenting:
            if(task["kataPenting"].lower() == kata):
                newTaskList.append(task)

    return newTaskList, keyword

def filterBasedOnMatkul(line, taskList):
    newTaskList = []

    for task in taskList:
        if(searchKMP(line.lower(), task["matkul"].lower()) != -1 and (task["kataPenting"] == "Tubes" or task["kataPenting"] == "Tucil")):
            newTaskList.append(task)

    if(newTaskList != []):
        return newTaskList
    else:
        return taskList

def filterBasedOnTopik(line, taskList):
    newTaskList = []

    for task in taskList:
        if(searchKMP(line.lower(), task["topik"].lower()) != -1 and (task["kataPenting"] == "Tubes" or task["kataPenting"] == "Tucil")):
            newTaskList.append(task)

    if(newTaskList != []):
        return newTaskList
    else:
        return taskList

def checkDeadline(line, taskList):
    line = removeWords(line, "kapan", "Kapan", "ya", "?", "Ya", "sih")

    taskList, keyword = filterBasedOnKataPenting(line.lower(), taskList)
    taskList = filterBasedOnMatkul(line.lower(), taskList)
    taskList = filterBasedOnTopik(line.lower(), taskList)

    if(taskList == []):
        return "Kamu tidak memiliki tugas yang sesuai dengan pencarianmu"
    elif(len(taskList) == 1):
        return taskList[0]["deadline"]
    else:
        message = "Kamu memiliki " + str(len(taskList)) + " " + keyword + " yang memenuhi pencarianmu.\n"
        message += "Berikut adalah daftar " + keyword + " dan deadlinenya:\n"
        for task in taskList:
            message += convertTaskToMessage(task) + "\n"
        return message

# Ngereturn tupple of (message, availID, taskList)
def checkFitur(line, availID, taskList):
    if(searchKMP(line.lower(), "apa saja", "tampil", "apa aja") != -1):
        return (daftarTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "kapan") != -1):
        return (checkDeadline(line, taskList), availID, taskList)
    else:
        return tambahTask(line, availID, taskList)
