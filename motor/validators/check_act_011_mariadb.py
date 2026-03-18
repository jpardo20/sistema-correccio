from pathlib import Path
from motor.tools.grading import ask_score_and_comment

def check_act_011_mariadb(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT011 MariaDB")

    evidence = []

    for path in repo_path.rglob("*.sql"):
        try:
            content = path.read_text(errors="ignore").lower()

            if "create table" in content or "mariadb" in content or "mysql" in content:
                evidence.append(str(path))

        except Exception:
            pass

    score = 10 if evidence else 0

    corrections[repo_name]["ACT_011_MARIADB"] = {
        "score": score,
        "max_score": 10,
        "files": evidence
    }

    save_corrections()

    print(f"✔ ACT011 -> {score}/10")
