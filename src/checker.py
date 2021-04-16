import re
from datetime import datetime

def convertMonth(month):
    if(month == "januari"):
        return "01"
    elif(month == "februari"):
        return "02"
    elif(month == "maret"):
        return "03"
    elif(month == "april"):
        return "04"
    elif(month == "mei"):
        return "05"
    elif(month == "juni"):
        return "06"
    elif(month == "juli"):
        return "07"
    elif(month == "agustus"):
        return "08"
    elif(month == "september"):
        return "09"
    elif(month == "oktober"):
        return "10"
    elif(month == "november"):
        return "11"
    elif(month == "desember"):
        return "12"

def convertDate(date):
    months = ["april", "juni", "september", "november", "januari", "maret","mei", "juli", "agustus", "oktober", "desember", "februari"]

    if(re.search("([0-2][0-9]|3[01])/[01][0-9]/[0-9]{2}", date) != None):
        return date[0:6] + "20" + date[6:8]
    elif(re.search("[0-9][0-9] (" + '|'.join(months) + ") [0-9]{4}", date) != None):
        return date[0:2] + "/" + convertMonth(date[3:-5]) + "/" + date[-4:]

def isLeapYear(year):
    if(len(year) == 2):
        year = int("20" + year)
    else:
        year = int(year[-4:0])

    print(year)
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# accept DD/MM/YY DD/MM/YYYY "DD Month Year"
# ex: 14/05/20 14/05/2020 14 Mei 2020
# Februari asumsi gamungkin masukkin 29 Februari tp yearnya ga kabisat 
def dateContained(line):
    line = line.lower()
    months30 = ["04", "06", "09", "11"]
    months31 = ["01", "03","05", "07", "08", "10", "12"]

    # Cek format DD/MM/YY
    date = re.search("([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{2}", line)
    if(date != None):
        return convertDate(date.group(0))

    date = re.search("([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{2}", line)
    if(date != None):
        return convertDate(date.group(0))

    date = re.search("[0-2][0-9]/02/[0-9]{2}", line)
    if(date != None):
        return convertDate(date.group(0))
    
    # Cek format DD/MM/YYYY
    date = re.search("([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))    
    
    date = re.search("([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))

    date = re.search("[0-2][0-9]/02/[0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))

    months30 = ["april", "juni", "september", "november"]
    months31 = ["januari", "maret","mei", "juli", "agustus", "oktober", "desember"]
    
    # Cek format DD Month YYY
    date = re.search("([0-2][0-9]|30) (" + '|'.join(months30) + ") [0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))

    date = re.search("([0-2][0-9]|3[01]) (" + '|'.join(months31) + ") [0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))

    date = re.search("([0-2][0-9]) Februari [0-9]{4}", line)
    if(date != None):
        return convertDate(date.group(0))
    
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

    return date

# Special word: Kuis, Tubes, Tucil, Ujian, Praktikum
def kataPentingContained(line):
    line = line.lower()
    kataPenting = ["kuis", "tubes", "tucil", "ujian", "praktikum"]
    kataPentingInLine = re.search('|'.join(kataPenting), line)

    if(kataPentingInLine != None):
        return kataPentingInLine.group(0)
    
    return kataPentingInLine

string = "Tubes 12 April 2020"
print(dateContained(string)) #print 12 April 2020
print(kataPentingContained(string)) #print Tubes
print(convertDate("12/02/20"))