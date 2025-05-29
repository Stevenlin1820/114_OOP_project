"""
math_game.py – 數學奇幻冒險（功能增強版）

👾 特色
    • 登入 / 註冊（帳號、密碼、最高分）
    • 主選單（開始遊戲 / 返回）
    • 四則速算：＋、－、×、÷（確保 ÷ 的答案為正整數）
    • 20 級，每級 10 題；每升 1 級，計時 * 0.9，最短 3 s
    • 暫停、存檔、續玩
    • 即時排行榜（前 5 名）
    • 支援跨次遊戲續接個人進度

執行：
    python math_game.py
"""

# --------------------------------------------------
#  Imports
# --------------------------------------------------
import os
import json
import random
import tkinter as tk
from tkinter import ttk, font, messagebox

# --------------------------------------------------
#  檔案路徑 & 常數設定
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR  # ⇨ 與程式放同層

USERS_FILE = os.path.join(DATA_DIR, "math_game_users.json")
STATE_FILE = os.path.join(DATA_DIR, "math_game_state.json")

MAX_LEVEL            = 20       # 最多 20 關
QUESTIONS_PER_LEVEL  = 10       # 每關 10 題
TIME_SHRINK_RATE     = 0.9      # 升級後時間倍率
BASE_TIME_LIMIT      = 15.0     # 起始答題秒數
MIN_TIME_LIMIT       = 3.0      # 最低秒數

print("📁 用戶資料：", USERS_FILE)
print("📁 進度資料：", STATE_FILE)

