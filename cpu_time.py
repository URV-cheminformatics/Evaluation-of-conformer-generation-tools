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
#This script allows calculate the CPU time of the user time of childrenprocess (os.times()[2]), that is, the time used to generate conformers for a ligand. The set is 700 ligands of 1-7 rotatable bonds.  

import os, pybel, subprocess, time,  shutil
from glob import glob

#CHANGE YOUR PATHS IN THOSE VARIABLES

path_to_ligands = 'Input_ligands/'
path_to_pretreatment_clean3d = "Pretreatments/CLEAN3D/"
path_to_pretreatment_standard = 'Pretractaments_lligands/STANDARD/'
path_to_pretreatment_ring = 'Pretractaments_lligands/RING_CONFORMATIONS/'
path_to_pretreatment_xedconvert = 'Pretractaments_lligands/XEDCONVERT/'

path_to_balloon = '/home/mjose/BioMolSoft/Balloon/balloon'
path_to_clean3d = '/home/mjose/BioMolSoft/Chemaxon/bin/cxcalc'
path_to_confab = '/usr/local/bin/confab'
path_to_cyndi = '/home/mjose/BioMolSoft/Cyndi/Cyndi'
path_to_omega = "/home/mjose/BioMolSoft/openeye/bin/omega2"
path_to_rotate = '/home/mjose/BioMolSoft/rotate.lnx'
path_to_vconf = "/home/mjose/BioMolSoft/Vconf_Verachem/vconf_v2_acad/vconf.exe"
path_to_xedex = "/home/mjose/BioMolSoft/cresset/xed/bin/xedex"
path_to_corina = '/home/mjose/BioMolSoft/corina.lnx'
path_to_xedconvert = "/home/mjose/BioMolSoft/cresset/xed/bin/xedconvert"


output_BALLOON = 'Conformations_CPU_TIME/BALLOON/'
output_CLEAN3D_wp = 'Conformations_CPU_TIME/CLEAN3D_white_paper/'
output_CLEAN3D_st = 'Conformations_CPU_TIME/CLEAN3D_standard/'
output_CLEAN3D_ring = 'Conformations_CPU_TIME/CLEAN3D_ring/'
output_CONFAB = 'Conformations_CPU_TIME/CONFAB/'
output_CYNDI_st = 'Conformations_CPU_TIME/CYNDI_standard/'
output_CYNDI_ring = 'Conformations_CPU_TIME/CYNDI_ring/'
output_OMEGA = 'Conformations_CPU_TIME/OMEGA/'
output_ROTATE_st = 'Conformations_CPU_TIME/ROTATE_standard/'
output_ROTATE_ring = 'Conformations_CPU_TIME/ROTATE_ring/'
output_Vconf_ring = 'Conformations_CPU_TIME/Vconf_ring/'
output_Vconf_st = 'Conformations_CPU_TIME/Vconf_standard/'
output_XedeX_wp = 'Conformations_CPU_TIME/XedeX_WP/'
output_XedeX_st = 'Conformations_CPU_TIME/XedeX_STANDARD/'
output_XedeX_ring = 'Conformations_CPU_TIME/XedeX_RING/'

#List of hetids
hetids = [line.strip() for line in open('hetids_CPU_TIME.txt',  'rb')] 


