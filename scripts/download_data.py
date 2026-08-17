"""Download the four ETT benchmark CSVs into ./data.

Public source: the official ETDataset repository. No account or key needed.
"""
import os
import urllib.request

BASE = "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small"
FILES = ["ETTh1", "ETTh2", "ETTm1", "ETTm2"]
OUT = os.path.join(os.path.dirname(__file__), "..", "data")


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in FILES:
        dst = os.path.join(OUT, f"{name}.csv")
        if os.path.exists(dst):
            print(f"skip {name} (exists)")
            continue
        url = f"{BASE}/{name}.csv"
        print(f"downloading {name} ...")
        urllib.request.urlretrieve(url, dst)
        print(f"  saved {dst}")
    print("done")


if __name__ == "__main__":
    main()
