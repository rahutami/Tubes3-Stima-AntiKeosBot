from app.library.checker import *
from app.library.util import *
import re
import random

# # DONE: fixed processing error still add new object to taskList and increment availID
# # TODO: fitur2 masih pada belom kelar bro
# # * ini kalo mau nambah2in langsung kesini aja harusnya udah langsung bisa kepake di websitenya

def tambahTask(line, id, taskList):
    newTask = extractTaskFromLine(line, id)
    message = convertTaskToMessage(newTask)
    
    if(message == ""):
        message = "Perintah tidak dapat dikenali"
    else:
        message = "[TASK BERHASIL DICATAT]<br>" + message
    
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
            message += convertTaskToMessage(task) + "<br>"

    if(message == ""):
        return "Tidak ada"
    else:
        return "[Daftar Deadline]<br>" + message

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
        message = "Kamu memiliki " + str(len(taskList)) + " " + keyword + " yang memenuhi pencarianmu.<br>"
        message += "Berikut adalah daftar " + keyword + " dan deadlinenya:<br>"
        for task in taskList:
            message += convertTaskToMessage(task) + "<br>"
        return message

def sendMeme():
    x = random.randint(1,11)
    return "<img src=\"/static/assets/meme/{}.jpg\" alt=\"meme\"".format(x)

# Ngereturn tupple of (message, availID, taskList)
def checkFitur(line, availID, taskList):
    if(searchKMP(line.lower(), "meme") != -1):
        return(sendMeme(), availID, taskList)
    elif(searchKMP(line.lower(), "apa saja", "tampil", "apa aja") != -1):
        return (daftarTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "kapan") != -1):
        return (checkDeadline(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "ubah") != -1):
        return (ubahTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "selesai") != -1):
        return(hapusTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "semua task") != -1):
        return(allTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "berdasarkan") != -1):
        return(kataPentingTask(line, taskList), availID, taskList)
    elif(searchKMP(line.lower(), "bantuan", "help") != -1):
        return(showHelp(), availID, taskList)
    else:
        return tambahTask(line, availID, taskList)

def ubahTask(line, taskList):
    result = re.findall('\d+', line)
    date = searchDate(line)
    dateFix = convertDate(date.group(0))
    found = False
    for task in taskList:
        if (task["id"] == int(result[0])):
            task["deadline"] = dateFix
            found = True
    if(found):
        return "Task berhasil diperbaharui"
    else:
        return "Task tidak ditemukan"

def hapusTask(line, taskList):
    result = re.findall('\d+', line)
    found = False
    for task in taskList:
        if (task["id"] == int(result[0])):
            taskList.remove(task)
            found = True
    if (found):
        return "Task berhasil dihapus. Selamat ya!"
    else:
        return "Task tidak ditemukan"

def allTask(line, taskList):
    message = ""
    for task in taskList:
        message += convertTaskToMessage(task) + "<br>"
    if (message == ""):
        return "Task kosong"
    else:
        return "[Daftar Task]<br>" + message

def kataPentingTask(line, taskList):
    if (searchKMP(line.lower(), "praktikum") != -1):
        message = ""
        for task in taskList:
            if (task["kataPenting"] == "Praktikum"):
                message += convertTaskToMessage(task) + "<br>"
        if (message == ""):
            return "Tidak ada praktikum"
        else:
            return "[Daftar Praktikum]<br>" + message
    elif (searchKMP(line.lower(), "tubes") != -1):
        message = ""
        for task in taskList:
            if (task["kataPenting"] == "Tubes"):
                message += convertTaskToMessage(task) + "<br>"
        if (message == ""):
            return "Tidak ada tubes"
        else:
            return "[Daftar Tubes]<br>" + message
    elif (searchKMP(line.lower(), "tucil") != -1):
        message = ""
        for task in taskList:
            if (task["kataPenting"] == "Tucil"):
                message += convertTaskToMessage(task) + "<br>"
        if (message == ""):
            return "Tidak ada tucil"
        else:
            return "[Daftar Tucil]<br>" + message
    elif (searchKMP(line.lower(), "ujian") != -1):
        message == ""
        for task in taskList:
            if (task["kataPenting"] == "Ujian"):
                message += convertTaskToMessage(task) + "<br>"
        if (message == ""):
            return "Tidak ada ujian"
        else:
            return "[Daftar Ujian]<br>" + message
    elif (searchKMP(line.lower(), "kuis") != -1):
        message = ""
        for task in taskList:
            if (task["kataPenting"] == "Kuis"):
                message += convertTaskToMessage(task) + "<br>"
        if (message == ""):
            return "Tidak ada kuis"
        else:
            return "[Daftar Kuis]<br>" + message
    else:
        return "Masukkan kata penting salah"

def showHelp():
    kata_penting = ["Tubes", "Tucil", "Ujian", "Kuis", "Praktikum"]
    fitur = ["Menambahkan task baru", 
    "Melihat daftar task",
    "Melihat daftar deadline", 
    "Menampilkan dedline dari suatu task tertentu", 
    "Memperbaharui task", 
    "Melihat daftar task sesuai dengan kata penting"
    "Help"]
    command = ["Menambahkan task baru : [Kata Penting] matkul [Kode/Nama Matkul] topik [Topik] [Tanggal deadline]",
    "Melihat daftar task : Lihat semua task",
    "Melihat semua daftar deadline : Apa saja/apa aja/tampilkan deadline yang ada?",
    "Melihat daftar deadline berdasarkan range waktu: Apa saja/apa aja/tampilkan deadline [Tanggal awal] sampai [Tanggal akhir]?",
    "Melihat daftar deadline beberapa hari, minggu, atau bulan kedepan : Apa saja/apa aja/tampilkan deadline [range] hari/minggu/bulan kedepan?",
    "Melihat deadline dari task tertentu : Kapan deadline [Kata Penting] [Matkul]",
    "Melihat task berdasarkan kata penting : Lihat berdasarkan [Kata Penting]",
    "Memperbaharui task : Ubah task [ID] menjadi tanggal [Tanggal]",
    "Menandai task selesai : Task [ID] sudah selesai",
    "Help : Aku butuh bantuan"]
    message1 = ""
    for i in range(len(kata_penting)):
        message1 += "   " + str(i+1) + ". " + kata_penting[i] + "<br>"

    message2 = ""
    for i in range(len(fitur)):
        message2 += "   " + str(i+1) + ". " + fitur[i] + "<br>"
    
    message3 = ""
    for i in range(len(command)):
        message3 += "   " + str(i+1) + ". " + command[i] + "<br><br>"
    return "[Fitur]<br>" + message2 + "<br>[Kata Penting]<br>" + message1 + "<br>[Command]<br>" + message3
