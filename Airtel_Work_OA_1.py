import pandas as pd
sheet_name_samsung = "NR"
sheet_name_Ericsson = "5G"
sheet_name_nokia = "Macro Data"

Nokia_df = pd.read_excel("/Users/anav_sobti/Desktop/OA_ANAV/5G Macro DPR_16 June'24.xlsx", sheet_name=sheet_name_nokia , header = 1)
Ericsson_df = pd.read_excel("/Users/anav_sobti/Desktop/OA_ANAV/Project summary(3268+3219) till 13th June'24 - Site list.xlsx", sheet_name=sheet_name_Ericsson)
Samsung_df = pd.read_excel("/Users/anav_sobti/Desktop/OA_ANAV/DPR for-Samsung-rollout_12-Jun-2024.xlsx", sheet_name=sheet_name_samsung)

#replacing CN to CH in erricson file
Ericsson_df['CIRCLE'] = Ericsson_df['CIRCLE'].replace('CN', 'CH')

#replacing BR to BH and JH to BH in nokia file
Nokia_df['Circle'] = Nokia_df['Circle'].replace('BR', 'BH')
Nokia_df['Circle'] = Nokia_df['Circle'].replace('JH', 'BH')

# Step 1 adding OEM column in the three files
Nokia_df['OEM'] = 'NOKIA'
Ericsson_df['OEM'] = 'ERICSSON'
Samsung_df['OEM'] = 'SAMSUNG'

# Adding column Identifier in all (circle pip site_id)
Nokia_df['IDENTIFIER'] = Nokia_df['Circle'].astype(str) + '|' + Nokia_df['Site ID'].astype(str)
Samsung_df['IDENTIFIER'] = Samsung_df['Circle'].astype(str) + '|' + Samsung_df['2G_SITE_ID'].astype(str)
Ericsson_df['IDENTIFIER'] = Ericsson_df['CIRCLE'].astype(str) + '|' + Ericsson_df['SITE_ID_2G'].astype(str)


# Changing names of column in all files
Nokia_subset = Nokia_df[['Circle', 'Site ID', 'MS 1/ OnAir', 'IDENTIFIER', 'OEM']].rename(columns={'Circle': 'CIRCLE', 'Site ID': 'SITE_ID', 'MS 1/ OnAir': 'ON AIR DATE', 'IDENTIFIER':'IDENTIFIER' , 'OEM':'OEM'})
Ericsson_subset = Ericsson_df[['CIRCLE', 'SITE_ID_2G', 'OA_DATE_ACTUAL', 'IDENTIFIER', 'OEM']].rename(columns={'CIRCLE': 'CIRCLE', 'SITE_ID_2G': 'SITE_ID', 'OA_DATE_ACTUAL': 'ON AIR DATE', 'IDENTIFIER':'IDENTIFIER' , 'OEM':'OEM'})
Samsung_subset = Samsung_df[['Circle', '2G_SITE_ID', 'Radiating_Date_NR', 'IDENTIFIER', 'OEM']].rename(columns={'Circle': 'CIRCLE', '2G_SITE_ID': 'SITE_ID', 'Radiating_Date_NR': 'ON AIR DATE', 'IDENTIFIER':'IDENTIFIER' , 'OEM':'OEM'})

# Concatenation of the files
combined_nok_eri_sam_df = pd.concat([Nokia_subset, Ericsson_subset, Samsung_subset], axis=0)

# Dropping rows where ON AIR DATE is NULL
OutPut1 = combined_nok_eri_sam_df.dropna(subset=['ON AIR DATE'])

'''print(OutPut1)'''
#OUTPUT 1 is done

OUTPUT_2 = OutPut1['CIRCLE'].value_counts().reset_index()
OUTPUT_2.columns = ['CIRCLE', 'TOTAL']
'''print(OUTPUT_2)'''
# Output 2 is done

OUTPUT_3 = OutPut1.groupby(['CIRCLE', 'OEM']).size().unstack(fill_value=0).reset_index()
OUTPUT_3.columns = ['CIRCLE' , 'ERICSSON' , 'NOKIA', 'SAMSUNG']
OUTPUT_3['TOTAL'] = OUTPUT_3['ERICSSON'] + OUTPUT_3['NOKIA'] + OUTPUT_3['SAMSUNG']
#print(OUTPUT_3)
total_sum = OUTPUT_3['TOTAL'].sum()
total_ericsson = OUTPUT_3['ERICSSON'].sum()
total_Nokia = OUTPUT_3['NOKIA'].sum()
total_Samsung = OUTPUT_3['SAMSUNG'].sum()
new_row = ({'CIRCLE': 'total' ,'ERICSSON': total_ericsson , 'NOKIA': total_Nokia , 'SAMSUNG': total_Samsung , 'TOTAL': total_sum})

print(OUTPUT_3)
#OUTPUT_3.to_excel("/Users/anav_sobti/Desktop/OA_ANAV/Required_OUTPUT.xlsx")

