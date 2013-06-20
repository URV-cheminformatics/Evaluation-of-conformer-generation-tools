#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012-2013 María José Ojeda Montes <mjose.ojeda@urv.cat>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
#This script allows calculate the CPU time of the user time of childrenprocess (os.times()[2]) generating conformers of ConfGen (Schrödinger Suite), that is, the time used to generate conformers for a ligand. The set is 700 ligands of 1-7 rotatable bonds.  

import os,  subprocess,  time, shutil
from glob import glob
from schrodinger.job import jobcontrol
import pickle
import time

#CHANGE YOUR PATHS IN THOSE VARIABLES
path_to_ligprep = 'Pretreatments/LIGPREP/'
output_CONFGEN = 'Conformations_CPU_TIME/CONFGEN/'

#List of hetids and rotatable bonds
hetids = [line.strip() for line in open('hetids_CPU_TIME.txt',  'rb')] 
enrot_dict = pickle.load(open('dictionary_enrot.bin'))

#Dictionary where the clue is the number of rotatable bonds and the values are the time
CPU_time ={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
keys = CPU_time.keys()
keys.sort()

lines = []
#Different methods availables by ConfGen to generate conformers
methods = ['VERY_FAST',  'FAST', 'INTERMEDIATE', 'COMPREHENSIVE', 'FAST_CF', 'PHASE_FAST', 'PHASE_QUALITY']

for method in methods:
    for hetid in hetids:
        ligprep = path_to_ligprep + hetid + "_ligprep.mae"
        CWD = os.getcwd()
        os.chdir(path_to_ligprep)
        print hetid
        
        #Command to generate conformers by Confgen. Methods: -VERY_FAST; -FAST; -INTERMEDIATE; -COMPREHENSIVE; -FAST_CF; -PHASE_FAST; -PHASE_QUALITY
        confgen =  os.path.join(os.environ['SCHRODINGER'], 'confgen') + " '-" + method + ",-MIN_OUT' " + os.path.basename(ligprep)
        job = jobcontrol.launch_job(confgen.split())
        os.chdir(CWD)
        
        #Output of conformers
        conformers = output_CONFGEN + method +'/'
        if not os.path.isdir(conformers):
            os.makedirs(conformers)
        
        #Select CPU time from .log files. 
        log = path_to_ligprep + hetid + "_ligprep.log"
        job.wait()
        filelog = open(log, 'rb')
        for line in filelog:
            lines.append(line)
        time_line = lines[-2]
        ctime = time_line.split('u')[0]
        print ctime
        #Add cpu time for each ligand to dictionary depends on number of rotatable bond. 
        for key in keys:
            if key == enrot_dict[hetid]:
                CPU_time[key] += float(ctime)
                print "Confgen",  method,  key, ':', CPU_time[key]
        filelog.close()       
        #Move file to another directory
        shutil.move(log, conformers)
        for maegz in glob (path_to_ligprep + '*.maegz'):
            shutil.move(maegz, conformers)
    out = open('cpu_time_schrodinger.txt','ab')
    out.write(method + ' '+ CPU_time + '\n')
    print CPU_time
                        
out.close()
    
