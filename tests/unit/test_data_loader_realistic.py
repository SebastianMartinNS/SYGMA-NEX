"""
Test realistici per sigma_nex.data_loader - focus su logica reale di caricamento dati
Testa comportamento effettivo del DataLoader con file reali e simulati
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from sigma_nex.data_loader import DataLoader, load_json_data


class TestDataLoaderRealistic:
    """Test realistici del DataLoader - logica effettiva con casi reali"""

    def test_dataloader_initialization_real(self):
        """Test inizializzazione DataLoader"""
        loader = DataLoader()

        # Verifica che DataLoader sia inizializzato correttamente
        assert loader is not None
        assert hasattr(loader, "load")
        assert callable(loader.load)

    def test_load_valid_json_file_real(self):
        """Test caricamento file JSON valido con struttura reale"""
        # Crea file temporaneo con struttura SIGMA-NEX reale
        test_data = {
            "framework": "SIGMA-NEX",
            "version": "1.0",
            "modules": [
                {
                    "id": "survival_001",
                    "name": "Water Procurement",
                    "category": "survival",
                    "priority": "critical",
                    "description": "Emergency water location and purification",
                },
                {
                    "id": "navigation_001",
                    "name": "GPS Navigation",
                    "category": "navigation",
                    "priority": "high",
                    "description": "GPS-based route planning",
                },
                {
                    "id": "communication_001",
                    "name": "Emergency Communications",
                    "category": "communication",
                    "priority": "critical",
                    "description": "Emergency communication protocols",
                },
            ],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, indent=2, ensure_ascii=False)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire il numero corretto di moduli
            assert result == 3
            assert isinstance(result, int)

        finally:
            # Cleanup
            os.unlink(temp_path)

    def test_load_empty_modules_real(self):
        """Test caricamento file con array modules vuoto"""
        test_data = {"framework": "SIGMA-NEX", "modules": []}  # Array vuoto

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire 0 per array vuoto
            assert result == 0

        finally:
            os.unlink(temp_path)

    def test_load_missing_modules_key_real(self):
        """Test caricamento file senza chiave 'modules'"""
        test_data = {
            "framework": "SIGMA-NEX",
            "version": "1.0",
            # Manca la chiave "modules"
            "other_data": "some value",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire 0 se manca la chiave "modules"
            assert result == 0

        finally:
            os.unlink(temp_path)

    def test_load_real_project_file(self):
        """Test caricamento file reale del progetto se esiste"""
        # Testa con il file reale del progetto
        project_file = Path("data/Framework_SIGMA.json")

        if project_file.exists():
            loader = DataLoader()
            result = loader.load(str(project_file))

            # File reale dovrebbe avere almeno alcuni moduli
            assert isinstance(result, int)
            assert result >= 0  # Almeno 0 moduli

            # Se il file contiene moduli, dovrebbe essere > 0
            with open(project_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                expected_modules = len(data.get("modules", []))
                assert result == expected_modules

                # Verifica che la struttura sia quella attesa del progetto SIGMA-NEX
                if expected_modules > 0:
                    first_module = data["modules"][0]
                    # I moduli reali hanno questa struttura specifica
                    assert "numero" in first_module
                    assert "nome" in first_module
                    assert "priorita" in first_module
                    assert "descrizione" in first_module
        else:
            # Se il file non esiste, skip il test
            pytest.skip("File reale Framework_SIGMA.json non trovato")

    def test_load_sigma_nex_structure_real(self):
        """Test caricamento con struttura SIGMA-NEX reale"""
        # Testa con la struttura reale dei moduli SIGMA-NEX
        test_data = {
            "modules": [
                {
                    "numero": 1,
                    "nome": "idratazione",
                    "priorita": "alta",
                    "descrizione": "Strategie per trovare, purificare e conservare acqua potabile",
                    "comandi": [
                        "1. Raccogli materiali naturali",
                        "2. Costruisci un filtro a strati",
                    ],
                    "fallback": "1. Raccogli rugiada al mattino",
                },
                {
                    "numero": 2,
                    "nome": "alimentazione",
                    "priorita": "alta",
                    "descrizione": "Tecniche per reperire, conservare e cucinare cibo",
                    "comandi": [
                        "1. Costruisci trappole semplici",
                        "2. Raccogli piante note come edibili",
                    ],
                    "fallback": "1. Scava per trovare radici amidacee",
                },
            ]
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, indent=2, ensure_ascii=False)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe contare correttamente moduli con struttura SIGMA-NEX
            assert result == 2

        finally:
            os.unlink(temp_path)


class TestDataLoaderErrorHandling:
    """Test gestione errori del DataLoader"""

    def test_load_nonexistent_file_real(self):
        """Test caricamento file inesistente"""
        loader = DataLoader()
        result = loader.load("nonexistent_file.json")

        # Dovrebbe restituire 0 per file inesistente
        assert result == 0

    def test_load_invalid_json_real(self):
        """Test caricamento file JSON malformato"""
        # Crea file con JSON invalido
        invalid_json = '{"framework": "SIGMA-NEX", "modules": [invalid json}'

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(invalid_json)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire 0 per JSON invalido
            assert result == 0

        finally:
            os.unlink(temp_path)

    def test_load_empty_file_real(self):
        """Test caricamento file vuoto"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            # File completamente vuoto
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire 0 per file vuoto
            assert result == 0

        finally:
            os.unlink(temp_path)

    def test_load_permission_denied_real(self):
        """Test caricamento file senza permessi di lettura - Skip su Windows"""
        import platform

        if platform.system() == "Windows":
            pytest.skip("Test permessi file non applicabile su Windows")

        # Crea file temporaneo
        test_data = {"modules": [{"id": "test"}]}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            # Rimuovi permessi di lettura (solo su sistemi Unix)
            os.chmod(temp_path, 0o000)  # Nessun permesso

            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe restituire 0 per file non leggibile
            assert result == 0

        finally:
            # Ripristina permessi per cleanup
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

    def test_load_non_dict_json_real(self):
        """Test caricamento JSON che non è un dizionario"""
        # JSON valido ma non è un dict
        test_cases = [
            [1, 2, 3],  # Array
            "string",  # Stringa
            42,  # Numero
            True,  # Boolean
        ]

        for test_case in test_cases:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as temp_file:
                json.dump(test_case, temp_file)
                temp_path = temp_file.name

            try:
                loader = DataLoader()
                result = loader.load(temp_path)

                # Dovrebbe restituire 0 per JSON non-dict
                assert result == 0

            finally:
                os.unlink(temp_path)


