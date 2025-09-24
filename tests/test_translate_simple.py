"""
Test estesi per sigma_nex.core.translate - versione semplificata
Mirati ad aumentare la copertura delle funzioni effettivamente disponibili
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from sigma_nex.core.translate import translate_it_to_en, translate_en_to_it, is_translation_available, preload_models


class TestTranslationAvailability:
    """Test per la disponibilità della traduzione"""
    
    def test_is_translation_available_with_transformers(self):
        """Test is_translation_available con transformers disponibile"""
        with patch('sigma_nex.core.translate.importlib.import_module') as mock_import:
            transformers_mock = Mock()
            transformers_mock.MarianMTModel = Mock()
            transformers_mock.MarianTokenizer = Mock()
            mock_import.return_value = transformers_mock
            
            # Clear the global cache
            import sigma_nex.core.translate as translate_module
            translate_module._transformers_available = None
            
            result = is_translation_available()
            
            assert result is True
    
    def test_is_translation_available_without_transformers(self):
        """Test is_translation_available senza transformers"""
        with patch('sigma_nex.core.translate.importlib.import_module', side_effect=ImportError("No module")):
            
            # Clear the global cache
            import sigma_nex.core.translate as translate_module
            translate_module._transformers_available = None
            
            result = is_translation_available()
            
            assert result is False


class TestTranslateItToEn:
    """Test per translate_it_to_en"""
    
    def test_translate_it_to_en_empty_text(self):
        """Test traduzione con testo vuoto"""
        result = translate_it_to_en("")
        assert result == ""
    
    def test_translate_it_to_en_whitespace_only(self):
        """Test traduzione con solo whitespace"""
        result = translate_it_to_en("   \n\t   ")
        assert result == "   \n\t   "  # Should return original
    
    def test_translate_it_to_en_no_model(self):
        """Test traduzione senza modello disponibile"""
        with patch('sigma_nex.core.translate._load_model', return_value=None):
            result = translate_it_to_en("Ciao mondo")
            assert result == "Ciao mondo"  # Should return original text
    
    def test_translate_it_to_en_with_model_success(self):
        """Test traduzione con modello disponibile - successo"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Setup tokenizer mock
        mock_tokenizer.return_value = {'input_ids': [1, 2, 3]}  # Short input
        mock_tokenizer.batch_decode.return_value = ["Hello world"]
        
        # Setup model mock
        mock_model.generate.return_value = [[4, 5, 6]]
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            result = translate_it_to_en("Ciao mondo")
            
            assert result == "Hello world"
            mock_tokenizer.assert_called()
            mock_model.generate.assert_called_once()
    
    def test_translate_it_to_en_with_model_error(self):
        """Test traduzione con modello che genera errore"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        mock_tokenizer.return_value = {'input_ids': [1, 2, 3]}
        mock_model.generate.side_effect = Exception("Model error")
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            result = translate_it_to_en("Ciao mondo")
            
            assert result == "Ciao mondo"  # Should return original on error


class TestTranslateEnToIt:
    """Test per translate_en_to_it"""
    
    def test_translate_en_to_it_empty_text(self):
        """Test traduzione con testo vuoto"""
        result = translate_en_to_it("")
        assert result == ""
    
    def test_translate_en_to_it_whitespace_only(self):
        """Test traduzione con solo whitespace"""
        result = translate_en_to_it("   \n\t   ")
        assert result == "   \n\t   "  # Should return original
    
    def test_translate_en_to_it_no_model(self):
        """Test traduzione senza modello disponibile"""
        with patch('sigma_nex.core.translate._load_model', return_value=None):
            result = translate_en_to_it("Hello world")
            assert result == "Hello world"  # Should return original text
    
    def test_translate_en_to_it_with_model_success(self):
        """Test traduzione con modello disponibile - successo"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Setup tokenizer mock
        mock_tokenizer.return_value = {'input_ids': [1, 2, 3]}  # Short input
        mock_tokenizer.batch_decode.return_value = ["Ciao mondo"]
        
        # Setup model mock
        mock_model.generate.return_value = [[4, 5, 6]]
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            result = translate_en_to_it("Hello world")
            
            assert result == "Ciao mondo"
            mock_tokenizer.assert_called()
            mock_model.generate.assert_called_once()
    
    def test_translate_en_to_it_with_model_error(self):
        """Test traduzione con modello che genera errore"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        mock_tokenizer.return_value = {'input_ids': [1, 2, 3]}
        mock_model.generate.side_effect = Exception("Model error")
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            result = translate_en_to_it("Hello world")
            
            assert result == "Hello world"  # Should return original on error


class TestLongTextTranslation:
    """Test per la traduzione di testi lunghi"""
    
    def test_translate_it_to_en_long_text(self):
        """Test traduzione italiano->inglese con testo lungo"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Setup for long text (> 500 tokens)
        mock_tokenizer.return_value = {'input_ids': list(range(600))}  # Long input
        mock_tokenizer.batch_decode.return_value = ["Translated chunk"]
        mock_model.generate.return_value = [[4, 5, 6]]
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            with patch('sigma_nex.core.translate._chunk_translate', return_value="Chunked translation"):
                long_text = "Questo è un testo molto lungo " * 50
                result = translate_it_to_en(long_text)
                
                assert result == "Chunked translation"
    
    def test_translate_en_to_it_long_text(self):
        """Test traduzione inglese->italiano con testo lungo"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Setup for long text (> 500 tokens)
        mock_tokenizer.return_value = {'input_ids': list(range(600))}  # Long input
        mock_tokenizer.batch_decode.return_value = ["Chunk tradotto"]
        mock_model.generate.return_value = [[4, 5, 6]]
        
        with patch('sigma_nex.core.translate._load_model', return_value=(mock_tokenizer, mock_model)):
            with patch('sigma_nex.core.translate._chunk_translate', return_value="Traduzione a chunk"):
                long_text = "This is a very long text " * 50
                result = translate_en_to_it(long_text)
                
                assert result == "Traduzione a chunk"


class TestPreloadModels:
    """Test per preload_models"""
    
    def test_preload_models_success(self):
        """Test preload modelli con successo"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=True):
            with patch('sigma_nex.core.translate._load_model') as mock_load:
                preload_models()
                
                # Should call _load_model for both directions
                assert mock_load.call_count == 2
                calls = [call[0][0] for call in mock_load.call_args_list]
                assert 'it-en' in calls
                assert 'en-it' in calls
    
    def test_preload_models_no_transformers(self):
        """Test preload modelli senza transformers"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=False):
            with patch('sigma_nex.core.translate._load_model') as mock_load:
                preload_models()
                
                # Should not call _load_model
                mock_load.assert_not_called()


class TestModelPathHandling:
    """Test per la gestione dei percorsi dei modelli"""
    
    def test_get_model_paths_with_config(self):
        """Test get_model_paths con configurazione disponibile"""
        mock_config = Mock()
        mock_path = Mock()
        mock_path.__truediv__ = lambda self, other: Path(f"/mock/path/{other}")
        mock_config.get_path.return_value = mock_path
        
        with patch('sigma_nex.core.translate.get_config', return_value=mock_config):
            from sigma_nex.core.translate import _get_model_paths
            
            paths = _get_model_paths()
            
            assert 'it-en' in paths
            assert 'en-it' in paths
            mock_config.get_path.assert_called_once()
    
    def test_get_model_paths_without_config(self):
        """Test get_model_paths senza configurazione"""
        with patch('sigma_nex.core.translate.get_config', return_value=None):
            from sigma_nex.core.translate import _get_model_paths
            
            paths = _get_model_paths()
            
            assert 'it-en' in paths
            assert 'en-it' in paths
            # Should use default paths
            assert 'sigma_nex' in str(paths['it-en']) and 'translate' in str(paths['it-en'])


class TestModelLoading:
    """Test per il caricamento dei modelli"""
    
    def test_load_model_success(self):
        """Test caricamento modello con successo"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=True):
            with patch('sigma_nex.core.translate._get_model_paths') as mock_paths:
                mock_path = Mock()
                mock_path.exists.return_value = True
                mock_paths.return_value = {'it-en': mock_path}
                
                with patch('sigma_nex.core.translate.MarianTokenizer') as mock_tokenizer_class:
                    with patch('sigma_nex.core.translate.MarianMTModel') as mock_model_class:
                        mock_tokenizer = Mock()
                        mock_model = Mock()
                        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
                        mock_model_class.from_pretrained.return_value = mock_model
                        
                        # Clear the cache
                        import sigma_nex.core.translate as translate_module
                        translate_module._models.clear()
                        
                        from sigma_nex.core.translate import _load_model
                        result = _load_model('it-en')
                        
                        assert result is not None
                        assert result == (mock_tokenizer, mock_model)
    
    def test_load_model_no_transformers(self):
        """Test caricamento modello senza transformers"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=False):
            from sigma_nex.core.translate import _load_model
            
            result = _load_model('it-en')
            
            assert result is None
    
    def test_load_model_path_not_exists(self):
        """Test caricamento modello con path non esistente"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=True):
            with patch('sigma_nex.core.translate._get_model_paths') as mock_paths:
                mock_path = Mock()
                mock_path.exists.return_value = False
                mock_paths.return_value = {'it-en': mock_path}
                
                from sigma_nex.core.translate import _load_model
                result = _load_model('it-en')
                
                assert result is None
    
    def test_load_model_loading_error(self):
        """Test caricamento modello con errore"""
        with patch('sigma_nex.core.translate._check_transformers', return_value=True):
            with patch('sigma_nex.core.translate._get_model_paths') as mock_paths:
                mock_path = Mock()
                mock_path.exists.return_value = True
                mock_paths.return_value = {'it-en': mock_path}
                
                with patch('sigma_nex.core.translate.MarianTokenizer') as mock_tokenizer_class:
                    mock_tokenizer_class.from_pretrained.side_effect = Exception("Loading failed")
                    
                    # Clear the cache
                    import sigma_nex.core.translate as translate_module
                    translate_module._models.clear()
                    
                    from sigma_nex.core.translate import _load_model
                    result = _load_model('it-en')
                    
                    assert result is None


