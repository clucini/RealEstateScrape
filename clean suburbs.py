subs = []
with open("suburbs.txt",'r') as f:
    line = f.readline()
    while line != "":
        subs.append(line.replace("-", '\n'))
        line = f.readline()
with open("cleansubs.txt",'w') as f:
    f.writelines(subs)