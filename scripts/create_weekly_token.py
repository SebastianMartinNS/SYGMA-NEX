#!/usr/bin/env python3
"""
SIGMA-NEX Weekly Token Creator
Script personale per creazione password settimanali per team sviluppo

Autore: Sebastian Martin
Repository: SYGMA-NEX
Versione: 1.0.0

Questo script genera password sicure settimanali per l'accesso
dev/admin al sistema SIGMA-NEX.
"""

import argparse
import hashlib
import secrets
import sys
from datetime import datetime, timedelta
from pathlib import Path


def show_token_banner():
    """Display SIGMA-NEX Token Generator ASCII banner."""
    banner = """
================================================================================
███████╗██╗ ██████╗ ███╗   ███╗ █████╗       ███╗   ██╗███████╗██╗  ██╗
██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗      ████╗  ██║██╔════╝╚██╗██╔╝
███████╗██║██║  ███╗██╔████╔██║███████║█████╗██╔██╗ ██║█████╗   ╚███╔╝
╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║╚════╝██║╚██╗██║██╔══╝   ██╔██╗
███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║      ██║ ╚████║███████╗██╔╝ ██╗
╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
================================================================================

              SIGMA-NEX Weekly Token Generator v1.0.0
              Sviluppato da: Martin Sebastian | Email: rootedlab6@gmail.com
              Repository: https://github.com/SebastianMartinNS/SYGMA-NEX

================================================================================
"""
    print(banner)


class WeeklyTokenGenerator:
    """Generatore token settimanali sicuri per SIGMA-NEX."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.tokens_dir = self.project_root / "tokens"
        self.ensure_tokens_directory()

    def ensure_tokens_directory(self):
        """Crea directory tokens se non esiste."""
        self.tokens_dir.mkdir(exist_ok=True)

        # Crea .gitignore per sicurezza
        gitignore_path = self.tokens_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("# Mai committare i token\n*\n!.gitignore\n")

    def get_current_week(self):
        """Ottiene numero settimana corrente."""
        today = datetime.now()
        year = today.year
        week = today.isocalendar()[1]
        return year, week

    def get_manual_password(self, username, length_min=8):
        """Richiede password manuale con validazione sicurezza e interfaccia migliorata."""
        print(f"\n[SECURE] Manual Password Input for {username.upper()}")
        print("="*50)
        print("Requirements:")
        print(f"  - Minimum {length_min} characters")
        print("  - Include uppercase, lowercase, numbers, and special characters")
        print("  - Will be hashed for security")

        while True:
            try:
                password = input(f"\nEnter {username} password: ").strip()
                if len(password) < length_min:
                    print(f"[ERROR] Password too short. Minimum {length_min} characters required.")
                    continue

                # Validazione sicurezza base
                has_upper = any(c.isupper() for c in password)
                has_lower = any(c.islower() for c in password)
                has_digit = any(c.isdigit() for c in password)
                has_special = any(c in "!@#$%^&*()-_=+[]{}|.<>?" for c in password)

                if not (has_upper and has_lower and has_digit and has_special):
                    print("[ERROR] Password must include uppercase, lowercase, numbers, and special characters")
                    continue

                confirm = input(f"Confirm {username} password: ").strip()
                if password != confirm:
                    print("[ERROR] Passwords don't match. Try again.")
                    continue

                print(f"[SUCCESS] {username} password accepted and secured")
                return password

            except KeyboardInterrupt:
                print("\n[WARNING] Password input cancelled")
                raise
            except EOFError:
                print("\n[WARNING] End of input detected")
                raise

    def generate_secure_password(self, length=16):
        """Genera password sicura con requisiti complessi."""
        # Caratteri disponibili (esclusi virgola, virgolette e altri problematici per PowerShell)
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special = "!@#$%^&*()-_=+[]{}|.<>?"  # Rimossa virgola e due punti

        # Almeno uno per categoria
        password_chars = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]

        # Riempie con caratteri casuali
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        # Mescola la password
        secrets.SystemRandom().shuffle(password_chars)
        return ''.join(password_chars)

    def create_weekly_hash(self, password, week_info):
        """Crea hash unico per la settimana."""
        year, week = week_info
        week_string = f"SIGMA-{year}-W{week:02d}-{password}"
        return hashlib.sha256(week_string.encode()).hexdigest()[:32]

    def generate_token_pair(self, manual_input=False):
        """Genera coppia token dev/admin per settimana corrente."""
        year, week = self.get_current_week()

        if manual_input:
            print("\n=== MANUAL PASSWORD INPUT ===")
            dev_password = self.get_manual_password("dev", 8)
            admin_password = self.get_manual_password("admin", 8)
        else:
            # Genera password sicure automaticamente
            dev_password = self.generate_secure_password(16)
            admin_password = self.generate_secure_password(20)

        # Crea hash SHA256 per autenticazione (da usare in auth.py)
        dev_auth_hash = hashlib.sha256(dev_password.encode()).hexdigest()
        admin_auth_hash = hashlib.sha256(admin_password.encode()).hexdigest()

        # Crea hash identificativi per tracking
        dev_hash = self.create_weekly_hash(dev_password, (year, week))
        admin_hash = self.create_weekly_hash(admin_password, (year, week))

        return {
            'year': year,
            'week': week,
            'dev_password': dev_password,
            'admin_password': admin_password,
            'dev_hash': dev_hash,
            'admin_hash': admin_hash,
            'dev_auth_hash': dev_auth_hash,      # Hash SHA256 per auth.py
            'admin_auth_hash': admin_auth_hash,  # Hash SHA256 per auth.py
            'generated_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
        }

    def save_tokens(self, tokens):
        """Salva token in file locale sicuro."""
        filename = f"tokens_Y{tokens['year']}_W{tokens['week']:02d}.txt"
        filepath = self.tokens_dir / filename

        content = f"""SIGMA-NEX Weekly Development Tokens
