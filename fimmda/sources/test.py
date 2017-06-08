import os, sys, shutil

input_file = "FIMMDA_ZERO CURVE_ZCYC_DAILY_25112016 - Copy.csv"
input_folder="./input/"
archive_folder = "./archive/"
#path = os.path.join(input_folder,input_file)
path = input_folder+input_file
#path = r'./input/FIMMDA_ZERO SPREAD_DAILY_25112016 - Copy.csv'
print path
#shutil.copy2("r'"+source+input_folder+input_file+"'"j, archive_folder)
shutil.copy2(path, archive_folder)

