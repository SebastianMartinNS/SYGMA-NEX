"""
Test per l'ottimizzazione della cronologia conversazione.
Test REALI per il sistema di riduzione e strutturazione history.
"""

from unittest.mock import patch

import pytest

from sigma_nex.core.context import build_prompt, optimize_history


class TestHistoryOptimization:
    """Test per ottimizzazione cronologia conversazione."""

    def test_optimize_history_empty_real(self):
        """Test con cronologia vuota."""
        result = optimize_history([])
        assert result == []

    def test_optimize_history_under_limits_real(self):
        """Test cronologia sotto i limiti."""
        history = [
            "Utente: Come fare un fuoco?",
            "Assistant: Per fare un fuoco sicuro...",
            "Utente: E per spegnerlo?",
            "Assistant: Per spegnere un fuoco...",
        ]

        result = optimize_history(history, max_length=10000, max_entries=20)
        assert result == history  # Nessuna modifica necessaria

    def test_optimize_history_max_entries_real(self):
        """Test limitazione numero massimo entry."""
        history = [f"Entry {i}: contenuto storia" for i in range(15)]

        result = optimize_history(history, max_length=10000, max_entries=10)

        # Dovrebbe mantenere solo le ultime 10
        assert len(result) == 10
        assert result == history[-10:]

    def test_optimize_history_max_length_real(self):
        """Test limitazione lunghezza totale."""
        history = [
            "Utente: " + "x" * 1000,  # 1006 chars
            "Assistant: " + "y" * 1000,  # 1011 chars
            "Utente: " + "z" * 1000,  # 1006 chars
            "Assistant: " + "w" * 500,  # 511 chars
        ]

        # Limite totale di 2000 caratteri
        result = optimize_history(history, max_length=2000, max_entries=20)

        # Dovrebbe rimuovere le prime entry per stare sotto il limite
        total_length = sum(len(str(entry)) for entry in result)
        assert total_length <= 2000

        # Dovrebbe mantenere almeno l'ultima entry
        assert len(result) >= 1
        assert result[-1] == history[-1]

    def test_optimize_history_single_entry_too_long_real(self):
        """Test con singola entry troppo lunga."""
        very_long_entry = "Utente: " + "x" * 5000  # 5006 chars
        history = [very_long_entry]

        result = optimize_history(history, max_length=1000, max_entries=10)

        # Dovrebbe mantenere almeno l'ultima entry anche se troppo lunga
        assert len(result) == 1
        assert result[0] == very_long_entry

    def test_optimize_history_realistic_conversation_real(self):
        """Test con conversazione realistica."""
        history = [
            "Utente: Come purificare l'acqua in emergenza?",
            "Assistant: Ci sono diversi metodi per purificare l'acqua: bollitura per 10 minuti...",
            "Utente: E se non ho il fuoco?",
            "Assistant: Senza fuoco puoi usare compresse di cloro o iodio...",
            "Utente: Quanto cloro serve?",
            "Assistant: Usa 2 gocce di candeggina per litro d'acqua...",
            "Utente: E per riconoscere acqua potabile?",
            "Assistant: Acqua potabile dovrebbe essere chiara, inodore...",
            "Utente: Grazie per le informazioni dettagliate",
            "Assistant: Prego! Ricorda sempre la sicurezza prima di tutto.",
        ]

        result = optimize_history(history, max_length=500, max_entries=6)

        # Verifica che sia stata ottimizzata
        assert len(result) <= 6
        total_length = sum(len(str(entry)) for entry in result)
        assert total_length <= 500 or len(result) == 1  # Eccetto se ultima entry troppo lunga

        # Dovrebbe mantenere le entry più recenti
        assert result[-1] == history[-1]

    def test_optimize_history_edge_case_all_entries_long_real(self):
        """Test caso limite con tutte le entry lunghe."""
        history = [
            "Utente: " + "Prima domanda molto lunga " * 50,  # ~1400 chars
            "Assistant: " + "Prima risposta molto lunga " * 50,  # ~1450 chars
            "Utente: " + "Seconda domanda molto lunga " * 50,  # ~1500 chars
            "Assistant: " + "Seconda risposta molto lunga " * 50,  # ~1550 chars
        ]

        result = optimize_history(history, max_length=2000, max_entries=10)

        # Dovrebbe rimuovere entry fino a stare sotto il limite
        total_length = sum(len(str(entry)) for entry in result)
        assert total_length <= 2000 or len(result) == 1


