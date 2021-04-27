from checker import *
from fitur import *

availableID = 1
taskList = []
line = ""

while(line != "exit"):
    line = input("Masukkan command: ")

    if(line != "exit"):
        (message, availID, taskList) = checkFitur(line, availableID, taskList)
        print(message)
        