from pathlib import Path


def run_generic_detector(repo_path, repo_name, activity_id, evidences, corrections, save_corrections):
    found = []
    for item in evidences:
        p = Path(repo_path) / item["path"]
        if p.exists():
            found.append(str(p))

    score = 10 if found else 0
    corrections.setdefault(repo_name, {})[activity_id] = {
        "score": score,
        "max_score": 10,
        "files": found,
    }
    save_corrections()


EVIDENCES = [
    {"name": "IIS configurat", "path": "docs/iis-config.png", "type": "image"},
    {"name": "Aplicació funcionant", "path": "docs/aplicacio-funcionant.png", "type": "image"},
    {"name": "Estructura MySQL", "path": "docs/mysql-estructura.png", "type": "image"},
    {"name": "SQL base de dades", "path": "docs/database.sql", "type": "sql"},
    {"name": "README", "path": "README.md", "type": "text"},
]


def check_act_012_webapp(repo_path, repo_name, corrections, save_corrections):
    run_generic_detector(
        repo_path,
        repo_name,
        "ACT_012_WEBAPP",
        EVIDENCES,
        corrections,
        save_corrections,
    )
