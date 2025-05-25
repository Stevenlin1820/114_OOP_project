"""
專案入口。把程式集中到一行，方便未來改用 PyInstaller 等工具封裝。
"""

import tkinter as tk
from gui import MathGameGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MathGameGUI(root)
    root.mainloop()
