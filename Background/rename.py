import os
path = r"C:\Users\subha\Desktop\Pycharm projects\first game la\Background1"
files = os.listdir(path)
print(files)


x = 0 
for file in files:
    # global x
    oldfileandpath = files[x]
    str(oldfileandpath)

    filenameandpath = f"{x}.jpg"
    os.rename(oldfileandpath,filenameandpath)
    x +=1