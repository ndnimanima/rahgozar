"""Provider-aware launcher for Shiprr and other source-based hosts.

Existing Railway deployments may keep their original 8080 start command.
State on a host without a persistent disk remains ephemeral.
"""
import os
import sys
from pathlib import Path
import tempfile

raw_port = (os.environ.get("PORT") or "8080").strip()
try:
    port = int(raw_port)
    if not 1 <= port <= 65535:
        raise ValueError
except ValueError:
    sys.exit("Invalid PORT: expected an integer between 1 and 65535")

# main.py uses this same value when configuring built-in inbounds and health.
os.environ["RAHGOZAR_LISTEN_PORT"] = str(port)

# Some source hosts run as non-root and cannot write /data. Do not override an
# explicitly selected directory; otherwise use a writable ephemeral directory
# only when /data cannot actually be written.
if not os.environ.get("DATA_DIR"):
    try:
        default_dir = Path("/data")
        default_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=default_dir):
            pass
    except OSError:
        os.environ["DATA_DIR"] = str(Path(tempfile.gettempdir()) / "rahgozar-data")
        print("Warning: /data is not writable; using temporary storage. Back up state before restart.", flush=True)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, workers=1)
