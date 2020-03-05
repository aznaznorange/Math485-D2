import os
import json

frame = ['Male', 'Age', 'Debt', 'Married',
             'BankCustomer', 'EducationLevel',
             'Ethnicity', 'YearsEmployed', 'PriorDefault',
             'Employed', 'CreditScore', 'DriversLicense',
             'Citizen', 'ZipCode', 'Income', 'Approved']

def main():
    inputFile = 'crx.data'
    outputFile = './lib/crx.py'

    if not os.path.exists(inputFile):
        print("error: %s not found", inputFile)
    if os.path.exists(outputFile):
        print("error: %s already exists", outputFile)
    
    try:
        fp = open(inputFile, 'r')
        lines = fp.readlines()
        
        fo = open(outputFile, 'w')
        
        fo.write('crx_data = [\n');

        lineNum = 1
        for line in lines:
            if "?" in line:
                continue
            if parseMethod1(line.split(','), fo, lineNum):
                fo.write(',\n')
            lineNum += 1

        fo.seek(0, os.SEEK_END)
        fo.seek(fo.tell() - 3, os.SEEK_SET)
        fo.truncate()
            
        fo.write('\n]')
            
    finally:
        fp.close()
        fo.close()

    return


def parseMethod1(dataArr, fo, lineNum):
    if len(dataArr) != len(frame):
        print('Invalid data, line %s', lineNum)
        return False

    dataObj = {}
    for i in range(len(frame)):
        if i == 0:
            if dataArr[i] == "a":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 1:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 2:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 3:
            if dataArr[i] == "u":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "y":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "l":
                dataObj[frame[i]] = 2
            else:
                dataObj[frame[i]] = 3
        elif i == 4:
            if dataArr[i] == "g":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "p":
                dataObj[frame[i]] = 1
            else:
                dataObj[frame[i]] = 2
        elif i == 5:
            if dataArr[i] == "c":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "d":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "cc":
                dataObj[frame[i]] = 2
            elif dataArr[i] == "i":
                dataObj[frame[i]] = 3
            elif dataArr[i] == "j":
                dataObj[frame[i]] = 4
            elif dataArr[i] == "k":
                dataObj[frame[i]] = 5
            elif dataArr[i] == "m":
                dataObj[frame[i]] = 6
            elif dataArr[i] == "r":
                dataObj[frame[i]] = 7
            elif dataArr[i] == "q":
                dataObj[frame[i]] = 8
            elif dataArr[i] == "w":
                dataObj[frame[i]] = 9
            elif dataArr[i] == "x":
                dataObj[frame[i]] = 10
            elif dataArr[i] == "e":
                dataObj[frame[i]] = 11
            elif dataArr[i] == "aa":
                dataObj[frame[i]] = 12
            else:
                dataObj[frame[i]] = 13
        elif i == 6:
            if dataArr[i] == "v":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "h":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "bb":
                dataObj[frame[i]] = 2
            elif dataArr[i] == "j":
                dataObj[frame[i]] = 3
            elif dataArr[i] == "n":
                dataObj[frame[i]] = 4
            elif dataArr[i] == "z":
                dataObj[frame[i]] = 5
            elif dataArr[i] == "dd":
                dataObj[frame[i]] = 6
            elif dataArr[i] == "ff":
                dataObj[frame[i]] = 7
            else:
                dataObj[frame[i]] = 8
        elif i == 7:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 8:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 9:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 10:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 11:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 12:
            if dataArr[i] == "g":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "p":
                dataObj[frame[i]] = 1
            else:
                dataObj[frame[i]] = 2
        elif i == 13:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 14:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 15:
            if "-" in dataArr[i]:
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        else:
            dataObj[frame[i]] = dataArr[i]

    fo.write(json.dumps(dataObj))
    return True

def parseMethod2(dataArr, fo, lineNum):
    if len(dataArr) != len(frame):
        print('Invalid data, line %s', lineNum)
        return False

    dataObj = {}
    writeObj = []
    for i in range(len(frame)):
        if i == 0:
            if dataArr[i] == "a":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 1:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 2:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 3:
            if dataArr[i] == "u":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "y":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "l":
                dataObj[frame[i]] = 2
            else:
                dataObj[frame[i]] = 3
        elif i == 4:
            if dataArr[i] == "g":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "p":
                dataObj[frame[i]] = 1
            else:
                dataObj[frame[i]] = 2
        elif i == 5:
            if dataArr[i] == "c":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "d":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "cc":
                dataObj[frame[i]] = 2
            elif dataArr[i] == "i":
                dataObj[frame[i]] = 3
            elif dataArr[i] == "j":
                dataObj[frame[i]] = 4
            elif dataArr[i] == "k":
                dataObj[frame[i]] = 5
            elif dataArr[i] == "m":
                dataObj[frame[i]] = 6
            elif dataArr[i] == "r":
                dataObj[frame[i]] = 7
            elif dataArr[i] == "q":
                dataObj[frame[i]] = 8
            elif dataArr[i] == "w":
                dataObj[frame[i]] = 9
            elif dataArr[i] == "x":
                dataObj[frame[i]] = 10
            elif dataArr[i] == "e":
                dataObj[frame[i]] = 11
            elif dataArr[i] == "aa":
                dataObj[frame[i]] = 12
            else:
                dataObj[frame[i]] = 13
        elif i == 6:
            if dataArr[i] == "v":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "h":
                dataObj[frame[i]] = 1
            elif dataArr[i] == "bb":
                dataObj[frame[i]] = 2
            elif dataArr[i] == "j":
                dataObj[frame[i]] = 3
            elif dataArr[i] == "n":
                dataObj[frame[i]] = 4
            elif dataArr[i] == "z":
                dataObj[frame[i]] = 5
            elif dataArr[i] == "dd":
                dataObj[frame[i]] = 6
            elif dataArr[i] == "ff":
                dataObj[frame[i]] = 7
            else:
                dataObj[frame[i]] = 8
        elif i == 7:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 8:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 9:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 10:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 11:
            if dataArr[i] == "t":
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        elif i == 12:
            if dataArr[i] == "g":
                dataObj[frame[i]] = 0
            elif dataArr[i] == "p":
                dataObj[frame[i]] = 1
            else:
                dataObj[frame[i]] = 2
        elif i == 13:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 14:
            dataObj[frame[i]] = float(dataArr[i])
        elif i == 15:
            if "-" in dataArr[i]:
                dataObj[frame[i]] = 0
            else:
                dataObj[frame[i]] = 1
        else:
            dataObj[frame[i]] = dataArr[i]

        writeObj.append(dataObj[frame[i]])

    fo.write(str(writeObj))
    return True

main()
