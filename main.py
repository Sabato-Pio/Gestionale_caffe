from gestione_caffe import aggiungi_caffe
def sottrazione(diminuzione, cassa):
    return cassa - diminuzione

def addizione(aumento, cassa):
    return cassa + aumento


def main():
    cassa = 0.0
    caffe_venduti=0
    menu = """
Scegli un'operazione:
1 - Stampa il saldo
2 - Aggiungi saldo
3 - Togli saldo
4 - Vendi un caffè
0 - Esci
Scelta: """

    while True:
        try:
            # Chiedo la scelta e quella che mi viene data viene anche convertita in int
            scelta_menu = int(input(menu))
            
            if scelta_menu == 1:
                print(f"\nSaldo attuale: {cassa:.2f} €")
                print(f"Caffe venduti: {caffe_venduti} ")
                
            elif scelta_menu == 2:
                aumento = float(input("Inserisci l'importo da aggiungere: "))
                cassa = addizione(aumento, cassa)
                print(f"Aggiunti {aumento:.2f} €. Nuovo saldo: {cassa:.2f} €")
                if cassa > 0.29:
                    modulo=cassa/0.3
                    caffe_venduti=int(modulo)
                print(caffe_venduti)
                
            elif scelta_menu == 3:
                diminuzione = float(input("Inserisci l'importo da togliere: "))
                cassa = sottrazione(diminuzione, cassa)
                print(f"Sottratti {diminuzione:.2f} €. Nuovo saldo: {cassa:.2f} €")
                
            
            elif scelta_menu == 4:
                stato_attuale={"cassa":cassa,"caffe_venduti":caffe_venduti}
                stato_aggiornato = aggiungi_caffe(stato_attuale)
                caffe_venduti=stato_aggiornato["caffe_venduti"]
                cassa=stato_aggiornato["cassa"]
                print(f"Caffè venduto! Saldo: {cassa:.2f} € | Totale caffè: {caffe_venduti}")
                
            elif scelta_menu == 0:
                print("Chiusura cassa in corso...")
                break
                
            else:
                print("Scelta non valida. Riprova.")
                
        except ValueError:
            print("\nErrore: Input non valido. Devi inserire un numero.")

# Questo costrutto avvia il programma solo se viene eseguito direttamente
if __name__ == "__main__":
    main()