import os
import time

for i in xrange(1, 9):
    os.system('cp input{}.txt input.txt'.format(i))
    print("-->On test case #{0}<--".format(i))
    start_time = time.time()
    os.system('python homework.py > /dev/null')
    print("Runing time: {0}ms".format(int((time.time() - start_time) * 1000)))
    os.system('diff -u --ignore-all-space ./output.txt ./output{}.txt'.format(i))

os.system('rm input.txt output.txt')
