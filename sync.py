import pandas as pd
import numpy as np
import datetime as datetime
import glob
import os

fpkey = pd.read_excel("//mydrive/SharedDataDept/FQA Warranty/Tools Backup/PowerBI Dashboard/Master_Files/PPM OR/SPPR_FCOK_Master.xlsx")
fpkey.columns = ['SBPR No.', 'Earliest', 'Latest']

fp = pd.read_excel("xlsx/FPCR Dump Data.xlsx") # Change Path

fpcr = pd.merge(left=fp, right=fpkey, on='SBPR No.', how='left')

fpcr['Earliest'] = pd.to_datetime(fpcr['Earliest'])
fpcr['Latest'] = pd.to_datetime(fpcr['Latest'])

ftir = pd.read_excel(sorted(glob.glob("//mydrive/SharedDataDept/MQDASHBOARD/BOT_DOWNLOADS/FTIR_Categorization/*.{}".format('xlsx')), key=os.path.getmtime)[-1], 
                     sheet_name='Sheet1', usecols = ['SBPR No.','FC-OK'])

ftir = ftir.groupby('SBPR No.')['FC-OK'].agg(['min','max']).reset_index()
ftir.columns = ['SBPR No.', 'Earliest', 'Latest']

ftir['Earliest'] = ftir['Earliest'] - pd.offsets.MonthBegin(1)
ftir['Latest'] = ftir['Latest'] - pd.offsets.MonthBegin(1)

df = pd.merge(left=fpcr, right=ftir, on='SBPR No.', how='left')

df['Earliest'] = df[['Earliest_x', 'Earliest_y']].min(axis=1)
df['Latest'] = df[['Latest_x', 'Latest_y']].max(axis=1)

df.drop(['Earliest_x', 'Earliest_y', 'Latest_x', 'Latest_y'], axis=1, inplace=True)

fpkeye = df.groupby('SBPR No.').agg({'Earliest':'min', 'Latest':'max'}).reset_index()
fpkeye.to_excel("//mydrive/SharedDataDept/FQA Warranty/Tools Backup/PowerBI Dashboard/Master_Files/PPM OR/FPCR BaseFile Earliest Latest FCOK.xlsx", index=False)

df['SalesModelCode'] = df['Sales Model Code (SBPR)'].str.split()


df = df.explode(['SalesModelCode'])


df['SalesModelCode'] = df['SalesModelCode'].str.split('(').str[0]


sales = pd.read_excel("//mydrive/SharedDataDept/FQA Warranty/Tools Backup/PowerBI Dashboard/Master_Files/PPM OR/Vehicle Dispatch Data.xlsx")


sales.columns = sales.iloc[0]
sales = sales[1:-1].copy()

sales.drop(columns = {'Grand Total'}, inplace=True)

sales.set_index('Month', inplace=True)

df['TotalSales'] = 0

for index, row in df.iterrows():
    start_date = row['Earliest']
    end_date = row['Latest']
    model_name = row['SalesModelCode']
    
    if model_name in sales.columns:
        mask = (sales.index >= start_date) & (sales.index <= end_date)
        total_sales = sales.loc[mask, model_name].sum()
        df.at[index, 'TotalSales'] = total_sales
    else:
        df.at[index, 'TotalSales'] = 0

data = df.groupby('SBPR No.').agg({'Sales Model Code (SBPR)':'first', 'Earliest':'min', 'Latest':'max', 'TotalSales':'sum'}).reset_index()

final = pd.merge(left=fp, right=data[['SBPR No.','TotalSales','Earliest','Latest']], on='SBPR No.', how='left')

final['PPM'] = final['FTIRs in the SBPR'] * 1000000 / final['TotalSales']
final['OR'] = final['FTIRs in the SBPR'] * 100 / final['TotalSales']

final.replace([np.inf, -np.inf], 0, inplace=True)

dept = pd.read_excel('//mydrive/SharedDataDept/FQA Warranty/Tools Backup/PowerBI Dashboard/Master_Files/PPM OR/Department Mapping.xlsx')

dept['Segments'] = dept['Segments'].str.strip()
dept['Department'] = dept['Department'].str.strip()

dept_dict = dict(zip(dept['Segments'], dept['Department']))

final['Segmentation'] = final['Segmentation'].str.strip()

for keyword, category in dept_dict.items():
    final.loc[final['Segmentation'].str.contains(keyword, case=False, na=False), 'Department'] = category

pn = pd.read_excel(sorted(glob.glob("//mydrive/SharedDataDept/MQDASHBOARD/BOT_DOWNLOADS/FPCR_Vendor_Wise/*.{}".format('xlsx')), key=os.path.getmtime)[-1], 
                   usecols = ['FPCR no', 'Part Name', 'Root cause', 'Countermeasure'])

final = pd.merge(left=final, right=pn, left_on='FPCR\xa0No.', right_on='FPCR no', how='left')
final.drop(['FPCR no'], axis=1, inplace=True)

final["C'measure"] = np.where(final["C'measure"].isna(), "Without C'measurre", "With C'measurre")
final['PPM_Bins'] = pd.cut(final["PPM"], bins=[1,300,1000,np.inf], labels = ["<300", ">300", ">1000"])
final['Department'] = final['Department'].str.replace('QA-','')
final.to_csv("//mydrive/SharedDataDept/FQA Warranty/Tools Backup/PowerBI Dashboard/PPM OR.csv", index=False)
