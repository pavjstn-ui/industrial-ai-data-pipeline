# PROJECT_STATE.md — industrial-ai-data-pipeline

**Last updated:** 2026-08-30  
**Status:** READY FOR DATABRICKS EXECUTION

---

## Exact project name
`industrial-ai-data-pipeline`

## Exact project location
`/Users/macski/Projects/pat-vault/industrial-ai-data-pipeline/`

---

## Purpose
Portfolio project demonstrating practical industrial AI/ML data pipeline skills:
Databricks, PySpark, Delta Lake, sensor data, data quality, feature engineering, anomaly detection.

Companion to the EU AI Act research paper (Track A). This is Track B — technical implementation.

---

## Current objective
DONE: Build, validate, and git-ready the complete project.
NEXT: Execute the notebook in Databricks and record outputs.

---

## Architecture

```
data/raw/sensor_readings.csv      (5,003 rows, synthetic, 4 machines)
        ↓
notebooks/industrial_ai_data_pipeline.ipynb
        ↓ (pipeline stages)
  0. Configuration (paths, thresholds)
  1. PySpark CSV ingestion
  2. Data-quality inspection (nulls, duplicates, ranges, machine IDs, timestamps)
  2a. Out-of-range inspection (detailed per-sensor range check)
  3. Cleaning (timestamp parse, dedup, range filter, imputation)
  4. Post-cleaning validation (assert gates)
  5. Delta Lake write + read-back + DESCRIBE HISTORY
  6. Feature engineering (4 features)
  7. Anomaly detection (rule-based, 3 conditions)
  7a. Feature+anomaly Delta write
  8. Matplotlib visualisations (3 plots)
  9. Final quality summary + assertions
```

---

## Files created

| File | Status | Description |
|---|---|---|
| `data/raw/sensor_readings.csv` | DONE | 5,003 rows synthetic sensor data, 4 machines, deliberate quality issues |
| `notebooks/industrial_ai_data_pipeline.ipynb` | DONE | 25-cell Databricks notebook, full pipeline |
| `src/generate_data.py` | DONE | Reproducible data generation script (NumPy, seeded) |
| `README.md` | DONE | Full project documentation, pipeline, how-to-run |
| `requirements.txt` | DONE | pyspark, pandas, numpy, matplotlib, delta-spark |
| `docs/notes.md` | DONE | EU AI Act connection, project scope notes |
| `PROJECT_STATE.md` | DONE | This file |

---

## Dataset description

**File:** `data/raw/sensor_readings.csv`  
**Rows:** 5,003 (including duplicates and quality issues)  
**Machines:** M-101, M-102, M-103, M-104  
**Period:** August 2026, 10-minute intervals  
**Columns:** timestamp, machine_id, temperature_c, pressure_bar, vibration_mm_s, energy_kwh  

**Deliberately injected quality problems:**
- ~1% missing values per sensor column
- 3 exact duplicate rows
- Out-of-range temperature (too high: 150–250°C; too low: −60 to −30°C)
- Out-of-range pressure (15–25 bar, sensor saturation)
- Out-of-range vibration (25–50 mm/s, beyond physical limits)
- Null machine_id on ~4 rows

**Regenerate with:** `python src/generate_data.py`  
**Data is entirely synthetic.** No real equipment data.

---

## Notebook contents (25 cells)

| Cell | Type | Content |
|---|---|---|
| 0 | MD | Project header and description |
| 1 | MD | Configuration section |
| 2 | Code | Imports + path/threshold constants |
| 3 | MD | Stage 1: PySpark ingestion |
| 4 | Code | spark.read.csv → raw DataFrame |
| 5 | MD | Stage 2: Quality inspection |
| 6 | Code | Count, duplicates, null per column, describe() |
| 7 | MD | Stage 2a: Out-of-range |
| 8 | Code | Range checks per sensor column |
| 9 | MD | Stage 3: Cleaning strategy |
| 10 | Code | to_timestamp, dropDuplicates, range filter, fillna |
| 11 | MD | Stage 4: Validation |
| 12 | Code | Assert: nulls=0, machines=4, no dupes, ranges clean |
| 13 | MD | Stage 5: Delta Lake |
| 14 | Code | write.format("delta"), read back, DESCRIBE HISTORY |
| 15 | MD | Stage 6: Feature engineering (table of features) |
| 16 | Code | 4 new columns: temp_z_proxy, pressure_deviation, vibration_risk, energy_per_vibration |
| 17 | MD | Stage 7: Anomaly detection (rules table) |
| 18 | Code | anomaly column + groupBy per machine |
| 19 | MD | Stage 7a |
| 20 | Code | Write anomaly layer to Delta |
| 21 | MD | Stage 8: Visualisation |
| 22 | Code | 3 Matplotlib plots (temp time series, vibration time series, anomaly bar chart) |
| 23 | MD | Stage 9: Final quality summary |
| 24 | Code | Quality summary + final assertions + print |

