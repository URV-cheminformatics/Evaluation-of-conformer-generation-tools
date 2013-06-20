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
#This script generate conformers of a set of bioactive conformers by different methodologies like: BALLOON, CLEAN3D, CONFAB, CYNDI, OMEGA, ROTATE
#Also, there is the pretreatment specific for each tool, like: CORINA, CLEAN3D

import os
import subprocess
from glob import glob

#CHANGE YOUR PATHS IN THOSE VARIABLES

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


output_BALLOON = 'Ligands_conformations/BALLOON/'
output_CLEAN3D_wp = 'Ligands_conformations/CLEAN3D_white_paper/'
output_CLEAN3D_st = 'Ligands_conformations/CLEAN3D_standard/'
output_CLEAN3D_ring = 'Ligands_conformations/CLEAN3D_ring/'
output_CONFAB = 'Ligands_conformations/CONFAB/'
output_CYNDI_st = 'Ligands_conformations/CYNDI_standard/'
output_CYNDI_ring = 'Ligands_conformations/CYNDI_ring/'
output_OMEGA = 'Ligands_conformations/OMEGA/'
output_ROTATE_st = 'Ligands_conformations/ROTATE_standard/'
output_ROTATE_ring = 'Ligands_conformations/ROTATE_ring/'
output_VCONF_st = 'Ligands_conformations/VCONF_standard/'
output_VCONF_ring = 'Ligands_conformations/VCONF_ring/'
output_XEDEX_st = 'Ligands_conformations/XEDEX_standard/'
output_XEDEX_ring = 'Ligands_conformations/XEDEX_ring/'
output_XEDEX_wp = 'Ligands_conformations/XEDEX_white_paper/'
standard_file_CORINA = 'Pretreatments/STANDARD/'
ring_file_CORINA = 'Pretreatments/RING_CONFORMATIONS/'
pretreatment_file_CLEAN3D = 'Pretreatments/CLEAN3D/'
pretreatment_file_XEDCONVERT = 'Pretreatments/XEDCONVERT/'


#List of hetids
hetids = [line.strip() for line in open('hetids5370.txt',  'rb')] 

