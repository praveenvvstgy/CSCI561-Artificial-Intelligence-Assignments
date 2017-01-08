import os
import time

for i in xrange(1, 11):
    os.system('cp ./inputs/Test{0}/input.txt input.txt'.format(i))
    print("-->On test case #{0}<--".format(i))
    start_time = time.time()
    os.system('./a.out > /dev/null')
    print("Runing time: {0}ms".format(int((time.time() - start_time) * 1000)))
    os.system('diff ./output.txt ./inputs/Test{0}/output.txt'.format(i))

os.system('rm input.txt output.txt')