Generated: {tokens['generated_at']}
Expires: {tokens['expires_at']}
Week: {tokens['year']}-W{tokens['week']:02d}

==== DEVELOPMENT ACCESS ====
SIGMA_DEV_PASSWORD={tokens['dev_password']}

==== ADMIN ACCESS ====
SIGMA_ADMIN_PASSWORD={tokens['admin_password']}

==== USAGE INSTRUCTIONS FOR TEAM ====
1. Linux/Mac:
   export SIGMA_DEV_PASSWORD="{tokens['dev_password']}"
   export SIGMA_ADMIN_PASSWORD="{tokens['admin_password']}"

2. Windows PowerShell:
   $env:SIGMA_DEV_PASSWORD="{tokens['dev_password']}"
   $env:SIGMA_ADMIN_PASSWORD="{tokens['admin_password']}"

3. Windows CMD:
   set SIGMA_DEV_PASSWORD={tokens['dev_password']}
   set SIGMA_ADMIN_PASSWORD={tokens['admin_password']}

==== CODE UPDATE FOR MAINTAINER ====
Update sigma_nex/auth.py file with these hash values:

current_week_hashes = {{
    "dev": "{tokens['dev_auth_hash']}",  # Hash of {tokens['dev_password']}
    "admin": "{tokens['admin_auth_hash']}"   # Hash of {tokens['admin_password']}
}}

==== SECURITY NOTES ====
- Questi token scadono tra 7 giorni
- Non condividere via email/chat non sicure
- Usa canali sicuri per distribuzione team
- Aggiorna auth.py con gli hash prima della distribuzione

==== HASH VERIFICATION ====
Dev SHA256: {tokens['dev_auth_hash']}
Admin SHA256: {tokens['admin_auth_hash']}
Dev Tracking: {tokens['dev_hash']}
Admin Tracking: {tokens['admin_hash']}
"""

        filepath.write_text(content, encoding='utf-8')
        return filepath

    def create_env_file(self, tokens):
        """Crea file .env per uso immediato."""
        env_file = self.tokens_dir / ".env.weekly"

        content = f"""# SIGMA-NEX Weekly Environment Variables
# Generated: {tokens['generated_at']}
# Expires: {tokens['expires_at']}

