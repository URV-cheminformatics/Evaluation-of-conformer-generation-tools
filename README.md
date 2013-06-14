Evaluation-of-conformer-generation-tools
========================================

María José Ojeda (1), Adrià Cereto-Massagué (1), Cristina Valls (1), Miquel Mulero (1), M. Josepa Salvado (1), Anna Arola-Arnal (1), Lluís Arola (1),(2), Santiago Garcia-Vallvé (1),(2) and Gerard Pujadas (1),(2),*

(1) Grup de Recerca en Nutrigenòmica, Departament de Bioquímica i Biotecnologia, Universitat Rovira i Virgili, Campus de Sescelades, C/ Marceŀlí Domingo s/n, 43007 Tarragona, Catalonia, Spain
(2) Centre Tecnològic de Nutrició i Salut (CTNS), TECNIO, CEICS, Avinguda Universitat 1, 43204, Reus, Catalonia, Spain

ABSTRACT

Virtual screeining workflows consist of several sequential filters where the output molecules of one step are the input molecules for the next step and so on. Conformer generation represents one of this filters to obtain input for other applications like shape comparison tools or docking engines. 

In order to optimize this workflow and decrease the lost of false negatives, the main goal of the current work consist in identifying to which extend available tools for conformational sampling are able to reproduce bioactive conformers. To get it, 5 126 smalls molecules have been tested by a wide number of methodologies implemented in Balloon, Clean3D, Confab, ConfGen, Cyndi, OMEGA, ROTATE, Vconf and XedeX. The succes to reproduced has done by comparison of rmsd value stablishing a threshold of 1 Å. Moreover, an analyse of eight ligands binded to different proteins with different geometries has done to determine the accuracy of each methodology. 

We have found that OMEGA (with default parameters), ROTATE (with a ring conformations of CORINA) and XedeX (with pretreatment of XedConvert and white paper settings) generate low RMSD conformers more precised to its bioactive conformation. Confab and Clean3D have generated more number of conformations while this last one has employed more cpu time. Although, only small molecules until seven rotatable bonds are confident to be reproduced because ligands with a large number of rotatable bonds are more difficult due to their flexibility and the combinatorial explosion associated with them.

This study was supported by Grant Number AGL2011-25831 from the Spanish Government. 

SUMMARY TO USE SCRIPTS

The Python scripts availables to download in this website has been used to prepare bioactive structures, generate conformers of ligands and calculate rmsd. 

CONFORMER GENERATION
1. Validation of Electron Density Map of bioactive structures using VHELIBS (https://github.com/URVnutrigenomica-CTNS/VHELIBS)
2. rmsd_bioactive_poses.py : calculate rmsd between poses from the same ligand in order to reduce redundance structures
3. change_coordinates_ligands.py : modify the coordinates of ligands in order to avoid biases of the results
4. conformer_generation.py : conformer generation by different tools and pretreatment recommended for this tools. BALLOON, CLEAN3D, CONFAB, CYNDI, OMEGA, ROTATE, VCONF, XEDEX
5. conformer_generation_confgen.py : conformer generation by CONFGEN and pretreatment of LigPrep.
6. rmsd.conformers.py  : calculation of rmsd between conformers and bioactive structures
7. tables_rmsd.py  :  analysis and ranking of the minimum of rmsd value for each bioactive structure depend on the number of rotatable bond

NUMBER OF CONFORMER AND CPU TIME USED
8. average_number_conformers.py  : calculate the number of conformers generates for the ligands between 1-7 rotatable bonds. 
9. cpu_time.py  : calculate the cpu time used during conformer generation for a subset of 700 ligands that have between 1-7 rotatable bonds. 
10. cpu_time_schrodinger.py  : calculate the cpu time by ConfGen used during conformer generation for a subset of 700 ligands that have between 1-7 rotatable bonds. 

Also, it is available a directory that contain the bioactive structures and the corresponding ligands ready to generate conformers. 
