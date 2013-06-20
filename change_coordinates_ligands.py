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
#This script change the configuration of ligands that will be the input for conformer generation. The ligand is configurate to 1D and later reconfigurate to 3D. After it, the inchikeys of the original structure and the new 
#3D configuration are compared in order to not loss the stereochemical information. 

import pybel,  os,  shutil
from glob import glob

#CHANGE YOUR PATHS IN THOSE VARIABLES

ouput_ligands = os.path.join('Lligands_i_poses_originals/Input_ligands/')
if not os.path.isdir(ouput_ligands):
    os.makedirs(ouput_ligands)
        
#list of hetids of bioactives structures that have been validated by the electron density map
bioactives = glob('Lligands_i_poses_originals/Bioactive_structures/*_Rotatable_bonds/ligand_*')
hetids_A = ([carpeta.split('/')[-1] for carpeta in bioactives])
hetids = ([carpeta.split('_')[1] for carpeta in hetids_A])

for bioactive in bioactives:
    mol = pybel.readfile('sdf', bioactive).next()
    print mol.title
    #sdf structures to smiles and again 3D configuration. 
    inchikey_mol = mol.write('inchikey')
    smiles = pybel.readstring('smi', mol.write('can'))
    smiles.make3D()
    inchikey_configuration = smiles.write('inchikey')
    #comparison of inchikeys in order to be sure that we have not lost stereochemistry
    if inchikey_mol == inchikey_configuration:
        print 'They have the same inchikeys'
        smiles.write('sdf',ouput_ligands + mol.title + '.sdf')
    else:
        print 'they DONT HAVE the same inchikeys'

