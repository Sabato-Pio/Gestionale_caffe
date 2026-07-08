import tkinter as tk
from gestione_caffe import aggiungi_caffe, addizione, carica_stato, salva_stato


def avvia_gui():
    global stato_cassa
    stato_cassa = carica_stato()  # carica (o crea) dati.json all'avvio

    finestra = tk.Tk()
    finestra.title("Gestione caffè di MR.S")
    finestra.geometry("720x400")
    frame_pagina1 = tk.Frame(finestra)
    frame_pagina1.pack(fill="both", expand=True)

    frame_pagina2 = tk.Frame(finestra, bg="grey")

    testo_benvenuto = tk.Label(frame_pagina1, text="Benvenuto nel gestionale di MR.S!")
    testo_benvenuto.pack(pady=20)  # aggiunge del margine

    # Display soldi e caffè, già con i valori caricati da dati.json
    display_saldo = tk.Label(frame_pagina1, text="", font=("Arial", 12))
    display_saldo.pack(pady=10)

    # funzione unica per aggiornare il testo del display, così non lo ripetiamo ovunque
    def aggiorna_display():
        display_saldo.config(
            text=(
                f"Saldo: {stato_cassa['cassa']:.2f}€ | "
                f"Caffè oggi: {stato_cassa['caffe_venduti_oggi']} | "
                f"Totali: {stato_cassa['caffe_venduti_totali']}"
            )
        )

    aggiorna_display()

    # funzione per il bottone per il caffe
    def premi_bottone():
        global stato_cassa
        stato_cassa = aggiungi_caffe(stato_cassa)
        salva_stato(stato_cassa)  # salviamo subito su file
        aggiorna_display()

    # Funzione per l'importo manuale
    def importo_manuale(soldi_inseriti):
        global stato_cassa
        stato_cassa = addizione(stato_cassa, soldi_inseriti)  # tocca solo la cassa
        salva_stato(stato_cassa)
        aggiorna_display()

    # CREAZIONE BOTTONE
    bottone_caffe = tk.Button(
        frame_pagina1,
        text="+1 Caffè(30cent)",
        command=premi_bottone,
        bg="red",
        fg="white",
        width=13,
        height=2,
        font=("Helvetica", 12, "bold")
        )
    bottone_caffe.pack(pady=20)

    # CREAZIONE LABEL INSERIMENTO MANUALE
    scritta_inserimento = tk.Label(frame_pagina1, text="Inserimento manuale soldi", font=("Helvetica", 14, "bold"))
    scritta_inserimento.pack(pady=8)
    input_importo = tk.Entry(frame_pagina1, width=15)
    input_importo.pack()

    # Funzione per prendere l'importo da tastiera
    def invio_importo(event=None):
        importo_inserito = input_importo.get()  # importo=input
        try:
            soldi_inseriti = float(importo_inserito)  # conversione input da stringa a float
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")  # se non è un numero stampa
            return
        importo_manuale(soldi_inseriti)  # chiamiamo la funzione che aggiorna il display e la cassa
        input_importo.delete(0, tk.END)  # cancella l'input dalla barra

    input_importo.bind('<Return>', invio_importo)  # esegui invio_importo solo se preme invio

    # FUNZIONE PER ANDARE ALLA CASSAFORTE
    def vai_a_cassaforte():
        # Nasconde il frame della prima pagina
        frame_pagina1.pack_forget()
        # Mostra il frame della seconda pagina
        frame_pagina2.pack(fill="both", expand=True)
        bottone_home.pack(pady=20)
        get_saldo()  # Aggiorniamo il saldo della cassaforte

    # CREAZIONE BOTTONE CASSAFORTE
    bottone_cassaforte = tk.Button(
        frame_pagina1,
        text="Vai a cassaforte",
        command=vai_a_cassaforte,
        bg="red",
        fg="white",
        width=13,
        height=2,
        font=("Helvetica", 12, "bold")
    )
    bottone_cassaforte.pack(pady=20)

    # LABEL SOLDI CASSA E CASSAFORTE
    display_cassaforte = tk.Label(frame_pagina2, text="Saldo cassa: 0.00 €", font=("Arial", 12), bg="red")
    display_cassaforte.pack(pady=10)

    # FUNZIONE PER AGGIORNARE SALDO
    def get_saldo():
        global stato_cassa  # prendiamo lo stato cassa
        soldi = stato_cassa["cassa"]
        display_cassaforte.config(text=f"Saldo:{soldi:.2f}€")

    # FUNZIONE PER LA HOME
    def vai_alla_home():
        frame_pagina2.pack_forget()
        frame_pagina1.pack(fill="both", expand=True)
        bottone_home.pack_forget()
        bottone_cassaforte.pack(pady=20)

    # BOTTONE PER TORNARE ALLA HOME
    bottone_home = tk.Button(
        frame_pagina2,
        text="Torna alla home",
        command=vai_alla_home,
        bg="red",
        fg="white",
        width=13,
        height=2,
        font=("Helvetica", 12, "bold")
        )
    bottone_home.pack(pady=20)

    finestra.mainloop()