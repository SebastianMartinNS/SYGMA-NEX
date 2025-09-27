# sigma_nex/core/context.py
def optimize_history(history: list, max_length: int = 4000, max_entries: int = 10) -> list:
    """
    Optimize conversation history by reducing length and keeping most relevant parts.

    Args:
        history: List of conversation history
        max_length: Maximum total character length
        max_entries: Maximum number of history entries

    Returns:
        Optimized history list
    """
    if not history:
        return []

    # First, limit by number of entries (keep most recent)
    if len(history) > max_entries:
        history = history[-max_entries:]

    # Then, limit by total length
    total_length = sum(len(str(entry)) for entry in history)

    if total_length <= max_length:
        return history

    # Remove entries from the beginning until we're under limit
    optimized = history[:]
    while optimized and sum(len(str(entry)) for entry in optimized) > max_length:
        optimized.pop(0)

    # Ensure we keep at least the last entry
    if not optimized and history:
        optimized = [history[-1]]

    return optimized


def build_prompt(system_prompt: str, history: list, query: str, retrieval_enabled: bool = True) -> str:
    """
    Costruisce il prompt finale per SIGMA-NEX unendo:
    - il prompt di sistema (interno, non rivelato)
    - la conoscenza operativa da FAISS (se abilitata)
    - la cronologia della conversazione ottimizzata
    - la nuova domanda dell'utente

    Il system_prompt serve solo a modulare il comportamento del modello,
    ma non deve mai essere esposto nella risposta.
    """
    # Optimize history first to prevent context overflow
    optimized_history = optimize_history(history)

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
    conversation = "\n".join(optimized_history + [f"Utente: {query}", "Assistant:"])

    # Restituisce il prompt finale completo
    if knowledge:
        return f"{system_prompt.strip()}\n\nContesto:{knowledge}\n\n{conversation}"
    else:
        return f"{system_prompt.strip()}\n\n{conversation}"
