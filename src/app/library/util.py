import re
def removeWords(line, *words):
    for word in words:
        line = line.replace(word, "")
    
    return line

# # * Convert task objek jadi :"(ID) Deadline-matkul-kata penting-topik"
def convertTaskToMessage(task):
    if(task != -1):
        return "(ID:" + str(task["id"]) + ") " + str(task["deadline"]) + " - " + task["matkul"] + " - " + task["kataPenting"] + " - " + task["topik"]

    return ""

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
        return date[0:6] + "20" + date[-2:]
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

# check if date1 sebelum date2
# ex; isBefore("14/05/2020", "14/06/2020") = True
def isBefore(date1, date2):
    arr1 = date1.split("/")
    day1 = int(arr1[0])
    month1 = int(arr1[1])
    year1 = int(arr1[2])

    arr2 = date2.split("/")
    day2 = int(arr2[0])
    month2 = int(arr2[1])
    year2 = int(arr2[2])

    # date 1 < date 2
    if ((month1 < month2 and year1 <= year2) or (day1 <= day2 and month1 == month2 and year1 == year2)):
        return True
    else:
        return False

def isQualified(task, katapenting, startDate, endDate):
    if(not (isBefore(startDate, task["deadline"]) and isBefore(task["deadline"], endDate))):
        return False
    
    if(katapenting == "" and (task["kataPenting"] == "Tubes" or task["kataPenting"] == "Tucil")):
        return True

    if(not(katapenting.lower() == task["kataPenting"].lower())):
        return False

    return True