class TestDataLoaderDataIntegrity:
    """Test integrità dati del DataLoader"""

    def test_load_unicode_handling_real(self):
        """Test gestione corretta caratteri Unicode"""
        test_data = {
            "framework": "SIGMA-NEX",
            "modules": [
                {
                    "id": "unicode_test",
                    "name": "Test con caratteri speciali: àèìòù ñ ç 中文 🚀",
                    "description": "Módulo con caractères especiálès",
                }
            ],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, ensure_ascii=False, indent=2)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe gestire Unicode correttamente
            assert result == 1

        finally:
            os.unlink(temp_path)

    def test_load_large_file_real(self):
        """Test caricamento file con molti moduli"""
        # Genera file con molti moduli per test performance
        modules = []
        for i in range(1000):
            modules.append(
                {
                    "id": f"module_{i:04d}",
                    "name": f"Module {i}",
                    "category": f"category_{i % 10}",
                    "description": f"Description for module {i}",
                }
            )

        test_data = {"framework": "SIGMA-NEX", "modules": modules}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe gestire file grandi
            assert result == 1000

        finally:
            os.unlink(temp_path)

    def test_load_nested_modules_structure_real(self):
        """Test caricamento struttura moduli complessa"""
        test_data = {
            "framework": "SIGMA-NEX",
            "modules": [
                {
                    "id": "complex_module",
                    "name": "Complex Module",
                    "submodules": [
                        {"sub_id": "sub1", "name": "Submodule 1"},
                        {"sub_id": "sub2", "name": "Submodule 2"},
                    ],
                    "metadata": {
                        "version": "1.0",
                        "tags": ["survival", "emergency"],
                        "requirements": ["water", "shelter"],
                    },
                }
            ],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, indent=2)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Dovrebbe contare solo i moduli top-level
            assert result == 1

        finally:
            os.unlink(temp_path)


