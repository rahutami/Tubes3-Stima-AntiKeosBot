from app.library.checker import *
from app.library.util import *

def convertObjectToMessage(task):
    return "(ID:" + str(task["id"]) + ") " + str(task["deadline"]) + " - " + task["matkul"] + " - " + task["kataPenting"] + " - " + task["topik"]

def tambahTask(line, id, taskList):
    newTask = extractTaskFromLine(line, id)
    taskList.append(newTask)
    message = "[TASK BERHASIL DICATAT]\n" + convertObjectToMessage(newTask)
    return(message, id+1, taskList)

def daftarTask(line, taskList):
    message = ""
    for task in taskList:
        message += convertObjectToMessage(task) + "\n"
    return message

def checkDeadline(line, taskList):
    line = removeWords(line, "kapan", "Kapan", "ya", "?", "Ya")
    
    (indexStart, indexEnd) = searchKeywords(line.lower(), "tugas")

# Ngereturn tupple of (message, availID, taskList)
def checkFitur(line, availID, taskList):
    if(searchKMP(line.lower(), "apa saja", "tampil") != -1):
        return (daftarTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "kapan") != -1):
        return (checkDeadline(line, taskList), availID, taskList)
    else:
        return tambahTask(line, availID, taskList)
