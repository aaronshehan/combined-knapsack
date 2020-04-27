  
import random
import sys

types = ['f', 'w']

f = open("input.txt", "w")

id = 0

for i in range(random.randint(1, int(sys.argv[1]))):
    f.write(str(id) + ' ' + str(random.randint(1, 11)) + ' ' + str(random.randint(11, 101)) + ' ' + str(random.choice(types)) + '\n')
    id += 1

f.close()
