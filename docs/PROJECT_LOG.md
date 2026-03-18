# Project Log — Sistema de correcció de repositoris

Aquest document registra les **decisions tècniques i d’arquitectura** preses durant el desenvolupament del sistema de correcció de repositoris.

L’objectiu és mantenir un **historial clar de l’evolució del projecte**, per facilitar:

- manteniment del sistema
- incorporació de nous docents
- continuïtat del projecte en cursos futurs

---

# 2026-03-18 — Creació del repositori

S'inicia el projecte **sistema-correccio** amb l'objectiu de crear un motor genèric per avaluar repositoris Git d'alumnes.

Motivació:

Els scripts existents per corregir repositoris:

- estaven molt lligats a activitats concretes
- eren difícils de mantenir
- no permetien reutilització entre mòduls o cicles

Per aquest motiu es decideix crear un **sistema modular i configurable**.

---

# 2026-03-18 — Separació entre motor i configuració pedagògica

Es decideix separar clarament dues capes:

```
ENGINE (Python)
CONFIGURATION (JSON)
```

## Motor

Responsable de:

- detectar evidències
- mostrar evidències
- demanar nota
- guardar correcció

El motor **no coneix la pedagogia del curs**.

---

## Configuració

La configuració del sistema es defineix en fitxers JSON.

Això permet que un docent pugui modificar:

- activitats
- mòduls
- RAs
- alumnes

sense modificar el codi.

---

# 2026-03-18 — Introducció del concepte "Unitat d'avaluació"

El sistema utilitza el concepte abstracte de:

```
UNITAT D'AVALUACIÓ
```

Una unitat pot ser:

```
alumne
grup
```

El motor no necessita saber quin tipus és.

Només necessita saber:

- quin repositori està associat
- quines activitats cal avaluar

Aquesta abstracció permet suportar:

- repositoris individuals
- repositoris de grup
- altres estructures futures

sense modificar el motor.

---

# 2026-03-18 — Estructura inicial del projecte

S’estableix la següent estructura de carpetes:

```
sistema-correccio/
│
├── main.py
│
├── motor/
│
├── detectors/
│
├── config/
│
├── results/
│
├── tools/
│
└── docs/
```

## motor/

Implementa la lògica del sistema.

## detectors/

Conté els detectors d’evidències.

## config/

Conté tota la configuració pedagògica.

## results/

Conté els resultats de correcció.

## tools/

Scripts auxiliars.

## docs/

Documentació del sistema.

---

# 2026-03-18 — Definició dels fitxers de configuració

Es defineixen els següents fitxers JSON:

```
config/
├── cycles.json
├── modules.json
├── ras.json
├── assignments.json
└── units.json
```

Cada fitxer té una responsabilitat clara.

---

## cycles.json

Defineix els cicles formatius.

Exemple:

```
SMX
DAM
```

---

## modules.json

Defineix els mòduls de cada cicle.

---

## ras.json

Defineix els Resultats d’Aprenentatge.

---

## assignments.json

Defineix les activitats a avaluar.

Cada activitat especifica:

- identificador
- RA associat
- tipus d’evidència
- ruta dins del repositori
- descripció

---

## units.json

Defineix les unitats d’avaluació.

Pot incloure:

- alumnes
- grups
- repositoris associats

---

# 2026-03-18 — Flux general del sistema

El flux de funcionament del motor és:

```
1 carregar configuració
2 carregar unitats
3 per cada unitat
4   localitzar repositori
5   per cada activitat
6       detectar evidència
7       mostrar evidència
8       demanar nota
9       guardar correcció
```

Aquest flux està implementat a:

```
main.py
```

---

# 2026-03-18 — Model d’evidències

Cada activitat defineix un **tipus d’evidència**.

Exemples:

```
file
image
sql
text
```

El motor utilitza aquesta informació per decidir:

- com detectar l’evidència
- com mostrar-la

---

# 2026-03-18 — Emmagatzematge de correccions

Les correccions es guarden en:

```
results/corrections.json
```

Aquest fitxer conté:

- unitat
- activitat
- nota
- comentari
- data

Aquest registre permet:

- reprendre correccions
- recalcular notes
- generar informes

---

# 2026-03-18 — Model de desenvolupament

El projecte segueix el següent model Git:

```
main
↑
PR
↑
feature/*
```

Regles:

- **main no es modifica directament**
- tot el desenvolupament es fa en **branques feature/**
- els canvis s’integren mitjançant **Pull Requests**

---

# Properes fites del projecte

Properes funcionalitats a implementar:

1. RepoLocator
2. ActivitiesLoader
3. EvidenceDetector genèric
4. CorrectionEngine
5. CorrectionsStore
6. càlcul de notes per RA
7. generació d’informes

---

# Objectiu final del sistema

Disposar d’un motor que permeti:

- avaluar repositoris d’alumnes
- registrar correccions de manera estructurada
- calcular notes per RA
- reutilitzar el sistema en diferents mòduls i cicles