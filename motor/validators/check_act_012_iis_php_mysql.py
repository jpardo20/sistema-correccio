from pathlib import Path
from motor.tools.grading import ask_score_and_comment

def check_act_012_iis_php_mysql(repo_path, repo_name, corrections, save_corrections):

    print("🔎 ACT012 IIS/PHP/MySQL")

    evidence = []

    for path in repo_path.rglob("*.php"):
        try:
            content = path.read_text(errors="ignore").lower()

            if "pdo" in content or "mysqli" in content or "mysql" in content:
                evidence.append(str(path))

        except Exception:
            pass

    score = 10 if evidence else 0

    corrections[repo_name]["ACT_012_IIS_PHP"] = {
        "score": score,
        "max_score": 10,
        "files": evidence
    }

    save_corrections()

    print(f"✔ ACT012 -> {score}/10")