class TestChunkingTranslation:
    """Test per la traduzione chunked"""
    
    def test_chunk_translate_basic(self):
        """Test traduzione chunked di base"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Setup tokenizer to return different lengths for different inputs
        def tokenizer_side_effect(text):
            return {'input_ids': [1] * len(text.split())}
        
        mock_tokenizer.side_effect = tokenizer_side_effect
        mock_tokenizer.batch_decode.return_value = ["Translated sentence"]
        mock_model.generate.return_value = [[4, 5, 6]]
        
        from sigma_nex.core.translate import _chunk_translate
        
        text = "Prima frase. Seconda frase. Terza frase."
        result = _chunk_translate(text, mock_tokenizer, mock_model, max_tokens=10)
        
        # Should return translated text
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_chunk_translate_tokenization_error(self):
        """Test chunked translation con errore di tokenizzazione"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        mock_tokenizer.side_effect = Exception("Tokenization error")
        mock_tokenizer.batch_decode.return_value = ["Fallback"]
        mock_model.generate.return_value = [[4, 5, 6]]
        
        from sigma_nex.core.translate import _chunk_translate
        
        text = "Test text for chunking."
        result = _chunk_translate(text, mock_tokenizer, mock_model, max_tokens=10)
        
        # Should fallback to character-based chunking
        assert isinstance(result, str)
    
    def test_chunk_translate_generation_error(self):
        """Test chunked translation con errore di generazione"""
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        mock_tokenizer.return_value = {'input_ids': [1, 2, 3]}
        mock_tokenizer.batch_decode.return_value = ["Original chunk"]
        mock_model.generate.side_effect = Exception("Generation error")
        
        from sigma_nex.core.translate import _chunk_translate
        
        text = "Test text for chunking."
        result = _chunk_translate(text, mock_tokenizer, mock_model, max_tokens=100)
        
        # Should return original text chunks on error
        assert "Test text for chunking." in result