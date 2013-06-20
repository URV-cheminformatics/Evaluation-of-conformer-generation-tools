Evaluation-of-conformer-generation-tools
========================================

María José Ojeda (1), Adrià Cereto-Massagué (1), Cristina Valls (1), Miquel Mulero (1), M. Josepa Salvado (1), Anna Arola-Arnal (1), Lluís Arola (1),(2), Santiago Garcia-Vallvé (1),(2) and Gerard Pujadas (1),(2),*

(1) Grup de Recerca en Nutrigenòmica, Departament de Bioquímica i Biotecnologia, Universitat Rovira i Virgili, Campus de Sescelades, C/ Marceŀlí Domingo s/n, 43007 Tarragona, Catalonia, Spain
(2) Centre Tecnològic de Nutrició i Salut (CTNS), TECNIO, CEICS, Avinguda Universitat 1, 43204, Reus, Catalonia, Spain

###ABSTRACT###

Virtual screening workflows consist of several sequential filters where the output molecules of one step are the input molecules for the next step and so on. Conformer generation represents one of this filters to obtain input for other applications like shape comparison tools or docking engines. 

In order to optimize this workflow and decrease the loss of false negatives, the main goal of the current work consist in identifying to which extent available tools for conformational sampling are able to reproduce bioactive conformers. To get it, 5126 small molecules have been tested using a wide number of methodologies implemented in Balloon, Clean3D, Confab, ConfGen, Cyndi, OMEGA, ROTATE, Vconf and XedeX. Their succes to reproduce bioactive conformations has been measured by comparison of RMSD value, stablishing a threshold of 1 Å. Moreover, an analysis of eight ligands bound to different proteins with different geometries was done to determine the accuracy of each methodology. 

OMEGA (with default parameters), ROTATE (with a ring conformations of CORINA) and XedeX (with pretreatment of XedConvert and white paper settings) have been found to generate low RMSD conformers closer to their bioactive conformation. Confab and Clean3D generated a higher number of conformations although the latter employed more CPU time. Only small molecules of up to seven rotatable bonds show reliability to be reproduced because ligands with a higher number of rotatable bonds pose a greater difficulty due to their flexibility and the combinatorial explosion associated with it.

This study was supported by Grant Number AGL2011-25831 from the Spanish Government. 


###HOW TO USE THE SCRIPTS###

These Python scripts have been used to prepare bioactive structures, generate conformers of ligands and calculate their RMSD. 

###CONFORMER GENERATION###

1. Validation of Electron Density Map of bioactive structures using VHELIBS (https://github.com/URVnutrigenomica-CTNS/VHELIBS)
2. rmsd_bioactive_poses.py : calculate RMSD between poses from the same ligand in order to reduce redundant structures
3. change_coordinates_ligands.py : modify the coordinates of ligands in order to avoid bias in the results
4. conformer_generation.py : conformer generation by different tools and pretreatment recommended for these tools.(BALLOON, CLEAN3D, CONFAB, CYNDI, OMEGA, ROTATE, VCONF, XEDEX)
5. conformer_generation_confgen.py : conformer generation by CONFGEN and pretreatment of LigPrep.
6. rmsd.conformers.py  : calculation of rmsd between conformers and bioactive structures
7. tables_rmsd.py  :  analysis and ranking of the minimum rmsd value for each bioactive structure depending on the number of rotatable bonds.

###NUMBER OF CONFORMER AND CPU TIME USED###

8. average_number_conformers.py  : calculate the number of conformers generated for ligands between 1-7 rotatable bonds. 
9. cpu_time.py  : calculate the CPU time used during conformer generation for a subset of 700 ligands which have between 1-7 rotatable bonds. 
10. cpu_time_schrodinger.py  : calculate the CPU time by ConfGen used during conformer generation for a subset of 700 ligands which have between 1-7 rotatable bonds. 

A directory containing the bioactive structures and their corresponding ligands ready to generate conformers is also available. 
