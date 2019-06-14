#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:47:06 2018

@author: peijun
"""
import os

def ligfile_finder(direct2, ffoldername):
    ligfiles = {}
    if ffoldername+'_decoys.mol2' in os.listdir(direct2): 
        decoyfile = open(direct2+ffoldername+'_decoys.mol2', 'r').readlines()
    indexes = []
    for i in range(len(decoyfile)):
        if '@<TRIPOS>MOLECULE' in decoyfile[i]:
            indexes.append(i)
    for i in range(len(indexes)):
        ligname = decoyfile[indexes[i]+1].replace('\n', '')
        if ligname in ligfiles:
            print (i)
            print ('error! Same ligand! Please check file: ',direct2+ffoldername+'_decoys.mol2', ligname)    
        ligfiles[ligname] = []
        a = 0; b = 0
        if i != len(indexes)-1:
            a = indexes[i]
            b = indexes[i+1]
        elif i == len(indexes)-1:
            a = indexes[i]
            b = len(decoyfile)
        for j in range(a, b):
            ligfiles[ligname].append(decoyfile[j])
    return ligfiles

def active_finder(direct2, ffoldername):
    ligfiles = {}
    direct3 = direct2+ffoldername+'/'
    if 'actives_final.mol2.gz' in os.listdir(direct3):
        decoyfile = gzip.open(direct3+'actives_final.mol2.gz', 'rb')
        decoyfile = decoyfile.readlines()
    else:
        print (direct3)
    indexes = []
    for i in range(len(decoyfile)):
        if '@<TRIPOS>MOLECULE' in decoyfile[i]:
            indexes.append(i)
    for i in range(len(indexes)):
        if 'lig'+str(i) in ligfiles:
            print ('error! Same ligand! Please check file: ',direct3+'decoys_final.mol2.gz')
        ligfiles['lig'+str(i)] = []
        a = 0; b = 0
        if i != len(indexes)-1:
            a = indexes[i]
            b = indexes[i+1]
        elif i == len(indexes)-1:
            a = indexes[i]
            b = len(decoyfile)
        for j in range(a, b):
            ligfiles['lig'+str(i)].append(decoyfile[j])
    return ligfiles


def insert(direct1,name):
    fp1 = file.readlines(open(direct1+name,'r'))
    fp2 = open(direct1+'temp','w')
    for line in fp1:
        newlist = []
        newlist = line.split()
        if len(newlist) > 4 and 'ATOM' in line:
            if newlist[3]+'     '+newlist[4] in line:
                if len(newlist[4]) == 1:
                    line = line.replace(newlist[3]+'     '+newlist[4], newlist[3]+' T   '+newlist[4])
                elif len(newlist[4]) == 2:
                        line = line.replace(newlist[3]+'     '+newlist[4], newlist[3]+' T  '+newlist[4])
                elif len(newlist[4]) == 3:
                        line = line.replace(newlist[3]+'     '+newlist[4], newlist[3]+' T '+newlist[4])
            elif newlist[3]+'    '+newlist[4] in line:
                    if len(newlist[4]) == 1:
                        line = line.replace(newlist[3]+'    '+newlist[4], newlist[3]+' T   '+newlist[4])
                    elif len(newlist[4]) == 2:
                        line = line.replace(newlist[3]+'    '+newlist[4], newlist[3]+' T  '+newlist[4])
                    elif len(newlist[4]) == 3:
                        line = line.replace(newlist[3]+'    '+newlist[4], newlist[3]+' T '+newlist[4])
            elif newlist[3]+'   '+newlist[4] in line:
                    if len(newlist[4]) == 1:
                        line = line.replace(newlist[3]+'   '+newlist[4], newlist[3]+' T   '+newlist[4])
                    elif len(newlist[4]) == 2:
                        line = line.replace(newlist[3]+'   '+newlist[4], newlist[3]+' T  '+newlist[4])
                    elif len(newlist[4]) == 3:
                        line = line.replace(newlist[3]+'   '+newlist[4], newlist[3]+' T '+newlist[4])
            fp2.write(line)
    fp2.close()
    os.remove(direct1+name)
    os.rename(direct1+'temp', direct1+name)


def native_finder(direct2, ffoldername):
    ligfiles = {}
    direct3 = direct2+ffoldername+'/'
    if ffoldername+'_ligand_opt.mol2' in os.listdir(direct3):
        decoyfile = open(direct3+ffoldername+'_ligand_opt.mol2', 'r').readlines()
    else:
        print (direct3)
    indexes = []
    for i in range(len(decoyfile)):
        if '@<TRIPOS>MOLECULE' in decoyfile[i]:
            indexes.append(i)
    for i in range(len(indexes)):
        ligname = decoyfile[indexes[i]+1].replace('\n', '')
        if ligname in ligfiles:
            print ('error! Same ligand! Please check file: ',direct3+ffoldername+'_ligand_opt.mol2', ligname)
        ligfiles[ligname] = []
        a = 0; b = 0
        if i != len(indexes)-1:
            a = indexes[i]
            b = indexes[i+1]
        elif i == len(indexes)-1:
            a = indexes[i]
            b = len(decoyfile)
        for j in range(a, b):
            ligfiles[ligname].append(decoyfile[j])
    return ligfiles

def temp_finder(direct2, ffoldername):
    ligfiles = {}
    direct3 = direct2+ffoldername+'/'
    if 'temp.mol2' in os.listdir(direct3):
        decoyfile = file.readlines(open(direct3+'temp.mol2', 'r'))
    else:
        print (direct3)
    indexes = []
    for i in range(len(decoyfile)):
        if '@<TRIPOS>MOLECULE' in decoyfile[i]:
            indexes.append(i)
    for i in range(len(indexes)):
        if 'lig'+str(i) in ligfiles:
            print ('error! Same ligand! Please check file: ',direct3+'decoys_final.mol2.gz')
        ligfiles['lig'+str(i)] = []
        a = 0; b = 0
        if i != len(indexes)-1:
            a = indexes[i]
            b = indexes[i+1]
        elif i == len(indexes)-1:
            a = indexes[i]
            b = len(decoyfile)
        for j in range(a, b):
            ligfiles['lig'+str(i)].append(decoyfile[j])
    return ligfiles

