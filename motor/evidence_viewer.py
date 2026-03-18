import subprocess
from pathlib import Path


class EvidenceViewer:

    def show(self, file_path, file_type):

        file_path = Path(file_path)

        if not file_path.exists():
            print("⚠ Fitxer no existeix")
            return

        if file_type in ["markdown", "sql", "text"]:
            self._show_text(file_path)

        elif file_type in ["image", "png", "jpg", "jpeg"]:
            self._open_external(file_path)

        elif file_type in ["diagram"]:
            self._open_external(file_path)

        elif file_type == "pdf":
            self._open_external(file_path)

        else:
            print("Tipus desconegut. Obrint externament.")
            self._open_external(file_path)


    def _show_text(self, file_path):

        print("\n----- CONTINGUT FITXER -----\n")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            print(f.read())

        print("\n----- FI FITXER -----\n")


    def _open_external(self, file_path):

        try:
            subprocess.run(["xdg-open", str(file_path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print("No s'ha pogut obrir el fitxer:", e)