import csv
# funzione per caricare un file
def carica_da_file(file_path):
    lista_libri = []
    # gestione dell'eccezione (FileNotFoundError)
    try:
        file = open(file_path, encoding='utf-8')
        # salto la prima riga del file (contiene solo il numero di sezioni)
        file.readline()
        # lista di dizionari
        for riga in file:
            dizionario = dict()
            campi = riga.rstrip('\n').split(',')
            # popolo il dizionario
            #   divisione chiave - valore
            dizionario['titolo'] = campi[0]
            dizionario['autori'] = campi[1]
            dizionario['anno di pubblicazione'] = campi[2]
            dizionario['pagine'] = campi[3]
            dizionario['numero della sezione'] = campi[4]
            # append per inserire il dizionario nella lista (lista di dizionari)
            lista_libri.append(dizionario)
        # chiudo il file
        file.close()
    except FileNotFoundError:
        print('None')
    return lista_libri


# funzione per aggiungere un libro nella biblioteca
def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    # controllo che il libro appena inserito dall'utente effettivamente NON è presente nel file per poterlo aggiornare
    for dizionario in biblioteca:
        if dizionario['titolo'] == titolo:
            # libro già presente nella biblioteca
            libro = False
            return libro

    # aggiungo al file il nuovo libro implementato (scrittura su file => 'a': modalità APPEND (aggiunge in coda al file))
    file = open(file_path,'a', newline='',encoding='utf-8')
    # creo oggetto writer usando csv
    book = csv.writer(file, delimiter=',')
    # aggiungo i campi inseriti dall'utente nel file csv
    args = [titolo, autore, anno, pagine, sezione]
    book.writerow(args)
    # chiudo il file
    file.close()

    # libro aggiunto con successo alla biblioteca
    libro = True
    return libro


# funzione per cercare un libro all'interno della biblioteca conoscendo il titolo
def cerca_libro(biblioteca, titolo):
    trovato = False
    for dizionario in biblioteca:
        if dizionario['titolo'] == titolo:
            trovato = True
    return (trovato, titolo)


# funzione per elenco dei libri divisi per sezione
def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    titoli = []
    try:
        for dizionario in biblioteca:
            if int(dizionario['numero della sezione']) == sezione:
                titoli.append(dizionario['titolo'])
    except:
        print('None')
    return titoli


# funzione principale
def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        # stampa del menu per permettere all'utente di scegliere cosa fare
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        # richiesta all'utente su quale scelta fare
        scelta = input("Scegli un'opzione >> ").strip()

# GESTIONE DELLE SCELTE DELL'UTENTE
#   caricare biblioteca dal file
        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

#   aggiungere un nuovo libro
        elif scelta == "2":
            # controllo sempre che la biblioteca sia già stata gestita
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            # richiesta del titolo e dell'autore del libro che l'utente vuole implementare
            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            # controllo sulle potenziali eccezioni
            try:
                # richiesta dei campi aggiuntivi
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

#   cercare un libro conoscendo il titolo
        elif scelta == "3":
            # in assenza di una biblioteca settata, il programma restituisce l'output suggerendo all'utente di inizializzarla
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            # richiesta all'utente del titolo
            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            (risultato, title) = cerca_libro(biblioteca, titolo)
            if risultato is True:
                print(f"Libro trovato: {title}")
            else:
                print("Libro non trovato.")

#   ordinare i titoli di una sezione
        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            # controllo se il numero inserito dall'utente è nel range della biblioteca
            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            # richiamo della funzione
            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)

            # analisi della lista restituita dalla funzione
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

# uscita dell'utente dal programma
        elif scelta == "5":
            print("Uscita dal programma...")
            break

        # in caso di input errato, viene restituito un messaggio
        else:
            print("Opzione non valida. Riprova.")
if __name__ == "__main__":
    main()