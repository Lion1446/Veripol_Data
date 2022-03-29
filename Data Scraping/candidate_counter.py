import csv


counter = 0
with open('D:\\Lion\\Non-School-Stuffs\\Projects\\ARDE\\VeriPol\\env\\templates\\file.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            int(row[0])
            counter+=1
            # print(row[0])
        except:
            # print(f"not: {row}")
            pass
        # if row[0].isnumeric:
        #     counter+=1
        #     print(row[0])
    
print(f"There are {counter} candidates in this file")
        
