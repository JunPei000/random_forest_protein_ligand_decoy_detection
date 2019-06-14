import os
import pandas as pd

direct1 = Path_of_CASF-2013
foldernames = ['coreset']
for foldername in foldernames:
    print (foldername)
    direct2 = direct1+foldername+'/origial_csv/'       #path of original_csv folder
    direct3 = direct1+foldername+'/final_csv/'         #path of final_csv folder, which will be used in RF models
    if not os.path.isdir(direct3):
        os.makedirs(direct3)
    rnames = [i for i in os.listdir(direct2) if 'result_' in i and '.csv' in i]
    for rname in rnames:
        print (rname)
        ddf = pd.read_csv(direct2+rname)
        if all(v == 0 for v in ddf):
            print ('zeros!',rname)
            continue
        sysname = rname.replace('result_scramble_20_20_', '').replace('.csv', '')
        ndf = ddf.loc[ddf['lig_name'] == sysname+'_ligand_opt']
        ndf = ndf.reset_index(drop=True)
        if len(ndf.index) == 0:
            print (sysname+'_ligand_opt')
            print ('Missing native row!', rname)
            break
        ddf = ddf.loc[ddf['lig_name'] != sysname+'_ligand_opt'].reset_index(drop=True)
        fdf1 = pd.DataFrame(columns=[c for c in ddf.columns if c != 'Unnamed: 0'], index=[r1 for r1 in range(0,len(ddf))])
        fdf2 = pd.DataFrame(columns=[c for c in ddf.columns if c != 'Unnamed: 0'], index=[r1 for r1 in range(0,len(ddf))])
        sname = rname.replace('_unif', '')
        fp1 = open(direct3+sname, 'w')
        ddff = pd.DataFrame(columns=[c for c in ddf.columns if c != 'lig_name' and c != 'Unnamed: 0'], index=[r1 for r1 in range(0,len(ddf))])
        ndff = pd.DataFrame(columns=[c for c in ddf.columns if c != 'lig_name' and c != 'Unnamed: 0'], index=[r1 for r1 in range(0,len(ddf))])
        ddff = ddf.drop(['lig_name', 'Unnamed: 0'], axis=1)
        ndff.loc[[r1 for r1 in range(0,len(ddf))],:] = ndf.drop(['lig_name', 'Unnamed: 0'], axis=1).loc[0].values
        fdf1[[c1 for c1 in fdf1.columns if c1 != 'lig_name']] = ndff.sub(ddff)
        fdf2[[c1 for c1 in fdf2.columns if c1 != 'lig_name']] = ddff.sub(ndff)
        fdf1['lig_name'] = ddf['lig_name']+'000'
        fdf2['lig_name'] = ddf['lig_name']+'111'
        fdf = pd.DataFrame()
        fdf = pd.concat([fdf1, fdf2])
        print (len(fdf.index))
        fdf.to_csv(fp1)
        fp1.close()   
