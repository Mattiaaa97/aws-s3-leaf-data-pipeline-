import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def carica_e_prepara_dati(percorso_csv: str):
    df = pd.read_csv(percorso_csv)
    x = df.drop(columns=['Leaf_Type'])
    y = df['Leaf_Type']
    return x, y

def applica_scaling(x_train, x_test):
    scaler = MinMaxScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    return x_train_scaled, x_test_scaled, scaler

def addestra_modello(x_train, y_train) -> RandomForestClassifier:
    modello = RandomForestClassifier(n_estimators=100, random_state=42)
    modello.fit(x_train, y_train)
    return modello

def valuta_modello(modello, x_test, y_test) -> None:
    previsioni = modello.predict(x_test)
    accuratezza = accuracy_score(y_test, previsioni)
    cm = confusion_matrix(y_test, previsioni)
    print(f"Accuratezza Modello: {accuratezza * 100:.2f}%")
    print("Matrice di Confusione:")
    print(cm)

def esporta_modello(modello, percorso_output: str) -> None:
    joblib.dump(modello, percorso_output)
    print(f"Modello salvato con successo in {percorso_output}")

x, y = carica_e_prepara_dati('warm_up.csv')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
x_train_scaled, x_test_scaled, scaler = applica_scaling(x_train, x_test)

modello_finale = addestra_modello(x_train_scaled, y_train)
valuta_modello(modello_finale, x_test_scaled, y_test)
esporta_modello(modello_finale, 'model.pkl')
