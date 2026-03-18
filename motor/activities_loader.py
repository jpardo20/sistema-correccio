import json
from pathlib import Path


class ActivitiesLoader:

    def __init__(self, assignments_file="config/assignments.json"):
        self.assignments_file = Path(assignments_file)
        self.activities = self._load_assignments()

    def _load_assignments(self):
        if not self.assignments_file.exists():
            raise FileNotFoundError(
                f"No s'ha trobat el fitxer d'activitats: {self.assignments_file}"
            )

        with open(self.assignments_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("assignments.json ha de contenir una llista d'activitats")

        for activity in data:
            if "id" not in activity:
                raise ValueError("Una activitat no té 'id'")
            if "path" not in activity:
                raise ValueError(f"L'activitat {activity['id']} no té 'path'")

        return data

    def get_activities(self):
        """
        Retorna la llista completa d'activitats.
        """
        return self.activities

    def get_activity(self, activity_id):
        """
        Retorna una activitat concreta pel seu id.
        """
        for activity in self.activities:
            if activity["id"] == activity_id:
                return activity

        raise ValueError(f"Activitat desconeguda: {activity_id}")

    def resolve_activity_path(self, activity, repo_path, unit):
        """
        Construeix la ruta real del fitxer d'evidència.

        Suporta placeholders:
        {unit}
        """

        raw_path = activity["path"]

        resolved = raw_path.replace("{unit}", unit)

        return repo_path / resolved