import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

new_f = pd.read_csv('warm_up.csv')

X = new_f[['Latitudine', 'Longitudine', 'Device_Type', 'Temperatura', 'Environmental_Temp']]
y = new_f['Device_Type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

sc = MinMaxScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

model = RandomForestClassifier(n_estimators = 100, random_state = 0)
model.fit(X_train, y_train)

score = model.score(X_test, y_test)

confusion = confusion_matrix(y_test, model.predict(X_test))

print('Predizione sul modello di Randomforrest -> ', confusion)
print('Analisi dello score del forrest -> ', score)

print('Dati caricati correttamente ✅!!!')

joblib.dump(model, 'model.pkl')