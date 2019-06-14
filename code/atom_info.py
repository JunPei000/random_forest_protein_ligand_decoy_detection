import json
from math import sqrt
import json
import pandas as pd
from math import exp,log

def atom_info_protein(pdbfile):
    dic1 = {}
    for line in pdbfile:
        if 'ATOM'  in line:
            newlist = []
            newlist = line.split()
            key = newlist[1]+'_'+newlist[2]
            if newlist[2][0].isdigit():
                check_type = newlist[2][1]
            elif not newlist[2][0].isdigit():
                check_type = newlist[2][0]
            if len(newlist[4]) == 1:
                if key not in dic1 and check_type != 'H' and check_type != 'P' and 'O1P' not in key and 'O2P' not in key and 'O3P' not in key:
                    dic1[key] = {}
                    dic1[key]['coor'] = []
                    if newlist[6].count('.') == 2:
                        a = []
                        a = check(newlist[6])
                        newlist[6] = a[0]
                        newlist.insert(7, a[1])
                    if newlist[6].count('.') == 3:
                        a = []
                        a = check(newlist[6])
                        newlist[6] = a[0]
                        newlist.insert(7, a[1])
                        newlist.insert(8, a[2])
                    if newlist[7].count('.') == 2 or newlist[7].count('.') == 3:
                        a = []
                        a = check(newlist[7])
                        newlist[7] = a[0]
                        newlist.insert(8, a[1])
                    dic1[key]['coor'].append(float(newlist[6]))
                    dic1[key]['coor'].append(float(newlist[7]))
                    dic1[key]['coor'].append(float(newlist[8]))
                    dic1[key]['res_info'] = newlist[3]
                    dic1[key]['GARF_type'] = GARF_atomtype(newlist[2], newlist[3])
            elif len(newlist[4]) != 1:
                if key not in dic1 and check_type != 'H':
                    dic1[key] = {}
                    dic1[key]['coor'] = []
                    if newlist[5].count('.') == 2:
                        a = []
                        a = check(newlist[5])
                        newlist[5] = a[0]
                        newlist.insert(6, a[1])
                    if newlist[5].count('.') == 3:
                        a = []
                        a = check(newlist[5])
                        newlist[5] = a[0]
                        newlist.insert(6, a[1])
                        newlist.insert(7, a[2])
                    if newlist[6].count('.') == 2 or newlist[6].count('.') == 3:
                        a = []
                        a = check(newlist[6])
                        newlist[6] = a[0]
                        newlist.insert(7, a[1])
                    dic1[key]['coor'].append(float(newlist[5]))
                    dic1[key]['coor'].append(float(newlist[6]))
                    dic1[key]['coor'].append(float(newlist[7]))
                    dic1[key]['res_info'] = newlist[3]
                    dic1[key]['GARF_type'] = GARF_atomtype(newlist[2], newlist[3])
    return dic1

def check(m):
    parts = []
    while '.' in m:
        ind = 0
        ind = m.index('.')
        parts.append(m[:ind+4])
        m = m[ind+4:]
    return parts

