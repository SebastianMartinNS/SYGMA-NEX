import subprocess
import sys

import click
import requests

from . import __version__
from .config import get_config
from .core.runner import Runner
from .data_loader import DataLoader


def show_ascii_banner():
    """Display SIGMA-NEX ASCII banner with author info."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  ███████╗██╗ ██████╗ ███╗   ███╗ █████╗      ███╗   ██╗███████╗██╗  ██╗      ║
║  ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗     ████╗  ██║██╔════╝╚██╗██╔╝      ║
║  ███████╗██║██║  ███╗██╔████╔██║███████║     ██╔██╗ ██║█████╗   ╚███╔╝       ║
║  ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║     ██║╚██╗██║██╔══╝   ██╔██╗       ║
║  ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║     ██║ ╚████║███████╗██╔╝ ██╗      ║
║  ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ║
║                                                                              ║
║                   Agente Cognitivo Autonomo per Sopravvivenza                ║
║                             Offline-First v0.3.5                             ║
║                                                                              ║
║      Sviluppato da: Martin Sebastian                                         ║
║      Email: rootedlab6@gmail.com                                             ║
║      Repository: https://github.com/SebastianMartinNS/SYGMA-NEX              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    click.echo(banner)


@click.group()
@click.option("--secure", is_flag=True, help="Modalità sicura (richiede password)")
@click.pass_context
def main(ctx, secure):
    """CLI di SIGMA-NEX - Agente cognitivo autonomo per sopravvivenza offline."""
    show_ascii_banner()
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


@main.command()
@click.option("--check-only", is_flag=True, help="Solo controllo senza aggiornare")
@click.option(
    "--force", is_flag=True, help="Forza aggiornamento anche se già aggiornato"
)
def update(check_only, force):
    """Aggiorna SIGMA-NEX dal repository GitHub."""
    click.echo(
        f"🔍 Controllo aggiornamenti SIGMA-NEX " f"(versione corrente: {__version__})"
    )

    cfg = get_config()
    project_root = cfg.project_root

    # 1. Verifica se siamo in un repository git
    git_dir = project_root / ".git"
    if not git_dir.exists():
        click.echo("❌ Non siamo in un repository git. " "Impossibile aggiornare.")
        click.echo(
            "💡 Clona il repository: "
            "git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git"
        )
        return

    # 2. Verifica connessione internet e repository
    api_url = (
        "https://api.github.com/repos/SebastianMartinNS/" "SYGMA-NEX/releases/latest"
    )
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip("v")
            click.echo(f"📡 Versione più recente su GitHub: {latest_version}")

            if latest_version == __version__ and not force:
                click.echo("✅ Sei già aggiornato all'ultima versione!")
                if not check_only:
                    click.echo("💡 Usa --force per forzare il pull comunque")
                return
            elif latest_version != __version__:
                click.echo(f"🆕 Nuova versione disponibile: {latest_version}")
        else:
            click.echo("⚠️  Impossibile verificare l'ultima versione " "dal GitHub API")
    except Exception as e:
        click.echo(f"⚠️  Errore connessione GitHub API: {e}")
        click.echo("🔄 Procedo comunque con git pull...")

    if check_only:
        click.echo("ℹ️  Solo controllo richiesto, non aggiorno.")
        return

    # 3. Controlla stato git locale
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            click.echo("⚠️  Ci sono modifiche locali non committate:")
            click.echo(result.stdout)
            if not click.confirm("Vuoi procedere comunque con git pull?"):
                click.echo("❌ Aggiornamento annullato")
                return
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Errore controllo git status: {e}")
        return
    except FileNotFoundError:
        click.echo("❌ Git non trovato. " "Installa Git per usare questa funzione.")
        return

    # 4. Esegui git pull
    click.echo("🔄 Aggiornamento in corso...")
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "master"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        click.echo("✅ Git pull completato!")
        click.echo(result.stdout)

        if "Already up to date" in result.stdout:
            click.echo("ℹ️  Repository già aggiornato")
        else:
            click.echo("🔄 Repository aggiornato, controllo dipendenze...")

            # 5. Aggiorna dipendenze se necessario
            if (project_root / "requirements.txt").exists():
                click.echo("📦 Aggiornamento dipendenze...")
                try:
                    subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "pip",
                            "install",
                            "-r",
                            str(project_root / "requirements.txt"),
                            "--upgrade",
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    click.echo("✅ Dipendenze aggiornate!")
                except subprocess.CalledProcessError as e:
                    click.echo(f"⚠️  Errore aggiornamento dipendenze: {e}")
                    msg = (
                        "💡 Potresti dover aggiornare manualmente con: "
                        "pip install -r requirements.txt --upgrade"
                    )
                    click.echo(msg)

            # 6. Ricarica configurazione se necessario
            try:
                # Verifica se la versione è cambiata dopo il pull
                import importlib

                import sigma_nex

                importlib.reload(sigma_nex)
                new_version = getattr(sigma_nex, "__version__", "unknown")
                if new_version != __version__:
                    click.echo(
                        f"🎉 SIGMA-NEX aggiornato alla " f"versione {new_version}!"
                    )
                else:
                    click.echo("✅ Aggiornamento completato!")
            except Exception:
                click.echo("✅ Aggiornamento completato!")

            click.echo("💡 Riavvia SIGMA-NEX per utilizzare " "la versione aggiornata")

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Errore durante git pull: {e}")
        click.echo(f"Output: {e.stdout}")
        click.echo(f"Error: {e.stderr}")
        click.echo("💡 Prova a risolvere i conflitti manualmente e riprova")


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
