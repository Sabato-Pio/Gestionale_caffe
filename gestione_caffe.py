import json
import os
from datetime import date, datetime

CARTELLA_ARCHIVIO = "archivio_mensile"

def _mese_da_data(data_iso):
    # da "2026-07-13" a "2026-07"
    return data_iso[:7] if data_iso else ""

def _percorso_file_mese(mese, cartella=CARTELLA_ARCHIVIO):
    return os.path.join(cartella, f"storico_{mese}.json")

# crea il file del mese se non esiste ancora, con il saldo di partenza
# (il saldo con cui il mese è iniziato, ereditato dal mese precedente)
def _crea_file_mese_se_serve(mese, saldo_iniziale, cartella=CARTELLA_ARCHIVIO):
    os.makedirs(cartella, exist_ok=True)
    percorso = _percorso_file_mese(mese, cartella)
    if not os.path.exists(percorso):
        contenuto = {
            "mese": mese,
            "saldo_iniziale": saldo_iniziale,
            "operazioni": [],
        }
        with open(percorso, "w", encoding="utf-8") as f:
            json.dump(contenuto, f, indent=4, ensure_ascii=False)
    return percorso

# registra un'operazione scrivendola SUBITO nel file del mese corrente
# (es. archivio_mensile/storico_2026-07.json): non resta solo in memoria,
# viene salvata su disco a ogni singola operazione, così il log è sempre
# aggiornato in tempo reale e consultabile in ogni momento, anche a mese
# ancora in corso.
def registra_operazione(stato, tipo, descrizione):
    oggi = date.today().isoformat()
    mese_corrente = _mese_da_data(oggi)
    saldo_iniziale = stato.get(
        "saldo_inizio_mese", {"cassa": stato["cassa"], "cassaforte": stato["cassaforte"]}
    )
    percorso = _crea_file_mese_se_serve(mese_corrente, saldo_iniziale)

    with open(percorso, "r", encoding="utf-8") as f:
        contenuto = json.load(f)

    adesso = datetime.now()
    contenuto["operazioni"].append({
        "data": adesso.strftime("%Y-%m-%d"),
        "ora": adesso.strftime("%H:%M:%S"),
        "tipo": tipo,
        "descrizione": descrizione,
        "cassa_dopo": round(stato["cassa"], 2),
        "cassaforte_dopo": round(stato["cassaforte"], 2),
    })

    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(contenuto, f, indent=4, ensure_ascii=False)

    return stato

#aggiunge 30 cent in cassa e aggiorna i contatori dei caffè (oggi + mese + totale)
def aggiungi_caffe(stato):
    stato["cassa"]+=0.3
    stato["caffe_venduti_oggi"]+=1
    stato["caffe_venduti_totali"] += 1
    stato["caffe_venduti_mese"] = stato.get("caffe_venduti_mese", 0) + 1
    registra_operazione(stato, "vendita_caffe", "Venduto 1 caffè (+0.30€)")
    return stato

def aggiungi_n_caffe(stato,n):
    stato["cassa"]+=(0.3*n)
    stato["caffe_venduti_oggi"]+=(1*n)
    stato["caffe_venduti_totali"] += (1*n)
    stato["caffe_venduti_mese"] = stato.get("caffe_venduti_mese", 0) + n
    registra_operazione(stato, "vendita_multipla", f"Venduti {n} caffè (+{0.3*n:.2f}€)")
    return stato

#fa l'addizione tra la cassa e l'aumento dato in input
def addizione(stato, aumento):
    stato["cassa"] += aumento
    registra_operazione(stato, "donazione", f"Donazione di {aumento:.2f}€")
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
    registra_operazione(stato, "trasferimento_a_cassaforte", f"Trasferiti {importo:.2f}€ dalla cassa alla cassaforte")
    return stato, True

def trasferisci_a_cassa(stato, importo):
    EPSILON = 1e-9
    if importo <= 0 or importo > stato["cassaforte"] + EPSILON:
        return stato, False
    stato["cassaforte"] -= importo
    if stato["cassaforte"] < 0:
        stato["cassaforte"] = 0.0  # corregge eventuali residui negativi trascurabili
    stato["cassa"] += importo
    registra_operazione(stato, "trasferimento_a_cassa", f"Trasferiti {importo:.2f}€ dalla cassaforte alla cassa")
    return stato, True

# Se è iniziato un nuovo mese rispetto all'ultima operazione registrata:
# 1) il saldo di inizio mese riparte da dove si era fermato quello vecchio
#    (cassa e cassaforte non si azzerano mai) e crea SUBITO il file del
#    nuovo mese (anche prima che avvenga la prima operazione).
# 2) se il nuovo mese è settembre, azzera "caffe_venduti_totali" (si
#    riparte da 0 col nuovo anno) e lo registra come operazione di sistema.
def gestisci_cambio_mese(stato):
    oggi = date.today().isoformat()
    mese_corrente = _mese_da_data(oggi)
    mese_precedente = _mese_da_data(stato.get("ultima_data", ""))

    if mese_precedente and mese_precedente != mese_corrente:
        stato["saldo_inizio_mese"] = {"cassa": stato["cassa"], "cassaforte": stato["cassaforte"]}
        stato["caffe_venduti_mese"] = 0

        _crea_file_mese_se_serve(mese_corrente, stato["saldo_inizio_mese"])

        # azzeramento annuale: solo quando si entra in settembre
        if mese_corrente[5:7] == "09":
            stato["caffe_venduti_totali"] = 0
            registra_operazione(
                stato,
                "reset_annuale",
                "Azzerato il conteggio dei caffè totali per l'inizio del nuovo anno (settembre)"
            )

    return stato

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
    stato.setdefault("caffe_venduti_mese", 0)
    stato.setdefault("ultima_data", "")
    stato.setdefault("saldo_inizio_mese", {"cassa": stato["cassa"], "cassaforte": stato["cassaforte"]})
    stato.pop("caffe_venduti", None)
    stato.pop("storico", None)  # il log ora vive nei file mensili, non più qui

    oggi = date.today().isoformat()
    stato = gestisci_cambio_mese(stato)

    if stato["ultima_data"] != oggi:
        stato["caffe_venduti_oggi"] = 0
        stato["ultima_data"] = oggi

    return stato

def salva_stato(stato, percorso="dati.json"):
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(stato, f, indent=4, ensure_ascii=False)