import json
from datetime import date

#aggiunge 30 cent in cassa e aggiorna i contatori dei caffè (oggi + totale)
def aggiungi_caffe(stato):
    stato["cassa"]+=0.3
    stato["caffe_venduti_oggi"]+=1
    stato["caffe_venduti_totali"] += 1
    return stato

def aggiungi_n_caffe(stato,n):
    stato["cassa"]+=(0.3*n)
    stato["caffe_venduti_oggi"]+=(1*n)
    stato["caffe_venduti_totali"] += (1*n)
    return stato

#fa l'addizione tra la cassa e l'aumento dato in input
def addizione(stato, aumento):
    stato["cassa"] += aumento
    return stato

# sposta un importo dalla cassa alla cassaforte.
# restituisce vero se buono, falso se non buono.
# la piccola tolleranza (EPSILON) serve per gestire le imprecisioni dei numeri
# decimali (es. 7.1999999999999975 invece di 7.2 esatto) utile per azzerare la cassa
def trasferisci_a_cassaforte(stato, importo):
    EPSILON = 1e-9
    if importo <= 0 or importo > stato["cassa"] + EPSILON:
        return stato, False
    stato["cassa"] -= importo
    if stato["cassa"] < 0:
        stato["cassa"] = 0.0  # corregge eventuali residui negativi trascurabili
    stato["cassaforte"] += importo
    return stato, True

def trasferisci_a_cassa(stato, importo):
    EPSILON = 1e-9
    if importo <= 0 or importo > stato["cassaforte"] + EPSILON:
        return stato, False
    stato["cassaforte"] -= importo
    if stato["cassaforte"] < 0:
        stato["cassaforte"] = 0.0  # corregge eventuali residui negativi trascurabili
    stato["cassa"] += importo
    return stato, True

def carica_stato(percorso="dati.json"):
    try:
        with open(percorso, "r", encoding="utf-8") as f:
            stato = json.load(f)
    except FileNotFoundError:
        stato = {}

    stato.setdefault("cassa", 0.0)
    stato.setdefault("cassaforte", 0.0)
    stato.setdefault("caffe_venduti_totali", stato.get("caffe_venduti", 0))
    stato.setdefault("caffe_venduti_oggi", 0)
    stato.setdefault("ultima_data", "")
    stato.pop("caffe_venduti", None)

    oggi = date.today().isoformat()
    if stato["ultima_data"] != oggi:
        stato["caffe_venduti_oggi"] = 0
        stato["ultima_data"] = oggi

    return stato

def salva_stato(stato, percorso="dati.json"):
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(stato, f, indent=4)