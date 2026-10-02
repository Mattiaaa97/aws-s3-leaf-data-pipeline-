# 🌿 AWS S3 Data Pipeline & Leaf Classification (Biomedical)

Benvenuti nel repository del progetto **AWS S3 Data Pipeline & Leaf Classification**. Questo progetto documenta lo sviluppo di una pipeline modulare di Data Engineering e Machine Learning per l'analisi e il controllo qualità di campioni botanici e biomedici: dalla generazione e validazione geografica dei dati grezzi, alla preparazione delle feature, fino all'archiviazione cloud scalabile su Amazon S3 e all'addestramento e serializzazione di modelli predittivi con Scikit-learn.

---

## 🛠️ Organizzazione dei Moduli

### 🔹 Fase 1: Data Ingestion & Storage Locale
* **Modulo 01: Simulazione e Strutturazione Dati** - Generazione controllata di dataset tabellari multilivello (coordinate GPS, temperature ambientali, sensori e indici di qualità).
* **Modulo 02: Validazione Geografica Relazionale** - Implementazione di controlli di conformità su coordinate GPS (latitudine [-90, +90], longitudine [-180, +180]) tramite SQLite.
* **Modulo 03: Smistamento e Isolamento Anomalie** - Segmentazione automatizzata dei record tra tabelle di scarto e archivio dei dati puliti (`analisi_foglie.db`).
* **Modulo 04: Esportazione Dataset Validato** - Generazione del dataset consolidato `foglie_pulite_gps_qualita.csv` privo di outlier e coordinate invalide.

### 🔹 Fase 2: Preprocessing & Data Cleaning
* **Modulo 05: Categorical Encoding** - Conversione delle variabili categoriche (`Leaf_Name`, `Device_Type`) in codici numerici discreti tramite `.cat.codes`.
* **Modulo 06: Trattamento Valori Nulli** - Bonifica dei record incompleti tramite rimozione sicura dei valori mancanti (`dropna`).
* **Modulo 07: Feature Selection Preliminare** - Separazione delle feature predittive dal target ed esportazione del dataset preparato `warm_up.csv`.

### 🔹 Fase 3: Cloud Ingestion & Scalabilità (AWS S3)
* **Modulo 08: Gestione Sicura delle Credenziali** - Adozione delle best practice cloud tramite variabili d'ambiente di sistema (`os.getenv`) senza chiavi hardcodate.
* **Modulo 09: Provisioning Cloud con Boto3** - Creazione programmatica di bucket su AWS S3 con vincoli regionali (`eu-central-1`).
* **Modulo 10: Storage Stratificato** - Caricamento dei file raw nel cloud storage per garantire persistenza, tracciabilità e versionamento del dato.
* **Modulo 11: Cross-Validation Manuale per Partizioni** - Verifica della stabilità dei parametri tramite partizionamento alternato e validazione incrociata.

### 🔹 Fase 4: Machine Learning & Validazione Predittiva
* **Modulo 12: Feature Scaling con MinMaxScaler** - Riscalatura uniforme delle feature continue nell'intervallo `[0.0, 1.0]` per bilanciare i pesi.
* **Modulo 13: Random Forest Classifier** - Addestramento del modello di classificazione ad alberi decisionali multipli per mitigare l'overfitting.
* **Modulo 14: Valutazione delle Performance** - Diagnostica approfondita del classificatore mediante accuratezza e matrice di confusione.
* **Modulo 15: Model Serialization** - Esportazione e persistenza del modello addestrato in formato binario `model.pkl` tramite `joblib` per l'inferenza in produzione.

---

## 🏆 Flusso Operativo: I Quattro Script del Progetto

1. **`leaf_data_raw.py`**: Generazione, validazione geometrica GPS, logging delle anomalie su database SQLite e salvataggio del dataset privo di anomalie.
2. **`leaf_data_preprocessing..py`**: Codifica numerica delle categorie, rimozione dei record nulli e generazione del file di input `warm_up.csv`.
3. **`1_Ingestion_to_AWS.py`**: Configurazione del client AWS S3, sincronizzazione cloud del dataset e validazione incrociata preliminare del modello.
4. **`3_AI_Model_Pipeline.py`**: Pipeline finale di Machine Learning: caricamento di `warm_up.csv`, scaling con `MinMaxScaler`, training del Random Forest e salvataggio dell'artefatto `model.pkl`.

---

## 🎓 Competenze Acquisite
* **Linguaggi & Ambienti:** Python 3.x (Modular Design, Automation Scripting, Cloud Connectivity).
* **Data Management & SQL:** SQLite3, Pandas.
* **Cloud & DevOps:** AWS S3, Boto3 SDK, Environment Variables Management.
* **Machine Learning & AI:** Scikit-Learn (Random Forest, Preprocessing, Model Metrics), Joblib.

---

**Progetto realizzato da Mattia Dellanoce**
