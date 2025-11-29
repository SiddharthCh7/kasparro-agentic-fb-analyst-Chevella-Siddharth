import os
import json
import yaml
from pathlib import Path

def load_config(path: str = "../../config/config.yaml"):
    with open(Path(__file__).parent / path, "r") as f:
        return yaml.safe_load(f)
    
config = load_config()

# Resolve paths relative to the project root
# src/utils/helper.py -> src/utils -> src
SRC_DIR = Path(__file__).parent.parent

def resolve_path(path_str):
    return str((SRC_DIR / path_str).resolve())

REPORT_SUMMARIES_DIR = resolve_path(config['paths']['report_summaries_dir'])
INSIGHTS_FILE = resolve_path(config['paths']['insights_file'])
CREATIVES_FILE = resolve_path(config['paths']['creatives_file'])
TESTS_FILE = resolve_path(config['paths']['tests_file'])

def append_insight(obj):
    # If file exists, load it
    if os.path.exists(INSIGHTS_FILE):
        with open(INSIGHTS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new entry
    data.append(obj)

    # Save back
    with open(INSIGHTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def append_creative(obj):
    # If file exists, load it
    if os.path.exists(CREATIVES_FILE):
        with open(CREATIVES_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new entry
    data.append(obj)

    # Save back
    with open(CREATIVES_FILE, "w") as f:
        json.dump(data, f, indent=4)


def append_tests(obj):
    # If file exists, load it
    if os.path.exists(TESTS_FILE):
        with open(TESTS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new entry
    data.append(obj)

    # Save back
    with open(TESTS_FILE, "w") as f:
        json.dump(data, f, indent=4)
