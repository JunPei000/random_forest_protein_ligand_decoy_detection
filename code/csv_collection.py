import os
from shutil import copyfile

direct1 = Path_of_CASF-2013
noneed = ['origial_csv', 'final_csv', '1hfs', '2jdu', 'README', 'index', '2d1o', '2jdy']
foldernames = ['coreset']
for foldername in foldernames:
    direct2 = direct1+foldername+'/'
    direct3 = direct2+'origial_csv/'
    if not os.path.isdir(direct3):
        os.makedirs(direct3)
    ffoldernames = [i for i in os.listdir(direct2) if i not in noneed and len(i) == 4]
    for ffoldername in ffoldernames:
        direct4 = direct2+ffoldername+'/'
        resultname = 'result_'+ffoldername+'.csv'
        if resultname in os.listdir(direct4):
            copyfile(direct4+resultname, direct3+resultname)
        else:
            print (foldername, ffoldername)
