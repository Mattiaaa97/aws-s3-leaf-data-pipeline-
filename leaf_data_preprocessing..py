import pandas as pd

fle = pd.read_csv('foglie_pulite_gps_qualita.csv')

def stampa_info_dataset() -> None:
    print(fle.isnull().sum())
    fle.dropna(inplace=True)

stampa_info_dataset()

def converti_formato() -> None:
    fle['Leaf_Name'] = fle['Leaf_Name'].astype('category').cat.codes
    fle['Device_Type'] = fle['Device_Type'].astype('category').cat.codes

converti_formato()

def estrai_features_e_target():
    x = fle.drop(columns=['Leaf_Type'])
    y = fle['Leaf_Type']
    return x, y

x, y = estrai_features_e_target()

def salva_file() -> None:
    fle.to_csv('warm_up.csv', index=False)
    print('File warm_up.csv salvato con successo!')

salva_file()