def GARF_atomtype(x,y):
    if y == 'TPO':
        y = 'THR'
    if x == 'OXT':
        atmtype = 'O2'
    if 'HI' in y:
        y = y.replace(y[-1],'D')
    if len(y) == 4 and y[0] == 'N':
        if x == 'N':
            atmtype = 'N3'
        elif x == 'CA' or x == 'CB':
            atmtype = 'CT'
        elif x == 'C':
            atmtype = 'C'
        elif x == 'O':
            atmtype = 'O'
    elif len(y) == 4 and y[0] == 'C':
        if x == 'N':
            atmtype = 'N'
        elif x == 'CA' or x == 'CB':
            atmtype = 'CT'
        elif x == 'C':
            atmtype = 'C'
        elif x == 'O' or x == 'OXT':
            atmtype = 'O2'
    elif len(y) == 3:
        if x == 'N':
            atmtype = 'N'
        elif x == 'CA' or x == 'CB':
            atmtype = 'CT'
        elif x == 'C':
            atmtype = 'C'
        elif x == 'O':
            atmtype = 'O'
    if 'ASP' in y:
        if x == 'CG':
            atmtype = 'C'
        elif x == 'OD1' or x == 'OD2':
            atmtype = 'O2'
    elif 'GLU' in y:
        if x == 'CG':
            atmtype = 'CT'
        elif x == 'CD':
            atmtype = 'C'
        elif x == 'OE1' or x == 'OE2':
            atmtype = 'O2'
    elif 'LEU' in y:
        if x == 'CG' or x == 'CD1' or x == 'CD2':
            atmtype = 'CT'
    elif 'ILE' in y:
        if x == 'CG1' or x == 'CG2' or x == 'CD1':
            atmtype = 'CT'
    elif 'ASN' in y:
        if x == 'CG':
            atmtype = 'C'
        elif x == 'OD1':
            atmtype = 'O'
        elif x == 'ND2':
            atmtype = 'N'
    elif 'GLN' in y:
        if x == 'CG':
            atmtype = 'CT'
        elif x == 'CD':
            atmtype = 'C'
        elif x == 'OE1':
            atmtype = 'O'
        elif x == 'NE2':
            atmtype = 'N'
    elif 'VAL' in y:
        if x == 'CG1' or x == 'CG2':
            atmtype = 'CT'
    elif 'HID' in y:
        if x == 'CG':
            atmtype = 'CC'
        elif x == 'ND1':
            atmtype = 'NA'
        elif x == 'CE1':
            atmtype = 'CR'
        elif x == 'NE2':
            atmtype = 'NB'
        elif x == 'CD2':
            atmtype = 'CV'
    elif 'SER' in y:
        if x == 'OG':
            atmtype = 'OH'
    elif 'THR' in y:
        if x == 'CG2':
            atmtype = 'CT'
        elif x == 'OG1':
            atmtype = 'OH'
    elif 'CYS' in y:
        if x == 'SG':
            atmtype = 'SH'
    elif 'MET' in y:
        if x == 'CG' or x == 'CE':
            atmtype = 'CT'
        elif x == 'SD':
            atmtype = 'S'
    elif 'PRO' in y:
        if x == 'CG' or x == 'CD':
            atmtype = 'CT'
    elif 'ARG' in y:
        if x == 'CG' or x == 'CD':
            atmtype = 'CT'
        elif x == 'NE' or x == 'NH1' or x == 'NH2':
            atmtype = 'N2'
        elif x == 'CZ':
            atmtype = 'CA'
    elif 'LYS' in y:
        if x == 'CG' or x == 'CD' or x == 'CE':
            atmtype = 'CT'
        elif x == 'NZ':
            atmtype = 'N3'
    elif 'PHE' in y:
        if x == 'CG' or x == 'CZ' or x == 'CD1' or x == 'CD2' or x == 'CE1' or x == 'CE2':
            atmtype = 'CA'
    elif 'TYR' in y:
        if x == 'CG' or x == 'CD1' or x == 'CD2' or x == 'CE1' or x == 'CE2':
            atmtype = 'CA'
        elif x == 'CZ':
            atmtype = 'C'
        elif x == 'OH':
            atmtype = 'OH'
    elif 'TRP' in y:
        if x == 'CG':
            atmtype = 'C*'
        elif x == 'CD1':
            atmtype = 'CW'
        elif x == 'NE1':
            atmtype = 'NA'
        elif x == 'CE2':
            atmtype = 'CN'
        elif x == 'CD2':
            atmtype = 'CB'
        elif x == 'CZ2' or x == 'CH2' or x == 'CZ3' or x == 'CE3':
            atmtype = 'CA'
    return atmtype






