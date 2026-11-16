"""
Rebuild every table and figure from the raw inputs, in order.

Usage (from the repo root):
    python run_all.py

SEC requires a contact email. Set it first:
    Mac/Linux:  export SEC_EMAIL=yourname@lehigh.edu
    Colab:      %env SEC_EMAIL=yourname@lehigh.edu

Each notebook is executed in place, so its outputs are saved inside it
and visible on GitHub.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = sorted((ROOT / "code").glob("0*.ipynb"))

for nb in NOTEBOOKS:
    print(f"Running {nb.name} ...", flush=True)
    subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
         "--ExecutePreprocessor.timeout=1800", str(nb)],
        check=True,
    )

print("\nDone. Final dataset: outputs/final_dataset.csv")
