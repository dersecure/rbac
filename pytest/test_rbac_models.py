import os
import re
import glob

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'sunspec-models', 'json')
RBAC_DIR = os.path.join(os.path.dirname(__file__), 'rbac')


def get_model_files(directory):
    return [f for f in glob.glob(os.path.join(directory, 'model_*.json'))]


def extract_model_id(filename):
    match = re.search(r"model_(\d+)\.json", filename)
    return int(match.group(1)) if match else None


def test_all_models_in_rbac():
    model_files = get_model_files(MODELS_DIR)
    rbac_files = get_model_files(RBAC_DIR)
    rbac_model_ids = {extract_model_id(f) for f in rbac_files}

    missing = []
    for model_file in model_files:
        model_id = extract_model_id(model_file)
        if model_id is not None and model_id < 10000:
            if model_id not in rbac_model_ids:
                missing.append(model_id)

    assert not missing, f"Missing RBAC files for model(s): {missing}"