def atom_info_lig(ligfile):
    dic1 = {}; ind1 = 0; ind2 = 0; ind3 = 0
    ind1 = ligfile.index('@<TRIPOS>ATOM\n')
    ind2 = ligfile.index('@<TRIPOS>BOND\n')
    if '@<TRIPOS>SUBSTRUCTURE\n' in ligfile:
        ind3 = ligfile.index('@<TRIPOS>SUBSTRUCTURE\n')
    elif '@<TRIPOS>SUBSTRUCTURE\n' not in ligfile:
        ind3 = len(ligfile)
    for i in range(ind1+1, ind2):
        newlist = []
        newlist = ligfile[i].split()
        if newlist[0] not in dic1:
            dic1[newlist[0]] = {}
            dic1[newlist[0]]['coor'] = []
            dic1[newlist[0]]['mol2_type'] = newlist[5]
            dic1[newlist[0]]['coor'].append(float(newlist[2]))
            dic1[newlist[0]]['coor'].append(float(newlist[3]))
            dic1[newlist[0]]['coor'].append(float(newlist[4]))
        elif newlist[0] in dic1:
            print ('error! same atom num!', newlist[0])
    bond = {}
    for i in range(ind2+1, ind3):
        newlist = []
        newlist = ligfile[i].split()
        if newlist[1] not in bond:
            bond[newlist[1]] = []
        if newlist[2] not in bond:
            bond[newlist[2]] = []
        #if dic1[newlist[2]]['mol2_type'] not in bond[newlist[1]]:
        #    bond[newlist[1]].append(dic1[newlist[2]]['mol2_type'])
        #if dic1[newlist[1]]['mol2_type'] not in bond[newlist[2]]:
        #    bond[newlist[2]].append(dic1[newlist[1]]['mol2_type'])
        if newlist[2] not in bond[newlist[1]]:
            bond[newlist[1]].append(newlist[2])
        if newlist[1] not in bond[newlist[2]]:
            bond[newlist[2]].append(newlist[1])
    for key in dic1:
        if dic1[key]['mol2_type'] == 'C.3':
            count = 0
            for atom in bond[key]:
                if dic1[atom]['mol2_type'][0] != 'C' and dic1[atom]['mol2_type'][0] != 'H':
                    count += 1
            if count != 0:
                dic1[key]['GARF_type'] = 'C.3x'
            elif count == 0:
                dic1[key]['GARF_type'] = 'C.3'
        if dic1[key]['mol2_type'] == 'C.2':
            count = 0
            for atom in bond[key]:
                if dic1[atom]['mol2_type'][0] != 'C' and dic1[atom]['mol2_type'][0] != 'H':
                    count += 1
            if count != 0:
                dic1[key]['GARF_type'] = 'C.2x'
            elif count == 0:
                dic1[key]['GARF_type'] = 'C.2'
        if dic1[key]['mol2_type'] == 'C.ar':
            count = 0
            for atom in bond[key]:
                if dic1[atom]['mol2_type'][0] != 'C' and dic1[atom]['mol2_type'][0] != 'H':
                    count += 1
            if count != 0:
                dic1[key]['GARF_type'] = 'C.arx'
            elif count == 0:
                dic1[key]['GARF_type'] = 'C.ar'
        if dic1[key]['mol2_type'][0] == 'N':
            count = 0
            for atom in bond[key]:
                if dic1[atom]['mol2_type'][0] == 'H':
                    count += 1
            if count == 1:
                dic1[key]['GARF_type'] = 'N.1h'
            if count == 2:
                dic1[key]['GARF_type'] = 'N.2h'
            if count == 3:
                dic1[key]['GARF_type'] = 'N.3h'
            if count == 0:
                dic1[key]['GARF_type'] = 'N.2'
        elif dic1[key]['mol2_type'][0] == 'O':
            count1 = 0
            for atom in bond[key]:
                if dic1[atom]['mol2_type'][0] == 'S' or dic1[atom]['mol2_type'][0] == 'P':
                    count1 += 1
            #print (count1, key)
            if count1 != 0:
                dic1[key]['GARF_type'] = 'O.2v'
            elif count1 == 0:
                count2 = 0
                count3 = 0
                for atom in bond[key]:
                    if dic1[atom]['mol2_type'][0] != 'H':
                        count2 += 1
                    elif dic1[atom]['mol2_type'][0] == 'H':
                        count3 += 1
                if count2 == 2:
                    dic1[key]['GARF_type'] = 'O.3p'
                elif count2 == 1:
                    for atom in bond[key]:
                        if dic1[atom]['mol2_type'][0] != 'H':
                            atom_name = atom
                    count4 = 0
                    for atom in bond[atom_name]:
                        if dic1[atom]['mol2_type'][0] == 'O':
                            count4 += 1
                    if count4 == 2:
                        dic1[key]['GARF_type'] = 'O.co2'
                    elif count4 != 2:
                        if count3 == 1:
                            dic1[key]['GARF_type'] = 'O.3'
                        elif count3 == 0:
                            dic1[key]['GARF_type'] = 'O.2'
                elif count2 >2:
                    print ('error! check atom type of ', key)
        elif dic1[key]['mol2_type'][0] == 'P':
            dic1[key]['GARF_type'] = 'P'
        elif dic1[key]['mol2_type'][0] == 'F':
            dic1[key]['GARF_type'] = 'F'
        elif dic1[key]['mol2_type'][:2] == 'Cl':
            dic1[key]['GARF_type'] = 'Cl'
        elif dic1[key]['mol2_type'][:2] == 'Br':
            dic1[key]['GARF_type'] = 'Br'
        elif dic1[key]['mol2_type'][0] == 'I':
            dic1[key]['GARF_type'] = 'I'
        elif dic1[key]['mol2_type'] == 'C.cat':
            dic1[key]['GARF_type'] = 'C.cat'
        elif dic1[key]['mol2_type'] == 'S.O' or dic1[key]['mol2_type'] == 'S.o2':
            dic1[key]['GARF_type'] = 'S.o'
        elif dic1[key]['mol2_type'][0] == 'S' and dic1[key]['mol2_type'] != 'S.O' and dic1[key]['mol2_type'] != 'S.o2':
            dic1[key]['GARF_type'] = 'S.3'
    return dic1, bond        
        
