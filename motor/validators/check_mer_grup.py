from datetime import datetime
from pathlib import Path
import subprocess

from motor.results_manager import GROUP_MEMBER_ID
from motor.tools.grading import ask_score_and_comment


def open_image(path):
    try:
        subprocess.run(["xdg-open", str(path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("⚠ No s'ha pogut obrir la imatge")


def check_mer_grup(activity, evidence, corrections, save_corrections):
    print("\n[MER GRUP]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    group_bucket = repo_bucket.setdefault(GROUP_MEMBER_ID, {})
    if activity_id in group_bucket:
        print("✔ MER de grup ja corregit")
        return

    docs_dir = repo_path / "docs"
    expected_png = docs_dir / f"{repo_name}-mer.png"
    expected_xml = docs_dir / f"{repo_name}-mer.xml"

    png_files = []
    xml_files = []
    status = "NOT_FOUND"

    if expected_png.exists():
        png_files.append(expected_png)
    if expected_xml.exists():
        xml_files.append(expected_xml)
    if png_files or xml_files:
        status = "OK_LOCATION"
    else:
        png_files = list(repo_path.rglob("*mer*.png"))
        xml_files = list(repo_path.rglob("*mer*.xml"))
        if png_files or xml_files:
            status = "WRONG_LOCATION"

    print({
        "OK_LOCATION": "✔ MER de grup al lloc correcte",
        "WRONG_LOCATION": "⚠ MER de grup trobat fora de lloc",
        "NOT_FOUND": "❌ MER de grup no trobat",
    }[status])

    if png_files:
        print("PNG trobats:")
        for p in png_files:
            print(" ", p)
        open_image(png_files[0])
    if xml_files:
        print("XML trobats:")
        for x in xml_files:
            print(" ", x)

    score, comment = ask_score_and_comment()
    group_bucket[activity_id] = {
        "score": score,
        "max_score": 10,
        "comment": comment,
        "structure_status": status,
        "files_png": [str(p) for p in png_files],
        "files_xml": [str(x) for x in xml_files],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    save_corrections()
