import tkinter as tk
from gestione_caffe import aggiungi_caffe
from gestione_caffe import aggiorna_caffe
from gestione_caffe import addizione

stato_cassa={
    "cassa":0.0,
    "cassaforte":0.0,
    "caffe_venduti":0
}

def avvia_gui():
    finestra=tk.Tk()
    finestra.title("Gestione caffè di MR.S")
    finestra.geometry("720x400")
    frame_pagina1 = tk.Frame(finestra)
    frame_pagina1.pack(fill="both", expand=True)

    frame_pagina2 = tk.Frame(finestra, bg="grey")

    testo_benvenuto=tk.Label(frame_pagina1,text="Benvenuto nel gestionale di MR.S!")
    testo_benvenuto.pack(pady=20)# aggiunge del margine

    # Display soldi e caffè
    display_saldo = tk.Label(frame_pagina1, text="Saldo: 0.00 € | Caffè: 0", font=("Arial", 12))
    display_saldo.pack(pady=10)
    
    #funzione che indica come funziona il bottone per i caffè
    def premi_bottone():
        global stato_cassa #prendiamo lo stato cassa
        stato_cassa=aggiungi_caffe(stato_cassa) #aggiungiamo 30 centesimi in cassa e un caffe, chiamando la funzione aggiungi caffe

    #aggiorniamo le variabili da mostrare
        nuovi_soldi=stato_cassa["cassa"] 
        nuovi_caffe=stato_cassa["caffe_venduti"]
    #mostriamo le variabili
        display_saldo.config(text=f"Saldo:{nuovi_soldi:.2f}€|Caffè: {nuovi_caffe}")
    
#Funzione per l'importo manuale
    def importo_manuale(soldi_inseriti):
        global stato_cassa #prendiamo lo stato cassa
        stato_cassa=addizione(stato_cassa,soldi_inseriti) #facciamo la somma tra i soldi inseriti e quelli in cassa
        nuovi_caffe=aggiorna_caffe(stato_cassa) # aggiorniamo il numero di caffè ricalcolandoli(avrà problemi con la scrittura su file)

        nuovi_soldi=stato_cassa["cassa"] #aggiorna la variabile cassa per il display
        nuovi_caffe=stato_cassa["caffe_venduti"]#aggiorna la variabile caffe per il display
        
        display_saldo.config(text=f"Saldo:{nuovi_soldi:.2f}€|Caffè: {nuovi_caffe}")#aggiorna il display

# CREAZIONE BOTTONE
    bottone_caffe=tk.Button(
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
    scritta_inserimento=tk.Label(frame_pagina1, text="Inserimento manuale soldi", font=("Helvetica",14,"bold"))
    scritta_inserimento.pack(pady=8)
# CREAZIONE INSERIMENTO MANUALE
    input_importo = tk.Entry(frame_pagina1,width=15)
    input_importo.pack()
# Funzione per prendere l'importo da tastiera
    def invio_importo(event=None):
        importo_inserito = input_importo.get() # importo=input
        try:
            soldi_inseriti = float(importo_inserito) #conversione input da stringa a float
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")# se non è un numero stampa
            return
        importo_manuale(soldi_inseriti) #chiamiamo la funzione che aggiorna il display e la cassa
        input_importo.delete(0, tk.END) #cancella l input dalla barra

    input_importo.bind('<Return>', invio_importo) #esegui invio_importo solo se preme invio

    #FUNZIONE PER ANDARE ALLA CASSAFORTE
    def vai_a_cassaforte():
    # Nasconde il frame della prima pagina
        frame_pagina1.pack_forget()
    # Mostra il frame della seconda pagina
        frame_pagina2.pack(fill="both", expand=True)
        bottone_cassaforte.pack_forget
        bottone_home.pack(pady=20)
        get_saldo() #Aggiorniamo il saldo della cassaforte

# CREAZIONE BOTTONE CASSAFORTE
    bottone_cassaforte=tk.Button(
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
    display_cassaforte = tk.Label(frame_pagina2, text="Saldo cassa: 0.00 €", font=("Arial", 12),bg="red")
    display_cassaforte.pack(pady=10)

    #FUNZIONE PER AGGIORNARE SALDO
    def get_saldo():
        global stato_cassa #prendiamo lo stato cassa
    #aggiorniamo le variabili da mostrare
        soldi=stato_cassa["cassa"] 
    #mostriamo le variabili
        display_cassaforte.config(text=f"Saldo:{soldi:.2f}€")

    #FUNZIONE PER LA HOME
    def vai_alla_home():
        frame_pagina2.pack_forget()
        frame_pagina1.pack(fill="both", expand=True)
        bottone_home.pack_forget()
        bottone_cassaforte.pack(pady=20)
    #BOTTONE PER TORNARE ALLA HOME
    bottone_home=tk.Button(
        frame_pagina2,
        text="Torna alla home",
        command=vai_alla_home,
        bg="red",
        fg="white",
        width=13,
        height=2,
        font=("Helvetica",12,"bold")
        )
    bottone_home.pack(pady=20)

    finestra.mainloop()