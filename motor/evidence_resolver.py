from pathlib import Path


class EvidenceResolver:

    def __init__(self):
        pass

    def resolve(self, repo_path, activity, unit):

        expected_path = activity["path"].replace("{unit}", unit)
        expected_full = repo_path / expected_path

        if expected_full.exists():
            return {
                "exists": True,
                "name_status": "OK_NAME",
                "location_status": "OK_LOCATION",
                "path": expected_full
            }

        # buscar mateix nom en qualsevol lloc
        expected_name = Path(expected_path).name

        for p in repo_path.rglob(expected_name):
            return {
                "exists": True,
                "name_status": "OK_NAME",
                "location_status": "WRONG_LOCATION",
                "path": p
            }

        # buscar per extensió
        ext = Path(expected_name).suffix

        candidates = list(repo_path.rglob(f"*{ext}"))

        if candidates:
            return {
                "exists": True,
                "name_status": "WRONG_NAME",
                "location_status": "UNKNOWN",
                "candidates": candidates
            }

        return {
            "exists": False
        }