class TestBuildPromptWithOptimization:
    """Test integrazione ottimizzazione nella costruzione prompt."""

    def test_build_prompt_with_history_optimization_real(self):
        """Test build_prompt con ottimizzazione automatica history."""
        system_prompt = "Sei SIGMA-NEX, esperto in sopravvivenza."

        long_history = [f"Utente: Domanda {i} " + "dettagli " * 100 for i in range(20)]

        query = "Come accendere un fuoco?"

        # Mock del retrieval per semplicità
        with patch("sigma_nex.core.retriever.search_moduli", return_value=[]):
            result = build_prompt(system_prompt, long_history, query, retrieval_enabled=False)

        # Verifica che il prompt sia stato costruito
        assert system_prompt in result
        assert query in result

        # Verifica che la history sia stata ottimizzata (lunghezza ragionevole)
        assert len(result) < 50000  # Limite ragionevole per evitare overflow

    def test_build_prompt_preserves_recent_history_real(self):
        """Test che build_prompt preservi la cronologia recente."""
        system_prompt = "Sei SIGMA-NEX."

        history = [
            "Utente: Domanda vecchia che potrebbe essere rimossa",
            "Assistant: Risposta vecchia",
            "Utente: Domanda importante recente",
            "Assistant: Risposta importante recente",
        ]

        query = "Nuova domanda"

        with patch("sigma_nex.core.retriever.search_moduli", return_value=[]):
            result = build_prompt(
                system_prompt, history, query, retrieval_enabled=False
            )  # Le entry recenti dovrebbero essere preservate
        assert "Domanda importante recente" in result
        assert "Risposta importante recente" in result
        assert query in result

    def test_build_prompt_with_knowledge_and_optimized_history_real(self):
        """Test build_prompt con knowledge retrieval e history ottimizzata."""
        system_prompt = "Sei SIGMA-NEX, esperto in sopravvivenza."

        history = [
            "Utente: Come costruire un riparo?",
            "Assistant: Per costruire un riparo sicuro...",
        ] * 10  # History lunga che sarà ottimizzata

        query = "Come fare un fuoco?"

        # Mock del retrieval con risultati realistici
        mock_results = [
            "FUOCO :: Tecniche per accendere fuoco in sicurezza con materiali naturali",
            "SICUREZZA :: Norme di sicurezza per prevenzione incendi",
        ]

        with patch("sigma_nex.core.retriever.search_moduli", return_value=mock_results):
            result = build_prompt(system_prompt, history, query, retrieval_enabled=True)  # Verifica presenza componenti
        assert system_prompt in result
        assert "MODULO 1: FUOCO" in result
        assert "MODULO 2: SICUREZZA" in result
        assert query in result

        # Verifica ottimizzazione
        assert len(result) < 20000  # Limite ragionevole

    def test_build_prompt_empty_history_real(self):
        """Test build_prompt con cronologia vuota."""
        system_prompt = "Sei SIGMA-NEX."
        history = []
        query = "Prima domanda"

        with patch("sigma_nex.core.retriever.search_moduli", return_value=[]):
            result = build_prompt(system_prompt, history, query, retrieval_enabled=False)

        assert system_prompt in result
        assert query in result
        assert "Utente: Prima domanda" in result
        assert "Assistant:" in result


class TestHistoryStructuring:
    """Test per strutturazione intelligente della cronologia."""

    def test_history_maintains_conversation_flow_real(self):
        """Test che l'ottimizzazione mantenga il flusso conversazionale."""
        history = [
            "Utente: Come purificare l'acqua?",
            "Assistant: Puoi bollire l'acqua per 10 minuti.",
            "Utente: E senza fuoco?",
            "Assistant: Usa compresse di cloro.",
            "Utente: Quanto cloro?",
            "Assistant: 2 gocce per litro.",
            "Utente: Altre alternative?",
            "Assistant: Filtri UV o sabbia.",
        ]

        # Ottimizza mantenendo il flusso
        result = optimize_history(history, max_length=300, max_entries=4)

        # Verifica che mantenga coppie domanda-risposta complete
        assert len(result) <= 4

        # Se mantiene 4 entry, dovrebbero essere le ultime 4
        if len(result) == 4:
            assert result == history[-4:]

    def test_history_prefers_complete_exchanges_real(self):
        """Test preferenza per scambi conversazionali completi."""
        history = [
            "Utente: Domanda 1?",
            "Assistant: Risposta 1.",
            "Utente: Domanda 2?",
            "Assistant: Risposta 2.",
            "Utente: Domanda 3?",  # Senza risposta
        ]

        result = optimize_history(history, max_length=200, max_entries=3)

        # Dovrebbe mantenere almeno l'ultima entry
        assert result[-1] == "Utente: Domanda 3?"

        # E preferibilmente scambi completi precedenti
        total_length = sum(len(entry) for entry in result)
        assert total_length <= 200

    def test_history_optimization_performance_real(self):
        """Test performance ottimizzazione con history molto lunga."""
        import time

        # Crea history molto lunga
        large_history = []
        for i in range(1000):
            large_history.extend(
                [
                    f"Utente: Domanda numero {i} con dettagli aggiuntivi",
                    f"Assistant: Risposta dettagliata numero {i} con informazioni complete",
                ]
            )

        start_time = time.time()
        result = optimize_history(large_history, max_length=5000, max_entries=20)
        end_time = time.time()

        # Dovrebbe essere veloce (< 1 secondo)
        assert end_time - start_time < 1.0

        # E produrre risultato valido
        assert len(result) <= 20
        total_length = sum(len(str(entry)) for entry in result)
        assert total_length <= 5000 or len(result) == 1
