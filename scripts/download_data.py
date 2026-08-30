"""Download the benchmark data into ./data.

ETT x4 from the official ETDataset repository, and the LTSF Electricity set
(321 client meters, S5 case study) from the LSTNet release the literature
standardises on. Both are public and need no account or key.

BDG2 is deliberately NOT fetched here. Its meter files are stored in Git LFS,
so a plain raw fetch returns a 134-byte pointer rather than the 174 MB CSV
[FACT, verified 2026-08-29]. It needs an explicit `git lfs` checkout, and
data/bdg2.py raises with that instruction rather than appearing to run on data
it does not have.
"""
import gzip
import os
import urllib.request

BASE = "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small"
FILES = ["ETTh1", "ETTh2", "ETTm1", "ETTm2"]
ECL = ("https://raw.githubusercontent.com/laiguokun/"
       "multivariate-time-series-data/master/electricity/electricity.txt.gz")
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

    dst = os.path.join(OUT, "electricity.txt")
    if os.path.exists(dst):
        print("skip electricity (exists)")
    else:
        print("downloading electricity (321 meters, ~18 MB gzipped) ...")
        raw = urllib.request.urlopen(ECL, timeout=600).read()
        with open(dst, "w") as f:
            f.write(gzip.decompress(raw).decode())
        print(f"  saved {dst}")
    print("done")


if __name__ == "__main__":
    main()
