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


@main.command("install-config")
@click.option("--uninstall", is_flag=True, help="Rimuove la configurazione globale")
def install_config(uninstall):
    """Installa/rimuove la configurazione globale per usare sigma ovunque."""
    import os
    import shutil
    from pathlib import Path

    # Determina il percorso root del progetto
    from .config import get_config

    config = get_config()
    project_root = config.project_root

    # Percorso di destinazione per i file globali
    if os.name == "nt":  # Windows
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:  # Unix/Linux/MacOS
        global_config_dir = Path.home() / ".config" / "sigma-nex"

    if uninstall:
        if global_config_dir.exists():
            response = click.confirm(f"🗑️  Rimuovere {global_config_dir}?")
            if response:
                shutil.rmtree(global_config_dir)
                click.echo(f"✅ Configurazione globale rimossa da: {global_config_dir}")
            else:
                click.echo("❌ Operazione annullata")
        else:
            click.echo(
                f"ℹ️  Nessuna configurazione globale trovata in: {global_config_dir}"
            )
        return

    click.echo(f"📁 Installazione configurazione globale in: {global_config_dir}")

    # Crea la directory se non esiste
    global_config_dir.mkdir(parents=True, exist_ok=True)

    # File da copiare
    files_to_copy = [
        ("config.yaml", "config.yaml"),
        ("data", "data"),
        ("logs", "logs"),
    ]

    for src_name, dst_name in files_to_copy:
        src_path = project_root / src_name
        dst_path = global_config_dir / dst_name

        if src_path.exists():
            try:
                if src_path.is_file():
                    click.echo(f"📄 Copiando {src_name}...")
                    # Verifica se il file esiste e ha lo stesso contenuto
                    if dst_path.exists():
                        if dst_path.stat().st_size == src_path.stat().st_size:
                            click.echo(f"   ✓ {src_name} già aggiornato")
                            continue
                    shutil.copy2(src_path, dst_path)
                elif src_path.is_dir():
                    click.echo(f"📁 Copiando directory {src_name}...")
                    if dst_path.exists():
                        try:
                            shutil.rmtree(dst_path)
                        except PermissionError:
                            click.echo(
                                f"⚠️  Non posso rimuovere {dst_path}, "
                                "provo a copiare sopra..."
                            )
                    try:
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    except FileNotFoundError:
                        # La directory di destinazione potrebbe non esistere
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            except PermissionError as e:
                click.echo(f"❌ Errore di permessi copiando {src_name}: {e}")
                click.echo(
                    "💡 Prova a chiudere altri programmi o eseguire "
                    "come amministratore"
                )
            except Exception as e:
                click.echo(f"❌ Errore copiando {src_name}: {e}")
        else:
            click.echo(f"⚠️  File/directory non trovato: {src_path}")

    click.echo("\n✅ Installazione completata!")
    click.echo("🎯 Per usare SIGMA-NEX da qualsiasi directory, imposta:")
    if os.name == "nt":
        click.echo(f"   set SIGMA_NEX_ROOT={global_config_dir}")
        click.echo("   Oppure aggiungi questa variabile alle variabili di sistema")
    else:
        click.echo(f"   export SIGMA_NEX_ROOT='{global_config_dir}'")
        click.echo("   Aggiungi questa riga al tuo ~/.bashrc o ~/.zshrc")
    click.echo("   Ora puoi usare 'sigma' da qualsiasi directory")


if __name__ == "__main__":
    main()
