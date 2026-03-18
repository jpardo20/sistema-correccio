import xml.etree.ElementTree as ET

from pathlib import Path

def normalize(name):
    return name.lower().rstrip("s")


# 🔥 MODE 1: parser estructural (bo si l'alumne ho fa bé)
def extract_tables_structural(root):

    tables = set()

    for cell in root.iter("mxCell"):
        style = cell.attrib.get("style", "")
        value = cell.attrib.get("value", "")

        if "shape=table" in style and value:
            tables.add(value.strip())

    return tables


# 🔥 MODE 2: fallback textual (robust)
def extract_all_values(root):

    values = []

    for cell in root.iter("mxCell"):
        value = cell.attrib.get("value")
        if value:
            values.append(value.strip())

    return values


# 🔥 FUNCIÓ PRINCIPAL
def extract_tables_from_mr(xml_file, sql_tables=None):

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception:
        return set()

    # 1️⃣ INTENT ESTRUCTURAL
    structural = extract_tables_structural(root)

    if structural:
        return {t.upper() for t in structural}

    # 2️⃣ FALLBACK TEXTUAL (🔥 el teu plantejament)
    if sql_tables:
        values = extract_all_values(root)
        values_norm = [normalize(v) for v in values]

        found = set()

        for table in sql_tables:
            if normalize(table) in values_norm:
                found.add(table)

        return found

    return set()


def find_model_relacional(repo_path: Path) -> Path | None:
    """
    Busca un fitxer de model relacional dins del repo.
    Prioritza XML de diagrams.net però accepta altres.
    """

    candidates = list(repo_path.rglob("*mr*.xml")) + \
                 list(repo_path.rglob("*model*.xml")) + \
                 list(repo_path.rglob("*relacional*.xml"))

    if not candidates:
        candidates = list(repo_path.rglob("*.xml"))

    return candidates[0] if candidates else None

import xml.etree.ElementTree as ET

def validate_diagrams_xml(xml_path):
    """
    Comprova si l'XML és vàlid (mínimament parsejable)
    """
    try:
        ET.parse(xml_path)
        return "OK"
    except Exception as e:
        return f"INVALID XML: {e}"