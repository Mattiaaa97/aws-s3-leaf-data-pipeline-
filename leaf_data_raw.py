import sqlite3
import pandas as pd

def genera_dataset_grezzo() -> pd.DataFrame:
    data = {
        'Latitudine': [45.0, 120.0, -10.0, 45.0, 46.2, 44.8, 45.1, 130.0, -20.0, 45.3, 46.5, 44.9, 45.2, 110.0, -5.0, 45.4, 46.1, 44.7],
        'Longitudine': [9.0, 10.0, 250.0, 9.0, 11.5, 8.9, 9.1, 10.5, 260.0, 9.2, 11.6, 9.0, 9.3, 10.2, 240.0, 9.4, 11.4, 8.8],
        'Leaf_Quality_Score': [85, 20, 55, 95, 78, 88, 82, 15, 60, 92, 75, 86, 80, 25, 50, 90, 77, 84],
        'Environmental_Temp': [22.5, 35.0, 15.0, 23.0, 19.5, 21.0, 22.0, 34.0, 16.0, 23.5, 20.0, 21.5, 22.8, 33.0, 14.0, 24.0, 19.0, 20.5],
        'Temperatura': [20.0, 32.0, 12.0, 21.0, 18.0, 19.0, 20.5, 31.0, 13.0, 22.0, 18.5, 19.5, 20.8, 30.0, 11.0, 22.5, 17.5, 18.5],
        'Device_Type': ['Smartphone', 'Sensore', 'Smartphone', 'Smartphone', 'Sensore', 'Smartphone'] * 3,
        'Leaf_Name': ['Quercia', 'Acero', 'Quercia', 'Pino', 'Acero', 'Pino'] * 3,
        'Leaf_Type': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    return pd.concat([df] * 10, ignore_index=True)

def inizializza_database(nome_db: str) -> sqlite3.Connection:
    conn = sqlite3.connect(nome_db)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Tb_Puliti (Lat REAL, Lon REAL, Qualita REAL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS Tb_Scarti_GPS (Lat REAL, Lon REAL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS Tb_Qualita_Bassa (Qualita REAL)')
    conn.commit()
    return conn

def valida_e_filtra_dati(df: pd.DataFrame, conn: sqlite3.Connection) -> pd.DataFrame:
    cursor = conn.cursor()
    righe_valide = []

    for index, riga in df.iterrows():
        lat = riga['Latitudine']
        lon = riga['Longitudine']
        qualita = riga['Leaf_Quality_Score']

        if (-90 <= lat <= 90) and (-180 <= lon <= 180):
            cursor.execute('INSERT INTO Tb_Puliti VALUES (?, ?, ?)', (lat, lon, qualita))
            righe_valide.append(riga)
        else:
            cursor.execute('INSERT INTO Tb_Scarti_GPS VALUES (?, ?)', (lat, lon))

        if qualita < 40:
            cursor.execute('INSERT INTO Tb_Qualita_Bassa VALUES (?)', (qualita,))

    conn.commit()
    return pd.DataFrame(righe_valide)

def salva_csv(df: pd.DataFrame, percorso_file: str) -> None:
    df.to_csv(percorso_file, index=False)
    print(f"File {percorso_file} generato con {len(df)} record validati.")

db_grezzo = genera_dataset_grezzo()
connessione = inizializza_database('analisi_foglie.db')
df_pulito = valida_e_filtra_dati(db_grezzo, connessione)
connessione.close()
salva_csv(df_pulito, 'foglie_pulite_gps_qualita.csv')
