import customtkinter as ctk
from gestione_caffe import (
    aggiungi_caffe,
    aggiungi_n_caffe,
    addizione,
    trasferisci_a_cassaforte,
    trasferisci_a_cassa,
    preleva_da_cassaforte,
    carica_stato,
    salva_stato,
    crea_snapshot,
    annulla_ultima_operazione,
)

# Numero massimo di operazioni "annullabili" con il bottone di undo.
MAX_CRONOLOGIA = 2

# --- PALETTE "COFFEE SHOP" ---
# marrone caffè per i bottoni principali, crema per lo sfondo, ambra per
# l'undo: un tocco un po' più curato senza esagerare con i colori.
COLORE_SFONDO = "#F5EFE6"
COLORE_SIDEBAR = "#3E2723"
COLORE_CARD = "#FFFFFF"
COLORE_TESTO = "#3E2723"
COLORE_TESTO_CHIARO = "#F5EFE6"
COLORE_BOTTONE = "#6F4E37"
COLORE_BOTTONE_HOVER = "#5A3D2B"
COLORE_ACCENTO = "#C9A227"
COLORE_ACCENTO_HOVER = "#A9871E"
COLORE_NAV = "#5D4037"
COLORE_NAV_HOVER = "#4E342E"

ctk.set_appearance_mode("light")


