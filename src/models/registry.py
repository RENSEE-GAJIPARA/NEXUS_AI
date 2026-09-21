"""Model Registry & Metadata Storage for NEXUS AI."""
import os
import json
import joblib
from datetime import datetime
from typing import Dict, Any
from src.utils.paths import MODELS_DIR
from src.utils.logging import logger

def save_model_artifact(model_name: str, model_object: Any, metadata: Dict[str, Any]):
    """Save trained model file and corresponding JSON metadata."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    model_path = MODELS_DIR / f"{model_name}.joblib"
    meta_path = MODELS_DIR / f"{model_name}_metadata.json"
    
    # Save model artifact
    joblib.dump(model_object, model_path)
    
    # Enrich metadata
    metadata["model_name"] = model_name
    metadata["saved_at"] = datetime.now().isoformat()
    
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
        
    logger.info(f"Saved model artifact '{model_name}' to {model_path}")

def load_model_artifact(model_name: str):
    """Load model artifact and metadata if present."""
    model_path = MODELS_DIR / f"{model_name}.joblib"
    meta_path = MODELS_DIR / f"{model_name}_metadata.json"
    
    if not model_path.exists():
        logger.warning(f"Model file '{model_path}' not found.")
        return None, {}
        
    model = joblib.load(model_path)
    metadata = {}
    if meta_path.exists():
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            
    return model, metadata
