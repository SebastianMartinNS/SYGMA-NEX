import json
import click

class DataLoader:
    """
    Classe responsabile del caricamento dei moduli operativi da un file JSON.
    Utilizzata per leggere il framework di sopravvivenza di SIGMA-NEX.

    La funzione `load()` restituisce il numero di moduli trovati nel file.
    """

    def load(self, path: str) -> int:
        """
        Carica un file JSON contenente il framework operativo.
        Restituisce il numero di moduli rilevati (presenti in data["modules"]).

        Args:
            path (str): Percorso al file JSON da caricare.

        Returns:
            int: Numero di moduli caricati, oppure 0 in caso di errore.
        """
        try:
            # Apertura del file JSON con codifica UTF-8
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Estrazione dell'elenco dei moduli dal campo "modules"
            modules = data.get("modules", [])

            # Output al terminale per conferma caricamento
            click.echo(f"Caricati {len(modules)} moduli dal file {path}")

            return len(modules)

        except Exception as e:
            # In caso di errore di parsing o apertura file
            click.echo(f"Errore caricamento scenario: {e}", err=True)
            return 0
