# Arquitectura del sistema de correcció de repositoris

## 1. Objectiu del sistema

Aquest projecte implementa un **motor d’avaluació assistida de repositoris Git d’alumnes**.

El sistema permet:

- detectar evidències dins dels repositoris dels alumnes
- mostrar-les al docent
- registrar una nota i un comentari
- associar les activitats a **Resultats d’Aprenentatge (RA)**
- calcular notes per **RA i mòdul**

El sistema està dissenyat per funcionar amb:

- diferents **cicles formatius** (SMX, DAM, etc.)
- diferents **mòduls**
- repositoris **individuals o de grup**
- activitats de diferents tipus (fitxer, imatge, SQL, etc.)

L’objectiu principal és que el sistema sigui **escalable, reutilitzable i mantenible durant diversos cursos acadèmics**.

---

## 2. Principi d’arquitectura

El sistema segueix una separació clara entre:

```bash
ENGINE (motor tècnic)
CONFIGURATION (model pedagògic)
```

### Motor tècnic

Implementat en Python.

Responsable de:

- localitzar repositoris
- detectar evidències
- mostrar evidències
- demanar notes
- guardar correccions

El motor **no coneix el model pedagògic**.

---

### Configuració pedagògica

Definida mitjançant fitxers JSON.

Permet definir:

- cicles
- mòduls
- resultats d’aprenentatge
- activitats
- unitats d’avaluació

Aquesta capa pot ser modificada per docents **sense tocar el codi Python**.

---

## 3. Estructura del repositori

```bash
sistema-correccio/
│
├── main.py
│
├── motor/
│   ├── repo_locator.py
│   ├── activities_loader.py
│   └── evidence_detector.py
│
├── detectors/
│
├── config/
│   ├── cycles.json
│   ├── modules.json
│   ├── ras.json
│   ├── assignments.json
│   └── units.json
│
├── results/
│
├── tools/
│
└── docs/
    ├── ARCHITECTURE.md
    └── PROJECT_LOG.md
```

---

## 4. Components del motor

### RepoLocator

Responsable de localitzar el repositori associat a una unitat d’avaluació.

Entrada:

```bash
unit
```

Sortida:

```bash
ruta del repositori
```

---

### ActivitiesLoader

Carrega la definició de les activitats des de:

```bash
config/assignments.json
```

Cada activitat defineix:

- identificador
- tipus d’evidència
- ruta de l’evidència
- descripció

---

### EvidenceDetector

Responsable de localitzar evidències dins del repositori.

Pot retornar:

```bash
OK_LOCATION
WRONG_LOCATION
NOT_FOUND
```

---

### CorrectionEngine

Gestiona el procés interactiu de correcció.

Funcions principals:

- mostrar evidència
- demanar nota
- demanar comentari
- guardar correcció

---

### CorrectionsStore

Guarda els resultats de la correcció en:

```bash
corrections.json
```

---

## 5. Model de configuració pedagògica

La configuració pedagògica es defineix a la carpeta:

```bash
config/
```

### cycles.json

Defineix els cicles formatius.

Exemple:

```bash
SMX
DAM
```

---

### modules.json

Defineix els mòduls associats a cada cicle.

Exemple:

```bash
0373 Aplicacions Ofimàtiques
0485 Bases de Dades
```

---

### ras.json

Defineix els resultats d’aprenentatge de cada mòdul.

---

### assignments.json

Defineix les activitats a avaluar.

Cada activitat especifica:

- RA associat
- tipus d’evidència
- ruta dins del repositori
- descripció

---

### units.json

Defineix les **unitats d’avaluació**.

Una unitat pot ser:

```bash
alumne
grup
```

Cada unitat indica:

- repositori associat
- membres del grup (si escau)

---

## 6. Flux de correcció

El flux d’execució del sistema és:

```bash
1 carregar configuració
2 carregar unitats d’avaluació
3 per cada unitat
4   localitzar repositori
5   per cada activitat
6       detectar evidència
7       mostrar evidència
8       demanar nota
9       guardar correcció
```

---

## 7. Avantatges del model

Aquest model permet:

- separar **pedagogia i implementació**
- afegir activitats **sense modificar el motor**
- reutilitzar el motor entre **diferents cicles**
- escalar el sistema durant **diversos cursos**

---

## 8. Filosofia del projecte

Aquest sistema es construeix amb els següents principis:

- simplicitat
- modularitat
- configuració externa
- reutilització
- mantenibilitat a llarg termini

L’objectiu és disposar d’una eina que permeti **avaluar repositoris d’alumnes de manera sistemàtica i eficient**.