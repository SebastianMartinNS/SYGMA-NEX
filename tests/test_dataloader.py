import json
from sigma_nex.data_loader import DataLoader


def test_data_loader_success(tmp_path, capsys):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"modules": [{"nome": "a"}, {"nome": "b"}]}), encoding="utf-8")
    count = DataLoader().load(str(p))
    assert count == 2
    out = capsys.readouterr().out
    assert "Caricati 2 moduli" in out


def test_data_loader_error(tmp_path, capsys):
    p = tmp_path / "bad.json"
    p.write_text("not-json", encoding="utf-8")
    count = DataLoader().load(str(p))
    assert count == 0
    err = capsys.readouterr().err
    assert "Errore" in err
