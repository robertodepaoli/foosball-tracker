# **Foosball Tracker** 🎱

Un progetto di **Computer Vision** basato su Python e OpenCV per il tracking degli elementi di un biliardino (*calcio balilla*). Il software rileva e traccia il movimento della pallina e dei giocatori, fornendo funzionalità avanzate come filtri configurabili, visualizzazione delle traiettorie e step di elaborazione.

---

## **Indice**
1. [Caratteristiche principali](#caratteristiche-principali)
2. [Installazione](#installazione)
3. [Struttura del progetto](#struttura-del-progetto)
4. [Configurazione](#configurazione)
5. [Materiale Video Fornito](#materiale-video-fornito)
6. [Esempio di utilizzo](#esempio-di-utilizzo)

---

## **Caratteristiche principali**

- 🎯 **Tracking della pallina**: Rilevamento accurato con Hough Transform e filtri di contorni.
- 🧩 **Pipeline modulare**: Gestione degli step di elaborazione tramite filtri configurabili.
- 🖼️ **Visualizzazione in tempo reale**: 
  - Step intermedi.
  - Traiettoria della pallina.
  - Griglia delle elaborazioni.
- ⚙️ **Filtri personalizzabili**: Configurazione dei parametri tramite file JSON.
- 📈 **Kalman Filter**: Previsione e correzione delle posizioni per un tracking fluido.

---

## **Installazione**

### **Requisiti**
- Python 3.8+
- Librerie:
  - `opencv-python`
  - `numpy`

### **Guida all'installazione**
1. Clona il repository:
   ```bash
   git clone https://github.com/<tuo-username>/foosball-tracker.git
   cd foosball-tracker
   ```
2. Crea un ambiente virtuale e attivalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   source venv\Scripts\activate     # Windows
   ```
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
4. Esegui il progetto:
   ```bash
   python main.py
   ```

---

## **Struttura del progetto**

```
foosball-tracker/
│
├── ball/                     # Modulo per il tracking della pallina
│   ├── __init__.py
│   ├── contours.py           # Rilevamento tramite contorni
│   ├── hough.py              # Rilevamento tramite Hough Transform
│   ├── kalman.py             # Kalman Filter per la stima
│   ├── tracker.py            # Script principale per il tracking
│   └── trajectory.py         # Gestione delle traiettorie
│
├── players/                  # Modulo per il tracking dei giocatori
│   ├── __init__.py
│   ├── biliardino.py         # Definizione struttura del tavolo
│   ├── tracker.py            # Script principale per il tracking
│   └── zone.py               # Definizione zone del campo
│
├── utils/                    # Utility condivise
│   ├── __init__.py
│   ├── edges.py              # Definizione dei bordi del tavolo
│   ├── filters.py            # Filtri per elaborazione delle immagini
│   ├── forces.py             # Definzione angoli del tavolo
│   ├── stabilizer.py         # Correzione dell'immagine
│   └── stream.py             # Gestione del video
│
├── .gitignore                
├── config.json               # Configurazione dei parametri dei filtri
├── main.py                   # Script principale
├── README.md                 # Documentazione del progetto
└── requirements.txt          
```

---

## **Configurazione**

I parametri per i filtri di elaborazione e altre impostazioni sono gestiti tramite il file **`config.json`**. Un esempio di configurazione:

```json
{
    "FILTERS": {
        "white_mask": {
            "lower_white": [0, 0, 200],
            "upper_white": [180, 30, 255]
        },
        "median_blur": {
            "kernel_size": 5
        },
        "gaussian_blur": {
            "kernel_size": 5,
            "sigma": 1.5
        }
    }
}
```
---

## **Materiale Video Fornito**

Il repository include una serie di video di esempio utili per testare il progetto e per sperimentare con i parametri di configurazione. I video sono archiviati nella cartella **`videos/`** e coprono diverse situazioni comuni di gioco.

### **Elenco dei video**

1. `match_example.mp4`  
   - **Descrizione:** Una partita simulata di biliardino con movimenti standard.  
   - **Scopo:** Testare il tracking della pallina in un contesto realistico.  

2. `high_speed_ball.mp4`  
   - **Descrizione:** Movimenti veloci della pallina con scatti improvvisi.  
   - **Scopo:** Valutare la capacità del sistema di seguire traiettorie rapide e imprevedibili.  

3. `occlusion_test.mp4`  
   - **Descrizione:** Situazioni in cui la pallina è parzialmente nascosta dai giocatori.  
   - **Scopo:** Testare la robustezza del sistema in presenza di occlusioni.

4. `lighting_variations.mp4`  
   - **Descrizione:** Cambiamenti di illuminazione durante il gioco.  
   - **Scopo:** Analizzare il comportamento del sistema in condizioni di luce variabili.

5. `noisy_background.mp4`  
   - **Descrizione:** Partita giocata su un biliardino con un fondo complesso e colori simili alla pallina.  
   - **Scopo:** Testare i filtri e la capacità di distinguere la pallina dallo sfondo.

### **Utilizzo**
- Copia i video di esempio nella directory desiderata o lasciali nella cartella **`videos/`**.  
- Modifica il file **`main.py`** per specificare il percorso del video da utilizzare per i test:
```py
stream = Video(cap=cv2.VideoCapture(r'./biliardino.mp4'))
```

---

## **Esempio di utilizzo**

### **Tracking della pallina**
Esegui lo script principale:
```bash
python main.py
```
- **Visualizzazione**: La finestra principale mostrerà:
  - La posizione della pallina.
  - La traiettoria calcolata.
  - Eventuali step intermedi configurati.

### **Personalizzazione**
Puoi abilitare/disabilitare la visualizzazione degli step intermedi modificando la pipeline nella classe `BallTracker`.