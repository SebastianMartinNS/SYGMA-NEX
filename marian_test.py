from transformers import MarianMTModel, MarianTokenizer

# Percorsi ai modelli locali
it_en_dir = "sigma_nex/core/models/translate/it-en"
en_it_dir = "sigma_nex/core/models/translate/en-it"

# Carica i modelli
it_en_tokenizer = MarianTokenizer.from_pretrained(it_en_dir)
it_en_model = MarianMTModel.from_pretrained(it_en_dir)

en_it_tokenizer = MarianTokenizer.from_pretrained(en_it_dir)
en_it_model = MarianMTModel.from_pretrained(en_it_dir)

def translate_it_to_en(text):
    batch = it_en_tokenizer([text], return_tensors="pt", padding=True)
    gen = it_en_model.generate(**batch)
    return it_en_tokenizer.batch_decode(gen, skip_special_tokens=True)[0]

def translate_en_to_it(text):
    batch = en_it_tokenizer([text], return_tensors="pt", padding=True)
    gen = en_it_model.generate(**batch)
    return en_it_tokenizer.batch_decode(gen, skip_special_tokens=True)[0]

def main():
    print("\n=== TRADUTTORE INTERATTIVO ITA <-> ENG ===")
    print("Digita '0' per uscire.\n")

    while True:
        print("Scegli direzione:")
        print("1: Italiano → Inglese")
        print("2: Inglese → Italiano")
        scelta = input("Seleziona (1/2/0): ").strip()
        if scelta == "0":
            print("Uscita.")
            break
        elif scelta == "1":
            testo = input("\nInserisci testo in italiano:\n> ")
            tradotto = translate_it_to_en(testo)
            print("\n[Traduzione in inglese]:\n", tradotto)
        elif scelta == "2":
            testo = input("\nEnter text in English:\n> ")
            tradotto = translate_en_to_it(testo)
            print("\n[Traduzione in italiano]:\n", tradotto)
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()
