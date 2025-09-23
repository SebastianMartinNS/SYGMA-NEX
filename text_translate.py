from transformers import MarianMTModel, MarianTokenizer
it_en_dir = "sigma_nex/core/models/translate/it-en"
tokenizer = MarianTokenizer.from_pretrained(it_en_dir)
model = MarianMTModel.from_pretrained(it_en_dir)
print("Tutto OK: modello e tokenizer caricati.")
