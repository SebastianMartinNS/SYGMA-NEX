import click
from .config import get_config
from .core.runner import Runner
from .data_loader import DataLoader


@click.group()
@click.option("--secure", is_flag=True, help="Modalità sicura (richiede password)")
@click.pass_context
def main(ctx, secure):
    """CLI di SIGMA-NEX - Agente cognitivo autonomo per sopravvivenza offline."""
    cfg = get_config()
    ctx.obj = {"config": cfg, "secure": secure}


@main.command()
@click.pass_context
def start(ctx):
    """Avvia l'agente in REPL interattivo."""
    cfg, secure = ctx.obj["config"], ctx.obj["secure"]
    Runner(cfg, secure=secure).interactive()


@main.command("load-framework")
@click.argument("path", type=click.Path(exists=True))
def load_framework(path):
    """Carica il file Framework_SIGMA.json."""
    count = DataLoader().load(path)
    click.echo(f"Caricati {count} moduli dal file {path}.")


@main.command()
@click.pass_context
def self_check(ctx):
    """Verifica che Ollama CLI e modelli siano disponibili."""
    cfg = ctx.obj["config"]
    Runner(cfg).self_check()


@main.command("self-heal")
@click.argument("file", type=click.Path(exists=True))
@click.pass_context
def self_heal(ctx, file):
    """Analizza e migliora il codice Python specificato."""
    cfg = ctx.obj["config"]
    secure = ctx.obj["secure"]
    runner = Runner(cfg, secure=secure)
    result = runner.self_heal_file(file)
    click.echo(result)


@main.command()
@click.option("--host", default="127.0.0.1", help="Host per il server API")
@click.option("--port", default=8000, type=int, help="Porta per il server API")
@click.pass_context
def server(ctx, host, port):
    """Avvia il server API REST."""
    try:
        from .server import SigmaServer

        click.echo(f"Avvio server SIGMA-NEX su {host}:{port}")
        server = SigmaServer()
        server.run(host=host, port=port)
    except ImportError:
        click.echo(
            "❌ Errore: dipendenze del server non installate. "
            "Installa con: pip install fastapi uvicorn",
            err=True,
        )
    except KeyboardInterrupt:
        click.echo("\nServer fermato.")


@main.command()
def gui():
    """Avvia l'interfaccia grafica."""
    try:
        from .gui import main as gui_main

        gui_main()
    except ImportError:
        click.echo(
            "❌ Errore: dipendenze GUI non installate. "
            "Installa con: pip install customtkinter",
            err=True,
        )
    except KeyboardInterrupt:
        click.echo("\nGUI chiusa.")


if __name__ == "__main__":
    main()
