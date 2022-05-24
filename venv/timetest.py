from random import randint
from time import sleep
from datetime import datetime

array1 = [
    "a",
    "b",
    "c",
    "x",
    "y",
    "z"
]

array2 = [
    "1",
    "20",
    "400"
]

def test():
    test.array3 = []
    for ele in array1:
        test.array3.apppend(ele)

test()

print(test.array3)

starttime = datetime.now()

totalparts = len(array1) * len(array2)
completedparts = 0


for ele in array1:
    for elem in array2:
        sleep(randint(1, 3))
        completedparts += 1
        currenttime = datetime.now()
        et = currenttime - starttime
        elapsedtime = et.seconds
        estimatedtime = elapsedtime * totalparts / completedparts
        timetocompletion = estimatedtime - elapsedtime
        print("time to completion %s seconds" % timetocompletion)
