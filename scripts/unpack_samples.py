#!/usr/bin/env python3
"""Download the public clinic preview PDFs and write them under samples/."""
from pathlib import Path
import hashlib, sys, urllib.request, zipfile

URL = "https://files.catbox.moe/sn33k9.zip"
EXPECTED_SHA256 = "7d89acd43cd50ef7bc5de0e6c69391160581e02a488fbdf490ad831e7ccf2b3c"
root = Path(__file__).resolve().parents[1]
dest = root / "samples"
dest.mkdir(parents=True, exist_ok=True)
zip_path = Path("/tmp/neuralconclave_samples.zip")

print("downloading", URL)
urllib.request.urlretrieve(URL, zip_path)
digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
if digest != EXPECTED_SHA256:
    raise SystemExit(f"checksum mismatch: {digest}")

written = 0
with zipfile.ZipFile(zip_path) as zf:
    for name in zf.namelist():
        if "/" in name or "\\" in name or name.startswith(".") or not name.endswith(".pdf"):
            raise SystemExit(f"refusing unsafe name {name!r}")
        data = zf.read(name)
        (dest / name).write_bytes(data)
        written += 1
        print("wrote", name, len(data))
print("wrote", written, "pdfs")
