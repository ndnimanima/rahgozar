"""ASGI entry point for source-based hosts, matching the upstream layout.

Run ``python app.py`` or point an ASGI server at ``app:app``.  The shared
launcher prepares PORT and a writable state directory before main is imported.
State on ephemeral hosting is not persistent.
"""
from __future__ import annotations

import run as _launcher
import main as rahgozar_main
import uvicorn

app = rahgozar_main.app


def _configured_port() -> int:
    port = _launcher.port
    rahgozar_main.PANEL_PORT = port
    rahgozar_main.CONFIG["port"] = port
    return port


_configured_port()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=_configured_port(), log_level="info", workers=1)


if __name__ == "__main__":
    main()
