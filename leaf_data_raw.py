import sqlite3
import pandas as pd

data = {
    'Latitudine': [45.0, 120.0, -10.0, 45.0, 46.2, 44.8, 45.1, 130.0, -20.0, 45.3, 46.5, 44.9, 45.2, 110.0, -5.0, 45.4, 46.1, 44.7],
    'Longitudine': [9.0, 10.0, 250.0, 9.0, 11.5, 8.9, 9.1, 10.5, 260.0, 9.2, 11.6, 9.0, 9.3, 10.2, 240.0, 9.4, 11.4, 8.8],
    'Leaf_Quality_Score': [85, 20, 55, 95, 78, 88, 82, 15, 60, 92, 75, 86, 80, 25, 50, 90, 77, 84],
    'Environmental_Temp': [22.5, 35.0, 15.0, 23.0, 19.5, 21.0, 22.0, 34.0, 16.0, 23.5, 20.0, 21.5, 22.8, 33.0, 14.0, 24.0, 19.0, 20.5],
    'Temperatura': [20.0, 32.0, 12.0, 21.0, 18.0, 19.0, 20.5, 31.0, 13.0, 22.0, 18.5, 19.5, 20.8, 30.0, 11.0, 22.5, 17.5, 18.5],
    'Device_Type': ['Smartphone', 'Sensore', 'Smartphone', 'Smartphone', 'Sensore', 'Smartphone']*3, # Ripete 3 volte
    'Leaf_Name': ['Quercia', 'Acero', 'Quercia', 'Pino', 'Acero', 'Pino']*3,
    'Leaf_Type': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
}
db = pd.DataFrame(data)
db = pd.concat([db] * 10, ignore_index=True)

scarti = sqlite3.connect('Scarti.db')
Puliti = sqlite3.connect('Puliti.db')
cursor = scarti.cursor()

def new_table() -> pd.DataFrame:
    data = {'Tree_ID' : [],
    'GPS_Coords' : [],
    'Device_Type' : [],
    'Leaf_Image_Path' : [],
    'Environmental_Temp' : [],
    'Leaf_Name' : [],
    'Leaf Quality Score' : [] }

    return pd.DataFrame(data)

def filtering_gps(Latitudine, Longitudine) -> None:
    if Latitudine < -90 or Latitudine > 90:
        scarti.execute('CREATE TABLE IF NOT EXISTS Tb_Latitudine (Lat REAL)')
        scarti.execute('INSERT INTO Tb_Latitudine (Lat) VALUES (?)', (Latitudine,))
        scarti.commit()
        print(f'Dati caricati correttamente nella tabella Scarti ({Latitudine}) !!!')

    elif Longitudine < -180 or Longitudine > 180:
        scarti.execute('CREATE TABLE IF NOT EXISTS Tb_Longitudine (Lon REAL)')
        scarti.execute('INSERT INTO Tb_Longitudine VALUES (?)', (Longitudine,))
        scarti.commit()
        print(f'Dati caricati correttamente nella tabella Scarti ({Longitudine})!!!')

    else:
        Puliti.execute('CREATE TABLE IF NOT EXISTS Tb_Puliti (Lat REAL, Lon REAL)')
        Puliti.execute('INSERT INTO Tb_Puliti (Lat, Lon) VALUES (?, ?)', (Latitudine, Longitudine))
        Puliti.commit()
        print('Dati caricati correttamente nella tabella Puliti ✅!!!')


hight_foglia = sqlite3.connect('Foglia.db')
medium_foglia = sqlite3.connect('Bad_foglia.db')
trash_foglia = sqlite3.connect('Trash_foglia.db')
cursor_2 = hight_foglia.cursor()
cursor_3 = medium_foglia.cursor()
cursor_4 = trash_foglia.cursor()

def filtering_quality(foglia) -> None:
    if foglia > 70:
        cursor_2.execute('CREATE TABLE IF NOT EXISTS Tb_hight_foglia (Fog REAL)')
        cursor_2.execute('INSERT INTO Tb_hight_foglia VALUES (?)', (foglia,))
        hight_foglia.commit()
        print(f'La foglia di alta qualità salvata in hight_foglia ({foglia})!!!')

    elif 40 <= foglia <= 70:
        cursor_3.execute('CREATE TABLE IF NOT EXISTS Tb_medium_foglia (Fog REAL)')
        cursor_3.execute('INSERT INTO Tb_medium_foglia VALUES (?)', (foglia,))
        medium_foglia.commit()
        print(f'La foglia è di media qualità salvata in medium_foglia ({foglia})!!!')

    else:
        cursor_4.execute('CREATE TABLE IF NOT EXISTS Tb_trash_foglia (Fog REAL)')
        cursor_4.execute('INSERT INTO Tb_trash_foglia VALUES (?)', (foglia,))
        trash_foglia.commit()
        print(f'La foglia è di bassa qualità salvata in trash_foglia ({foglia})!!!')

for index, riga in db.iterrows():
    l = riga['Latitudine']
    lo = riga['Longitudine']
    qualita = riga['Leaf_Quality_Score']

    filtering_gps(l, lo)
    filtering_quality(qualita)

scarti.close()
Puliti.close()
hight_foglia.close()
medium_foglia.close()
trash_foglia.close()

print(f"Processo terminato. Ho analizzato {len(db)} righe.")

filter_data = db.to_csv('foglie_pulite_gps_qualita.csv', index=False)









