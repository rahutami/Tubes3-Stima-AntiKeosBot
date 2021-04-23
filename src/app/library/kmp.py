def makeBorderFunction(str1):
    k = [i for i in range (-1, len(str1) - 1)]

    borderFunction = []
    for i in range (len(k)):
        borderFunction.append(0)

        for j in range (k[i]):
            if str1[0:j+1] == str1[k[i]-j:k[i]+1]:
                borderFunction[i] = len(str1[0:j+1])
    
    return borderFunction


def searchKMP (str1, str2):
    if(len(str1) > len(str2)):
        str3 = str1
        str1 = str2
        str2 = str3

    str1 = str1.lower()
    str2 = str2.lower()
    
    borderFunction = makeBorderFunction(str1)
    print(borderFunction)
    found = False

    (i,j) = (0,0)

    while(i < len(str2) and not found):
        if(j == len(str1) - 1 and str1[j] == str2[i]):
            found = True

        if(str1[j] != str2[i]):
            j = borderFunction[j-1] - 1
        
        j += 1
        i += 1
    
    # return index start
    if(not found):
         return -1

    return i-len(str1)