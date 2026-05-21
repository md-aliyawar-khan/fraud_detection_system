# Fraud Detection System

Credit card fraud detection using a RandomForest classifier, Flask API, and SMOTE for class imbalance.

## Stack

- Python 3.11+
- scikit-learn (RandomForest)
- imbalanced-learn (SMOTE)
- Flask + Waitress
- pandas, numpy, joblib

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Place `creditcard_2023.csv` in `data/raw/` (see `data/raw/README.md`). The CSV is not in Git because it exceeds GitHub's 100 MB limit.

Train if needed:

```powershell
python scripts/preprocess.py
python scripts/train.py
```

## Run

Terminal 1:

```powershell
python run_production.py
```

Browser: http://127.0.0.1:5000/

Terminal 2:

```powershell
python test_api.py
```

Different port:

```powershell
$env:PORT=5001
$env:API_BASE_URL="http://localhost:5001"
python run_production.py
```

## API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/health` | GET | Health check |
| `/predict` | POST | Single transaction |
| `/predict_batch` | POST | Batch scoring |

## Load testing

```powershell
python scripts/load_test.py --base-url http://127.0.0.1:5000 --duration 600 --concurrency 8
```

Document results in `reports/load_test_report_template.md`. Use throughput and latency numbers on a resume only after you run this test.

## Push to GitHub

See `PUSH_CHECKLIST.md` in the project root.

## Deployment

See `DEPLOYMENT.md` for Heroku.
