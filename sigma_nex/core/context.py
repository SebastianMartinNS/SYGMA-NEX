# sigma_nex/core/context.py
def build_prompt(
    system_prompt: str, history: list, query: str, retrieval_enabled: bool = True
) -> str:
    """
    Costruisce il prompt finale per SIGMA-NEX unendo:
    - il prompt di sistema (interno, non rivelato)
    - la conoscenza operativa da FAISS (se abilitata)
    - la cronologia della conversazione
    - la nuova domanda dell'utente

    Il system_prompt serve solo a modulare il comportamento del modello,
    ma non deve mai essere esposto nella risposta.
    """
    knowledge = ""
    if retrieval_enabled:
        # Recupera moduli rilevanti tramite FAISS (lazy import and safe fallback)
        try:
            from sigma_nex.core.retriever import search_moduli

            moduli_rilevanti = search_moduli(query, k=3)
        except Exception:
            moduli_rilevanti = []

        for i, mod in enumerate(moduli_rilevanti):
            if isinstance(mod, str):
                parts = mod.split("::", 1)
                if len(parts) == 2:
                    nome, descrizione = parts
                    knowledge += f"\n[MODULO {i+1}: {nome.strip().upper()}]\n"
                    knowledge += f"{descrizione.strip()}\n"
                else:
                    knowledge += f"\n[MODULO {i+1}]\n{mod.strip()}\n"

    # Costruisce la conversazione simulando continuità logica
    conversation = "\n".join(history + [f"Utente: {query}", "Assistant:"])

    # Restituisce il prompt finale completo
    if knowledge:
        return f"{system_prompt.strip()}\n\nContesto:{knowledge}\n\n{conversation}"
    else:
        return f"{system_prompt.strip()}\n\n{conversation}"
