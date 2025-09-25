"""
Test realistici completi per sigma_nex.core.context - 80% coverage target
Test REALI senza mock pesanti - focus su costruzione prompt effettiva
"""

import pytest
from unittest.mock import Mock, patch

from sigma_nex.core.context import build_prompt


class TestContextRealistic:
    """Test realistici completi per build_prompt - copertura costruzione prompt effettiva"""

    def test_build_prompt_basic_real(self):
        """Test costruzione prompt di base senza retrieval"""
        system_prompt = "Sei SIGMA-NEX, un agente cognitivo autonomo."
        history = ["Utente: Come stai?", "Assistant: Sto bene, grazie!"]
        query = "Dimmi qualcosa di interessante"

        # Test senza retrieval
        prompt = build_prompt(system_prompt, history, query, retrieval_enabled=False)

        # Verifica struttura del prompt
        assert system_prompt in prompt
        assert "Utente: Come stai?" in prompt
        assert "Assistant: Sto bene, grazie!" in prompt
        assert "Utente: Dimmi qualcosa di interessante" in prompt
        assert "Assistant:" in prompt

        # Non dovrebbe contenere sezione Contesto
        assert "Contesto:" not in prompt

    def test_build_prompt_empty_history_real(self):
        """Test prompt con cronologia vuota"""
        system_prompt = "System prompt di test"
        history = []
        query = "Prima domanda"

        prompt = build_prompt(system_prompt, history, query, retrieval_enabled=False)

        assert system_prompt in prompt
        assert "Utente: Prima domanda" in prompt
        assert "Assistant:" in prompt
        assert len(prompt.strip()) > 0

    def test_build_prompt_long_history_real(self):
        """Test prompt con cronologia lunga"""
        system_prompt = "System prompt"
        history = [
            "Utente: Domanda 1",
            "Assistant: Risposta 1",
            "Utente: Domanda 2",
            "Assistant: Risposta 2",
            "Utente: Domanda 3",
            "Assistant: Risposta 3",
        ]
        query = "Nuova domanda"

        prompt = build_prompt(system_prompt, history, query, retrieval_enabled=False)

        # Verifica che tutta la cronologia sia inclusa
        for item in history:
            assert item in prompt

        assert "Utente: Nuova domanda" in prompt
        assert "Assistant:" in prompt

    def test_build_prompt_with_retrieval_success_real(self):
        """Test prompt con retrieval funzionante"""
        system_prompt = "Test system prompt"
        history = ["Utente: Test", "Assistant: OK"]
        query = "Come funziona la sopravvivenza?"

        # Mock moduli rilevanti realistici
        mock_moduli = [
            "SOPRAVVIVENZA_BASE::Tecniche di base per la sopravvivenza in ambiente ostile. Include reperimento acqua, cibo e riparo.",
            "PRIMO_SOCCORSO::Procedure di emergenza per il primo soccorso. Fondamentale per situazioni critiche.",
            "NAVIGAZIONE::Orientamento e navigazione senza strumenti moderni usando stelle e punti di riferimento.",
        ]

        with patch("sigma_nex.core.retriever.search_moduli", return_value=mock_moduli):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Verifica sezione Contesto
        assert "Contesto:" in prompt
        assert "[MODULO 1: SOPRAVVIVENZA_BASE]" in prompt
        assert "Tecniche di base per la sopravvivenza" in prompt
        assert "[MODULO 2: PRIMO_SOCCORSO]" in prompt
        assert "Procedure di emergenza" in prompt
        assert "[MODULO 3: NAVIGAZIONE]" in prompt
        assert "Orientamento e navigazione" in prompt

        # Verifica cronologia ancora presente
        assert "Utente: Test" in prompt
        assert "Assistant: OK" in prompt
        assert "Utente: Come funziona la sopravvivenza?" in prompt

    def test_build_prompt_retrieval_exception_real(self):
        """Test gestione eccezione durante retrieval"""
        system_prompt = "System prompt"
        history = ["Utente: Test"]
        query = "Test query"

        # Simula eccezione durante search_moduli
        with patch(
            "sigma_nex.core.retriever.search_moduli",
            side_effect=Exception("FAISS error"),
        ):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Dovrebbe fallback a prompt senza contesto
        assert system_prompt in prompt
        assert "Utente: Test" in prompt
        assert "Utente: Test query" in prompt
        assert "Contesto:" not in prompt  # Non dovrebbe esserci sezione contesto

    def test_build_prompt_retrieval_no_modules_real(self):
        """Test retrieval che non trova moduli"""
        system_prompt = "System prompt"
        history = []
        query = "Query senza risultati"

        # Mock che restituisce lista vuota
        with patch("sigma_nex.core.retriever.search_moduli", return_value=[]):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Non dovrebbe esserci sezione Contesto per lista vuota
        assert "Contesto:" not in prompt
        assert system_prompt in prompt
        assert "Utente: Query senza risultati" in prompt

    def test_build_prompt_malformed_modules_real(self):
        """Test gestione moduli malformati"""
        system_prompt = "System prompt"
        history = []
        query = "Test malformed"

        # Mock con moduli malformati
        mock_moduli = [
            "MODULO_CORRETTO::Descrizione corretta del modulo",
            "modulo_senza_separatore_doppio",  # Formato sbagliato
            "ALTRO_MODULO::Descrizione normale",
            "",  # Stringa vuota
            "   ",  # Solo spazi
        ]

        with patch("sigma_nex.core.retriever.search_moduli", return_value=mock_moduli):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Verifica gestione moduli corretti
        assert "[MODULO 1: MODULO_CORRETTO]" in prompt
        assert "Descrizione corretta del modulo" in prompt
        assert "[MODULO 3: ALTRO_MODULO]" in prompt
        assert "Descrizione normale" in prompt

        # Verifica gestione moduli malformati
        assert "[MODULO 2]" in prompt  # Senza nome specifico
        assert "modulo_senza_separatore_doppio" in prompt
        assert "[MODULO 4]" in prompt  # Stringa vuota come modulo generico
        assert "[MODULO 5]" in prompt  # Spazi come modulo generico


