from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ClientInstallSettings:
    install_client_choice_saved: bool = False
    install_client: str = "Steam"
    steam_install_root: str | None = None
    steamcmd_install_root: str | None = None
    steamcmd_force_install_dir: str | None = None
    server_root: str | None = None


def sync_steamcmd_sidecar(
    install_client: str, force_dir: str | None, sidecar: Path
) -> None:
    if install_client != "SteamCMD":
        try:
            if sidecar.is_file():
                sidecar.unlink()
        except OSError:
            pass
        return
    if not force_dir:
        return
    try:
        sidecar.write_text(force_dir.rstrip("\\/"), encoding="utf-8")
    except OSError:
        pass


def import_steamcmd_force_from_sidecar(sidecar: Path) -> str | None:
    if not sidecar.is_file():
        return None
    try:
        line = sidecar.read_text(encoding="utf-8").strip()
        return line.rstrip("\\/") if line else None
    except OSError:
        return None


def read_client_settings(paths) -> ClientInstallSettings | None:
    if paths.client_settings_file.is_file():
        try:
            data = json.loads(paths.client_settings_file.read_text(encoding="utf-8"))
            if not data.get("InstallClientChoiceSaved"):
                return None
            ic = data.get("InstallClient")
            if ic not in ("Steam", "SteamCMD"):
                return None
            return ClientInstallSettings(
                install_client_choice_saved=True,
                install_client=ic,
                steam_install_root=_norm(data.get("SteamInstallRoot")),
                steamcmd_install_root=_norm(data.get("SteamCmdInstallRoot")),
                steamcmd_force_install_dir=_norm(data.get("SteamCmdForceInstallDir")),
                server_root=_norm(data.get("ServerRoot")),
            )
        except (OSError, json.JSONDecodeError, TypeError):
            return None

    if paths.settings_file.is_file():
        try:
            legacy = json.loads(paths.settings_file.read_text(encoding="utf-8"))
            if legacy.get("InstallClientChoiceSaved") and legacy.get("InstallClient"):
                s = ClientInstallSettings(
                    install_client_choice_saved=True,
                    install_client=str(legacy["InstallClient"]),
                    steam_install_root=_norm(legacy.get("SteamInstallRoot")),
                    steamcmd_install_root=_norm(legacy.get("SteamCmdInstallRoot")),
                    steamcmd_force_install_dir=_norm(legacy.get("SteamCmdForceInstallDir")),
                    server_root=_norm(legacy.get("ServerRoot")),
                )
                if s.install_client not in ("Steam", "SteamCMD"):
                    return None
                save_client_settings(paths, s)
                return s
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return None


def _norm(p: Any) -> str | None:
    if not p or not str(p).strip():
        return None
    return str(p).rstrip("\\/")


def save_client_settings(paths, s: ClientInstallSettings) -> None:
    try:
        payload = {
            "InstallClientChoiceSaved": s.install_client_choice_saved,
            "InstallClient": s.install_client,
            "SteamInstallRoot": s.steam_install_root,
            "SteamCmdInstallRoot": s.steamcmd_install_root,
            "SteamCmdForceInstallDir": s.steamcmd_force_install_dir,
            "ServerRoot": s.server_root,
        }
        paths.client_settings_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        sync_steamcmd_sidecar(s.install_client, s.steamcmd_force_install_dir, paths.steamcmd_sidecar)
    except OSError:
        pass


@dataclass
class ManagerSettings:
    auto_restart: bool = False
    auto_backup: bool = False
    backup_interval_value: int = 4
    backup_interval_unit: str = "hours"
    schedule_enabled: bool = False
    schedule_time: str = "04:00"
    steamcmd_force_install_dir: str | None = None


def load_manager_settings(paths) -> ManagerSettings:
    m = ManagerSettings()
    if not paths.settings_file.is_file():
        return m
    try:
        s = json.loads(paths.settings_file.read_text(encoding="utf-8"))
        if "AutoRestart" in s:
            m.auto_restart = bool(s["AutoRestart"])
        if "AutoBackup" in s:
            m.auto_backup = bool(s["AutoBackup"])
        if "BackupIntervalValue" in s:
            m.backup_interval_value = max(1, int(s["BackupIntervalValue"]))
        elif "BackupInterval" in s:
            # Backward compatibility with old combobox index storage.
            idx = int(s["BackupInterval"])
            m.backup_interval_value = (1, 4, 8, 16, 24)[idx] if 0 <= idx < 5 else 4
        if "BackupIntervalUnit" in s:
            u = str(s["BackupIntervalUnit"]).strip().lower()
            m.backup_interval_unit = "minutes" if u.startswith("minute") else "hours"
        if "ScheduleEnabled" in s:
            m.schedule_enabled = bool(s["ScheduleEnabled"])
        if s.get("ScheduleTime"):
            m.schedule_time = str(s["ScheduleTime"])
        if s.get("SteamCmdForceInstallDir"):
            m.steamcmd_force_install_dir = str(s["SteamCmdForceInstallDir"]).rstrip("\\/")
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return m


def save_manager_settings(
    paths,
    m: ManagerSettings,
    client: ClientInstallSettings,
) -> None:
    payload = {
        "AutoRestart": m.auto_restart,
        "AutoBackup": m.auto_backup,
        "BackupInterval": m.backup_interval_value,
        "BackupIntervalValue": m.backup_interval_value,
        "BackupIntervalUnit": m.backup_interval_unit,
        "ScheduleEnabled": m.schedule_enabled,
        "ScheduleTime": m.schedule_time,
        "InstallClientChoiceSaved": client.install_client_choice_saved,
        "InstallClient": client.install_client,
        "SteamInstallRoot": client.steam_install_root,
        "SteamCmdInstallRoot": client.steamcmd_install_root,
        "SteamCmdForceInstallDir": client.steamcmd_force_install_dir,
    }
    try:
        paths.settings_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        sync_steamcmd_sidecar(
            client.install_client, client.steamcmd_force_install_dir, paths.steamcmd_sidecar
        )
    except OSError:
        pass
