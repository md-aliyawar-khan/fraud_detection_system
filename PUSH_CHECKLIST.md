# Pre-push checklist

## Ready to push

- [x] API tests pass (`python test_api.py`)
- [x] Model artifacts in `models/` (under 100 MB total)
- [x] `.gitignore` excludes `venv/`, large CSVs, logs, audit DBs
- [x] Root `README.md` with setup and run steps
- [x] No secrets in repo

## Do not push (gitignored or too large)

- `venv/` (~5000+ files)
- `data/raw/creditcard_2023.csv` (~325 MB)
- `data/processed/X_processed.csv` (~323 MB)
- `data/processed/y_processed.csv` if present

## Before first push

```powershell
git init
git add .
git status
```

Confirm `git status` does **not** list `venv/` or `*.csv` under `data/raw` or `data/processed`.

```powershell
git commit -m "Add fraud detection API and ML pipeline"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

## Optional: Git LFS for dataset

If you need the CSV on GitHub, use Git LFS for files over 100 MB instead of committing them directly.

## Resume claims

Only claim 10K+/hour or sub-200ms latency if `reports/load_test_result.json` supports it from your own benchmark run.
