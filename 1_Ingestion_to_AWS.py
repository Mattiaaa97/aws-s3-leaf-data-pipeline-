import os
import boto3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

nome_bucket = 'biomedical_ingestion'
regione = 'eu-central-1'

def carica_su_s3(file_locale: str, bucket: str, file_s3: str, reg: str) -> None:
    s3 = boto3.client(
        's3',
        region_name=reg,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    configurazione_posizione = {'LocationConstraint': reg}
    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration=configurazione_posizione
    )
    s3.upload_file(file_locale, bucket, file_s3)

carica_su_s3('foglie_pulite_gps_qualita.csv', nome_bucket, 'dataset_foglie_raw.csv', regione)

df = pd.read_csv('foglie_pulite_gps_qualita.csv')

def pulisci_dataset(df_input: pd.DataFrame) -> pd.DataFrame:
    df_pulito = df_input.dropna().copy()
    df_pulito['Leaf_Name'] = df_pulito['Leaf_Name'].astype('category').cat.codes
    df_pulito = df_pulito.drop(columns=['Device_Type'])
    return df_pulito

df_processato = pulisci_dataset(df)

def esegui_cross_validation(dati: pd.DataFrame) -> None:
    meta = len(dati) // 2

    parte_1 = dati.iloc[:meta]
    parte_2 = dati.iloc[meta:]

    x_train_1 = parte_1.drop(columns=['Leaf_Quality_Score'])
    y_train_1 = parte_1['Leaf_Quality_Score']
    x_test_1 = parte_2.drop(columns=['Leaf_Quality_Score'])
    y_test_1 = parte_2['Leaf_Quality_Score']

    modello_1 = RandomForestClassifier(random_state=42)
    modello_1.fit(x_train_1, y_train_1)
    accuratezza_1 = modello_1.score(x_test_1, y_test_1)
    print(f"Accuratezza Test 1 (Train su Parte 1, Test su Parte 2): {accuratezza_1 * 100:.2f}%")

    x_train_2 = parte_2.drop(columns=['Leaf_Quality_Score'])
    y_train_2 = parte_2['Leaf_Quality_Score']
    x_test_2 = parte_1.drop(columns=['Leaf_Quality_Score'])
    y_test_2 = parte_1['Leaf_Quality_Score']

    modello_2 = RandomForestClassifier(random_state=42)
    modello_2.fit(x_train_2, y_train_2)
    accuratezza_2 = modello_2.score(x_test_2, y_test_2)
    print(f"Accuratezza Test 2 (Train su Parte 2, Test su Parte 1): {accuratezza_2 * 100:.2f}%")

esegui_cross_validation(df_processato)
