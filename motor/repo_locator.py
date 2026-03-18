import json
from pathlib import Path


class RepoLocator:

    def __init__(self,
                 units_file="config/units.json",
                 system_file="config/system.json"):

        self.units_file = Path(units_file)
        self.system_file = Path(system_file)

        self.system_config = self._load_system_config()
        self.repos_base_path = Path(self.system_config["repos_base_path"])

        self.units = self._load_units()

    def _load_system_config(self):
        if not self.system_file.exists():
            raise FileNotFoundError(
                f"No s'ha trobat el fitxer de configuració del sistema: {self.system_file}"
            )

        with open(self.system_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_units(self):
        with open(self.units_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_units(self):
        return list(self.units.keys())

    def get_repo_path(self, unit):
        if unit not in self.units:
            raise ValueError(f"Unitat desconeguda: {unit}")

        repo_name = self.units[unit]["repo"]
        repo_path = self.repos_base_path / repo_name

        return repo_path

    def repo_exists(self, unit):
        repo_path = self.get_repo_path(unit)
        return repo_path.exists()

    def debug_print(self):
        for unit in self.get_units():
            repo = self.get_repo_path(unit)
            print(f"{unit} -> {repo}")