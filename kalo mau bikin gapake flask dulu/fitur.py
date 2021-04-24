from checker import *
from util import *

def convertObjectToMessage(task):
    if(task != -1):
        return "[TASK BERHASIL DICATAT]\n(ID:" + str(task["id"]) + ") " + str(task["deadline"]) + " - " + task["matkul"] + " - " + task["kataPenting"] + " - " + task["topik"]

    return "Perintah tidak dapat dikenali"

def tambahTask(line, id, taskList):
    newTask = extractTaskFromLine(line, id)
    message = convertObjectToMessage(newTask)
    
    if newTask != -1:
        taskList.append(newTask)
        return(message, id+1, taskList)
    else:
        return(message, id, taskList)

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
