# **Foosball Tracker** 🎱

Un progetto di **Computer Vision** basato su Python e OpenCV per il tracking degli elementi di un biliardino (*calcio balilla*). Il software rileva e traccia il movimento della pallina e dei giocatori, fornendo funzionalità avanzate come filtri configurabili, visualizzazione delle traiettorie e step di elaborazione.
Report completo: [Foosball Tracker Report](./de-paoli-roberto-foosball_tracker-report.pdf).

---

## **Indice**
1. [Caratteristiche principali](#caratteristiche-principali)
2. [Installazione](#installazione)
3. [Struttura del progetto](#struttura-del-progetto)
4. [Configurazione](#configurazione)
5. [Esempio di utilizzo](#esempio-di-utilizzo)

---

## **Caratteristiche principali**

- 🎯 **Tracking della pallina**: Rilevamento della pallina tramite un approccio combinato.
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
├── de-paoli... .pdf          # Report completo del progetto
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


### **Utilizzo**
- Copia i video di esempio nella directory desiderata o lasciali nella cartella **`videos/`**.  
- Modifica il file **`main.py`** per specificare il percorso del video da utilizzare per i test:
```py
stream = Video(cap=cv2.VideoCapture(r'./videos/esempio-1.mp4'))
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
Puoi abilitare/disabilitare la visualizzazione degli step intermedi modificando la pipeline nella classe BallTracker. Per visualizzare questi passaggi, è necessario sostituire la classe Filters con la classe VisualFilters e decommentare le righe corrispondenti in cui viene attivato visualize_steps. Questo permetterà di visualizzare ogni fase del processo di rilevamento.

Inoltre, nella funzione detect di BallTracker, è possibile visualizzare le coordinate stimate della pallina abilitando la variabile draw_point_on_frame. Quando attivata, questa opzione disegnerà un punto rosso sul frame per ogni posizione stimata della pallina, offrendo una visione dettagliata del movimento.

Per visualizzare anche il tracking dei giocatori, bisogna decommentare la riga pit_rosso/blu_tracker.detect nel file main.py. Questo avvierà il rilevamento e il tracciamento dei giocatori tramite la combinazione di filtri e algoritmi preconfigurati.

Tuttavia, è fortemente sconsigliato visualizzare contemporaneamente sia il tracking della pallina che quello dei giocatori, per ottenere una visualizzazione chiara e priva di conflitti.