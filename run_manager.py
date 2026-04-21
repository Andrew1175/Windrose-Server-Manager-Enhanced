"""Launch Windrose Server Manager (tkinter). Double-click or: python run_manager.py"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path

from windrose_manager.main_window import WindroseServerManagerApp


def main() -> None:
    root = tk.Tk()
    initial = Path(__file__).resolve().parent
    WindroseServerManagerApp(root, initial)
    root.mainloop()


if __name__ == "__main__":
    main()
