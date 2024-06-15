import pandas as pd

path_master = input("Enter the path of the MASTER file in double quotes (csv): ").strip('"')
path_smaller = input("Enter the path of the SMALLER file in double quotes (excel): ").strip('"')

try:
    Master_df = pd.read_csv(path_master)
    print("\nLOADING SUCCESS!!")
except :
    print("Error loading files: {}".format(path_master))
    exit(1)
    
try:        
    Site_ID_df = pd.read_excel(path_smaller)
    print("\nLOADING SUCCESS!!")
except :
    print("Error loading files: {}".format(path_smaller))
    exit(1)

x = int(input("\nWANT TO DISPLAY COLUMNS? (YES=1 / NO=0)\n"))
if(x == 1): 
    print("Master file columns:\n", Master_df.columns,"\n")
    print("Smaller file columns:\n", Site_ID_df.columns,"\n")


col_master = input("Enter the name of the column in master file in single quotes you want to filter: ").strip("'")
col_smaller = input("Enter the name of the column in smaller file in single quotes: ").strip("'")


if col_master not in Master_df.columns:
    print("\nCOLUMN '{}' NOT FOUND IN THE MASTER FILE.".format(col_master))
    exit(1)
    
if col_smaller not in Site_ID_df.columns:
    print("\nCOLUMN '{}' NOT FOUND IN THE SMALLER FILE".format(col_smaller))
    exit(1)


master_site_ids = Master_df[col_master]
random_site_ids = Site_ID_df[col_smaller]


print("\nExtracted master site IDs:\n")
print(master_site_ids)

print("\nExtracted smaller site IDs:\n")
print(random_site_ids)

common_site_ids = random_site_ids[random_site_ids.isin(master_site_ids)]

filtered_master_df = Master_df[Master_df[col_master].isin(common_site_ids)]

print(filtered_master_df)

exp = int(input("\nDo you want to import the file? (YES=1 / NO=0)"))

if(exp == 1):
    name = input("ENTER THE OUTPUT FILE NAME: ")
    filtered_master_df.to_excel("/Users/anav_sobti/Downloads/ACTIVITY_1/{}.xlsx".format(name), index=False)
    print("\nIMPORTED!!\n  CHECK THE FILE")

print("DONE SUBSET")