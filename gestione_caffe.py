#aggiunge 30 cent in cassa e 1 caffe al conteggio
def aggiungi_caffe(stato):
    stato["cassa"]+=0.3
    stato["caffe_venduti"]+=1
    return stato

#calcola quanti caffè sono stati venduti sapendo che costa 30 centesimi
def aggiorna_caffe(stato):
    modulo=stato["cassa"]/0.3
    stato["caffe_venduti"]=int(modulo)
    return stato["caffe_venduti"]

#fa l'addizione tra la cassa e l'aumento dato in input
def addizione(stato, aumento):
    stato["cassa"] += aumento
    return stato

