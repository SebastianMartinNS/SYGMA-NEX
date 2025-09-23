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

# Supporta sia "modules" che "moduli" come campo JSON
modules = framework.get("modules") or framework.get("moduli") or []

if not modules:
    raise ValueError("❌ Nessun modulo trovato nel framework. Verifica la struttura del file JSON.")

# === 3. CARICA IL MODELLO LOCALE ===
print("📦 Caricamento modello locale...")
model = SentenceTransformer(model_path)

# === 4. COSTRUISCI LE FRASI TESTUALI (TEXTS) ===
texts = []
for mod in modules:
    nome = mod.get("nome") or mod.get("name") or "??"
    descrizione = mod.get("descrizione") or mod.get("description") or "(nessuna descrizione fornita)"
    comandi = mod.get("comandi") or mod.get("parameters") or {}

    if isinstance(comandi, dict):
        param_summary = ", ".join(comandi.keys()) if comandi else "parametri non specificati"
    elif isinstance(comandi, list):
        param_summary = f"{len(comandi)} istruzioni"
    else:
        param_summary = "parametri non specificati"

    text = f"{nome.strip()} :: {descrizione.strip()}. Parametri principali: {param_summary}"
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