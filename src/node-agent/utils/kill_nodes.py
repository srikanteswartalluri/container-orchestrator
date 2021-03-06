import random
import sys
import os

n = int(sys.argv[1])
if n > 5:
    sys.exit("n should be less than 6")
l = []
list_len = len(l)
while list_len < n:
    temp = random.randint(12375, 12379)
    if temp not in l:
        l.append(temp)
    list_len = len(l)
print(l)
for n in l:
    node = "co_node_{}".format(n)
    os.system("docker stop {}".format(node))