class TestContextIntegration:
    """Test integrazione build_prompt con altri moduli"""

    def test_build_prompt_retriever_integration_real(self):
        """Test integrazione reale con retriever"""
        system_prompt = "SIGMA-NEX Integration Test"
        history = ["Utente: Ciao", "Assistant: Salve"]
        query = "Come posso orientarmi di notte?"

        # Test con moduli realistici che potrebbero esistere
        realistic_modules = [
            "NAVIGAZIONE_NOTTURNA::Orientamento usando costellazioni. Identifica Orsa Maggiore e Stella Polare per determinare il nord.",
            "SOPRAVVIVENZA_URBANA::Tecniche per orientarsi in ambiente urbano durante emergenze o blackout.",
            "STRUMENTI_PRIMITIVI::Costruzione di bussola improvvisata usando ago magnetizzato e recipiente d'acqua.",
        ]

        with patch(
            "sigma_nex.core.retriever.search_moduli", return_value=realistic_modules
        ) as mock_search:
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

            # Verifica che search_moduli sia stato chiamato correttamente
            mock_search.assert_called_once_with(query, k=3)

        # Verifica struttura del prompt finale
        assert "Contesto:" in prompt
        assert "NAVIGAZIONE_NOTTURNA" in prompt
        assert "costellazioni" in prompt
        assert "Orsa Maggiore" in prompt
        assert "SOPRAVVIVENZA_URBANA" in prompt
        assert "STRUMENTI_PRIMITIVI" in prompt

        # Verifica che cronologia e query siano preservate
        assert "Utente: Ciao" in prompt
        assert "Assistant: Salve" in prompt
        assert "Utente: Come posso orientarmi di notte?" in prompt
        assert "Assistant:" in prompt

    def test_build_prompt_lazy_import_handling_real(self):
        """Test gestione lazy import del retriever"""
        system_prompt = "Lazy import test"
        history = []
        query = "Test query"

        # Test quando il modulo retriever non è disponibile
        with patch(
            "sigma_nex.core.retriever.search_moduli",
            side_effect=ImportError("Module not found"),
        ):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Dovrebbe gestire gracefully l'errore di import
        assert system_prompt in prompt
        assert "Utente: Test query" in prompt
        assert "Contesto:" not in prompt