SIGMA_DEV_PASSWORD={tokens['dev_password']}
SIGMA_ADMIN_PASSWORD={tokens['admin_password']}
"""

        env_file.write_text(content, encoding='utf-8')
        return env_file

    def show_summary(self, tokens, token_file, env_file):
        """Mostra riassunto generazione token con interfaccia migliorata."""
        print(f"\n{'='*70}")
        print("                    SIGMA-NEX WEEKLY TOKEN GENERATION")
        print(f"{'='*70}")
        print(f"Week: {tokens['year']}-W{tokens['week']:02d}")
        print(f"Generated: {tokens['generated_at']}")
        print(f"Expires: {tokens['expires_at']}")
        print("\nFiles created:")
        print(f"  - Token file: {token_file}")
        print(f"  - Env file: {env_file}")

        print(f"\n{'='*70}")
        print("                    QUICK SETUP INSTRUCTIONS")
        print(f"{'='*70}")

        print("\n1. Linux/Mac:")
        print(f"   export SIGMA_DEV_PASSWORD=\"{tokens['dev_password']}\"")
        print(f"   export SIGMA_ADMIN_PASSWORD=\"{tokens['admin_password']}\"")

        print("\n2. Windows PowerShell:")
        print(f"   $env:SIGMA_DEV_PASSWORD=\"{tokens['dev_password']}\"")
        print(f"   $env:SIGMA_ADMIN_PASSWORD=\"{tokens['admin_password']}\"")

        print("\n3. Windows CMD:")
        print(f"   set SIGMA_DEV_PASSWORD={tokens['dev_password']}")
        print(f"   set SIGMA_ADMIN_PASSWORD={tokens['admin_password']}")

        print(f"\n{'='*70}")
        print("                    SECURITY REMINDERS")
        print(f"{'='*70}")
        print("- Tokens expire automatically in 7 days")
        print("- Use secure channels for team distribution")
        print("- Never commit token files to repository")
        print("- tokens/ directory is already in .gitignore")

        print(f"\n{'='*70}")
        print("                    TEAM DISTRIBUTION")
        print(f"{'='*70}")
        print("Send to development team via secure channels:")
        print("- Encrypted email")
        print("- Secure messaging app")
        print("- Private shared drive")
        print("- Direct secure handoff")

        print(f"\n{'='*70}")
        print("                    NEXT STEPS")
        print(f"{'='*70}")
        print("1. Update sigma_nex/auth.py with the new hashes")
        print("2. Distribute credentials to development team")
        print("3. Test authentication with new tokens")
        print("4. Schedule next token rotation in 7 days")

    def cleanup_old_tokens(self, keep_weeks=2):
        """Rimuove token vecchi per sicurezza con feedback migliorato."""
        current_year, current_week = self.get_current_week()
        removed_count = 0

        for token_file in self.tokens_dir.glob("tokens_Y*_W*.txt"):
            try:
                # Estrai anno e settimana dal nome file
                name_parts = token_file.stem.split('_')
                file_year = int(name_parts[1][1:])  # Rimuove 'Y'
                file_week = int(name_parts[2][1:])  # Rimuove 'W'

                # Calcola età in settimane
                current_total_weeks = current_year * 52 + current_week
                file_total_weeks = file_year * 52 + file_week
                weeks_old = current_total_weeks - file_total_weeks

                if weeks_old > keep_weeks:
                    token_file.unlink()
                    removed_count += 1
                    print(f"   [REMOVED] Removed old token: {token_file.name}")

            except (ValueError, IndexError):
                # Nome file non valido, ignora
                continue

        if removed_count > 0:
            print(f"[SUCCESS] Cleaned up {removed_count} old token files")
        else:
            print("[INFO] No old token files to clean up")


def main():
    """Funzione principale con interfaccia migliorata."""
    # Mostra banner di benvenuto
    show_token_banner()

    parser = argparse.ArgumentParser(
        description="SIGMA-NEX Weekly Token Generator - Secure Development Access",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_weekly_token.py                    # Generate new weekly tokens
  python create_weekly_token.py --cleanup          # Generate + cleanup old tokens
  python create_weekly_token.py --cleanup-only     # Only cleanup old tokens
  python create_weekly_token.py --quiet            # Generate without summary
  python create_weekly_token.py --manual           # Manually input passwords

Security Notes:
  - Tokens expire automatically after 7 days
  - Use secure channels for team distribution
  - Never commit token files to repository
  - tokens/ directory is automatically gitignored
        """
    )

    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Cleanup old token files after generation'
    )

    parser.add_argument(
        '--cleanup-only',
        action='store_true',
        help='Only cleanup old tokens, do not generate new ones'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode - minimal output'
    )

    parser.add_argument(
        '--manual', '-m',
        action='store_true',
        help='Manually input passwords instead of auto-generation'
    )

    parser.add_argument(
        '--keep-weeks',
        type=int,
        default=2,
        help='Number of weeks to keep old tokens (default: 2)'
    )

    args = parser.parse_args()

    try:
        generator = WeeklyTokenGenerator()

        if args.cleanup_only:
            if not args.quiet:
                print("[CLEANUP] Cleaning up old token files...")
            generator.cleanup_old_tokens(args.keep_weeks)
            if not args.quiet:
                print("[SUCCESS] Cleanup completed successfully!")
            return

        # Genera nuovi token
        if not args.quiet:
            mode = "manual input" if args.manual else "secure auto-generation"
            print(f"[SECURE] Generating weekly tokens for SIGMA-NEX using {mode}...")
            print("   This may take a few seconds...")

        tokens = generator.generate_token_pair(manual_input=args.manual)
        token_file = generator.save_tokens(tokens)
        env_file = generator.create_env_file(tokens)

        if not args.quiet:
            generator.show_summary(tokens, token_file, env_file)
            print("\n[SUCCESS] Token generation completed successfully!")
        else:
            print(f"[SUCCESS] Tokens generated: {token_file}")
            print(f"[FILE] Env file: {env_file}")

        # Cleanup se richiesto
        if args.cleanup:
            if not args.quiet:
                print("\n[CLEANUP] Cleaning up old tokens...")
            generator.cleanup_old_tokens(args.keep_weeks)
            if not args.quiet:
                print("[SUCCESS] Cleanup completed!")

    except KeyboardInterrupt:
        print("\n\n[WARNING] Operation cancelled by user")
        print("   No files were created or modified")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("   Please check your permissions and try again")
        print("   If the problem persists, contact the development team")
        sys.exit(1)


if __name__ == "__main__":
    main()
