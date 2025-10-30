import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model" / "best_pipeline.joblib"

def load_pipeline():
    """
    Load and return the save pipeline.
    Raises FileNotFoundError if the model is not present.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

    print(f"Model loaded from {MODEL_PATH}")

    return joblib.load(MODEL_PATH)