def name(key):
    ind = 0
    ind = key.index('_')
    a = key[ind+1:]
    return a

def distance(dicp, dicl):
    dic_dist = {}
    for key in dicl:
        for key1 in dicp:
            dist = 0
            dist = sqrt((dicl[key]['coor'][0]-dicp[key1]['coor'][0])**2+(dicl[key]['coor'][1]-dicp[key1]['coor'][1])**2+(dicl[key]['coor'][2]-dicp[key1]['coor'][2])**2)
            lig_atom_name = dicl[key]['GARF_type']
            pro_atom_name = dicp[key1]['GARF_type']
            newkey = lig_atom_name+'__'+pro_atom_name
            if dist <= 6:
                if newkey not in dic_dist:
                    dic_dist[newkey] = {}
                    dic_dist[newkey]['dist'] = []
                    dic_dist[newkey]['atoms'] = []
                    dic_dist[newkey]['dist'].append(dist)
                    dic_dist[newkey]['atoms'].append(key+'_'+key1)
                elif newkey in dic_dist:
                    dic_dist[newkey]['dist'].append(dist)
                    dic_dist[newkey]['atoms'].append(key+'_'+key1)
    return dic_dist

def nonb_calc(Interf):
    R = 1.987*10**(-3)
    T = 298
    nonb_file = open(Path_of_GARF_reduced.json,'r')
    N_data = {}
    N_data = json.load(nonb_file)
    print len(N_data)
    dicN_energy = {}
    
    for key in Interf:
        if 'x' in key and '*' not in key:
            newkey = key.replace('x', 'Oa')
        if '*' in key and 'x' not in key:
            newkey = key.replace('*', 's')
        if 'x' in key and '*' in key:
            newkey = key.replace('*', 's').replace('x', 'Oa')
        elif 'x' not in key and '*' not in key:
            newkey = key
        dicN_energy[key] = []
        if N_data.has_key(newkey):
            E1 = float(N_data[newkey]['E1'])
            E2 = float(N_data[newkey]['E2'])
            a = float(N_data[newkey]['alpha'])
            b = float(N_data[newkey]['beta'])
            sigma1 = float(N_data[newkey]['A'])
            sigma2 = float(N_data[newkey]['B'])
            
        elif not N_data.has_key(newkey):
            print 'error! Cannot find nonb atom pair in database!', newkey
        if N_data.has_key(newkey):
            for i in range(len(Interf[key]['dist'])):
                r = 0
                dist_vec_n = []
                r = float("{0:.3f}".format(Interf[key]['dist'][i]))
                if (6 - r) >= 0.5 and (r - 2) >= 0.5:
                    for j in range(-100,101):
                        dist_vec_n.append(float("{0:.3f}".format(0.005*j+r)))
                elif (6 - r) < 0.5:
                    for j in range(-200,1):
                        dist_vec_n.append(float("{0:.3f}".format(0.005*j+r)))
                elif (r - 2) < 0.5:
                    for j in range(0,201):
                        dist_vec_n.append(float("{0:.3f}".format(0.005*j+r)))
                dist_vec_n_energy = []
                if len(dist_vec_n) != 201:
                    print 'error! Wrong dist_vec_n!'
                    break
                elif len(dist_vec_n) == 201:
                    for j in range(len(dist_vec_n)):
                        t = (E1*((sigma1/dist_vec_n[j])**a)+E2*((sigma2/dist_vec_n[j])**b))/(-R*T)
                        prob = 0
                        if t <=500:
                            prob = exp((E1*((sigma1/dist_vec_n[j])**a)+E2*((sigma2/dist_vec_n[j])**b))/(-R*T))
                        elif t > 500:
                            prob = exp(500)
                        elif dist_vec_n[j] < 2:
                            prob = 10**(-30)
                        if prob <= 10**(-30):
                            prob = 10**(-30)
                        dist_vec_n_energy.append(prob)
                if dist_vec_n_energy != []:                
                    sum_dist_n_energy = 0
                    sum_dist_n_energy = sum(dist_vec_n_energy)
                    dicN_energy[key].append(sum_dist_n_energy)
                else:
                    dicN_energy[key].append(0)
    desn = {}
    for key in dicN_energy:
        sum2 = 0
        for i in range(len(dicN_energy[key])):
            sum2 += log(dicN_energy[key][i])
        desn[key] = sum2 - len(dicN_energy[key])*log(201)
    return desn




