import subprocess
from pathlib import Path
from datetime import datetime

from motor.results_manager import GROUP_MEMBER_ID
from motor.tools.grading import ask_score_and_comment


def open_image(path):
    try:
        subprocess.run(["xdg-open", str(path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("⚠ No s'ha pogut obrir la imatge")


def check_mr_grup(activity, evidence, corrections, save_corrections):
    print("\n[MODEL RELACIONAL GRUP]")

    repo_path = Path(evidence["repo_path"])
    repo_name = evidence["repo_name"]
    activity_id = activity["id"]

    repo_bucket = corrections.setdefault(repo_name, {})
    group_bucket = repo_bucket.setdefault(GROUP_MEMBER_ID, {})
    if activity_id in group_bucket:
        print("✔ MR de grup ja corregit")
        return

    docs_dir = repo_path / "docs"
    expected_png = docs_dir / f"{repo_name}-mr.png"
    expected_xml = docs_dir / f"{repo_name}-mr.xml"

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
        png_alt = list(docs_dir.glob("*mr*.png")) if docs_dir.exists() else []
        xml_alt = list(docs_dir.glob("*mr*.xml")) if docs_dir.exists() else []
        if not png_alt and not xml_alt and docs_dir.exists():
            png_alt = list(docs_dir.glob("*rel*.png"))
            xml_alt = list(docs_dir.glob("*rel*.xml"))
        if not png_alt and not xml_alt:
            png_alt = list(repo_path.rglob("*.png"))
            xml_alt = list(repo_path.rglob("*.xml"))
        if png_alt or xml_alt:
            status = "WRONG_LOCATION"
            png_files = png_alt
            xml_files = xml_alt

    print({
        "OK_LOCATION": "✔ Model relacional al lloc correcte",
        "WRONG_LOCATION": "⚠ Model relacional trobat però fora de lloc",
        "NOT_FOUND": "❌ Model relacional no trobat",
    }[status])

    mer_entry = group_bucket.get("MER_GRUP")
    if mer_entry and mer_entry.get("files_png"):
        mer_path = Path(mer_entry["files_png"][0])
        if mer_path.exists():
            print("\nMER de referència:", mer_path)
            open_image(mer_path)

    if png_files:
        print("\nMR trobats:")
        for p in png_files:
            print(" ", p)
        open_image(png_files[0])
    if xml_files:
        print("\nXML trobats:")
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
