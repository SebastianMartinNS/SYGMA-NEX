import pytest
import json
from unittest.mock import patch, MagicMock
from sigma_nex.core.retriever import Retriever, search_moduli, get_moduli, build_index, get_moduli, build_index

def test_search():
    # Mock the search_moduli function
    with patch('sigma_nex.core.retriever.search_moduli', return_value=['result1', 'result2']):
        retriever = Retriever('dummy.idx', 'dummy_model')
        results = retriever.search('test query')
        assert results == ['result1', 'result2']


def test_get_moduli():
    # Mock the file open
    mock_data = {"modules": [{"nome": "test", "descrizione": "desc"}]}
    with patch('builtins.open', create=True) as mock_open:
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = json.dumps(mock_data)
        mock_open.return_value = mock_file
        
        with patch('json.load', return_value=mock_data):
            modules = get_moduli()
            assert modules == [{"nome": "test", "descrizione": "desc"}]


def test_search_moduli():
    # Mock FAISS and model
    with patch('faiss.read_index') as mock_read_index, \
         patch('sigma_nex.core.retriever.model') as mock_model, \
         patch('builtins.open', create=True) as mock_open, \
         patch('json.load', return_value=['text1', 'text2']):
        
        mock_index = MagicMock()
        # index.search returns (D, I) where I is indices
        mock_index.search.return_value = (None, [[0, 1]])  # I[0] = [0, 1]
        mock_read_index.return_value = mock_index
        
        mock_model.encode.return_value = MagicMock()
        
        results = search_moduli('query')
        assert results == ['text1', 'text2']
