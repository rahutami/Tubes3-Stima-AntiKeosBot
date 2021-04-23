import re
def removeWords(line, *words):
    for word in words:
        line = line.replace(word, "")
    
    return line

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

def convertDateToDays(date):
    arr = date.split("/")
    day = int(arr[0])
    month = int(arr[1])
    year = int(arr[2])

    return day + month*30 + year*365

def compareDates(date1, date2):
    if(convertDateToDays(date1) < convertDateToDays(date2)):
        return -1
    if(convertDateToDays(date1) == convertDateToDays(date2)):
        return 0
    if(convertDateToDays(date1) < convertDateToDays(date2)):
        return 1
