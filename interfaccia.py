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

    testo_benvenuto=tk.Label(finestra,text="Benvenuto nel gestionale di MR.S!")
    testo_benvenuto.pack(pady=20)# aggiunge del margine

    # Display soldi e caffè
    display_saldo = tk.Label(finestra, text="Saldo: 0.00 € | Caffè: 0", font=("Arial", 12))
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
        finestra,
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
    scritta_inserimento=tk.Label(finestra, text="Inserimento manuale soldi", font=("Helvetica",14,"bold"))
    scritta_inserimento.pack(pady=8)
# CREAZIONE INSERIMENTO MANUALE
    input_importo = tk.Entry(finestra,width=15)
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

    
    finestra.mainloop()
