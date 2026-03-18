from datetime import datetime
from pathlib import Path

from motor.tools.grading import ask_score_and_comment
from motor.tools.sql_mr_consistency import compare_mr_sql
from motor.tools.sql_schema_analyzer import analyze_sql_file, find_sql_candidates


def _choose_sql_analysis(analyses):
    if not analyses:
        return None

    print("\nANÀLISI DELS SQL TROBATS\n")
    for i, analysis in enumerate(analyses):
        print(f"[{i}] {Path(analysis.file).name}")
        print(f"    taules: {len(analysis.tables)}")
        print(f"    pk: {analysis.primary_keys_count}")
        print(f"    fk: {analysis.foreign_keys_count}")
        print(f"    score estimat: {analysis.estimated_score}\n")

    best_index = max(range(len(analyses)), key=lambda i: analyses[i].estimated_score)
    print(f"✔ Recomanat: [{best_index}]")

    raw = input("\nEscull fitxer (ENTER = recomanat): ").strip()
    if raw == "":
        return analyses[best_index]
    try:
        selected = int(raw)
        if 0 <= selected < len(analyses):
            return analyses[selected]
    except ValueError:
        pass

    print("Opció no vàlida, es farà servir la recomanada")
    return analyses[best_index]


def check_sql_schema(activity, evidence, corrections, save_corrections):
    print("\n[SQL SCHEMA v2]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    member = evidence.get("member", {})
    member_id = member.get("id") or evidence.get("unit")
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    member_bucket = repo_bucket.setdefault(member_id, {})
    if activity_id in member_bucket:
        print("✔ SQL ja corregit")
        return

    expected_relative_path = activity.get("path")
    status, sql_files = find_sql_candidates(repo_path, repo_name, expected_relative_path)

    print({
        "OK_LOCATION": "✔ SQL trobat al lloc correcte",
        "WRONG_LOCATION": "⚠ SQL trobat però fora de lloc",
        "NOT_FOUND": "❌ SQL no trobat",
    }[status])

    if sql_files:
        print("\nFitxers SQL trobats:")
        for f in sql_files:
            print(" ", f)

    analyses = []
    for sql_file in sql_files:
        try:
            analyses.append(analyze_sql_file(sql_file))
        except Exception as exc:
            print(f"⚠ No s'ha pogut analitzar {sql_file}: {exc}")

    selected = _choose_sql_analysis(analyses)

    if selected is None:
        print("\nANÀLISI SQL")
        print("No s'ha pogut seleccionar cap fitxer SQL")
        consistency = compare_mr_sql(repo_path, [])
        default_score = 0
    else:
        print("\nANÀLISI SQL")
        print("Taules detectades:", len(selected.tables))
        print("PRIMARY KEY:", selected.primary_keys_count)
        print("FOREIGN KEY:", selected.foreign_keys_count)
        if selected.tables:
            print("\nTaules:")
            for table in selected.tables:
                print(" -", table)

        consistency = compare_mr_sql(repo_path, selected.tables)
        sql_score = selected.estimated_score
        mr_score = consistency.score

        # combinació simple (mitjana)
        default_score = round((sql_score + mr_score) / 2)

    print("\nCOHERÈNCIA MR ↔ SQL")
    if consistency.mr_file:
        print("Model relacional detectat:")
        print(" ", consistency.mr_file)
        if consistency.mr_status == "OK":
            print("✔ XML vàlid de diagrams.net")
        elif consistency.mr_status == "INVALID_XML":
            print("❌ XML corrupte")
        elif consistency.mr_status == "NOT_DIAGRAMS":
            print("⚠ XML vàlid però no sembla de diagrams.net")

        print(f"Taules SQL: {len(consistency.sql_tables)}")
        print(f"Taules trobades al MR: {len(consistency.matching_tables)}")
        if consistency.missing_in_mr:
            print("⚠ Taules del SQL que NO apareixen al MR:")
            for table in consistency.missing_in_mr:
                print(" ", table)
        else:
            print("✔ Totes les taules del SQL apareixen al MR")
    else:
        print("⚠ Model relacional no trobat")

    score, comment = ask_score_and_comment(default_score=default_score)

    payload = {
        "score": score,
        "max_score": 10,
        "comment": comment,
        "structure_status": status,
        "files": [str(f) for f in sql_files],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "analysis": {
            "selected_file": selected.file if selected else None,
            "tables_detected": selected.tables if selected else [],
            "tables_count": len(selected.tables) if selected else 0,
            "primary_keys_count": selected.primary_keys_count if selected else 0,
            "foreign_keys_count": selected.foreign_keys_count if selected else 0,
            "estimated_score": default_score,
            "candidates": [analysis.to_dict() for analysis in analyses],
        },
        "mr_sql_consistency": consistency.to_dict(),
    }

    member_bucket[activity_id] = payload
    save_corrections()
