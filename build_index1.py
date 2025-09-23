import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === CONFIGURAZIONI ===
framework_path = "data/Framework_SIGMA.json"
model_path = "sigma_nex/core/models/paraphrase-MiniLM-L6-v2"
index_path = "data/moduli.index"
mapping_path = "data/moduli.mapping.json"

# === 1. VERIFICHE PRELIMINARI ===
if not os.path.exists(framework_path):
    raise FileNotFoundError(f"❌ File framework non trovato: {framework_path}")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Modello locale non trovato: {model_path}\nAssicurati di averlo scaricato correttamente.")

# === 2. CARICA IL FRAMEWORK ===
with open(framework_path, "r", encoding="utf-8") as f:
    framework = json.load(f)

modules = framework.get("modules", [])

if not modules:
    raise ValueError("❌ Nessun modulo trovato nel framework. Verifica la struttura del file JSON.")

# === 3. CARICA IL MODELLO LOCALE ===
print("📦 Caricamento modello locale...")
model = SentenceTransformer(model_path)

# === 4. COSTRUISCI LE FRASI TESTUALI (TEXTS) ===
texts = []
for mod in modules:
    name = mod.get("name", "??")
    desc = mod.get("description", "")
    params = mod.get("parameters", {})

    # Fallback se mancano informazioni
    if not desc:
        desc = "(nessuna descrizione fornita)"
    if not params:
        param_summary = "parametri non specificati"
    else:
        param_summary = ", ".join(params.keys())

    text = f"{name} :: {desc}. Parametri principali: {param_summary}"
    texts.append(text)

# === 5. OTTIENI EMBEDDING VETTORIALI ===
print("🧠 Generazione embedding...")
embeddings = model.encode(texts, convert_to_numpy=True)

# === 6. CREA E SALVA L’INDICE FAISS ===
print("🗂️ Costruzione indice FAISS...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, index_path)

# === 7. SALVA LA MAPPATURA TESTUALE ===
with open(mapping_path, "w", encoding="utf-8") as mf:
    json.dump(texts, mf, ensure_ascii=False, indent=2)

# === 8. RISULTATO ===
print(f"✅ Indice creato con successo: {index_path}")
print(f"📝 Mappatura semantica salvata in: {mapping_path}")