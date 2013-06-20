#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#This scrit calculate the RMSD between two poses that belongs to the same small molecule. It is done in order to have ligands to be reproduces as different as possible and reduce the redundance. In case that RMSD is 
#lower or equal to 1.5 A, we consider that are the same structure, then only one copy will be saved. However, in case that RMSD is higher than 1.5 A, the two poses will be saved. 
#
#IT'S IMPORTANT TO HAVE IN THE SAME DIRECTORY rmsd.py FROM SCHRÖDINGER. AND ACADEMIC LICENSE. YOU CAN DOWNLOAD IN: http://www.schrodinger.com/scriptcenter/ 

import os
import csv
from glob import glob
import pybel
import subprocess

#CHANGE YOUR PATHS IN THOSE VARIABLES

bioactive_conformers = 'Bioactive_structures/'
hetids = [line.strip() for line in open('hetids5370.txt',  'rb')] 

error = []

for hetid in hetids:   
    poses = glob(bioactive_conformers + '*_Rotatable_bonds/ligand_'+hetid+'/*.sdf' )
    
    #Calculate the rmsd value between all poses that belong to the same ligand
    while poses:
        struc_ref = poses.pop()
        if os.path.isfile(struc_ref):
            for struc_comp in poses:
                if os.path.isfile(struc_comp):
                    
                    #Comparison of the number of heavy atoms of each structure to avoid error of rmsd calculation. 
                    mol_ref = next(pybel.readfile('sdf', struc_ref))
                    mol_comp = next(pybel.readfile('sdf', struc_comp))
                    atom_ref = len([atom for atom in mol_ref.atoms if atom.atomicnum !=1])
                    atom_comp = len([atom for atom in mol_comp.atoms if atom.atomicnum !=1])
                    if atom_ref == atom_comp: 
                        
                        #RMSD calculation between two active poses from the same ligand
                        try:
                            calculrmsd =  os.path.join(os.environ['SCHRODINGER'], 'run') + " rmsd.py -m " +  struc_ref  +  ' ' + struc_comp + " -c %s.csv" % struc_comp
                            subprocess.call(calculrmsd.split())

                            #If RMSD value is lower than 1.5 A, we consider that they are the same pose, then one copy is removed. However, if rmsd value is higher, two copies are saved.   
                            csv = open(struc_comp+'.csv',  'rb')
                            csvfile = csv.read()
                            rmsd = float(csvfile.split('","')[9])
                            print hetid ,  rmsd
                            if rmsd <= 1.5:
                                print 'They are the SAME pose'
                                os.remove(struc_comp)
                            else:
                                print 'They are DIFFERENT pose'
                        except Exception,  error:
                            print hetid, error
                        os.remove(struc_comp + '.csv')
                    else:
                        print 'They DO NOT have the same number of atoms: %s vs %s' % (atom_ref, atom_comp)