# --------------------------------------------------
#  主 GUI 類別
# --------------------------------------------------
class MathGameGUI:
    """Tkinter GUI – 數學奇幻冒險"""

    # ------------------------------
    #  初始化
    # ------------------------------
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("🎮 數學奇幻冒險 🎮")
        master.state('zoomed')
        master.configure(bg="#0B0C10")

        # ——— 字體 ———
        self.title_font = font.Font(family="Comic Sans MS", size=48, weight="bold")
        self.ui_font    = font.Font(family="微軟正黑體",   size=16)
        self.q_font     = font.Font(family="Arial",        size=32, weight="bold")

        # ——— 載入資料 ———
        self.users  = self._load_json(USERS_FILE)
        self.states = self._load_json(STATE_FILE)

        # ——— 三大畫面 ———
        self.login_frame = tk.Frame(master, bg="#0B0C10")
        self.menu_frame  = tk.Frame(master, bg="#0B0C10")
        self.game_frame  = tk.Frame(master, bg="#0B0C10")

        # 建構各區域
        self._build_login()
        self._build_menu()
        self._build_game()

        # 先顯示登入畫面
        self.login_frame.pack(fill="both", expand=True)

    # ==================================================
    #  檔案 I/O
    # ==================================================
    def _load_json(self, path: str) -> dict:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_json(self, path: str, data: dict) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ==================================================
    #  登入 / 註冊
    # ==================================================
    def _build_login(self) -> None:
        panel = tk.Frame(self.login_frame, bg="#1F2833", bd=2, relief="ridge")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        tk.Label(panel,
                 text="🌟 數學奇幻冒險 🌟",
                 font=self.title_font,
                 fg="#FFD700",
                 bg="#1F2833").pack(pady=(20, 10))

        tk.Label(panel, text="用戶名：", font=self.ui_font, fg="#FFFFFF", bg="#1F2833").pack(pady=5)
        self.login_user = tk.Entry(panel, font=self.ui_font, width=30, justify="center")
        self.login_user.pack(pady=5)

        tk.Label(panel, text="密碼：", font=self.ui_font, fg="#FFFFFF", bg="#1F2833").pack(pady=5)
        self.login_pass = tk.Entry(panel, font=self.ui_font, show="*", width=30, justify="center")
        self.login_pass.pack(pady=5)

        tk.Button(panel,
                  text="🔑 登入",
                  font=self.ui_font,
                  bg="#00AA00",
                  fg="#FFFFFF",
                  bd=0,
                  command=self._handle_login).pack(pady=(20, 5))

        tk.Button(panel,
                  text="➕ 註冊",
                  font=self.ui_font,
                  bg="#E94560",
                  fg="#FFFFFF",
                  bd=0,
                  command=self._open_register).pack(pady=5)

    def _handle_login(self) -> None:
        user = self.login_user.get().strip()
        pwd  = self.login_pass.get().strip()

        if user in self.users and self.users[user]['password'] == pwd:
            self.username = user
            self.login_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)
        else:
            messagebox.showerror("登入失敗", "帳號或密碼錯誤")

    # ---------- 註冊 ----------
    def _open_register(self) -> None:
        dlg = tk.Toplevel(self.master)
        dlg.title("➕ 註冊新帳號")
        dlg.configure(bg="#1F2833")
        dlg.geometry("400x260")
        dlg.resizable(False, False)
        dlg.transient(self.master)
        dlg.grab_set()

        tk.Label(dlg,
                 text="➕ 新帳號註冊",
                 font=self.ui_font,
                 fg="#FFFFFF",
                 bg="#16202A").pack(fill="x")

        content = tk.Frame(dlg, bg="#1F2833")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(content, text="用戶名：", font=self.ui_font, fg="#CCCCCC", bg="#1F2833").grid(row=0, column=0, sticky="e", pady=8)
        entry_user = tk.Entry(content, font=self.ui_font, width=25, justify="center")
        entry_user.grid(row=0, column=1, pady=8, padx=(10, 0))

        tk.Label(content, text="密碼：", font=self.ui_font, fg="#CCCCCC", bg="#1F2833").grid(row=1, column=0, sticky="e", pady=8)
        entry_pwd = tk.Entry(content, font=self.ui_font, width=25, show="*", justify="center")
        entry_pwd.grid(row=1, column=1, pady=8, padx=(10, 0))

        btn_frame = tk.Frame(dlg, bg="#1F2833")
        btn_frame.pack(fill="x", pady=(0, 20))

        tk.Button(btn_frame,
                  text="取消",
                  font=self.ui_font,
                  bg="#555555",
                  fg="#FFFFFF",
                  bd=0,
                  command=dlg.destroy).pack(side="left", expand=True, padx=20)

        tk.Button(btn_frame,
                  text="註冊",
                  font=self.ui_font,
                  bg="#E94560",
                  fg="#FFFFFF",
                  bd=0,
                  command=lambda: self._handle_register(entry_user.get(), entry_pwd.get(), dlg)).pack(side="right", expand=True, padx=20)

    def _handle_register(self, user: str, pwd: str, dlg: tk.Toplevel) -> None:
        if not user or not pwd:
            messagebox.showwarning("輸入錯誤", "請填寫完整資料")
            return

        if user in self.users:
            messagebox.showinfo("提示", "帳號已存在")
            return

        self.users[user] = {"password": pwd, "score": 0}
        self._save_json(USERS_FILE, self.users)
        messagebox.showinfo("註冊成功", "請使用新帳號登入")
        dlg.destroy()

    # ==================================================
    #  主選單
    # ==================================================
    def _build_menu(self) -> None:
        tk.Button(self.menu_frame,
                  text="▶️ 開始遊戲",
                  font=self.ui_font,
                  bg="#00AA00",
                  fg="#FFFFFF",
                  bd=0,
                  command=self._on_start_game).pack(expand=True)
        tk.Button(self.menu_frame,
                  text="🔙 登出",
                  font=self.ui_font,
                  bg="#555555",
                  fg="#FFFFFF",
                  bd=0,
                  command=self._logout).pack()
    def _on_start_game(self) -> None:
        self.menu_frame.pack_forget()
        self._start_game()

    # ==================================================
    #  遊戲畫面
    # ==================================================
    def _build_game(self) -> None:
        # ---------- Header ----------
        header = tk.Frame(self.game_frame, bg="#1F2833")
        header.pack(fill="x")

        self.user_label = tk.Label(header, text="", font=self.ui_font, fg="#66FCF1", bg="#1F2833")
        self.user_label.pack(side="left", padx=20)

        self.score_label = tk.Label(header, text="分數：0  等級：1", font=self.title_font, fg="#00FF00", bg="#1F2833")
        self.score_label.pack(side="left", padx=50)

        tk.Button(header,
                  text="⏸ 暫停",
                  font=self.ui_font,
                  bg="#555555",
                  fg="#FFFFFF",
                  bd=0,
                  command=self._pause_game).pack(side="right", padx=10)

        # ---------- Body ----------
        body = tk.Frame(self.game_frame, bg="#0B0C10")
        body.pack(expand=True, fill="both")

        card = tk.Frame(body, bg="#45A29E", bd=8, relief="ridge")
        card.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.6, relheight=0.2)

        self.question_label = tk.Label(card, text="", font=self.q_font, fg="#FFFFFF", bg="#45A29E")
        self.question_label.pack(expand=True)

        self.entry = tk.Entry(body, font=self.ui_font, justify="center")
        self.entry.place(relx=0.5, rely=0.5, anchor="center", width=300)
        self.entry.bind("<Return>", lambda _e: self._check_answer())

        self.submit_btn = tk.Button(body, text="✔️ 提交", font=self.ui_font, bg="#0099FF", fg="#FFFFFF", bd=0, command=self._check_answer)
        self.submit_btn.place(relx=0.5, rely=0.6, anchor="center")

        # ---------- Timer ----------
        self.timer_label = tk.Label(body, text="剩餘時間：", font=self.ui_font, fg="#FFAA00", bg="#0B0C10")
        self.timer_label.place(relx=0.5, rely=0.7, anchor="center")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Timer.Horizontal.TProgressbar', troughcolor="#000000", thickness=20, background="#00FF00")
        style.configure('Red.Horizontal.TProgressbar', background="#FF0000")

        self.timerbar = ttk.Progressbar(body, style='Timer.Horizontal.TProgressbar', maximum=100)
        self.timerbar.place(relx=0.5, rely=0.75, anchor="center", relwidth=0.6)

        # ---------- Leaderboard ----------
        board_frame = tk.Frame(self.game_frame, bg="#1F2833")
        board_frame.pack(fill="x", pady=(20, 0))

        tk.Label(board_frame, text="🏆 排行榜 🏆", font=self.ui_font, fg="#FFCE00", bg="#1F2833").pack(pady=(5, 2))

        self.board = ttk.Treeview(board_frame, columns=("玩家", "分數"), show="headings", height=5)
        self.board.heading("玩家", text="玩家")
        self.board.heading("分數", text="分數")
        self.board.column("玩家", anchor="center")
        self.board.column("分數", anchor="center")
        self.board.pack(padx=20, pady=(0, 10))

    # ==================================================
    #  遊戲流程控制
    # ==================================================
    def _prompt_continue(self) -> bool:
        """詢問是否接續舊進度"""
        dlg = tk.Toplevel(self.master)
        dlg.title("續玩進度？")
        dlg.configure(bg="#1F2833")
        dlg.geometry("400x150")

        tk.Label(dlg, text="偵測到舊進度，是否繼續？", font=self.ui_font, fg="#FFFFFF", bg="#1F2833").pack(pady=20)

        frm = tk.Frame(dlg, bg="#1F2833")
        frm.pack()

        result = {"yes": False}

        tk.Button(frm,
                  text="是",
                  font=self.ui_font,
                  bg="#00AA00",
                  fg="#FFFFFF",
                  bd=0,
                  command=lambda: (result.update({"yes": True}), dlg.destroy())).pack(side="left", padx=10)

        tk.Button(frm,
                  text="否",
                  font=self.ui_font,
                  bg="#AA0000",
                  fg="#FFFFFF",
                  bd=0,
                  command=dlg.destroy).pack(side="right", padx=10)

        dlg.transient(self.master)
        dlg.grab_set()
        self.master.wait_window(dlg)
        return result["yes"]

    def _start_game(self) -> None:
        """初始化 / 回復 遊戲狀態"""
        self.game_frame.pack(fill="both", expand=True)

        # 顯示名稱
        self.user_label.config(text=f"玩家：{self.username}")

        # 讀取舊進度
        state = self.states.get(self.username)
        if state and self._prompt_continue():
            self.score       = state['score']
            self.level       = state['level']
            self.time_limit  = state['time_limit']
            self.correct_cnt = state.get('correct_cnt', 0)
        else:
            self.score       = 0
            self.level       = 1
            self.time_limit  = BASE_TIME_LIMIT
            self.correct_cnt = 0
            self._clear_state()

        self.time_left = self.time_limit
        self._update_status()
        self._refresh_leaderboard()
        self._next_question()
        self._run_timer()

    # ------------------------------
    #  狀態刷新
    # ------------------------------
    def _update_status(self) -> None:
        self.score_label.config(text=f"分數：{self.score}  等級：{self.level}")

    def _refresh_leaderboard(self) -> None:
        self.board.delete(*self.board.get_children())
        ranking = sorted(self.users.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
        for user, data in ranking:
            self.board.insert('', 'end', values=(user, data['score']))

    # ------------------------------
    #  出題邏輯
    # ------------------------------
    def _generate_question(self) -> str:
        """隨機生成一題四則運算，÷ 題確保整除"""
        op_list = ['+', '-', '*', '/']
        op = random.choice(op_list)
        max_num = 5 + self.level * 5

        if op == '/':
            divisor   = random.randint(1, max_num)
            quotient  = random.randint(1, max_num)
            dividend  = divisor * quotient
            a, b, ans = dividend, divisor, quotient
        else:
            a = random.randint(1, max_num)
            b = random.randint(1, max_num)

            if op == '-' and a < b:
                a, b = b, a  # 避免負數

            if op == '+':
                ans = a + b
            elif op == '-':
                ans = a - b
            else:  # '*'
                ans = a * b

        disp_op = {'+': '+', '-': '-', '*': '×', '/': '÷'}[op]
        self.answer = ans
        return f"{a} {disp_op} {b} = ?"

    def _next_question(self) -> None:
        if self.level > MAX_LEVEL:
            self._end_game("🎉 恭喜通關！")
            return

        self.time_left = self.time_limit
        q_text = self._generate_question()
        self.question_label.config(text=q_text)

        self.entry.delete(0, tk.END)
        self.timerbar.config(value=100, style='Timer.Horizontal.TProgressbar')
        self.timer_label.config(text=f"剩餘時間：{self.time_left:.1f}s")

    # ------------------------------
    #  Timer
    # ------------------------------
    def _run_timer(self) -> None:
        if self.time_left > 0:
            pct = int(100 * self.time_left / self.time_limit)
            self.timerbar['value'] = pct

            if self.time_left <= 5:
                self.timerbar.config(style='Red.Horizontal.TProgressbar')

            self.timer_label.config(text=f"剩餘時間：{self.time_left:.1f}s")

            self.time_left -= 1
            self.timer_id = self.master.after(1000, self._run_timer)
        else:
            self._end_game("⏰ 時間到！")

    # ------------------------------
    #  答題判定
    # ------------------------------
    def _check_answer(self) -> None:
        # 停計時
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)

        # 轉 int
        try:
            user_ans = int(self.entry.get())
        except ValueError:
            messagebox.showwarning("輸入無效", "請輸入數字")
            self._run_timer()
            return

        # 判分
        if user_ans == self.answer:
            self.score += 1
            self.correct_cnt += 1

            if self.correct_cnt >= QUESTIONS_PER_LEVEL:
                self.level += 1
                self.correct_cnt = 0
                self.time_limit = max(MIN_TIME_LIMIT, self.time_limit * TIME_SHRINK_RATE)

            # 更新個人最佳
            if self.score > self.users[self.username]['score']:
                self.users[self.username]['score'] = self.score
                self._save_json(USERS_FILE, self.users)

            self._update_status()
            self._refresh_leaderboard()
            self._next_question()
            self._run_timer()
        else:
            self._end_game("❌ 答錯了！")

    # ==================================================
    #  暫停 / 儲存
    # ==================================================
    def _pause_game(self) -> None:
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
            del self.timer_id

        dlg = tk.Toplevel(self.master)
        dlg.title("遊戲暫停")
        dlg.configure(bg="#1F2833")
        dlg.geometry("300x150")

        tk.Label(dlg, text="遊戲已暫停", font=self.q_font, fg="#FFFFFF", bg="#1F2833").pack(pady=10)

        frm = tk.Frame(dlg, bg="#1F2833")
        frm.pack(pady=10)

        def on_continue():
            dlg.destroy()
            self._run_timer()

        def on_quit():
            dlg.destroy()
            self._save_state()
            self.game_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)

        tk.Button(frm, text="儲存並退出", font=self.ui_font, bg="#AA0000", fg="#FFFFFF", bd=0, command=on_quit).pack(side="left", padx=5)
        tk.Button(frm, text="繼續", font=self.ui_font, bg="#00AA00", fg="#FFFFFF", bd=0, command=on_continue).pack(side="right", padx=5)

        dlg.protocol("WM_DELETE_WINDOW", on_continue)

    # ==================================================
    #  遊戲結束
    # ==================================================
    def _end_game(self, msg: str) -> None:
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)

        dlg = tk.Toplevel(self.master)
        dlg.title("遊戲結束")
        dlg.configure(bg="#1F2833")
        dlg.geometry("300x180")

        tk.Label(dlg, text=msg, font=self.q_font, fg="#FFFFFF", bg="#1F2833").pack(pady=10)
        tk.Label(dlg, text=f"你的分數：{self.score}", font=self.ui_font, fg="#FFFF00", bg="#1F2833").pack(pady=5)

        frm = tk.Frame(dlg, bg="#1F2833")
        frm.pack(pady=10)

        def on_retry():
            dlg.destroy()
            self._play_again()

        def on_exit():
            dlg.destroy()
            self._clear_state()
            self.game_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)

        tk.Button(frm, text="再玩一局", font=self.ui_font, bg="#00AA00", fg="#FFFFFF", bd=0, command=on_retry).pack(side="left", padx=5)
        tk.Button(frm, text="退出", font=self.ui_font, bg="#AA0000", fg="#FFFFFF", bd=0, command=on_exit).pack(side="right", padx=5)

        dlg.protocol("WM_DELETE_WINDOW", on_exit)

    def _play_again(self) -> None:
        self.score       = 0
        self.level       = 1
        self.correct_cnt = 0
        self.time_limit  = BASE_TIME_LIMIT
        self.time_left   = self.time_limit

        self._update_status()
        self._next_question()
        self._run_timer()

    def _logout(self) -> None:
        """登出回登入頁"""
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)

        self._save_json(USERS_FILE, self.users)
        self._save_json(STATE_FILE, self.states)

        self.game_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

        self.login_user.delete(0, tk.END)
        self.login_pass.delete(0, tk.END)



    # ==================================================
    #  Save / Load State
    # ==================================================
    def _save_state(self) -> None:
        self.states[self.username] = {
            'score':       self.score,
            'level':       self.level,
            'time_limit':  self.time_limit,
            'correct_cnt': self.correct_cnt
        }
        self._save_json(STATE_FILE, self.states)
        self._save_json(USERS_FILE, self.users)

    def _clear_state(self) -> None:
        if self.username in self.states:
            del self.states[self.username]
            self._save_json(STATE_FILE, self.states)


# --------------------------------------------------
#  程式進入點
# --------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app  = MathGameGUI(root)
    root.mainloop()
