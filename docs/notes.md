# Project Notes

## Purpose
Small portfolio project: `raw CSV → PySpark cleaning → Delta → features → anomaly detection → Matplotlib`.

Demonstrates practical familiarity with the Databricks / industrial AI stack.

## EU AI Act / Data Governance connection

This project is the practical B-track alongside the research paper:

**"Data Governance for AI Systems Under the EU AI Act: From Data Quality to Compliance Evidence"**

Relevant artefacts for the paper already in place:
- **Data quality checks** — null counts, duplicate detection, range validation (Annex IV documentation)
- **Validation assertions** — pipeline gates that produce visible pass/fail evidence
- **Delta table history** — `DESCRIBE HISTORY` provides lineage / audit trail
- **Quality evidence record** — final summary cell produces a structured quality report
- **Dataset documentation** — synthetic data clearly documented; fields, ranges, and injected errors all described in README

## What not to do to this project
- Do not turn it into a legal/compliance project
- Do not add a full medallion architecture
- Do not train production ML models here
- Keep it technically focused and small
