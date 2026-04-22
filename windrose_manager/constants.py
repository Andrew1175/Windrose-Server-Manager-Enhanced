# Developed by: https://github.com/Andrew1175

APP_VERSION = "1.0.2"

# GitHub REST API for the latest published release (used by Check for Updates).
GITHUB_LATEST_RELEASE_API_URL = (
    "https://api.github.com/repos/Andrew1175/Windrose-Server-Manager-Enhanced/releases/latest"
)

DONATE_URL = "https://buymeacoffee.com/TheWisestGuy"

WINDROSE_STEAM_APP_ID = "4129620"

PATCH_NOTES: dict[str, list[str]] = {
    "1.0.2": [
        "Fixed the 'Check for Updates' feature not working correctly.",
    ],
    "1.0.1": [
        "Added a safety check to prevent configuration changes while the server is running.",
        "Added a safety check to prevent the server from being updated while it is running.",
    ],
    "1.0.0": [
        "Initial Release",
    ]
}

# Theme (hex without # for tk)
COLORS = {
    "bg": "#0F1923",
    "bg_header": "#0A1520",
    "bg_panel": "#111E2A",
    "bg_input": "#1A2736",
    "border": "#1E3348",
    "border_input": "#2A3E55",
    "text": "#C0CDD8",
    "text_dim": "#8DA4B5",
    "text_muted": "#607080",
    "accent": "#D4A843",
    "green": "#70C48A",
    "red": "#CC3333",
    "blue_btn": "#1A4A7A",
    "gray_btn": "#2A3E55",
    "green_btn": "#1A6B3A",
    "red_btn": "#6B1A1A",
    "navy_btn": "#1A3A7A",
    "save_btn": "#2A3A4A",
    "folder_btn": "#1A4A2A",
    "warn_btn": "#7A3A1A",
    "history_clear": "#5A2020",
    "tab_bg": "#162330",
    "tab_selected": "#1E3348",
    "status_stopped": "#555555",
}

FLOAT_PARAM_KEYS = {
    "mob_health": '{"TagName": "WDS.Parameter.MobHealthMultiplier"}',
    "mob_damage": '{"TagName": "WDS.Parameter.MobDamageMultiplier"}',
    "ship_health": '{"TagName": "WDS.Parameter.ShipsHealthMultiplier"}',
    "ship_damage": '{"TagName": "WDS.Parameter.ShipsDamageMultiplier"}',
    "boarding": '{"TagName": "WDS.Parameter.BoardingDifficultyMultiplier"}',
    "coop_stats": '{"TagName": "WDS.Parameter.Coop.StatsCorrectionModifier"}',
    "coop_ship": '{"TagName": "WDS.Parameter.Coop.ShipStatsCorrectionModifier"}',
}

BOOL_PARAM_KEYS = {
    "coop_quests": '{"TagName": "WDS.Parameter.Coop.SharedQuests"}',
    "easy_explore": '{"TagName": "WDS.Parameter.EasyExplore"}',
}

TAG_COMBAT_KEY = '{"TagName": "WDS.Parameter.CombatDifficulty"}'
