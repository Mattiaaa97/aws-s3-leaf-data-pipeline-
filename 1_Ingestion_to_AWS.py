import boto3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

AWS_ACCESS_KEY = 'Mtna6'
AWS_SECRET_KEY = '09rf0s404j0w'
AWS_REGION = 'eu-central-1'

backet = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      region_name=AWS_REGION)

biomedical_ingestion = 'mybucket'

try:
    backet.create_bucket(
        Bucket=biomedical_ingestion,
        CreateBucketConfiguration={
            'LocationConstraint': AWS_REGION
        }
    )
    backet.upload_file('foglie_pulite_gps_qualita.csv', biomedical_ingestion, 'raw/dati_test_01.csv')
except FileNotFoundError as e:
    print('Il file non è presente al suo interno!!!')


def clean_data() -> str:
    file = backet.get_object(Bucket=biomedical_ingestion, Key='raw/dati_test_01.csv')

    df = pd.read_csv(file['Body'])

    df['Leaf_Name'] = df['Leaf_Name'].astype('category').cat.codes

    new_backet = backet.put_object(Bucket=biomedical_ingestion, Key='processed/dati_reclean.csv', Body=df.to_csv(
        index=False
    ))

    return 'Pulizia completata correttamente ✅'

print(clean_data())

df = pd.read_csv('processed/dati_reclean.csv')
def validation_parts(df: pd.DataFrame) -> pd.DataFrame:
    tot_righe: int = len(df)
    metà : int = tot_righe // 2
    for_a = df.iloc[:metà]
    for_b = df.iloc[metà:]

    y_a = for_a['Qualità']
    X_a = for_a.drop(columns=['Qualità', 'Leaf_Name'])

    y_b = for_b['Qualità']
    X_b = for_b.drop(columns=['Qualità', 'Leaf_Name'])

    return X_a, y_a, X_b, y_b

def fit_Run_Forrest(X_a, y_a, X_b, y_b) -> df:
    print('Random forrest prima metà dei dati')
    model_1 = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)

    model_1.fit(X_a, y_a)

    y_pred = model_1.predict(X_b)

    print(f"Score Modello 1: {model_1.score(X_b, y_b)}")  # Esame su B!
    print("Matrice di Confusione 1:")
    print(confusion_matrix(y_b, y_pred))

    print('Random forrest seconda metà dei dati')
    model_2 = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)

    model_2.fit(X_b, y_b)

    y_pred_2 = model_2.predict(X_a)

    print(f"Score Modello 2: {model_2.score(X_a, y_a)}")  # Esame su B!
    print("Matrice di Confusione 1:")
    print(confusion_matrix(y_a, y_pred_2))

    return model_1, model_2

Xa, ya, Xb, yb = validation_parts(df)
m1, m2 = fit_Run_Forrest(Xa, ya, Xb, yb)

print("\nValidazione incrociata completata con successo! 🚀")
























