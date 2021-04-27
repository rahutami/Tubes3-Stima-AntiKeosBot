import re
from app.library.util import *
# from util import *
from datetime import datetime, timedelta

def makeBorderFunction(str1):
    k = [i for i in range (-1, len(str1) - 1)]

    borderFunction = []
    for i in range (len(k)):
        borderFunction.append(0)

        for j in range (k[i]):
            if str1[0:j+1] == str1[k[i]-j:k[i]+1]:
                borderFunction[i] = len(str1[0:j+1])
    
    return borderFunction

def searchKMP (line, *words):
    line = line.lower()

    for word in words:
        word = word.lower()
    
        borderFunction = makeBorderFunction(word)
        found = False

        (i,j) = (0,0)

        while(i < len(line) and not found):
            if(j == len(word) - 1 and word[j] == line[i]):
                found = True

            if(word[j] != line[i]):
                j = borderFunction[j-1] - 1
            
            j += 1
            i += 1

        # return index start
        if(found):
            return i-len(word)
        
    return -1

# accept DD/MM/YY DD/MM/YYYY "DD Month Year"
# ex: 14/05/20 14/05/2020 14 Mei 2020
# Februari asumsi gamungkin masukkin 29 Februari tp yearnya ga kabisat 
# return regex object --> buat ambil tanggalnya convertDate(obj.group(0))

def searchDate(line):
    line = line.lower()
    months30 = ["04", "06", "09", "11"]
    months31 = ["01", "03","05", "07", "08", "10", "12"]

    # Cek format DD/MM/YY
    date = re.search("(([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{2})|(([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{2})|([0-2][0-9]/02/[0-9]{2})", line)
    if(date != None):
        return date
    
    # Cek format DD/MM/YYYY
    date = re.search("(([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{4})|(([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{4})|([0-2][0-9]/02/[0-9]{4})", line)
    if(date != None):
        return date    

    months30 = ["april", "juni", "september", "november"]
    months31 = ["januari", "maret","mei", "juli", "agustus", "oktober", "desember"]
    
    # Cek format DD Month YYYY
    date = re.search("(([0-2][0-9]|30) (" + '|'.join(months30) + ") [0-9]{4})|(([0-2][0-9]|3[01]) (" + '|'.join(months31) + ") [0-9]{4})|([0-2][0-9] februari [0-9]{4})", line)
    return date
    
    # # Cek Februari
    # year = re.search("[0-9]{4}", line).group(0)

    # if(year == None):
    #     year = re.search("[0-9]{2}", line).group(0)   

    # print(isLeapYear(year))
    # if(len(year) == 2):
    #     if(isLeapYear(year)):
    #         date = re.search("[0-2][0-9]/02/[0-9]{2}", line)
    #     else:
    #         date = re.search("[0-2][0-8]/02/[0-9]{2}", line)
    #     return date
    # else:
    #     if(isLeapYear(year)):
    #         date = re.search("[0-2][0-9] Februari [0-9]{4}", line)
    #         if(date != None):
    #             return date.group(0)
    #         date = re.search("[0-2][0-9]/02/[0-9]{4}", line)
    #         return date
    #     else:
    #         date = re.search("[0-2][0-8] Februari [0-9]{4}", line)
    #         if(date != None):
    #             return date.group(0)
    #         date = re.search("[0-2][0-8]/02/[0-9]{4}", line)            

# # *Special word: Kuis, Tubes, Tucil, Ujian, Praktikum
def searchKataPenting(line):
    kataPenting = ["kuis", "tubes", "tucil", "ujian", "praktikum"]
    
    kataPentingInLine = re.search('|'.join(kataPenting), line)

    return kataPentingInLine


# # *Cari keywords
def searchKeywords(line, *keywords):

    for keyword in keywords:
        index = searchKMP(line, keyword)
        if(index != None):
            return (index, index+len(keyword))

    return (-1,-1)