for hetid in hetids:
    input = os.path.join('Input_ligands',  hetid + '.sdf')
    
    # CORINA
    #Standard pretreatment
    if not os.path.isdir(standard_file_CORINA):
        os.makedirs(standard_file_CORINA)
    pretreatment_corina =  path_to_corina + " -d neu,r2d,errorfile=errors_corina.sdf " + input + " " +  standard_file_CORINA + hetid + "_corina.sdf"
    subprocess.call(pretreatment_corina.split())
    corina_STANDARD = 'Pretreatments/STANDARD/' + hetid + "_corina.sdf"
    print hetid, "pretreatment CORINA STANDARD done"
    
   #Ring conformation pretreatment
    if not os.path.isdir(ring_file_CORINA):
        os.makedirs(ring_file_CORINA)
    pretreatment_corina = path_to_corina + " -d neu,r2d,rc,errorfile=errors_corina.sdf " + input + " " +  ring_file_CORINA + hetid + "_corina.sdf"
    subprocess.call(pretreatment_corina.split())
    corina_RING_CONFORMATIONS = 'Pretreatments/RING_CONFORMATIONS/' + hetid + "_corina.sdf"
    print hetid, "pretreatment CORINA RING done"
    
    #BALLOON
    if not os.path.isdir(output_BALLOON):
        os.makedirs(output_BALLOON)
    conformation_balloon = path_to_balloon + " -f /home/Biomolsoft/MMFF94.mff --nconfs 20 --nGenerations 300 --maxtime 60000 -t 0.1 --maxiter 1000 " + input + " " +  output_BALLOON + hetid + "_balloon.sdf"
    subprocess.call(conformation_balloon.split())
    print hetid, "conformations BALLOON done"
             
    #CHEMAXON_CLEAN3D    
    #Pretreatment 
    if not os.path.isdir(pretreatment_file_CLEAN3D):
        os.makedirs(pretreatment_file_CLEAN3D)
    pretreatment_CLEAN3D = path_to_clean3d + " -o " + pretreatment_file_CLEAN3D + hetid + "_CHEMAXON_CLEAN3D.sdf majormicrospecies -H 7.4 -f mol " + input 
    subprocess.call(pretreatment_CLEAN3D.split())
    print hetid, "pretreatment CLEAN3D done"
        
    #Conformer generation (white paper)
    if not os.path.isdir(output_CLEAN3D_wp):
        os.makedirs(output_CLEAN3D_wp)
    conformation_CLEAN3D = path_to_clean3d + " -Xmx4g -o " + output_CLEAN3D_wp + hetid + "_CHEMAXON_CLEAN3D.sdf  conformers -m 1000 -y false " + pretreatment_file_CLEAN3D + hetid + "_CHEMAXON_CLEAN3D.sdf" 
    subprocess.call(conformation_CLEAN3D.split())
    print hetid, "conformations CLEAN3D done"
    
    #Standard pretreatment (default parameters)
    if not os.path.isdir(output_CLEAN3D_st):
        os.makedirs(output_CLEAN3D_st)
    conformation_CLEAN3D =  path_to_clean3d + " -o " + output_CLEAN3D_st + hetid + "_CHEMAXON_CLEAN3D.sdf conformers " + corina_STANDARD
    subprocess.call(conformation_CLEAN3D.split())
    print hetid, "conformations CLEAN3D done"
    
    #Ring conformations pretreatment (default parameters)
    if not os.path.isdir(output_CLEAN3D_ring):
        os.makedirs(output_CLEAN3D_ring)
    conformation_CLEAN3D = path_to_clean3d + " -o " + output_CLEAN3D_ring + hetid + "_CHEMAXON_CLEAN3D.sdf conformers " + corina_RING_CONFORMATIONS
    subprocess.call(conformation_CLEAN3D.split())
    print hetid, "conformations CLEAN3D done"
    
   #CYNDI
   #Change sdf file to mol2 file
    charge_format = '/usr/bin/babel ' + corina_STANDARD + ' Pretreatments/STANDARD/' + hetid + "_corina.mol2"    
    subprocess.call(charge_format.split())
    charge_format = '/usr/bin/babel ' + corina_RING_CONFORMATIONS + ' Pretreatments/RING_CONFORMATIONS/' + hetid + "_corina.mol2"    
    subprocess.call(charge_format.split())
    corina_STANDARD_mol2 = standard_file_CORINA + hetid + "_corina.mol2"
    corina_RING_mol2 = ring_file_CORINA + hetid + "_corina.mol2"
   
   #Standard pretreatment
    if not os.path.isdir(output_CYNDI_st):
        os.makedirs(output_CYNDI_st)
    conformation_cyndi =  path_to_cyndi + " -i " + corina_STANDARD_mol2 + " -o " + output_CYNDI_st + hetid + "_cyndi.sdf -p Cyndi.param"
    subprocess.call(conformation_cyndi.split())
    print hetid, "conformations CYNDI done"

    #Ring conformations pretreatment 
    if not os.path.isdir(output_CYNDI_ring):
        os.makedirs(output_CYNDI_ring)
    conformation_cyndi = path_to_cyndi + " -i " + corina_RING_mol2 + " -o " + output_CYNDI_ring + hetid + "_cyndi.sdf -p Cyndi.param"
    subprocess.call(conformation_cyndi.split())
    print hetid, "conformations CYNDI done"
        
    #CONFAB
    #Standard pretreatment
    if not os.path.isdir(output_CONFAB):
        os.makedirs(output_CONFAB)
    conformation_confab = path_to_confab + " " + corina_STANDARD + " " +  output_CONFAB + hetid + "_confab.sdf"
    subprocess.call(conformation_confab.split())
    print hetid, "conformations CONFAB done"

    # OMEGA
    if not os.path.isdir(output_OMEGA):
        os.makedirs(output_OMEGA) 
    conformation_omega = path_to_omega +' -in ' + input + ' -out ' +  output_OMEGA + hetid + '_omega.sdf'
    subprocess.call(conformation_omega.split())
    print hetid, "conformations OMEGA done"

    #ROTATE
    #Standard pretreatment
    if not os.path.isdir(output_ROTATE_st):
        os.makedirs(output_ROTATE_st)
    conformation_ROTATE = path_to_rotate + " -d auto " + corina_STANDARD + " " + output_ROTATE_st + hetid + "_rotate.sdf"
    subprocess.call(conformation_ROTATE.split())
    print hetid, "conformations ROTATE done"
    
    #Ring conformations pretreatment 
    if not os.path.isdir(output_ROTATE_ring):
        os.makedirs(output_ROTATE_ring)
    conformation_ROTATE = path_to_rotate + " -d auto " + corina_RING_CONFORMATIONS + " " + output_ROTATE_ring + hetid + "_rotate.sdf"
    subprocess.call(conformation_ROTATE.split())
    print hetid, "conformations ROTATE done"
    
    # VCONF
    #Standard pretreatment
    if not os.path.isdir(output_VCONF_st):
        os.makedirs(output_VCONF_st) 
    output_standard = output_VCONF_st + hetid + '_corina_mol_1_confs.sdf'
    conformation_VCONF = path_to_Vconf +' ' + corina_STANDARD 
    subprocess.call(conformation_VCONF.split())
    print hetid,"conformations VCONF done"
    if os.path.isfile(hetid + '_corina_mol_1_confs.sdf'):
        shutil.move(hetid + '_corina_mol_1_confs.sdf',  output_standard)

    #Ring conformations pretreatment 
    if not os.path.isdir(output_VCONF_ring):
        os.makedirs(output_VCONF_ring) 
    outputfile = output_VCONF_ring + hetid + '_ring_vconf.sdf'
    conformation_VCONF = path_to_Vconf +' ' + corina_RING_CONFORMATIONS
    subprocess.call(conformation_VCONF.split())
    print hetid, "conformations VCONF done"
    for vconffile in glob(hetid+ '*_confs.sdf'):
        conf = open(vconffile,  'rb')
        out = open(outputfile,'ab')
        out.write(conf.read())
        out.close()
        os.remove(vconffile)

    # XEDEX TOOLS
    #Standard pretreatment
    if not os.path.isdir(output_XEDEX_st):
        os.makedirs(output_XEDEX_st) 
    outputfile = output_XEDEX_st + hetid + '_xedex.sdf'
    conformation_XEDEX = path_to_XedeX +' -0 -w '  + corina_STANDARD
    print hetid,  "conformations XEDEX done"
    subprocess.call(conformation_XEDEX.split())
    if os.path.isfile(corina_STANDARD.replace('.sdf', '_xedex.sdf')):
        shutil.move(corina_STANDARD.replace('.sdf', '_xedex.sdf'), outputfile)

   #Ring conformations pretreatment 
    if not os.path.isdir(output_XEDEX_ring):
        os.makedirs(output_XEDEX_ring) 
    outputfile = output_XEDEX_ring + hetid + '_xedex.sdf'
    if not os.path.isfile(outputfile):
        conformation_XEDEX = path_to_XedeX +' -0 -w '  + corina_RING_CONFORMATIONS
        print hetid,  "conformations XEDEX done"
        subprocess.call(conformation_XEDEX.split())
        for xedexfile in glob(corina_RING.replace('.sdf', '_xedex*.sdf')):
            conf = open(xedexfile,  'rb')
            out = open(outputfile,'ab')
            out.write(conf.read())
            out.close()
            os.remove(xedexfile)

    #Conformer generation (white paper)
    #Pretractatment xedconvert
    if not os.path.isdir(pretreatment_file_XEDCONVERT):
        os.makedirs(pretreatment_file_XEDCONVERT) 
    outputfile =pretreatment_file_XEDCONVERT + hetid + '_xedex.sdf'
    pretractament = path_to_xedconvert +' -c -o s '  + input 
    print hetid,  'Pretreatment XEDCONVERT done'
    outfile = open(outputfile,  'wb')
    subprocess.call(pretractament.split(),  stdout=outfile)
    
    if not os.path.isdir(output_XEDEX_wp):
        os.makedirs(output_XEDEX_wp) 
    input_wp = xedconvert + hetid + '_xedex.sdf'
    outputfile = output_XEDEX_wp + hetid + '_xedex.sdf'
    conformation_XEDEX = path_to_XedeX +' -0 -m 300 -w '  + input_wp 
    print hetid,  "conformations XEDEX done"
    subprocess.call(conformation_XEDEX.split())
    if os.path.isfile(input_wp.replace('.sdf', '_xedex.sdf')):
        shutil.move(input_wp.replace('.sdf', '_xedex.sdf'), outputfile)

