import re

def getcsvData_dict(filePath):
    '''OutPut: 
    Dict {Header_0: [data0, data1, data2,], Header_1 : [data0, data1, data2,], Header_1]} '''
    file1 = open(filePath, 'r')

    data = {}
    line = file1.readline().strip()
    Headers = re.split(",", line)

    for header in Headers:
        data[header] = []

    units = file1.readline().strip()
    #print(units)

    while True:
        line = file1.readline().strip()
        if not line:
            break
        dataLine = line.strip()
        dataLine = re.split(",", dataLine)

        if dataLine[-1] == '':
            break

        for i, header in enumerate(Headers):
            
            data[header].append(float(dataLine[i]))

    file1.close()
    return data

if __name__ == '__main__':
    x = getcsvData_dict('Electronique\Lab5\Data(5)\scope_5.csv')
    print(x)
    print(x.keys())