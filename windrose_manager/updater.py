from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from . import constants


def fetch_remote_version(url: str) -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Windrose-Server-Manager"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        m = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', text)
        if m:
            return m.group(1), None
        return None, "Could not read version from remote file."
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def parse_version(v: str) -> tuple[int, ...]:
    parts = []
    for p in re.split(r"[^\d]+", v):
        if p.isdigit():
            parts.append(int(p))
    return tuple(parts) if parts else (0,)


def is_remote_newer(remote: str, local: str) -> bool:
    return parse_version(remote) > parse_version(local)


def find_windrose_package_dir(start: Path) -> Path | None:
    for p in start.rglob("windrose_manager"):
        if p.is_dir() and (p / "__init__.py").is_file():
            return p
    return None


def apply_zip_update(zip_url: str, app_package_dir: Path, log_callback) -> bool:
    if not zip_url.strip():
        return False
    try:
        req = urllib.request.Request(zip_url, headers={"User-Agent": "Windrose-Server-Manager"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
        with tempfile.TemporaryDirectory(prefix="wr_update_") as tmp:
            zpath = Path(tmp) / "src.zip"
            zpath.write_bytes(data)
            extract_root = Path(tmp) / "out"
            with zipfile.ZipFile(zpath, "r") as zf:
                zf.extractall(extract_root)
            new_pkg = find_windrose_package_dir(extract_root)
            if not new_pkg:
                log_callback("Update zip did not contain a windrose_manager package.")
                return False
            # Backup and replace
            bak = app_package_dir.with_name(app_package_dir.name + "_bak")
            if bak.exists():
                shutil.rmtree(bak, ignore_errors=True)
            shutil.move(str(app_package_dir), str(bak))
            shutil.copytree(new_pkg, app_package_dir)
        log_callback("Update applied. Restarting...")
        subprocess.Popen([sys.executable, "-m", "windrose_manager"], close_fds=True)
        return True
    except Exception as e:  # noqa: BLE001
        log_callback(f"Update failed: {e}")
        return False