class TestContextDataFlow:
    """Test flusso dati nella costruzione prompt"""

    def test_build_prompt_data_flow_complete_real(self):
        """Test flusso dati completo"""
        system_prompt = "## SIGMA-NEX SYSTEM ##\nSei un agente cognitivo."
        history = [
            "Utente: Qual è la procedura per purificare l'acqua?",
            "Assistant: Ci sono diversi metodi di purificazione dell'acqua.",
            "Utente: Puoi essere più specifico sui metodi chimici?",
        ]
        query = "Come funziona la clorazione?"

        mock_knowledge = [
            "PURIFICAZIONE_ACQUA::Metodi chimici includono clorazione, iodio e UV. La clorazione è il più comune.",
            "CHIMICA_BASE::Principi chimici della disinfezione. Il cloro elimina batteri e virus ossidandone le pareti cellulari.",
            "DOSAGGIO_CHIMICI::Calcolo delle dosi corrette per diversi volumi d'acqua e livelli di contaminazione.",
        ]

        with patch(
            "sigma_nex.core.retriever.search_moduli", return_value=mock_knowledge
        ):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Verifica sequenza corretta nel prompt
        prompt_lines = prompt.split("\n")

        # System prompt all'inizio
        assert prompt_lines[0] == "## SIGMA-NEX SYSTEM ##"
        assert "Sei un agente cognitivo." in prompt

        # Sezione Contesto dopo system prompt
        context_index = None
        for i, line in enumerate(prompt_lines):
            if line == "Contesto:":
                context_index = i
                break
        assert context_index is not None

        # Cronologia dopo contesto
        assert "Utente: Qual è la procedura per purificare l'acqua?" in prompt
        assert (
            "Assistant: Ci sono diversi metodi di purificazione dell'acqua." in prompt
        )
        assert "Utente: Puoi essere più specifico sui metodi chimici?" in prompt
        assert "Utente: Come funziona la clorazione?" in prompt
        assert prompt.endswith("Assistant:")

    def test_build_prompt_special_characters_real(self):
        """Test gestione caratteri speciali"""
        system_prompt = "System prompt con àccenti e €moji 🤖"
        history = [
            "Utente: Tëst con carattëri spëciali àéìòù",
            "Assistant: Rïsposta con ëmoji 😊 e símbolí spëcialï",
        ]
        query = "Dómanda con €€€ e 中文字符?"

        mock_modules = [
            "TËST_MÒDULE::Descrizione con carattëri spëciali àéìòù e símbolí 🌟",
            "UNICODE_SUPPORT::Test completo Unicode: ñáéíóú, Ελληνικά, 中文, العربية, עברית",
        ]

        with patch("sigma_nex.core.retriever.search_moduli", return_value=mock_modules):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Verifica che tutti i caratteri speciali siano preservati
        assert "àccenti e €moji 🤖" in prompt
        assert "Tëst con carattëri spëciali àéìòù" in prompt
        assert "Rïsposta con ëmoji 😊" in prompt
        assert "Dómanda con €€€ e 中文字符?" in prompt
        assert "TËST_MÒDULE" in prompt
        assert "carattëri spëciali àéìòù e símbolí 🌟" in prompt
        assert "Ελληνικά, 中文, العربية, עברית" in prompt