def avvia_gui():
    global stato_cassa, cronologia_stati
    stato_cassa = carica_stato()  # carica (o crea) dati.json all'avvio
    cronologia_stati = []  # cronologia degli stati precedenti, per l'undo (si azzera ad ogni avvio)

    finestra = ctk.CTk()
    finestra.title("Gestione caffè di MR.S")
    finestra.geometry("950x650")
    finestra.configure(fg_color=COLORE_SFONDO)

    # -----------------------------------------------------------------
    # SIDEBAR: navigazione tra le pagine + bottone di undo (sempre visibile)
    # -----------------------------------------------------------------
    sidebar = ctk.CTkFrame(finestra, width=210, corner_radius=0, fg_color=COLORE_SIDEBAR)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)  # non farla restringere in base al contenuto

    titolo_sidebar = ctk.CTkLabel(
        sidebar, text="☕ MR.S", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORE_TESTO_CHIARO
    )
    titolo_sidebar.pack(pady=(30, 40))

    # -----------------------------------------------------------------
    # AREA PRINCIPALE: contiene le due pagine (cassa / cassaforte), una
    # nascosta e una visibile alla volta, come nella versione precedente
    # -----------------------------------------------------------------
    area_principale = ctk.CTkFrame(finestra, fg_color=COLORE_SFONDO, corner_radius=0)
    area_principale.pack(side="left", fill="both", expand=True, padx=24, pady=24)

    pagina_cassa = ctk.CTkFrame(area_principale, fg_color=COLORE_SFONDO)
    pagina_cassaforte = ctk.CTkFrame(area_principale, fg_color=COLORE_SFONDO)
    pagina_cassa.pack(fill="both", expand=True)

    # -----------------------------------------------------------------
    # Helper: crea una "card" con angoli arrotondati e un titolo, usata
    # per raggruppare ogni funzionalità (vendita caffè, donazioni, ecc.)
    # -----------------------------------------------------------------
    def crea_card(padre, titolo):
        card = ctk.CTkFrame(padre, corner_radius=18, fg_color=COLORE_CARD)
        card.pack(fill="x", pady=(0, 16))
        card.grid_columnconfigure(0, weight=1)

        etichetta_titolo = ctk.CTkLabel(
            card, text=titolo, font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORE_TESTO
        )
        etichetta_titolo.grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(16, 4))
        return card

    # ===================================================================
    # PAGINA CASSA
    # ===================================================================
    titolo_pagina_cassa = ctk.CTkLabel(
        pagina_cassa, text="Cassa", font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORE_TESTO
    )
    titolo_pagina_cassa.pack(anchor="w", pady=(0, 16))

    # --- Card riepilogo ---
    card_riepilogo = crea_card(pagina_cassa, "Riepilogo")

    ctk.CTkLabel(card_riepilogo, text="Saldo cassa", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=6)
    valore_saldo = ctk.CTkLabel(card_riepilogo, text="", font=ctk.CTkFont(weight="bold"), text_color=COLORE_TESTO)
    valore_saldo.grid(row=1, column=1, columnspan=2, sticky="e", padx=18, pady=6)

    ctk.CTkLabel(card_riepilogo, text="Caffè venduti oggi", text_color=COLORE_TESTO, anchor="w").grid(
        row=2, column=0, sticky="w", padx=18, pady=6)
    valore_oggi = ctk.CTkLabel(card_riepilogo, text="", font=ctk.CTkFont(weight="bold"), text_color=COLORE_TESTO)
    valore_oggi.grid(row=2, column=1, columnspan=2, sticky="e", padx=18, pady=6)

    ctk.CTkLabel(card_riepilogo, text="Caffè venduti totali", text_color=COLORE_TESTO, anchor="w").grid(
        row=3, column=0, sticky="w", padx=18, pady=(6, 18))
    valore_totali = ctk.CTkLabel(card_riepilogo, text="", font=ctk.CTkFont(weight="bold"), text_color=COLORE_TESTO)
    valore_totali.grid(row=3, column=1, columnspan=2, sticky="e", padx=18, pady=(6, 18))

    # funzione unica per aggiornare tutte le etichette del riepilogo cassa
    def aggiorna_display():
        valore_saldo.configure(text=f"{stato_cassa['cassa']:.2f} €")
        valore_oggi.configure(text=str(stato_cassa['caffe_venduti_oggi']))
        valore_totali.configure(text=str(stato_cassa['caffe_venduti_totali']))

    aggiorna_display()

    # mette da parte una fotografia dello stato attuale PRIMA di un'operazione,
    # così se serve annullare (undo) si può tornare indietro a questo punto
    def salva_snapshot():
        cronologia_stati.append(crea_snapshot(stato_cassa))
        if len(cronologia_stati) > MAX_CRONOLOGIA:
            cronologia_stati.pop(0)

    # --- Card vendita caffè ---
    card_vendita = crea_card(pagina_cassa, "Vendita caffè")

    ctk.CTkLabel(card_vendita, text="Un caffè alla volta (0.30€)", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=10)

    def premi_bottone():
        global stato_cassa
        salva_snapshot()
        stato_cassa = aggiungi_caffe(stato_cassa)
        salva_stato(stato_cassa)  # salviamo subito su file
        aggiorna_display()

    ctk.CTkButton(
        card_vendita, text="+1 ☕", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=premi_bottone
    ).grid(row=1, column=1, columnspan=2, sticky="e", padx=18, pady=10)

    ctk.CTkLabel(card_vendita, text="Più caffè insieme (quantità)", text_color=COLORE_TESTO, anchor="w").grid(
        row=2, column=0, sticky="w", padx=18, pady=(6, 18))

    input_n_caffe = ctk.CTkEntry(card_vendita, width=90, corner_radius=10, placeholder_text="es. 3")
    input_n_caffe.grid(row=2, column=1, sticky="e", padx=(0, 8), pady=(6, 18))

    def invio_n_caffe(event=None):
        n_inserito = input_n_caffe.get()
        try:
            n = int(n_inserito)  # deve essere un numero intero di caffè, non ha senso "2.5 caffè"
        except ValueError:
            print("Errore: devi inserire un numero intero valido!")
            return
        if n <= 0:
            print("Errore: il numero di caffè deve essere positivo!")
            return

        global stato_cassa
        salva_snapshot()
        stato_cassa = aggiungi_n_caffe(stato_cassa, n)
        salva_stato(stato_cassa)
        aggiorna_display()
        input_n_caffe.delete(0, "end")

    input_n_caffe.bind('<Return>', invio_n_caffe)

    ctk.CTkButton(
        card_vendita, text="Conferma", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=invio_n_caffe
    ).grid(row=2, column=2, sticky="e", padx=18, pady=(6, 18))

    # --- Card donazioni ---
    card_donazioni = crea_card(pagina_cassa, "Donazioni")

    ctk.CTkLabel(card_donazioni, text="Importo (€)", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=(10, 18))

    input_importo = ctk.CTkEntry(card_donazioni, width=90, corner_radius=10, placeholder_text="es. 5.00")
    input_importo.grid(row=1, column=1, sticky="e", padx=(0, 8), pady=(10, 18))

    def importo_manuale(soldi_inseriti):
        global stato_cassa
        salva_snapshot()
        stato_cassa = addizione(stato_cassa, soldi_inseriti)  # tocca solo la cassa
        salva_stato(stato_cassa)
        aggiorna_display()

    def invio_importo(event=None):
        importo_inserito = input_importo.get()
        try:
            soldi_inseriti = float(importo_inserito)
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")
            return
        importo_manuale(soldi_inseriti)
        input_importo.delete(0, "end")

    input_importo.bind('<Return>', invio_importo)

    ctk.CTkButton(
        card_donazioni, text="Aggiungi", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=invio_importo
    ).grid(row=1, column=2, sticky="e", padx=18, pady=(10, 18))

    # --- Card trasferimento a cassaforte ---
    card_trasferimento = crea_card(pagina_cassa, "Trasferisci alla cassaforte")

    ctk.CTkLabel(card_trasferimento, text="Importo (€)", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=(10, 18))

    input_trasferisci = ctk.CTkEntry(card_trasferimento, width=90, corner_radius=10, placeholder_text="es. 10.00")
    input_trasferisci.grid(row=1, column=1, sticky="e", padx=(0, 8), pady=(10, 18))

    def scambio_cassaforte(event=None):
        importo_inserito = input_trasferisci.get()
        try:
            soldi_inseriti = float(importo_inserito)
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")
            return

        global stato_cassa
        salva_snapshot()
        stato_cassa, riuscito = trasferisci_a_cassaforte(stato_cassa, soldi_inseriti)
        if not riuscito:
            cronologia_stati.pop()  # operazione non riuscita, togliamo lo snapshot inutile
            print("Errore: importo non valido o superiore ai soldi disponibili in cassa!")
            return

        salva_stato(stato_cassa)
        aggiorna_display()
        input_trasferisci.delete(0, "end")

    input_trasferisci.bind('<Return>', scambio_cassaforte)

    ctk.CTkButton(
        card_trasferimento, text="Trasferisci", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=scambio_cassaforte
    ).grid(row=1, column=2, sticky="e", padx=18, pady=(10, 18))

    # ===================================================================
    # PAGINA CASSAFORTE
    # ===================================================================
    titolo_pagina_cassaforte = ctk.CTkLabel(
        pagina_cassaforte, text="Cassaforte", font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORE_TESTO
    )
    titolo_pagina_cassaforte.pack(anchor="w", pady=(0, 16))

    # --- Card riepilogo cassaforte ---
    card_riepilogo_cassaforte = crea_card(pagina_cassaforte, "Riepilogo")

    ctk.CTkLabel(card_riepilogo_cassaforte, text="Saldo cassaforte", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=6)
    valore_saldo_cassaforte = ctk.CTkLabel(card_riepilogo_cassaforte, text="", font=ctk.CTkFont(weight="bold"), text_color=COLORE_TESTO)
    valore_saldo_cassaforte.grid(row=1, column=1, columnspan=2, sticky="e", padx=18, pady=6)

    ctk.CTkLabel(card_riepilogo_cassaforte, text="Cassa rimasta", text_color=COLORE_TESTO, anchor="w").grid(
        row=2, column=0, sticky="w", padx=18, pady=(6, 18))
    valore_cassa_rimasta = ctk.CTkLabel(card_riepilogo_cassaforte, text="", font=ctk.CTkFont(weight="bold"), text_color=COLORE_TESTO)
    valore_cassa_rimasta.grid(row=2, column=1, columnspan=2, sticky="e", padx=18, pady=(6, 18))

    def get_saldo():
        valore_saldo_cassaforte.configure(text=f"{stato_cassa['cassaforte']:.2f} €")
        valore_cassa_rimasta.configure(text=f"{stato_cassa['cassa']:.2f} €")

    # --- Card trasferimento a cassa ---
    card_trasferimento_cassa = crea_card(pagina_cassaforte, "Trasferisci alla cassa")

    ctk.CTkLabel(card_trasferimento_cassa, text="Importo (€)", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=(10, 18))

    input_trasferisci_cassa = ctk.CTkEntry(card_trasferimento_cassa, width=90, corner_radius=10, placeholder_text="es. 10.00")
    input_trasferisci_cassa.grid(row=1, column=1, sticky="e", padx=(0, 8), pady=(10, 18))

    def scambio_cassa(event=None):
        importo_inserito = input_trasferisci_cassa.get()
        try:
            soldi_inseriti = float(importo_inserito)
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")
            return

        global stato_cassa
        salva_snapshot()
        stato_cassa, riuscito = trasferisci_a_cassa(stato_cassa, soldi_inseriti)
        if not riuscito:
            cronologia_stati.pop()  # operazione non riuscita, togliamo lo snapshot inutile
            print("Errore: importo non valido o superiore ai soldi disponibili in cassaforte!")
            return

        salva_stato(stato_cassa)
        aggiorna_display()
        get_saldo()
        input_trasferisci_cassa.delete(0, "end")

    input_trasferisci_cassa.bind('<Return>', scambio_cassa)

    ctk.CTkButton(
        card_trasferimento_cassa, text="Trasferisci", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=scambio_cassa
    ).grid(row=1, column=2, sticky="e", padx=18, pady=(10, 18))

    # --- Card prelievo dalla cassaforte ---
    card_prelievo = crea_card(pagina_cassaforte, "Preleva dalla cassaforte")

    ctk.CTkLabel(card_prelievo, text="Importo (€)", text_color=COLORE_TESTO, anchor="w").grid(
        row=1, column=0, sticky="w", padx=18, pady=(10, 18))

    input_prelievo = ctk.CTkEntry(card_prelievo, width=90, corner_radius=10, placeholder_text="es. 5.00")
    input_prelievo.grid(row=1, column=1, sticky="e", padx=(0, 8), pady=(10, 18))

    def invio_prelievo(event=None):
        importo_inserito = input_prelievo.get()
        try:
            soldi_inseriti = float(importo_inserito)
        except ValueError:
            print("Errore: devi inserire un importo numerico valido!")
            return

        global stato_cassa
        salva_snapshot()
        stato_cassa, riuscito = preleva_da_cassaforte(stato_cassa, soldi_inseriti)
        if not riuscito:
            cronologia_stati.pop()  # operazione non riuscita, togliamo lo snapshot inutile
            print("Errore: importo non valido o superiore ai soldi disponibili in cassaforte!")
            return

        salva_stato(stato_cassa)
        aggiorna_display()
        get_saldo()
        input_prelievo.delete(0, "end")

    input_prelievo.bind('<Return>', invio_prelievo)

    ctk.CTkButton(
        card_prelievo, text="Preleva", width=90, corner_radius=10,
        fg_color=COLORE_BOTTONE, hover_color=COLORE_BOTTONE_HOVER, command=invio_prelievo
    ).grid(row=1, column=2, sticky="e", padx=18, pady=(10, 18))

    # ===================================================================
    # NAVIGAZIONE (bottoni nella sidebar)
    # ===================================================================
    def vai_a_cassa():
        pagina_cassaforte.pack_forget()
        pagina_cassa.pack(fill="both", expand=True)
        aggiorna_display()

    def vai_a_cassaforte():
        pagina_cassa.pack_forget()
        pagina_cassaforte.pack(fill="both", expand=True)
        get_saldo()

    ctk.CTkButton(
        sidebar, text="🏠  Cassa", command=vai_a_cassa,
        fg_color=COLORE_NAV, hover_color=COLORE_NAV_HOVER,
        corner_radius=10, width=170, height=40, anchor="w"
    ).pack(pady=6, padx=20)

    ctk.CTkButton(
        sidebar, text="🔒  Cassaforte", command=vai_a_cassaforte,
        fg_color=COLORE_NAV, hover_color=COLORE_NAV_HOVER,
        corner_radius=10, width=170, height=40, anchor="w"
    ).pack(pady=6, padx=20)

    # ===================================================================
    # ANNULLA ULTIMA OPERAZIONE (bottone di undo, sempre visibile in sidebar)
    # ===================================================================
    def annulla_operazione():
        global stato_cassa
        stato_ripristinato, riuscito = annulla_ultima_operazione(cronologia_stati)
        if not riuscito:
            print("Errore: non c'è nessuna operazione da annullare!")
            return
        stato_cassa = stato_ripristinato
        salva_stato(stato_cassa)
        aggiorna_display()
        get_saldo()  # aggiorna anche il saldo cassaforte, se è già stato mostrato

    ctk.CTkButton(
        sidebar, text="↩  Annulla ultima\n     operazione", command=annulla_operazione,
        fg_color=COLORE_ACCENTO, hover_color=COLORE_ACCENTO_HOVER, text_color=COLORE_TESTO,
        corner_radius=10, width=170, height=50, anchor="w", font=ctk.CTkFont(size=12)
    ).pack(side="bottom", pady=30, padx=20)

    finestra.mainloop()