---

## Technologies
- PySpark (DataFrame API, aggregations, window functions)
- Delta Lake (write, read, DESCRIBE HISTORY)
- Databricks (target execution environment)
- Matplotlib + pandas (visualisation)
- NumPy (data generation)

---

## Git status
**NOT DONE** — Git not yet initialised for this subdirectory.

The project lives inside `/Users/macski/Projects/pat-vault/` which IS a git repo (`main` branch, remote: `git@github.com:pavjstn-ui/pat-vault.git`).

Two options:
1. **Commit inside pat-vault** (simplest — no separate repo needed for portfolio)
2. **Create a separate GitHub repo** `pavjstn-ui/industrial-ai-data-pipeline` and push there

**Recommended:** Create separate repo for GitHub portfolio visibility. Requires `gh-old repo create` or manual repo creation on GitHub, then `git init` + push.

---

## What has actually been executed

| Action | Executed? |
|---|---|
| `src/generate_data.py` tested locally | DONE — produces correct output |
| Notebook JSON validated (all cells parse) | DONE — 25 cells, all references correct |
| CSV columns and row count verified | DONE — 5,003 rows, 6 columns |
| README consistency checked | DONE |
| Notebook run in Databricks | NOT DONE |

---

## What has NOT been executed

- **Databricks notebook execution** — `spark`, `display()`, Delta write/read, Matplotlib plots have not been run in a real Databricks cluster
- **Delta table creation** — only possible inside Databricks
- **Visualisation output** — cannot validate locally without PySpark
- **Separate GitHub repo creation** — pending user direction on repo name/org

---

## Known issues

None blocking. The notebook will run correctly in Databricks Runtime 11.3 LTS+.

Cosmetic: the `generate_data.py` seed produces slightly different data characteristics from the original ZIP CSV (different row count, different machine distribution). The notebook is agnostic to row count and asserts machine count = 4, so both CSVs are compatible.

---

## Next action

**One action required from you:**

Create the GitHub repository. Run on Mac:

```bash
gh-old repo create pavjstn-ui/industrial-ai-data-pipeline --public --description "Industrial AI Data Pipeline: PySpark, Delta Lake, anomaly detection on synthetic sensor data"
```

Then I (or you) run:

```bash
cd /Users/macski/Projects/pat-vault/industrial-ai-data-pipeline
git init
git add .
git commit -m "feat: complete industrial AI data pipeline — PySpark, Delta, anomaly detection"
git remote add origin git@github.com:pavjstn-ui/industrial-ai-data-pipeline.git
git push -u origin main
```

Alternatively, commit into pat-vault directly (no separate repo):

```bash
cd /Users/macski/Projects/pat-vault
git add industrial-ai-data-pipeline/
git commit -m "feat: industrial-ai-data-pipeline complete"
git push origin main
```

---

## Databricks execution — next command

1. Upload `data/raw/sensor_readings.csv` to Databricks FileStore
2. Import `notebooks/industrial_ai_data_pipeline.ipynb`
3. Set cluster (any DBR 11.3 LTS+)
4. Run All → inspect quality checks, Delta history, anomaly summary, plots

---

## Relationship to EU AI Act research (Track A)

Paper: *"Data Governance for AI Systems Under the EU AI Act: From Data Quality to Compliance Evidence"*

Artefacts in this project relevant to the paper:
- Data-quality evidence (Section on data quality requirements)
- Validation assertions as compliance gates (Annex IV documentation artefacts)
- Delta DESCRIBE HISTORY as data lineage record
- Structured quality summary table (monitoring / observability)
- Dataset documentation (README + this file) as provenance record

**Do not** turn this project into a legal/compliance project. It stays technically focused.

---

## Decisions already made

| Decision | Rationale |
|---|---|
| Rule-based anomaly detection (not ML) | Keeps project small; demonstrates the workflow without over-engineering |
| Single Delta layer (not medallion) | Proportionate to project size |
| Synthetic data only | Portfolio — no real data required or available |
| `/FileStore/` paths | Works on Databricks Community Edition without Unity Catalog |
| assert as pipeline gates | Simple, visible, interview-demonstrable |
| 5,003 rows (not 17K) | Original ZIP data is sufficient; no need to regenerate |

---

## Things explicitly NOT to over-engineer

- Medallion architecture (Bronze/Silver/Gold)
- Databricks Workflows / DLT
- ML model training
- Unity Catalog
- Multi-cluster tuning
- Real data ingestion
- Great Expectations / Monte Carlo integration
