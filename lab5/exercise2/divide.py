import os

folder = 'img'
file = open("index.txt", "r")
while True:
    line  =  file.readline()
    # If line is empty then end of file reached
    if  not  line  :
        break
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    filename = line.split('\t')[1] + '.txt'
    f = open(os.path.join(folder, filename), 'w')
    f.write(line)  # 将网页存入文件
    f.close()