class TestDataLoaderOutput:
    """Test output e messaging del DataLoader"""

    def test_load_click_output_success(self, capsys):
        """Test output click per caricamento riuscito"""
        test_data = {
            "framework": "SIGMA-NEX",
            "modules": [
                {"id": "test1", "name": "Test Module 1"},
                {"id": "test2", "name": "Test Module 2"},
            ],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            loader = DataLoader()
            result = loader.load(temp_path)

            # Verifica risultato
            assert result == 2

            # Verifica output click
            captured = capsys.readouterr()
            assert f"Caricati 2 moduli dal file {temp_path}" in captured.out

        finally:
            os.unlink(temp_path)

    def test_load_click_output_error(self, capsys):
        """Test output click per errore di caricamento"""
        loader = DataLoader()
        result = loader.load("file_inesistente.json")

        # Verifica risultato
        assert result == 0

        # Verifica output errore
        captured = capsys.readouterr()
        assert "Errore caricamento scenario:" in captured.err


class TestUtilityFunctions:
    """Test funzioni utility del modulo data_loader"""

    def test_load_json_data_success(self):
        """Test load_json_data con file valido"""
        test_data = {
            "framework": "SIGMA-NEX",
            "modules": [{"id": "test", "name": "Test Module"}],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, indent=2)
            temp_path = temp_file.name

        try:
            result = load_json_data(temp_path)

            # Dovrebbe restituire i dati JSON
            assert result == test_data
            assert result["framework"] == "SIGMA-NEX"
            assert len(result["modules"]) == 1

        finally:
            os.unlink(temp_path)

    def test_load_json_data_file_not_found(self):
        """Test load_json_data con file inesistente"""
        result = load_json_data("file_inesistente.json")

        # Dovrebbe restituire lista vuota per FileNotFoundError
        assert result == []
        assert isinstance(result, list)

    def test_load_json_data_invalid_json(self):
        """Test load_json_data con JSON invalido"""
        invalid_json = '{"invalid": json content}'

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(invalid_json)
            temp_path = temp_file.name

        try:
            result = load_json_data(temp_path)

            # Dovrebbe restituire lista vuota per JSON invalido
            assert result == []
            assert isinstance(result, list)

        finally:
            os.unlink(temp_path)

    def test_load_json_data_empty_file(self):
        """Test load_json_data con file vuoto"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            # File vuoto
            temp_path = temp_file.name

        try:
            result = load_json_data(temp_path)

            # Dovrebbe restituire lista vuota per file vuoto
            assert result == []
            assert isinstance(result, list)

        finally:
            os.unlink(temp_path)


class TestDataLoaderPerformance:
    """Test performance del DataLoader"""

    def test_load_performance_characteristics(self):
        """Test caratteristiche performance del caricamento"""
        import time

        # Crea file di dimensioni moderate
        modules = [{"id": f"mod_{i}", "name": f"Module {i}"} for i in range(100)]
        test_data = {"framework": "SIGMA-NEX", "modules": modules}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            loader = DataLoader()

            # Misura tempo di caricamento
            start_time = time.time()
            result = loader.load(temp_path)
            end_time = time.time()

            # Verifica risultato
            assert result == 100

            # Il caricamento dovrebbe essere veloce
            load_time = end_time - start_time
            assert load_time < 1.0  # Meno di 1 secondo per 100 moduli

        finally:
            os.unlink(temp_path)

    def test_load_memory_usage_real(self):
        """Test uso memoria durante caricamento"""
        import gc

        initial_objects = len(gc.get_objects())

        # Carica e scarica più volte
        for i in range(10):
            modules = [{"id": f"mod_{j}", "name": f"Module {j}"} for j in range(50)]
            test_data = {"modules": modules}

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as temp_file:
                json.dump(test_data, temp_file)
                temp_path = temp_file.name

            try:
                loader = DataLoader()
                result = loader.load(temp_path)
                assert result == 50

            finally:
                os.unlink(temp_path)

        gc.collect()
        final_objects = len(gc.get_objects())

        # Non dovrebbe esserci memory leak significativo
        objects_increase = final_objects - initial_objects
        assert objects_increase < 1000  # Threshold ragionevole
