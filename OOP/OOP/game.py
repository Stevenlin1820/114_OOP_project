import tkinter as tk
from tkinter import ttk, font, messagebox
import random
import json
import os

"""
math_game.py

功能：
- 登入/註冊（帳號+密碼+最高分）
- 主選單（開始遊戲）
- 四則速算 (+, -, ×, ÷)，答案皆為正整數
- 20 級，每級 10 題，限時逐級 ×0.9（最短 3 秒）
- 隨局排行榜顯示前 5 名
- 暫停、進度續玩
- 遊戲結束後可再玩一局或返回選單

執行： python math_game.py
"""

# --------------------- 全局設定 ---------------------
USERS_FILE          = 'math_game_users.json'
STATE_FILE          = 'math_game_state.json'
MAX_LEVEL           = 20
QUESTIONS_PER_LEVEL = 10
TIME_SHRINK_RATE    = 0.9
BASE_TIME_LIMIT     = 15.0
MIN_TIME_LIMIT      = 3.0

class MathGameGUI:
    def __init__(self, master):
        self.master = master
        master.title('🎮 數學奇幻冒險 🎮')
        master.state('zoomed')
        master.configure(bg='#0B0C10')

        # 字體設定
        self.title_font = font.Font(family='Comic Sans MS', size=48, weight='bold')
        self.ui_font    = font.Font(family='微軟正黑體',    size=16)
        self.q_font     = font.Font(family='Arial',         size=32, weight='bold')

        # 載入資料
        self.users  = self._load_json(USERS_FILE)
        self.states = self._load_json(STATE_FILE)

        # 建構三大畫面
        self.login_frame = tk.Frame(master, bg='#0B0C10')
        self.menu_frame  = tk.Frame(master, bg='#0B0C10')
        self.game_frame  = tk.Frame(master, bg='#0B0C10')

        # 先建構所有內容
        self._build_login()
        self._build_menu()
        self._build_game()

        # 初始顯示登入
        self.login_frame.pack(fill='both', expand=True)

    # --------- JSON I/O ---------
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

    # ------ 登入/註冊 ------
    def _build_login(self):
        panel = tk.Frame(self.login_frame, bg='#1F2833', bd=2, relief='ridge')
        panel.place(relx=0.5, rely=0.5, anchor='center', width=600, height=400)
        tk.Label(panel, text='🌟 數學奇幻冒險 🌟', font=self.title_font,
                 fg='#FFD700', bg='#1F2833').pack(pady=(20,10))
        tk.Label(panel, text='用戶名：', font=self.ui_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=5)
        self.login_user = tk.Entry(panel, font=self.ui_font, width=30, justify='center')
        self.login_user.pack(pady=5)
        tk.Label(panel, text='密碼：', font=self.ui_font,
                 fg='#FFFFFF', bg='#1F2833').pack(pady=5)
        self.login_pass = tk.Entry(panel, font=self.ui_font, show='*', width=30, justify='center')
        self.login_pass.pack(pady=5)
        tk.Button(panel, text='🔑 登入', font=self.ui_font, bg='#00AA00', fg='#FFFFFF', bd=0,
                  command=self._handle_login).pack(pady=(20,5))
        tk.Button(panel, text='➕ 註冊', font=self.ui_font, bg='#E94560', fg='#FFFFFF', bd=0,
                  command=self._open_register).pack(pady=5)

    def _handle_login(self):
        user, pwd = self.login_user.get().strip(), self.login_pass.get().strip()
        if user in self.users and self.users[user]['password'] == pwd:
            self.username = user
            self.login_frame.pack_forget()
            self.menu_frame.pack(fill='both', expand=True)
        else:
            messagebox.showerror('登入失敗', '帳號或密碼錯誤')

    def _open_register(self):
        dlg = tk.Toplevel(self.master)
        dlg.title('➕ 註冊新帳號')
        dlg.configure(bg='#1F2833'); dlg.geometry('400x260'); dlg.resizable(False,False)
        dlg.transient(self.master); dlg.grab_set()
        tk.Label(dlg, text='➕ 新帳號註冊', font=self.ui_font,
                 fg='#FFFFFF', bg='#16202A').pack(fill='x')
        frm = tk.Frame(dlg, bg='#1F2833'); frm.pack(padx=20,pady=20)
        tk.Label(frm, text='用戶名：', font=self.ui_font, fg='#CCCCCC', bg='#1F2833').grid(row=0,column=0)
        e_user = tk.Entry(frm, font=self.ui_font, width=25, justify='center'); e_user.grid(row=0,column=1)
        tk.Label(frm, text='密碼：', font=self.ui_font, fg='#CCCCCC', bg='#1F2833').grid(row=1,column=0)
        e_pwd  = tk.Entry(frm, font=self.ui_font, width=25, show='*', justify='center'); e_pwd.grid(row=1,column=1)
        btnf = tk.Frame(dlg, bg='#1F2833'); btnf.pack(fill='x', pady=(0,20))
        tk.Button(btnf, text='取消', font=self.ui_font, bg='#555555', fg='#FFFFFF', bd=0,
                  command=dlg.destroy).pack(side='left', expand=True, padx=20)
        tk.Button(btnf, text='註冊', font=self.ui_font, bg='#E94560', fg='#FFFFFF', bd=0,
                  command=lambda: self._handle_register(e_user.get(), e_pwd.get(), dlg)
        ).pack(side='right', expand=True, padx=20)

    def _handle_register(self, user, pwd, dlg):
        if not user or not pwd:
            messagebox.showwarning('輸入錯誤', '請填寫完整資料'); return
        if user in self.users:
            messagebox.showinfo('提示', '帳號已存在'); return
        self.users[user] = {'password': pwd, 'score': 0}
        self._save_json(USERS_FILE, self.users)
        messagebox.showinfo('註冊成功', '請使用新帳號登入')
        dlg.destroy()

    # ------ 主選單 ------
    def _build_menu(self):
        for w in self.menu_frame.winfo_children():
            w.destroy()
        btn = tk.Button(self.menu_frame, text='▶️ 開始遊戲', font=self.ui_font,
                        bg='#00AA00', fg='#FFFFFF', bd=0,
                        command=self._on_start_game)
        btn.pack(expand=True)

    def _on_start_game(self):
        self.menu_frame.pack_forget()
        self._start_game()

    # ------ 遊戲畫面 ------
    def _build_game(self):
        # Header
        hdr = tk.Frame(self.game_frame, bg='#1F2833'); hdr.pack(fill='x')
        self.user_label  = tk.Label(hdr, text='', font=self.ui_font, fg='#66FCF1', bg='#1F2833'); self.user_label.pack(side='left', padx=20)
        self.score_label = tk.Label(hdr, text='分數：0  等級：1', font=self.title_font, fg='#00FF00', bg='#1F2833'); self.score_label.pack(side='left', padx=50)
        tk.Button(hdr, text='⏸ 暫停', font=self.ui_font, bg='#555555', fg='#FFFFFF', bd=0, command=self._pause_game).pack(side='right', padx=10)
        # Body
        body = tk.Frame(self.game_frame, bg='#0B0C10'); body.pack(expand=True, fill='both')
        card = tk.Frame(body, bg='#45A29E', bd=8, relief='ridge')
        card.place(relx=0.5, rely=0.25, anchor='center', relwidth=0.6, relheight=0.2)
        self.question_label = tk.Label(card, text='', font=self.q_font, fg='#FFFFFF', bg='#45A29E'); self.question_label.pack(expand=True)
        self.entry = tk.Entry(body, font=self.ui_font, justify='center'); self.entry.place(relx=0.5, rely=0.5, anchor='center', width=300); self.entry.bind('<Return>', lambda e: self._check_answer())
        self.submit_btn = tk.Button(body, text='✔️ 提交', font=self.ui_font, bg='#0099FF', fg='#FFFFFF', bd=0, command=self._check_answer); self.submit_btn.place(relx=0.5, rely=0.6, anchor='center')
        # Timer
        self.timer_label = tk.Label(body, text='剩餘時間：', font=self.ui_font, fg='#FFAA00', bg='#0B0C10'); self.timer_label.place(relx=0.5, rely=0.7, anchor='center')
        style = ttk.Style(); style.theme_use('clam'); style.configure('Timer.Horizontal.TProgressbar', troughcolor='#000000', thickness=20, background='#00FF00'); style.configure('Red.Horizontal.TProgressbar', background='#FF0000')
        self.timerbar = ttk.Progressbar(body, style='Timer.Horizontal.TProgressbar', maximum=100); self.timerbar.place(relx=0.5, rely=0.75, anchor='center', relwidth=0.6)
        # 排行榜
        lbf = tk.Frame(self.game_frame, bg='#1F2833'); lbf.pack(fill='x', pady=(20,0))
        tk.Label(lbf, text='🏆 排行榜 🏆', font=self.ui_font, fg='#FFCE00', bg='#1F2833').pack(pady=(5,2))
        self.board = ttk.Treeview(lbf, columns=('玩家','分數'), show='headings', height=5)
        self.board.heading('玩家', text='玩家'); self.board.heading('分數', text='分數')
        self.board.column('玩家', anchor='center'); self.board.column('分數', anchor='center')
        self.board.pack(padx=20, pady=(0,10))

    # ------ 遊戲流程 ------
    def _prompt_continue(self):
        dlg = tk.Toplevel(self.master); dlg.title('續玩進度？'); dlg.configure(bg='#1F2833'); dlg.geometry('400x150')
        tk.Label(dlg, text='偵測到舊進度，是否繼續？', font=self.ui_font, fg='#FFFFFF', bg='#1F2833').pack(pady=20)
        frm = tk.Frame(dlg, bg='#1F2833'); frm.pack()
        res = {'yes': False}
        tk.Button(frm, text='是', font=self.ui_font, bg='#00AA00', fg='#FFFFFF', bd=0, command=lambda:(res.update({'yes':True}), dlg.destroy())).pack(side='left', padx=10)
        tk.Button(frm, text='否', font=self.ui_font, bg='#AA0000', fg='#FFFFFF', bd=0, command=dlg.destroy).pack(side='right', padx=10)
        dlg.transient(self.master); dlg.grab_set(); self.master.wait_window(dlg)
        return res['yes']

    def _start_game(self):
        self.menu_frame.pack_forget(); self.game_frame.pack(fill='both', expand=True)
        self.user_label.config(text=f"玩家：{self.username}")
        state = self.states.get(self.username)
        if state and self._prompt_continue():
            self.score, self.level, self.time_limit = state['score'], state['level'], state['time_limit']
        else:
            self.score, self.level, self.time_limit = 0, 1, BASE_TIME_LIMIT
        self.correct_count = 0
        self._update_status(); self._refresh_leaderboard(); self._next_question(); self._run_timer()

    def _update_status(self):
        self.score_label.config(text=f"分數：{self.score}  等級：{self.level}")

    def _refresh_leaderboard(self):
        for row in self.board.get_children(): self.board.delete(row)
        ranking = sorted(self.users.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
        for u,d in ranking: self.board.insert('', 'end', values=(u, d['score']))

    def _generate_question(self):
        # 支援 + - × ÷，並讓 ÷ 的答案為整數
        ops = ['+','-','*','/']
        op = random.choice(ops)
        max_n = 5 + self.level * 5

        if op == '/':
            # 先隨機 b、ans，再算 a = b*ans
            b   = random.randint(1, max_n)
            ans = random.randint(1, max_n)
            a   = b * ans
        else:
            a = random.randint(1, max_n)
            b = random.randint(1, max_n)
            # 減法確保不負
            if op == '-' and a < b:
                a, b = b, a
            ans = a + b if op == '+' else a - b if op == '-' else a * b

        # 顯示用符號
        disp_op = {'+': '+', '-': '-', '*': '×', '/': '÷'}[op]
        self.answer = ans
        return f"{a} {disp_op} {b} = ?"


    def _next_question(self):
        if self.level>MAX_LEVEL: return self._end_game('🎉 恭喜完成所有關卡！')
        self.time_left=self.time_limit
        q=self._generate_question(); self.question_label.config(text=q)
        self.entry.delete(0, tk.END); self.timerbar.config(value=100, style='Timer.Horizontal.TProgressbar')
        self.timer_label.config(text=f"剩餘時間：{self.time_left:.1f}s")

    def _run_timer(self):
        if self.time_left>0:
            pct=int(100*self.time_left/self.time_limit); self.timerbar['value']=pct
            if self.time_left<=5: self.timerbar.config(style='Red.Horizontal.TProgressbar')
            self.timer_label.config(text=f"剩餘時間：{self.time_left:.1f}s")
            self.time_left-=1; self.timer_id=self.master.after(1000,self._run_timer)
        else: self._end_game('⏰ 時間到！')

    def _check_answer(self):
        if hasattr(self,'timer_id'): self.master.after_cancel(self.timer_id)
        try: ans=int(self.entry.get())
        except: messagebox.showwarning('輸入無效','請輸入數字'); self._run_timer(); return
        if ans==self.answer:
            self.score+=1; self.correct_count+=1
            if self.correct_count>=QUESTIONS_PER_LEVEL:
                self.level+=1; self.correct_count=0
                self.time_limit=max(MIN_TIME_LIMIT,self.time_limit*TIME_SHRINK_RATE)
            if self.score>self.users[self.username]['score']: self.users[self.username]['score']=self.score; self._save_json(USERS_FILE,self.users)
            self._update_status(); self._next_question(); self._run_timer()
        else: self._end_game('❌ 答錯了！')

    def _pause_game(self):
        if hasattr(self,'timer_id'): self.master.after_cancel(self.timer_id)
        dlg=tk.Toplevel(self.master); dlg.title('遊戲暫停'); dlg.configure(bg='#1F2833'); dlg.geometry('300x150')
        tk.Label(dlg,text='遊戲已暫停',font=self.q_font,fg='#FFFFFF',bg='#1F2833').pack(pady=10)
        frm=tk.Frame(dlg,bg='#1F2833'); frm.pack(pady=10)
        tk.Button(frm,text='儲存並退出',font=self.ui_font,bg='#AA0000',fg='#FFFFFF',bd=0,command=lambda:(self._save_state(),dlg.destroy(),self.menu_frame.pack(fill='both',expand=True))).pack(side='left',padx=5)
        tk.Button(frm,text='繼續',font=self.ui_font,bg='#00AA00',fg='#FFFFFF',bd=0,command=lambda:(dlg.destroy(),self._run_timer())).pack(side='right',padx=5)

    def _end_game(self,msg):
        if hasattr(self,'timer_id'): self.master.after_cancel(self.timer_id)
        dlg=tk.Toplevel(self.master); dlg.title('遊戲結束'); dlg.configure(bg='#1F2833'); dlg.geometry('300x180')
        tk.Label(dlg,text=msg,font=self.q_font,fg='#FFFFFF',bg='#1F2833').pack(pady=10)
        tk.Label(dlg,text=f"你的分數：{self.score}",font=self.ui_font,fg='#FFFF00',bg='#1F2833').pack(pady=5)
        frm=tk.Frame(dlg,bg='#1F2833'); frm.pack(pady=10)
        def on_exit(): dlg.destroy(); self.game_frame.pack_forget(); self.menu_frame.pack(fill='both',expand=True)
        def on_retry(): dlg.destroy(); self._play_again()
        tk.Button(frm,text='再玩一局',font=self.ui_font,bg='#00AA00',fg='#FFFFFF',bd=0,command=on_retry).pack(side='left',padx=5)
        tk.Button(frm,text='退出',font=self.ui_font,bg='#AA0000',fg='#FFFFFF',bd=0,command=on_exit).pack(side='right',padx=5)
        dlg.protocol('WM_DELETE_WINDOW',on_exit)

    def _play_again(self):
        if hasattr(self,'timer_id'): self.master.after_cancel(self.timer_id)
        self.score=0; self.level=1; self.correct_count=0; self.time_limit=BASE_TIME_LIMIT
        self._update_status(); self._next_question(); self._run_timer()

    def _save_state(self):
        self.states[self.username]={'score':self.score,'level':self.level,'time_limit':self.time_limit}
        self._save_json(STATE_FILE,self.states)

    def _clear_state(self):
        if self.username in self.states:
            del self.states[self.username]; self._save_json(STATE_FILE,self.states)

# 主程式入口
if __name__=='__main__':
    root=tk.Tk(); app=MathGameGUI(root); root.mainloop()