class TestContextPerformance:
    """Test performance build_prompt"""

    def test_build_prompt_performance_large_history_real(self):
        """Test performance con cronologia grande"""
        import time

        system_prompt = "Performance test system prompt"

        # Crea cronologia lunga
        history = []
        for i in range(200):  # 200 scambi = 400 messaggi
            history.append(f"Utente: Domanda numero {i}")
            history.append(f"Assistant: Risposta numero {i}")

        query = "Domanda finale performance test"

        start_time = time.time()

        # Test senza retrieval (più veloce)
        prompt = build_prompt(system_prompt, history, query, retrieval_enabled=False)

        end_time = time.time()
        execution_time = end_time - start_time

        # Dovrebbe essere ragionevolmente veloce anche con cronologia grande
        assert execution_time < 0.1  # Meno di 100ms
        assert len(prompt) > 10000  # Prompt dovrebbe essere sostanzioso
        assert "Domanda numero 199" in prompt
        assert "Risposta numero 199" in prompt
        assert "Domanda finale performance test" in prompt

    def test_build_prompt_performance_with_retrieval_real(self):
        """Test performance con retrieval"""
        import time

        system_prompt = "Performance test with retrieval"
        history = ["Utente: Test", "Assistant: OK"]
        query = "Performance query"

        # Mock che simula retrieval lento ma realistico
        def slow_search_moduli(query, k):
            time.sleep(0.01)  # Simula 10ms di ricerca
            return [
                f"MODULE_{i}::Descrizione del modulo {i} per query '{query}'"
                for i in range(k)
            ]

        start_time = time.time()

        with patch(
            "sigma_nex.core.retriever.search_moduli", side_effect=slow_search_moduli
        ):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        end_time = time.time()
        execution_time = end_time - start_time

        # Dovrebbe includere il tempo di retrieval ma rimanere ragionevole
        assert execution_time < 0.1  # Meno di 100ms totali
        assert "Contesto:" in prompt
        assert "MODULE_0" in prompt
        assert "MODULE_1" in prompt
        assert "MODULE_2" in prompt


class TestContextEdgeCases:
    """Test casi limite per build_prompt"""

    def test_build_prompt_edge_cases_real(self):
        """Test casi limite vari"""
        # System prompt vuoto
        prompt1 = build_prompt("", [], "Test", retrieval_enabled=False)
        assert "Utente: Test" in prompt1
        assert "Assistant:" in prompt1

        # Query vuota
        prompt2 = build_prompt("System", ["Utente: Hi"], "", retrieval_enabled=False)
        assert "System" in prompt2
        assert "Utente: Hi" in prompt2
        assert "Utente: " in prompt2  # Query vuota

        # Tutto vuoto tranne query
        prompt3 = build_prompt("", [], "Solo query", retrieval_enabled=False)
        assert "Utente: Solo query" in prompt3
        assert "Assistant:" in prompt3

    def test_build_prompt_whitespace_handling_real(self):
        """Test gestione spazi bianchi"""
        system_prompt = "   System con spazi   "
        history = [
            "  Utente: Domanda con spazi  ",
            "   Assistant: Risposta con spazi   ",
        ]
        query = "  Query con spazi  "

        mock_modules = [
            "  MODULE_SPACES  ::  Descrizione con spazi  ",
        ]

        with patch("sigma_nex.core.retriever.search_moduli", return_value=mock_modules):
            prompt = build_prompt(system_prompt, history, query, retrieval_enabled=True)

        # Verifica che gli spazi siano gestiti correttamente
        assert "System con spazi" in prompt  # System prompt trimmed
        assert "  Utente: Domanda con spazi  " in prompt  # History preservata
        assert "  Query con spazi  " in prompt  # Query preservata
        assert "[MODULO 1: MODULE_SPACES]" in prompt  # Nome modulo trimmed
        assert "Descrizione con spazi" in prompt  # Descrizione trimmed