def extractTaskFromLine(line, id):
    line = removeWords(line, "tanggal", "Tanggal", "deadline", "Deadline")
    loweredline = line.lower()

    listIndex = []

    kataPentingObj = searchKataPenting(loweredline)

    if(kataPentingObj != None):
        kataPentingStart = kataPentingObj.start()
        kataPenting = kataPentingObj.group(0)
        listIndex.append(["katapenting", kataPentingStart])
    else:
        listIndex.append(["katapenting", -1])

    dateObj = searchDate(loweredline)

    if(dateObj != None):
        dateStart = dateObj.start()
        date = convertDate(dateObj.group(0))
        listIndex.append(["tanggal", dateStart])
    else:
        listIndex.append(["tanggal", -1])

    (matkulStart, matkulEnd) = searchKeywords(loweredline, "matkul", "mata kuliah")
    listIndex.append(["matkul", matkulStart])

    (topikStart, topikEnd) = searchKeywords(line, "topik", "materi")
    listIndex.append(["topik", topikStart])

    listIndex.sort(key=lambda x: x[1])
    
    for pair in listIndex:
        if(pair[1] == -1):
            return -1

    for i in range (len(listIndex)):
        if(listIndex[i][0] == "matkul"):
            if(i == len(listIndex) - 1):
                namaMatkul = (line[matkulEnd:]).strip()
            else:
                namaMatkul = (line[matkulEnd: listIndex[i+1][1]]).strip()

        elif(listIndex[i][0] == "topik"):
            if(i == len(listIndex) - 1):
                namaTopik = (line[topikEnd:]).strip()
            else:
                namaTopik = (line[topikEnd: listIndex[i+1][1]]).strip()
    
    obj = {
        "id" : id,
        "kataPenting" : kataPenting.capitalize(),
        "deadline" : date,
        "matkul" : namaMatkul,
        "topik" : namaTopik,
    }

    return obj

def extractDateStartDateEnd(line):
    if(searchKeywords(line.lower(), "sampai", "dan") != (-1, -1)):
        tanggal1 = searchDate(line)

    if(tanggal1 != None):
        tanggal2 = searchDate(line[tanggal1.end():])
        tanggal1 = convertDate(tanggal1.group(0))

        if(tanggal2 != None):
            tanggal2 = convertDate(tanggal2.group(0))
            return (tanggal1, tanggal2)

    if(searchKeywords(line.lower(), "minggu") != (-1,-1)):
        jmlMinggu = re.search("[0-9]+ minggu", line.lower())
        if(jmlMinggu != None):
            jmlMinggu = int(jmlMinggu.group(0).split(" ")[0])
            startDate = datetime.now()
            endDate = datetime.now() + timedelta(jmlMinggu*7)
            return(startDate.strftime("%d/%m/%Y"), endDate.strftime("%d/%m/%Y"))

    if(searchKeywords(line.lower(), "hari") != (-1,-1)):
        jmlHari = re.search("[0-9]+ hari", line.lower())
        if(jmlHari != None):
            jmlHari = int(jmlHari.group(0).split(" ")[0])
            startDate = datetime.now()
            endDate = datetime.now() + timedelta(jmlHari)
            return(startDate.strftime("%d/%m/%Y"), endDate.strftime("%d/%m/%Y"))

    return (datetime.now().strftime("%d/%m/%Y"), "31/12/9999")

# def extractJenisTugas(line):
#     (keywordStart, keywordEnd) = searchKeywords(line.lower(), "kuis", "tubes", "tucil", "ujian", "praktikum")

#     if(keywordStart != -1):
#         return line[keywordStart:keywordEnd + 1]

#     return "all"
obj = {
    "id" : 1,
    "kataPenting" : "Tucil",
    "deadline" : "14/05/2020",
    "matkul" : "Strategi Algoritma",
    "topik" : "Anu",
}

# print(searchDate("14/02/2021 adhajdhajsdhk"))
# print(searchDate("14 Februari 2021 adhajdhajsdhk"))