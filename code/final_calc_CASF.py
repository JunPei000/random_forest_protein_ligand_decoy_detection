#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:02:27 2018

@author: peijun
"""

import os
from atom_info import atom_info_protein
from atom_info import atom_info_lig
from atom_info import distance
from atom_info import nonb_calc
import pandas as pd
from CASF_seperate import ligfile_finder
from CASF_seperate import native_finder

direct1 = Path_of_CASF2013_coreset
direct_decoy = Path_of_CASF-2013_decoys_docking
fp1 = file.readlines(open(Path_of_GARF_potential_clumns, 'r'))
column = []
column = fp1[0].split()
column.append('lig_name')
noneed = ['origial_csv', 'final_csv', '1hfs', '2jdu', 'README', 'index', '2d1o', '2jdy']
foldernames = [i for i in os.listdir(direct1) if i not in noneed and len(i) == 4]
for foldername in foldernames:
    print (foldername)
    direct2 = direct1+foldername+'/'
    filename = foldername+'_protein.pdb'
    #insert(direct2, filename)
    protein_file = open(direct2+filename, 'r').readlines()
    lig_names = foldername+'_decoys.mol2'
    dicp = atom_info_protein(protein_file)
    fp2 = open(direct2+'result_'+foldername+'.csv', 'w')
    df1 = pd.DataFrame(columns=column)
    ligfiles = ligfile_finder(direct_decoy, foldername)
    ligfiles_native = native_finder(direct1, foldername)
    print len(ligfiles)
    for key in ligfiles_native:
        if key not in ligfiles:
            ligfiles[key] = ligfiles_native[key]
        else:
            print ('Attention! Native ligand already in decoys! Please check :', foldername)
    count = 0
    for key in ligfiles:
        print (key, count)
        lig_file = ligfiles[key]
        dicl = atom_info_lig(lig_file)
        dicp = atom_info_protein(protein_file)
        dicl_f = {}
        for key1 in dicl[0]:
            if dicl[0][key1]['mol2_type'] == 'H':
                continue
            if 'GARF_type' not in dicl[0][key1]:
                continue
            dicl_f[key1] = {}
            dicl_f[key1]['GARF_type'] = dicl[0][key1]['GARF_type']
            dicl_f[key1]['coor'] = dicl[0][key1]['coor']
        
        dists = {}
        dists = distance(dicl_f, dicp)
        final_r = nonb_calc(dists)
        df1.loc[count, 'lig_name'] = key
        for key1 in final_r:
            if '*' in key1:
                newkey = key1.replace('*', 's')
            else:
                newkey = key1
            if newkey not in df1.columns:
                print ('missing atompair!', key1)
            elif newkey in df1.columns:
                df1.loc[count, newkey] = final_r[key1]
        count += 1
    df1 = df1.fillna(0)
    df1.to_csv(fp2)
    fp2.close()
            
        
        
        
            
    
    
