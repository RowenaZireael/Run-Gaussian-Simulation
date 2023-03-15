#/usr/bin/env python
"""
Created on Mon Apr 18 11:58:06 2022

@author: Rowena
"""

import os
import sys
import re

file_dir = "/Users/your_user_name/Desktop/today/"
filetype = ".gjf"
Names=[]
for root, dirs, files in os.walk(file_dir):
    for name in files:
        if filetype in name:          
            N=name[:-4]
            Names.append(N)
print(Names)

print('Enter walltime in hh:mm(eg. 10:00) :')
walltime=sys.stdin.readline().rstrip()

            
print('Enter vmem in mb (eg. 800) :')
mem=sys.stdin.readline().rstrip()


print('Enter jobfs in mb (eg. 800) :')
jobfs=sys.stdin.readline().rstrip()


for i in Names:
    with open("/Users/your_user_name/Desktop/today/"+str(i)+".gjf") as ofile:
        lines=ofile.read()
    findcore=re.search('nproc',lines)
    corepos=findcore.span()
    findcoreend=re.search('chk',lines)
    coreendpos=findcoreend.span()
    rawcorenum=lines[corepos[1]:coreendpos[0]]    
    corenum=re.search(r"\d+",rawcorenum).group()
        
    file = open("/Users/your_user_name/Desktop/today/"+str(i)+".submit","w")
    file.write("#!/bin/bash\n#PBS -l wd\n#PBS -q normal\n#PBS -l walltime=")
    file.write(walltime)
    file.write(":00,mem=")
    file.write(mem)
    file.write("mb,ncpus=")
    file.write(corenum)
    file.write(",software=g16,jobfs=")
    file.write(jobfs)
    file.write("mb,storage=scratch/p39\n\nmodule load gaussian/g16c01\
\ncpulist=`grep Cpus_allowed_list: /proc/self/status | awk '{print $2}'` ")
    file.write('\nexport GAUSS_CDEF="$cpulist"\ng16 < ')
    file.write(str(i))
    file.write(".gjf > ")
    file.write(str(i))
    file.write(".out 2>&1")
    file.close()
