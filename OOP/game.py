import tkinter as tk
from tkinter import ttk, font, messagebox
import random
import json
import os

# 檔案路徑
USERS_FILE = "math_game_users.json"
STATE_FILE = "math_game_state.json"

class MathGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎮 數學奇幻冒險 🎮")
        master.state('zoomed')
        master.configure(bg='#0B0C10')

        # 字體設定
        self.title_font = font.Font(family='Comic Sans MS', size=48, weight='bold')
        self.ui_font    = font.Font(family='微軟正黑體', size=16)
        self.q_font     = font.Font(family='Arial', size=32, weight='bold')

        # 載入用戶與進度
        self.users  = self._load_json(USERS_FILE)
        self.states = self._load_json(STATE_FILE)

        # 三大區塊
        self.login_frame  = tk.Frame(master, bg='#0B0C10')
        self.game_frame   = tk.Frame(master, bg='#0B0C10')
        self.leader_frame = tk.Frame(master, bg='#1F2833')

        # 建構介面
        self._build_login()
        self._build_game()
        self._build_leaderboard()

        # 顯示登入畫面
        self.login_frame.pack(fill='both', expand=True)

    def _load_json(self, path):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # — 登入 & 註冊 —

    def _build_login(self):
        panel = tk.Frame(self.login_frame, bg='#1F2833', bd=2, relief='ridge')
        panel.place(relx=0.5, rely=0.5, anchor='center', width=700, height=500)
        tk.Label(panel, text="🌟 數學奇幻冒險 🌟", font=self.title_font,
                 fg='#FFD700', bg='#1F2833').pack(pady=(20,10))
        tk.Label(panel, text="用戶名：", font=self.ui_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=5)
        self.login_user = tk.Entry(panel, font=self.ui_font, width=30, justify='center')
        self.login_user.pack(pady=5)
        tk.Label(panel, text="密碼：", font=self.ui_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=5)
        self.login_pass = tk.Entry(panel, font=self.ui_font, show='*', width=30, justify='center')
        self.login_pass.pack(pady=5)
        tk.Button(panel, text="🔑 登入", font=self.ui_font,
                  bg='#00AA00', fg='#FFFFFF', bd=0,
                  command=self._handle_login).pack(pady=(20,10))
        tk.Frame(panel, bg='#444444', height=1).pack(fill='x', padx=50, pady=10)
        tk.Button(panel, text="➕ 註冊", font=self.ui_font,
                  bg='#E94560', fg='#FFFFFF', bd=0,
                  command=self._open_register).pack(pady=5)

    def _handle_login(self):
        user = self.login_user.get().strip()
        pwd  = self.login_pass.get().strip()
        if user in self.users and self.users[user]['password'] == pwd:
            self.username = user
            self._start_game()
        else:
            messagebox.showerror('登入失敗', '帳號或密碼錯誤')

    def _open_register(self):
        dlg = tk.Toplevel(self.master)
        dlg.title('註冊新帳號')
        dlg.configure(bg='#1F2833')
        dlg.geometry('400x260')
        dlg.resizable(False, False)
        dlg.transient(self.master)
        dlg.grab_set()

        header = tk.Frame(dlg, bg='#16202A')
        header.pack(fill='x')
        tk.Label(header, text="➕ 新帳號註冊", font=self.ui_font,
                 fg='#FFFFFF', bg='#16202A').pack(pady=10)

        content = tk.Frame(dlg, bg='#1F2833')
        content.pack(fill='both', expand=True, padx=20, pady=10)
        tk.Label(content, text='用戶名：', font=self.ui_font,
                 fg='#CCCCCC', bg='#1F2833').grid(row=0, column=0, sticky='e', pady=8)
        entry_user = tk.Entry(content, font=self.ui_font, width=25,
                              bd=0, relief='flat', justify='center')
        entry_user.grid(row=0, column=1, pady=8, padx=(10,0))
        entry_user.configure(highlightthickness=1, highlightbackground='#444444')
        tk.Label(content, text='密碼：', font=self.ui_font,
                 fg='#CCCCCC', bg='#1F2833').grid(row=1, column=0, sticky='e', pady=8)
        entry_pwd = tk.Entry(content, font=self.ui_font, width=25,
                             show='*', bd=0, relief='flat', justify='center')
        entry_pwd.grid(row=1, column=1, pady=8, padx=(10,0))
        entry_pwd.configure(highlightthickness=1, highlightbackground='#444444')

        separator = tk.Frame(dlg, bg='#444444', height=1)
        separator.pack(fill='x', pady=(0,10))

        btn_frame = tk.Frame(dlg, bg='#1F2833')
        btn_frame.pack(fill='x', pady=(0,20))
        tk.Button(btn_frame, text='取消', font=self.ui_font,
                  bg='#555555', fg='#FFFFFF', bd=0, padx=20, pady=8,
                  command=dlg.destroy).pack(side='left', expand=True, padx=20)
        tk.Button(btn_frame, text='註冊', font=self.ui_font,
                  bg='#E94560', fg='#FFFFFF', bd=0, padx=20, pady=8,
                  command=lambda: self._handle_register(
                      entry_user.get(), entry_pwd.get(), dlg)
                 ).pack(side='right', expand=True, padx=20)

    def _handle_register(self, user, pwd, dlg):
        if not user or not pwd:
            messagebox.showwarning('輸入錯誤', '請填寫完整資料')
            return
        if user in self.users:
            messagebox.showinfo('提示', '帳號已存在')
            return
        self.users[user] = {'password': pwd, 'score': 0}
        self._save_json(USERS_FILE, self.users)
        messagebox.showinfo('註冊成功', '請使用新帳號登入')
        dlg.destroy()

    # — 遊戲畫面 —

    def _build_game(self):
        hdr = tk.Frame(self.game_frame, bg='#1F2833')
        hdr.pack(fill='x')
        self.user_label  = tk.Label(hdr, text='', font=self.ui_font,
                                    fg='#66FCF1', bg='#1F2833')
        self.user_label.pack(side='left', padx=20)
        self.score_label = tk.Label(hdr, text='分數：0', font=self.title_font,
                                    fg='#00FF00', bg='#1F2833')
        self.score_label.pack(side='left', padx=50)
        tk.Button(hdr, text='⏸ 暫停', font=self.ui_font,
                  bg='#555555', fg='#FFFFFF', bd=0,
                  command=self._pause_game).pack(side='right', padx=10)

        body = tk.Frame(self.game_frame, bg='#0B0C10')
        body.pack(expand=True, fill='both')
        card = tk.Frame(body, bg='#45A29E', bd=8, relief='ridge')
        card.place(relx=0.5, rely=0.3, anchor='center',
                   relwidth=0.6, relheight=0.2)
        self.question_label = tk.Label(card, text='', font=self.q_font,
                                       fg='#FFFFFF', bg='#45A29E')
        self.question_label.pack(expand=True)

        self.entry = tk.Entry(body, font=self.ui_font, justify='center')
        self.entry.place(relx=0.5, rely=0.5, anchor='center', width=300)
        self.entry.bind('<Return>', lambda e: self._check_answer())

        self.submit_btn = tk.Button(body, text='✔️ 提交', font=self.ui_font,
                                    bg='#0099FF', fg='#FFFFFF', bd=0,
                                    command=self._check_answer)
        self.submit_btn.place(relx=0.5, rely=0.6, anchor='center')

        self.timer_label = tk.Label(body, text='剩餘時間：', font=self.ui_font,
                                    fg='#FFAA00', bg='#0B0C10')
        self.timer_label.place(relx=0.5, rely=0.7, anchor='center')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Timer.Horizontal.TProgressbar',
                        troughcolor='#000000', thickness=20,
                        background='#00FF00')
        style.configure('Red.Horizontal.TProgressbar',
                        background='#FF0000')
        self.timerbar = ttk.Progressbar(body,
                                        style='Timer.Horizontal.TProgressbar',
                                        maximum=100)
        self.timerbar.place(relx=0.5, rely=0.75,
                            anchor='center', relwidth=0.6)

    def _build_leaderboard(self):
        tk.Label(self.leader_frame, text='🏆 排行榜 🏆',
                 font=self.ui_font, fg='#FFCE00',
                 bg='#1F2833').pack(pady=(10,0))
        self.board = ttk.Treeview(self.leader_frame,
                                  columns=('玩家','分數'),
                                  show='headings', height=5)
        self.board.heading('玩家', text='玩家')
        self.board.heading('分數', text='分數')
        self.board.column('玩家', anchor='center')
        self.board.column('分數', anchor='center')
        self.board.pack(pady=10)

    def _prompt_continue(self):
        dlg = tk.Toplevel(self.master)
        dlg.title('繼續進度')
        dlg.configure(bg='#1F2833')
        dlg.geometry('400x150')
        tk.Label(dlg, text='偵測到舊進度，是否繼續？',
                 font=self.ui_font, fg='#FFFFFF',
                 bg='#1F2833').pack(pady=20)
        frm = tk.Frame(dlg, bg='#1F2833')
        frm.pack()
        result = {'yes': False}
        def on_yes():
            result['yes'] = True
            dlg.destroy()
        def on_no():
            dlg.destroy()
        tk.Button(frm, text='是', font=self.ui_font,
                  bg='#00AA00', fg='#FFFFFF', bd=0,
                  command=on_yes).pack(side='left', padx=10)
        tk.Button(frm, text='否', font=self.ui_font,
                  bg='#AA0000', fg='#FFFFFF', bd=0,
                  command=on_no).pack(side='right', padx=10)
        dlg.transient(self.master)
        dlg.grab_set()
        self.master.wait_window(dlg)
        return result['yes']

    def _start_game(self):
        self.login_frame.pack_forget()
        self.leader_frame.pack(side='bottom', fill='x')
        self.game_frame.pack(fill='both', expand=True)

        self.user_label.config(text=f"玩家：{self.username}")

        state = self.states.get(self.username)
        if state and self._prompt_continue():
            self.score      = state['score']
            self.level      = state['level']
            self.time_limit = state['time_limit']
        else:
            if state:
                self._clear_state()
            self.score      = 0
            self.level      = 1
            self.time_limit = 15.0

        self.score_label.config(text=f"分數：{self.score}")
        self.min_time  = 3.0
        self.time_left = self.time_limit
        self._refresh_leaderboard()
        self._next_question()
        self._run_timer()

    def _refresh_leaderboard(self):
        self.board.delete(*self.board.get_children())
        ranking = sorted(self.users.items(),
                         key=lambda x: x[1]['score'],
                         reverse=True)[:5]
        for u, d in ranking:
            self.board.insert('', 'end',
                              values=(u, d['score']))

    def _generate_question(self):
        op = random.choice(['+','-','*'])
        a = random.randint(1, 5 + self.level*5)
        b = random.randint(1, 5 + self.level*5)
        if op=='-' and a<b:
            a, b = b, a
        self.answer = eval(f"{a}{op}{b}")
        return f"{a} {op} {b} = ?"

    def _next_question(self):
        self.time_limit = max(self.min_time,
                              self.time_limit * 0.9)
        self.time_left  = self.time_limit
        q = self._generate_question()
        self.question_label.config(text=q)
        self.entry.delete(0, tk.END)
        self.timerbar.config(value=100,
                             style='Timer.Horizontal.TProgressbar')
        self.timer_label.config(
            text=f"剩餘時間：{int(self.time_left)}s")

    def _run_timer(self):
        if self.time_left > 0:
            pct = int(100 * self.time_left / self.time_limit)
            self.timerbar['value'] = pct
            if self.time_left <= 5:
                self.timerbar.config(
                    style='Red.Horizontal.TProgressbar')
            self.timer_label.config(
                text=f"剩餘時間：{int(self.time_left)}s")
            self.time_left -= 1
            self.timer_id = self.master.after(
                1000, self._run_timer)
        else:
            self._end_game('⏰ 時間到！')

    def _check_answer(self):
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
        try:
            ans = int(self.entry.get())
        except:
            messagebox.showwarning('輸入無效', '請輸入數字')
            self._run_timer()
            return
        if ans == self.answer:
            self.score += 1
            if self.score > self.users[self.username]['score']:
                self.users[self.username]['score'] = self.score
                self._save_json(USERS_FILE, self.users)
            self.score_label.config(text=f"分數：{self.score}")
            self._refresh_leaderboard()
            self._next_question()
            self._run_timer()
        else:
            self._end_game('❌ 答錯了！')

    def _pause_game(self):
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
        dlg = tk.Toplevel(self.master)
        dlg.title('遊戲暫停')
        dlg.configure(bg='#1F2833')
        dlg.geometry('300x150')
        tk.Label(dlg, text='遊戲已暫停', font=self.q_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=10)
        frm = tk.Frame(dlg, bg='#1F2833')
        frm.pack(pady=10)
        tk.Button(frm, text='儲存並退出', font=self.ui_font,
                  bg='#AA0000', fg='#FFFFFF', bd=0,
                  command=lambda: (self._save_state(), dlg.destroy(), self._logout())
                 ).pack(side='left', padx=5)
        tk.Button(frm, text='繼續', font=self.ui_font,
                  bg='#00AA00', fg='#FFFFFF', bd=0,
                  command=lambda: (dlg.destroy(), self._run_timer())
                 ).pack(side='right', padx=5)

    def _end_game(self, msg):
        dlg = tk.Toplevel(self.master)
        dlg.title('遊戲結束')
        dlg.configure(bg='#1F2833')
        dlg.geometry('300x180')
        tk.Label(dlg, text=msg, font=self.q_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=10)
        tk.Label(dlg, text=f"你的分數：{self.score}",
                 font=self.ui_font, fg='#FFFF00',
                 bg='#1F2833').pack(pady=5)
        frm = tk.Frame(dlg, bg='#1F2833')
        frm.pack(pady=10)
        tk.Button(frm, text='再玩一局', font=self.ui_font,
                  bg='#00AA00', fg='#FFFFFF', bd=0,
                  command=lambda: (dlg.destroy(), self._play_again())
                 ).pack(side='left', padx=5)
        tk.Button(frm, text='退出', font=self.ui_font,
                  bg='#AA0000', fg='#FFFFFF', bd=0,
                  command=lambda: (dlg.destroy(), self._clear_state(), self._logout())
                 ).pack(side='right', padx=5)

    def _play_again(self):
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
        # 重置所有狀態
        self.score      = 0
        self.level      = 1
        self.time_limit = 15.0
        self.score_label.config(text=f"分數：{self.score}")
        self._refresh_leaderboard()
        self.time_left = self.time_limit
        self._next_question()
        self._run_timer()

    def _save_state(self):
        self.states[self.username] = {
            'score':self.score,
            'level':self.level,
            'time_limit':self.time_limit
        }
        self._save_json(STATE_FILE, self.states)
        self._save_json(USERS_FILE, self.users)

    def _clear_state(self):
        if self.username in self.states:
            del self.states[self.username]
            self._save_json(STATE_FILE, self.states)

    def _logout(self):
        # 返回主畫面
        if hasattr(self, 'timer_id'):
            self.master.after_cancel(self.timer_id)
        self._save_json(USERS_FILE, self.users)
        self.game_frame.pack_forget()
        self.leader_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    app = MathGameGUI(root)
    root.mainloop()
