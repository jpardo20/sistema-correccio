import json

from pathlib import Path
from motor.tools.grading import ask_score_and_comment

def check_act_014_json_concepts(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT014 JSON concepts")

    structures = []

    for path in repo_path.rglob("*.json"):
        try:
            with open(path) as f:
                data = json.load(f)

            if isinstance(data, dict) or isinstance(data, list):
                structures.append(str(path))

        except Exception:
            pass

    score = 10 if structures else 0

    corrections[repo_name]["ACT_014_JSON_CONCEPTS"] = {
        "score": score,
        "max_score": 10,
        "files": structures
    }

    save_corrections()

    print(f"✔ ACT014 -> {score}/10")
