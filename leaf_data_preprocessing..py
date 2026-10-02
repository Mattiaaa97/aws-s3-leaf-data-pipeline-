import pandas as pd

fle = pd.read_csv('foglie_pulite_gps_qualita.csv')

def converti_formato() -> None:
    fle['Leaf_Name'] = fle['Leaf_Name'].astype('category').cat.codes
    fle['Device_Type'] = fle['Device_Type'].astype('category').cat.codes

converti_formato()

X = fle[['Latitudine', 'Longitudine', 'Device_Type', 'Temperatura', 'Environmental_Temp', 'Leaf_Name']]
y = fle[['Leaf_Type']]

fle.dropna(inplace=True)

f = fle.to_csv('warm_up.csv', index = False)
print('File caricati con successo!!!')

