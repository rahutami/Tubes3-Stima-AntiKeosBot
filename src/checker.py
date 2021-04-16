import re
from datetime import datetime

# accept DD/MM/YY DD/MM/YYYY "DD Month Year"
# ex: 14/05/20 14/05/2020 14 Mei 2020
# Februari asumsi gamungkin masukkin 29 Februari tp yearnya ga kabisat 
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

def dateContained(line):

    months30 = ["04", "06", "09", "11"]
    months31 = ["01", "03","05", "07", "08", "10", "12"]

    # Cek format DD/MM/YY
    date = re.search("([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{2}", line)
    if(date != None):
        return date.group(0)

    date = re.search("([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{2}", line)
    if(date != None):
        return date.group(0)

    date = re.search("[0-2][0-9]/02/[0-9]{2}", line)
    if(date != None):
        return date.group(0)
    
    # Cek format DD/MM/YYYY
    date = re.search("([0-2][0-9]|30)/(" + '|'.join(months30) + ")/[0-9]{4}", line)
    if(date != None):
        return date.group(0)    
    
    date = re.search("([0-2][0-9]|3[01])/(" + '|'.join(months31) + ")/[0-9]{4}", line)
    if(date != None):
        return date.group(0)

    date = re.search("[0-2][0-9]/02/[0-9]{4}", line)
    if(date != None):
        return date.group(0)

    months30 = ["April", "Juni", "September", "November"]
    months31 = ["Januari", "Maret","Mei", "Juli", "Agustus", "Oktober", "Desember"]
    
    # Cek format DD Month YYY
    date = re.search("([0-2][0-9]|30) (" + '|'.join(months30) + ") [0-9]{4}", line)
    if(date != None):
        return date.group(0)

    date = re.search("([0-2][0-9]|3[01]) (" + '|'.join(months31) + ") [0-9]{4}", line)
    if(date != None):
        return date.group(0)

    date = re.search("([0-2][0-9]) Februari [0-9]{4}", line)
    if(date != None):
        return date.group(0)
    
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
    kataPenting = ["Kuis", "Tubes", "Tucil", "Ujian", "Praktikum"]
    return re.search('|'.join(kataPenting), line).group(0)

string = "Tubes 12 April 2020"
print(dateContained(string)) #print 12 April 2020
print(kataPentingContained(string)) #print Tubes