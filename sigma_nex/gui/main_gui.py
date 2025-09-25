import os
import sys
import threading

try:
    import customtkinter as ctk
except ImportError as e:
    # Allow tests to simulate missing dependency or handle when customtkinter is not installed
    ctk = None
    print(f"[WARNING] customtkinter not available: {e}")
except Exception as e:
    # Handle other potential import errors
    ctk = None
    print(f"[WARNING] Error importing customtkinter: {e}")
from tkinter import messagebox, filedialog


# Imposta la working directory alla root del progetto
def set_project_root():
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    os.chdir(base_path)
    # Insert project root at position 0 for imports
    try:
        sys.path.insert(0, base_path)
    except Exception:
        pass
    print(f"[DEBUG] Working directory impostata a: {base_path}")


set_project_root()

# Importa core
from sigma_nex.config import load_config
from sigma_nex.core.runner import Runner
from sigma_nex.data_loader import DataLoader

# Tema GUI
if ctk is not None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")


class SigmaNexGUI(ctk.CTk if ctk is not None else object):
    def __init__(self):
        if ctk is None:
            raise ImportError(
                "customtkinter is not available. Please install it with: pip install customtkinter"
            )

        super().__init__()
        self.title("SIGMA-NEX :: Interfaccia Cognitiva")
        self.geometry("760x560")
        self.resizable(False, False)

        try:
            self.cfg = load_config()
            self.runner = Runner(self.cfg, secure=False)
        except Exception as e:
            messagebox.showerror("Errore Critico", str(e))
            self.destroy()
            return

        self.progress_label = ctk.CTkLabel(self, text="", font=("Courier", 14))
        self.progress_running = False

        # Interfaccia
        self.title_label = ctk.CTkLabel(
            self, text="SIGMA-NEX [modalità offline]", font=("Orbitron", 24)
        )
        self.title_label.pack(pady=10)

        self.command_entry = ctk.CTkEntry(
            self, placeholder_text="Inserisci comando...", width=500
        )
        self.command_entry.pack(pady=5)
        self.command_entry.bind("<Return>", lambda event: self.process_command())

        self.send_button = ctk.CTkButton(
            self, text="Invia", command=self.process_command
        )
        self.send_button.pack(pady=5)

        self.output_box = ctk.CTkTextbox(self, width=720, height=260)
        self.output_box.pack(pady=10)

        self.progress_label.pack(pady=2)

        # Pulsanti funzionali
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=5)

        self.selfcheck_button = ctk.CTkButton(
            self.button_frame, text="Self-Check", command=self.run_selfcheck
        )
        self.selfcheck_button.pack(side="left", padx=5)

        self.selfheal_button = ctk.CTkButton(
            self.button_frame, text="Self-Heal .py", command=self.run_selfheal
        )
        self.selfheal_button.pack(side="left", padx=5)

        self.loadfw_button = ctk.CTkButton(
            self.button_frame, text="Carica Framework", command=self.run_load_framework
        )
        self.loadfw_button.pack(side="left", padx=5)

        self.exit_button = ctk.CTkButton(self, text="Chiudi", command=self.destroy)
        self.exit_button.pack(pady=5)

    # -------------------- Barra di Progresso --------------------
    def show_progress(self):
        self.progress_running = True
        symbols = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"]
        idx = 0
        while self.progress_running:
            self.progress_label.configure(
                text=f"Elaborazione {symbols[idx % len(symbols)]*5}"
            )
            self.progress_label.update()
            idx += 1
            self.after(100)

    def stop_progress(self):
        self.progress_running = False
        self.progress_label.configure(text="")

    def run_background(self, func, *args):
        def wrapper():
            self.show_progress()
            try:
                func(*args)
            finally:
                self.stop_progress()

        threading.Thread(target=wrapper, daemon=True).start()

    # -------------------- Comandi principali --------------------
    def process_command(self):
        comando = self.command_entry.get().strip()
        if not comando:
            return

        self.output_box.insert("end", f"> {comando}\n")
        prompt = self.runner.system_prompt
        full_prompt = f"{prompt}\n\nUtente: {comando}\nAssistant:"

        def execute():
            risposta = self.runner._send_with_progress(full_prompt)
            self.output_box.insert("end", f"{risposta}\n\n")
            self.output_box.see("end")
            self.runner.history.append(f"Utente: {comando}")
            self.runner.history.append(f"Assistant: {risposta}")

        self.run_background(execute)
        self.command_entry.delete(0, "end")

    def run_selfcheck(self):
        def check():
            self.runner.self_check()
            self.output_box.insert("end", "[✔] Ollama verificato.\n\n")
            self.output_box.see("end")

        self.run_background(check)

    def run_selfheal(self):
        filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not filepath:
            return

        def heal():
            result = self.runner.self_heal_file(filepath)
            self.output_box.insert("end", f"{result}\n\n")
            self.output_box.see("end")

        self.run_background(heal)

    def run_load_framework(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        def load():
            count = DataLoader().load(filepath)
            self.output_box.insert(
                "end", f"[✔] Caricati {count} moduli dal file {filepath}\n\n"
            )
            self.output_box.see("end")

        self.run_background(load)


def main():
    try:
        if ctk is None:
            print("Error: customtkinter is not available.")
            print("Please install it with: pip install customtkinter")
            return False

        app = SigmaNexGUI()
        app.mainloop()
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install customtkinter with: pip install customtkinter")
        return False
    except Exception as e:
        print(f"GUI error: {e}")
        return False


if __name__ == "__main__":
    main()
