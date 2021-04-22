from checker import *

def tambahTask(line, id, taskList):
    newTask = extractTaskFromLine(line, id)
    taskList.append(newTask)
    message = "[TASK BERHASIL DICATAT]\n(ID:" + str(newTask["id"]) + ") " + str(newTask["deadline"]) + " - " + newTask["matkul"] + " - " + newTask["kataPenting"] + " - " + newTask["topik"]
    return(message, id+1, taskList)

# Ngereturn tupple of (message, availID, taskList)
def checkFitur(line, availID, taskList):
    print(searchKMP(line.lower(), "semua"))
    if(searchKMP(line.lower(), "semua") != -1):
        print("fitur tampilkan daftar task")
    elif(searchKMP(line.lower(), "apa saja") != -1):
        print("fitur tampilkan task dengan deadline dari x smp y")
    else:
        return tambahTask(line, availID, taskList)
