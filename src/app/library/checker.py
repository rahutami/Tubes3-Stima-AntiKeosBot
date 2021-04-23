import re
from app.library.util import *

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
def searchDate(line):
    line = line.lower()
    months30 = ["04", "06", "09", "11"]
    months31 = ["01", "03","05", "07", "08", "10", "12"]

    # Cek format DD/MM/YY
    date = re.search("(([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{2})|(([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{2})|([0-2][0-9]/02/[0-9]{2})", line)
    if(date != None):
        return (date.start(), convertDate(date.group(0)))
    
    # Cek format DD/MM/YYYY
    date = re.search("(([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{4})|(([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{4})|([0-2][0-9]/02/[0-9]{4})", line)
    if(date != None):
        return (date.start(), convertDate(date.group(0)))    

    months30 = ["april", "juni", "september", "november"]
    months31 = ["januari", "maret","mei", "juli", "agustus", "oktober", "desember"]
    
    # Cek format DD Month YYY
    date = re.search("(([0-2][0-9]|30) (" + '|'.join(months30) + ") [0-9]{4})|(([0-2][0-9]|3[01]) (" + '|'.join(months31) + ") [0-9]{4})|([0-2][0-9] Februari [0-9]{4})", line)
    if(date != None):
        return (date.start(), convertDate(date.group(0)))
    
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

    return (-1, -1)

# Special word: Kuis, Tubes, Tucil, Ujian, Praktikum
def searchKataPenting(line):
    kataPenting = ["kuis", "tubes", "tucil", "ujian", "praktikum"]
    kataPentingInLine = re.search('|'.join(kataPenting), line)

    if(kataPentingInLine != None):
        return (kataPentingInLine.start(), kataPentingInLine.group(0))
    
    return (-1, -1)

# Cari "matkul" or "mata kuliah"
def searchKeywordMatkul(line):
    keyword = re.search(" matkul ", line)

    if(keyword == None):
        keyword = re.search(" mata kuliah ", line)

    if(keyword == None):
        return (-1,-1)
    else:
        return (keyword.start(), keyword.end())

# Cari "topik" or "materi"
def searchKeywords(line, *keywords):

    for keyword in keywords:
        index = re.search(keyword, line)
        if(index != None):
            return (index.start(), index.end())

    return (-1,-1)

def extractTaskFromLine(line, id):
    line = removeWords(line, "tanggal", "Tanggal", "deadline", "Deadline")
    loweredline = line.lower()

    listIndex = []

    (kataPentingStart, kataPenting) = searchKataPenting(loweredline)
    listIndex.append(["katapenting", kataPentingStart])

    (dateStart, date) = searchDate(loweredline)
    listIndex.append(["tanggal", dateStart])

    (matkulStart, matkulEnd) = searchKeywords(loweredline, " matkul ", " mata kuliah ")
    listIndex.append(["matkul", matkulStart])

    (topikStart, topikEnd) = searchKeywords(line, " topik ", " materi ")
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

# removeUnnecessaryWords("tanggal 1")