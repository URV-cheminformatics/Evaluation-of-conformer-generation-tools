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
#This script generate conformers of a set of bioactive conformers by CONFGEN using different methodologies like: VERY FAST, FAST, INTERMEDIATE, COMPREHENSIVE, PHASE FAST, PHASE QUALITY AND FAST CF
#Also, there is the pretreatment specific, like: LIGPREP EPIK AND LIGPREP IONIZER

import os, subprocess
from glob import glob
from schrodinger.job import jobcontrol


#CHANGE YOUR PATHS IN THOSE VARIABLES

output_EPIK_conformation = 'Ligands_conformations/CONFGEN_epik/'
output_IONIZER_conformation = 'Ligands_conformations/CONFGEN_ionizer/'
output_pretractament_IONIZER = 'Pretreatments/CONFGEN_Ionizer/'
output_pretractament_EPIK = 'Pretreatments/CONFGEN_Epik/'
input_ligand = 'Input_ligands/'

#List of hetids
hetids = [line.strip() for line in open('hetids5370.txt',  'rb')] 

methods = ['VERY_FAST' , 'FAST',  'INTERMEDIATE', 'COMPREHENSIVE', 'PHASE_QUALITY',  'PHASE_FAST',  'FAST_CF']


for hetid in hetids:
    print hetid
        
    input = os.path.join(input_ligand,  hetid + '.sdf')
    
    #PRETREATMENT LIGPREP WITH EPIK
    pretractament =  os.path.join(os.environ['SCHRODINGER'], 'ligprep') + " -g  -W e,-ph,7.0,-pht,0.0 -nt -nz -s 32" + " -isd " + input +   " -omae " + output_pretractament_EPIK + hetid + '_epik.mae' 
    job = jobcontrol.launch_job(pretractament.split())
    job.wait()
    print 'pretreatment epik done'
    
    #PRETREATMENT LIGPREP WITH IONIZER
    pretractament =  os.path.join(os.environ['SCHRODINGER'], 'ligprep') + " -g  -W i,-ph,7.0,-pht,0.0 -nt -nz -s 32" + " -isd " + input +   " -omae " + output_pretractament_IONIZER + hetid + '_ionizer.mae' 
    job = jobcontrol.launch_job(pretractament.split())
    job.wait()
    print 'pretreatment ionizer done'
    
    pretreated_EPIK = output_pretractament_EPIK + hetid + '_epik.mae'
    pretreated_IONIZER = output_pretractament_IONIZER + hetid + '_ionizer.mae'

    CWD = os.getcwd()
    
    #CONFORMER GENERATION
    for method in methods:
        
            #CONFORMER GENERATION WITH IONIZER
            if os.path.isfile(pretreated_IONIZER):
                if not os.path.isdir(output_IONIZER_conformation + method + '/'):
                    os.makedirs(output_IONIZER_conformation + method + '/')
                if not os.path.isfile(output_IONIZER_conformation + method +'/' + hetid + '_CONFGEN_' + method + '.sdf'):
                    os.chdir(output_pretractament_IONIZER)
                    confgen =  os.path.join(os.environ['SCHRODINGER'], 'confgen') + " '-" + method +",-MIN_OUT' " + os.path.basename(pretreated_IONIZER)
                    job = jobcontrol.launch_job(confgen.split())
                    job.wait()
                    print 'conformations ionizer', hetid, method
                    
                    os.chdir(CWD)      
                    conformations = output_pretractament_IONIZER + hetid + '_ionizer-out.maegz'
                    
                    #CONVERTION TO SDF 
                    convertion_sdf =  os.path.join(os.environ['SCHRODINGER'], 'utilities',  'structconvert') + " -imae " + conformations +  " -osd " + output_IONIZER_conformation + method + '/' + hetid + "_CONFGEN_" + method + ".sdf"
                    subprocess.call(convertion_sdf.split())
                    print 'convertion sdf done'
                    os.remove(conformations)
                    os.remove(conformations.replace('-out.maegz', '.log'))
                    print 'maegz borrat'  
            
            
            #CONFORMER GENERATION WITH EPIK
            if os.path.isfile( pretreated_EPIK):
                if not os.path.isdir(output_EPIK_conformation + method + '/'):
                    os.makedirs(output_EPIK_conformation + method + '/')
                if not os.path.isfile(output_EPIK_conformation + method +'/' + hetid + '_CONFGEN_' + method + '.sdf'):
                    os.chdir(output_pretractament_EPIK)
                    confgen =  os.path.join(os.environ['SCHRODINGER'], 'confgen') + " '-" + method +",-MIN_OUT' " + os.path.basename(pretreated_EPIK)
                    job = jobcontrol.launch_job(confgen.split())
                    job.wait()
                    print 'conformations epik', hetid, method
                    
                    os.chdir(CWD)      
                    conformations = output_pretractament_EPIK + hetid + '_epik-out.maegz'
                    
                    #CONVERTION TO SDF 
                    convertion_sdf =  os.path.join(os.environ['SCHRODINGER'], 'utilities',  'structconvert') + " -imae " + conformations +  " -osd " + output_EPIK_conformation + method + '/' + hetid + "_CONFGEN_" + method + ".sdf"
                    subprocess.call(conversio.split())
                    print 'convertion sdf done'
                    os.remove(conformations)
                    os.remove(conformations.replace('-out.maegz', '.log'))
                    print 'maegz borrat'
        
    log =  glob('*.log')
    for file in log:
        os.remove(file)
        
    maegz =  glob('*.maegz')
    for file in maegz:
        os.remove(file)
