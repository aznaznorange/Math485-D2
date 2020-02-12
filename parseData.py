import os
import json

frame = ['Male', 'Age', 'Debt', 'Married',
             'BankCustomer', 'EducationLevel',
             'Ethnicity', 'YearsEmployed', 'PriorDefault',
             'Employed', 'CreditScore', 'DriversLicense',
             'Citizen', 'ZipCode', 'Income', 'Approved']

def main():
    inputFile = 'crx.data'
    outputFile = 'crx.py'

    if not os.path.exists(inputFile):
        print("error: %s not found", inputFile)
    if os.path.exists(outputFile):
        print("error: %s already exists", outputFile)
    
    try:
        fp = open(inputFile, 'r')
        lines = fp.readlines()
        
        fo = open(outputFile, 'w')
        
        fo.write('crx = [\n');
        
        for line in lines:
            if parseMethod1(line.split(','), fo):
                fo.write(',\n')

        fo.seek(0, os.SEEK_END)
        fo.seek(fo.tell() - 3, os.SEEK_SET)
        fo.truncate()
            
        fo.write('\n]')
            
    finally:
        fp.close()
        fo.close()

    return


def parseMethod1(dataArr, fo):
    if len(dataArr) != len(frame):
        return False

    dataObj = {}
    for i in range(len(frame)):
        dataObj[frame[i]] = dataArr[i]

    fo.write(json.dumps(dataObj))
    return True
        
main()