#Dictionary that has a key as number of rotatable bonds and a value as the total time needed for each rotatable bond. 
CPU_time ={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
keys = CPU_time.keys()
keys.sort()

for hetid in hetids:
    input = path_to_ligands + hetid + ".sdf"
    input_CLEAN3D =  path_to_pretreatment_clean3d + hetid + "_clean3D.sdf" 
    standard_input_CORINA =  path_to_pretreatment_standard + hetid + "_corina.sdf"
    ring_input_CORINA = path_to_pretreatment_ring + hetid + "_corina_ring.sdf"
    standard_input_CORINA_mol2 = path_to_pretreatment_standard + hetid + "_corina.mol2"
    ring_input_CORINA_mol2 = path_to_pretreatment_ring + hetid + "_corina.mol2"
    xedconvert =  path_to_pretreatment_xedconvert+ hetid + '_xedex.sdf'
    mol = pybel.readfile('sdf', standard_input_CORINA).next()
    enrot = mol.OBMol.NumRotors()
    print enrot

    #Each tool has been calculated one by one. Then, IT HAS TO UNCOMMENT IT. 

#   #BALLOON
#    if not os.path.isdir(output_BALLOON):
#        os.makedirs(output_BALLOON)
#    conformacio_balloon = path_to_balloon+ ' --nconfs 20 --nGenerations 300 --maxtime 60000 -t 0.1 --maxiter 1000 ' +  input + " " + output_BALLOON + hetid + "_balloon.sdf"
#    t0 = os.times()
#    subprocess.call(conformacio_balloon.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Balloon",  clau, ':', CPU_time[clau]
#print CPU_time
#
#   #CLEAN3D    
#   #Conformer generation (white paper)
#    if not os.path.isdir(output_CLEAN3D_wp):
#        os.makedirs(output_CLEAN3D_wp)
#    conformacio_CLEAN3D = path_to_clean3d  + " -Xmx4g "+ " -o " + output_CLEAN3D_wp + hetid + "_clean3D.sdf "+ "conformers -m 1000 -y false " + input_CLEAN3D
#    t0 = os.times()
#    subprocess.call(conformacio_CLEAN3D.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Clean3D",  clau, ':', CPU_time[clau]
#print CPU_time
#    
#    #Standard pretreatment (default parameters)
#    if not os.path.isdir(output_CLEAN3D_st):
#        os.makedirs(output_CLEAN3D_st)
#    conformacio_CHEMAXON_CLEAN3D = path_to_clean3d  + " -o " + output_CLEAN3D_st + hetid + "_clean3D.sdf " + "conformers " + standard_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformacio_CHEMAXON_CLEAN3D.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Clean3D",  clau, ':', CPU_time[clau]
#print CPU_time
#    
#    #Ring conformations pretreatment (default parameters)
#    if not os.path.isdir(output_CLEAN3D_ring):
#        os.makedirs(output_CLEAN3D_ring)
#    conformacio_CHEMAXON_CLEAN3D = path_to_clean3d  + " -o " + output_CLEAN3D_ring + hetid + "_clean3D.sdf " + "conformers " + ring_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformacio_CHEMAXON_CLEAN3D.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Clean3D",  clau, ':', CPU_time[clau]
#print CPU_time
#
#    
#       #CONFAB
#    if not os.path.isdir(output_CONFAB):
#        os.makedirs(output_CONFAB)
#    conformacio_confab = path_to_confab + ' '  + standard_input_CORINA + " " + output_CONFAB+  hetid + "_confab.sdf"
#    t0 = os.times()
#    subprocess.call(conformacio_confab.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Cyndi",  clau, ':', CPU_time[clau]
#print CPU_time
#
#    #CYNDI
#    #Standard pretreatment
#    if not os.path.isdir(output_CYNDI_st):
#        os.makedirs(output_CYNDI_st)
#    conformacio_cyndi =  path_to_cyndi + " -i " + standard_input_CORINA_mol2 + " -o " + output_CYNDI_st + hetid + "_cyndi.mol2 -p Cyndi.param"
#    t0 = os.times()
#    subprocess.call(conformacio_cyndi.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2]  #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Cyndi",  clau, ':', CPU_time[clau]
#print CPU_time  
#
#    #Ring conformations pretreatment 
#    if not os.path.isdir(output_CYNDI_ring):
#        os.makedirs(output_CYNDI_ring)
#    conformacio_cyndi = path_to_cyndi  + " -i " + ring_input_CORINA_mol2 + " -o " + output_CYNDI_ring + hetid + "_cyndi.mol2 -p Cyndi.param"
#    t0 = os.times()
#    subprocess.call(conformacio_cyndi.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Cyndi",  clau, ':', CPU_time[clau]
#print CPU_time
#
#
#   #OMEGA
#    if not os.path.isdir(output_OMEGA):
#        os.makedirs(output_OMEGA)
#    conformacio_omega = path_to_omega +' -in ' + input + " -out " + output_OMEGA + hetid + '_omega.sdf'
#    t0 = os.times()
#    subprocess.call(conformacio_omega.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Omega",  clau, ':', CPU_time[clau]
#print CPU_time
#
#   #ROTATE
#   #Standard pretreatment
#    if not os.path.isdir(output_ROTATE_st):
#        os.makedirs(output_ROTATE_st)
#    conformacio_corina = path_to_rotate + " -d auto " + standard_input_CORINA + " " + output_ROTATE_st + hetid + "_rotate.sdf"
#    t0 = os.times()
#    subprocess.call(conformacio_corina.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Rotate",  clau, ':', CPU_time[clau]
#print CPU_time
#
#    #Ring conformations pretreatment
#    if not os.path.isdir(output_ROTATE_ring):
#        os.makedirs(output_ROTATE_ring)
#    conformacio_corina = path_to_rotate + " -d auto " + ring_input_CORINA  + " " + output_ROTATE_ring +hetid + "_rotate.sdf"
#    t0 = os.times()
#    subprocess.call(conformacio_corina.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Rotate",  clau, ':', CPU_time[clau]
#print CPU_time

#   # Vconf
#    #Standard pretreatment
#    if not os.path.isdir(output_Vconf_st):
#        os.makedirs(output_Vconf_st) 
#    conformation_vconf = path_to_Vconf +' ' + standard_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformation_vconf.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Vconf",  clau, ':', CPU_time[clau]
#    if os.path.isfile(hetid + '_corina_mol_1_confs.sdf'):
#        shutil.move(hetid + '_corina_mol_1_confs.sdf',  output_Vconf_st + hetid + '_corina_mol_1_confs.sdf')
#print CPU_time
        
#    #Ring conformations pretreatment
#    if not os.path.isdir(output_Vconf_ring):
#        os.makedirs(output_Vconf_ring) 
#    conformation_vconf = path_to_Vconf +' ' + ring_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformation_vconf.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "Vconf",  clau, ':', CPU_time[clau]
#            
#    outputfile = output_Vconf_ring + hetid + '_ring_vconf.sdf'
#    for vconffile in glob(hetid+ '*_confs.sdf'):
#        conf = open(vconffile,  'rb')
#        out = open(outputfile,'ab')
#        out.write(conf.read())
#        out.close()
#        os.remove(vconffile)
#print CPU_time
    
#    
#    # XedTools
#    #Standard pretreatment
#    if not os.path.isdir(output_XedeX_st):
#        os.makedirs(output_XedeX_st) 
#    conformation_XedeX = path_to_XedeX +' -0 -w '  + standard_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformation_XedeX.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "XedeX",  clau, ':', CPU_time[clau]
#    if os.path.isfile(standard_input_CORINA.replace('.sdf', '_xedex.sdf')):
#        outputfile = output_XedeX_st + hetid + '_xedex.sdf'
#        shutil.move(standard_input_CORINA.replace('.sdf', '_xedex.sdf'), outputfile)
#print CPU_time
#                    
#    #Ring conformations pretreatment
#    if not os.path.isdir(output_XedeX_ring):
#        os.makedirs(output_XedeX_ring) 
#    conformation_XedeX = path_to_XedeX +' -0 -w '  + ring_input_CORINA
#    t0 = os.times()
#    subprocess.call(conformation_XedeX.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "XedeX",  clau, ':', CPU_time[clau]
#    for xedexfile in glob( ring_input_CORINA.replace('.sdf', '_xedex*.sdf')):
#        outputfile = output_XedeX_ring + hetid + '_xedex.sdf'
#        conf = open(xedexfile,  'rb')
#        out = open(outputfile,'ab')
#        out.write(conf.read())
#        out.close()
#        os.remove(xedexfile)
#print CPU_time

#    #Conformer generation (white paper)
#       
#    if not os.path.isdir(output_XedeX_wp):
#        os.makedirs(output_XedeX_wp) 
#    conformation_XedeX = path_to_XedeX +' -0 -m 300 -w '  + xedconvert
#    t0 = os.times()
#    subprocess.call(conformation_XedeX.split())
#    tf = os.times()
#    ctime = tf[2] - t0[2] #child system time
#    print hetid
#    print ctime
#    for clau in keys:
#        if clau == enrot:
#            CPU_time[clau] += ctime
#            print "XedeX",  clau, ':', CPU_time[clau]
#    if os.path.isfile(xedconvert.replace('.sdf', '_xedex.sdf')):
#        outputfile = output_XedeX_wp + hetid + '_xedex.sdf'
#        shutil.move(xedconvert.replace('.sdf', '_xedex.sdf'), outputfile)
#print CPU_time
#             
