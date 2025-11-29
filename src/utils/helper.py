import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
INSIGHTS_FILE = os.path.join(REPORTS_DIR, "insights.json")
CREATIVES_FILE = os.path.join(REPORTS_DIR, "creatives.json")
TESTS_FILE=os.path.join(REPORTS_DIR, "tests.json")


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