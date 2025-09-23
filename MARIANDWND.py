import os
from transformers import MarianMTModel, MarianTokenizer

def scarica_modello(model_name, save_path):
    print(f"Scarico tokenizer: {model_name} → {save_path}")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_path)

    print(f"Scarico modello: {model_name} → {save_path}")
    model = MarianMTModel.from_pretrained(model_name)
    model.save_pretrained(save_path)

    print(f"✅ Modello '{model_name}' salvato in '{save_path}'\n")

def main():
    base_dir = "sigma_nex/core/models/translate"
    os.makedirs(base_dir, exist_ok=True)

    MODELS = {
        "it-en": "Helsinki-NLP/opus-mt-it-en",
        "en-it": "Helsinki-NLP/opus-mt-en-it"
    }

    for subdir, model_ref in MODELS.items():
        path = os.path.join(base_dir, subdir)
        os.makedirs(path, exist_ok=True)
        scarica_modello(model_ref, path)

    print("\nTutti i modelli sono stati scaricati e salvati localmente.")
    print("Percorso finale: sigma_nex/core/models/translate/")

if __name__ == "__main__":
    main()
