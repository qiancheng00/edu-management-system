import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

# ===================== 全局配置 & 数据初始化 =====================
# 配色方案（现代简约风）
BG_COLOR = "#f5f7fa"       # 主背景
CARD_COLOR = "#ffffff"     # 卡片背景
PRIMARY_COLOR = "#409eff"  # 主色调（蓝）
TEXT_COLOR = "#333333"     # 正文文字
GRAY_COLOR = "#999999"     # 辅助文字
DANGER_COLOR = "#f56c6c"   # 警示红
SUCCESS_COLOR = "#67c23a"  # 成功绿

# 数据文件路径
USER_DATA_FILE = "user_data.json"
COURSE_DATA_FILE = "course_data.json"
SCORE_DATA_FILE = "score_data.json"
SELECT_DATA_FILE = "select_course.json"

# 初始化默认数据
def init_default_data():
    """初始化系统默认账号、课程数据"""
    # 用户数据：{账号: {密码, 角色, 状态(启用/禁用)}}
    default_users = {
        "admin": {"pwd": "123456", "role": "admin", "status": 1},
        "teacher1": {"pwd": "123456", "role": "teacher", "status": 1},
        "student1": {"pwd": "123456", "role": "student", "status": 1}
    }
    # 课程数据
    default_courses = {
        "C001": {"name": "Python编程", "teacher": "teacher1", "max_num": 30, "now_num": 0},
        "C002": {"name": "计算机网络", "teacher": "teacher1", "max_num": 25, "now_num": 0}
    }
    # 成绩数据
    default_scores = {}
    # 选课数据
    default_select = {}

    # 写入文件
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, ensure_ascii=False, indent=2)
    if not os.path.exists(COURSE_DATA_FILE):
        with open(COURSE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_courses, f, ensure_ascii=False, indent=2)
    if not os.path.exists(SCORE_DATA_FILE):
        with open(SCORE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_scores, f, ensure_ascii=False, indent=2)
    if not os.path.exists(SELECT_DATA_FILE):
        with open(SELECT_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_select, f, ensure_ascii=False, indent=2)

# 数据读写工具函数
def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化数据文件
init_default_data()

# ===================== 主程序类 =====================
class EduSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("现代教务管理系统")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # 全局登录用户信息
        self.current_user = ""
        self.current_role = ""

        # 先加载登录界面
        self.show_login_page()

    # ---------------------- 通用组件美化函数 ----------------------
    def create_card(self, parent, x, y, w, h):
        """创建圆角卡片容器"""
        card = tk.Frame(parent, bg=CARD_COLOR, relief=tk.RIDGE, bd=1)
        card.place(x=x, y=y, width=w, height=h)
        return card

    def create_btn(self, parent, text, command, x, y, w=100, h=35, color=PRIMARY_COLOR):
        """创建美化按钮"""
        btn = tk.Button(
            parent, text=text, command=command,
            bg=color, fg="white", font=("微软雅黑", 10),
            relief=tk.FLAT, bd=0, activebackground="#66b1ff"
        )
        btn.place(x=x, y=y, width=w, height=h)
        return btn

    # ---------------------- 1. 登录界面 ----------------------
    def show_login_page(self):
        # 清空原有界面
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root, text="现代教务管理系统",
            font=("微软雅黑", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR
        )
        title_label.place(x=380, y=120)

        # 登录卡片
        login_card = self.create_card(self.root, 320, 200, 360, 280)

        # 账号
        tk.Label(login_card, text="账号", font=("微软雅黑", 11), bg=CARD_COLOR, fg=TEXT_COLOR).place(x=50, y=40)
        self.var_username = tk.StringVar()
        entry_user = ttk.Entry(login_card, textvariable=self.var_username, font=("微软雅黑", 11))
        entry_user.place(x=110, y=40, width=200, height=30)

        # 密码
        tk.Label(login_card, text="密码", font=("微软雅黑", 11), bg=CARD_COLOR, fg=TEXT_COLOR).place(x=50, y=100)
        self.var_pwd = tk.StringVar()
        entry_pwd = ttk.Entry(login_card, textvariable=self.var_pwd, show="*", font=("微软雅黑", 11))
        entry_pwd.place(x=110, y=100, width=200, height=30)

        # 登录按钮
        self.create_btn(login_card, "立即登录", self.login_check, 130, 160, 100, 38)

        # 底部提示
        tip_label = tk.Label(
            self.root, text="默认账号：admin/teacher1/student1  密码统一：123456",
            font=("微软雅黑", 9), bg=BG_COLOR, fg=GRAY_COLOR
        )
        tip_label.place(x=340, y=520)

    # 登录校验
    def login_check(self):
        username = self.var_username.get().strip()
        pwd = self.var_pwd.get().strip()
        if not username or not pwd:
            messagebox.showwarning("提示", "账号和密码不能为空！")
            return

        user_data = read_json(USER_DATA_FILE)
        if username not in user_data:
            messagebox.showerror("错误", "账号不存在！")
            return

        user_info = user_data[username]
        # 校验账号状态（是否被管理员禁用）
        if user_info["status"] == 0:
            messagebox.showerror("禁止登录", "该账号已被管理员禁用！")
            return
        # 校验密码
        if user_info["pwd"] != pwd:
            messagebox.showerror("错误", "密码错误！")
            return

        # 登录成功，记录当前用户
        self.current_user = username
        self.current_role = user_info["role"]
        messagebox.showinfo("登录成功", f"欢迎您，{self.get_role_name(self.current_role)}！")
        # 跳转对应角色主页
        self.jump_main_page()

    # 角色名称转换
    def get_role_name(self, role):
        role_map = {"admin": "管理员", "teacher": "教师", "student": "学生"}
        return role_map.get(role, "未知角色")

    # ---------------------- 2. 主页面分发（按角色跳转） ----------------------
    def jump_main_page(self):
        if self.current_role == "admin":
            self.show_admin_page()
        elif self.current_role == "teacher":
            self.show_teacher_page()
        elif self.current_role == "student":
            self.show_student_page()

    # ---------------------- 通用功能：修改密码、退出登录 ----------------------
    def change_pwd(self):
        """修改密码"""
        pwd_win = tk.Toplevel(self.root)
        pwd_win.title("修改密码")
        pwd_win.geometry("400x220")
        pwd_win.configure(bg=BG_COLOR)
        pwd_win.grab_set()

        tk.Label(pwd_win, text="原密码", bg=BG_COLOR, font=("微软雅黑", 11)).place(x=60, y=30)
        old_pwd = ttk.Entry(pwd_win, show="*", font=("微软雅黑", 11))
        old_pwd.place(x=140, y=30, width=200, height=30)

        tk.Label(pwd_win, text="新密码", bg=BG_COLOR, font=("微软雅黑", 11)).place(x=60, y=80)
        new_pwd = ttk.Entry(pwd_win, show="*", font=("微软雅黑", 11))
        new_pwd.place(x=140, y=80, width=200, height=30)

        def save_pwd():
            o_p = old_pwd.get().strip()
            n_p = new_pwd.get().strip()
            if not o_p or not n_p:
                messagebox.showwarning("提示", "密码不能为空！")
                return
            user_data = read_json(USER_DATA_FILE)
            if user_data[self.current_user]["pwd"] != o_p:
                messagebox.showerror("错误", "原密码不正确！")
                return
            user_data[self.current_user]["pwd"] = n_p
            write_json(USER_DATA_FILE, user_data)
            messagebox.showinfo("成功", "密码修改完成！")
            pwd_win.destroy()

        self.create_btn(pwd_win, "保存修改", save_pwd, 150, 140, 100)

    def logout(self):
        """退出登录，返回登录页"""
        res = messagebox.askyesno("退出", "确定要退出当前账号吗？")
        if res:
            self.current_user = ""
            self.current_role = ""
            self.show_login_page()

    # ---------------------- 3. 管理员页面（权限管理、用户管理） ----------------------
    def show_admin_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("管理员中心 - 教务系统")

        # 顶部导航栏
        top_card = self.create_card(self.root, 0, 0, 1000, 60)
        tk.Label(
            top_card, text=f"当前登录：{self.current_user}（管理员）",
            font=("微软雅黑", 12), bg=CARD_COLOR, fg=TEXT_COLOR
        ).place(x=20, y=15)
        self.create_btn(top_card, "修改密码", self.change_pwd, 750, 12, 90)
        self.create_btn(top_card, "退出登录", self.logout, 860, 12, 90, color=DANGER_COLOR)

        # 功能卡片
        main_card = self.create_card(self.root, 20, 80, 960, 580)
        tk.Label(main_card, text="用户权限管理", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        # 表格展示所有用户
        columns = ("账号", "角色", "账号状态")
        self.admin_tree = ttk.Treeview(main_card, columns=columns, show="headings", height=18)
        for col in columns:
            self.admin_tree.heading(col, text=col)
            self.admin_tree.column(col, width=280, anchor="center")
        self.admin_tree.place(x=20, y=50, width=920)

        # 刷新用户列表
        self.refresh_user_list()

        # 操作按钮
        self.create_btn(main_card, "启用账号", self.enable_user, 220, 520)
        self.create_btn(main_card, "禁用账号", self.disable_user, 340, 520, color=DANGER_COLOR)
        self.create_btn(main_card, "新增用户", self.add_user, 460, 520, color=SUCCESS_COLOR)

    def refresh_user_list(self):
        """刷新用户表格"""
        # 清空旧数据
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        user_data = read_json(USER_DATA_FILE)
        role_map = {"admin": "管理员", "teacher": "教师", "student": "学生"}
        status_map = {1: "正常启用", 0: "已禁用"}
        for username, info in user_data.items():
            role = role_map[info["role"]]
            status = status_map[info["status"]]
            self.admin_tree.insert("", "end", values=(username, role, status))

    def enable_user(self):
        """启用选中账号"""
        select = self.admin_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请先选择用户！")
            return
        item = self.admin_tree.item(select[0])
        username = item["values"][0]
        user_data = read_json(USER_DATA_FILE)
        user_data[username]["status"] = 1
        write_json(USER_DATA_FILE, user_data)
        self.refresh_user_list()
        messagebox.showinfo("成功", f"账号 {username} 已启用！")

    def disable_user(self):
        """禁用选中账号"""
        select = self.admin_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请先选择用户！")
            return
        item = self.admin_tree.item(select[0])
        username = item["values"][0]
        if username == "admin":
            messagebox.showerror("禁止操作", "超级管理员账号不可禁用！")
            return
        user_data = read_json(USER_DATA_FILE)
        user_data[username]["status"] = 0
        write_json(USER_DATA_FILE, user_data)
        self.refresh_user_list()
        messagebox.showinfo("成功", f"账号 {username} 已禁用！")

    def add_user(self):
        """新增用户弹窗"""
        add_win = tk.Toplevel(self.root)
        add_win.title("新增用户")
        add_win.geometry("400x260")
        add_win.configure(bg=BG_COLOR)
        add_win.grab_set()

        tk.Label(add_win, text="账号", bg=BG_COLOR, font=("微软雅黑", 11)).place(x=60, y=30)
        var_acc = tk.StringVar()
        entry_acc = ttk.Entry(add_win, textvariable=var_acc, font=("微软雅黑", 11))
        entry_acc.place(x=140, y=30, width=200)

        tk.Label(add_win, text="初始密码", bg=BG_COLOR, font=("微软雅黑", 11)).place(x=60, y=80)
        var_p = tk.StringVar(value="123456")
        entry_p = ttk.Entry(add_win, textvariable=var_p, font=("微软雅黑", 11))
        entry_p.place(x=140, y=80, width=200)

        tk.Label(add_win, text="角色", bg=BG_COLOR, font=("微软雅黑", 11)).place(x=60, y=130)
        role_list = ["teacher", "student"]
        var_role = tk.StringVar(value="student")
        cbx_role = ttk.Combobox(add_win, textvariable=var_role, values=["教师", "学生"], state="readonly")
        cbx_role.place(x=140, y=130, width=200)

        def save_new_user():
            acc = var_acc.get().strip()
            pwd = var_p.get().strip()
            r_text = cbx_role.get()
            if not acc or not pwd:
                messagebox.showwarning("提示", "账号密码不能为空！")
                return
            user_data = read_json(USER_DATA_FILE)
            if acc in user_data:
                messagebox.showerror("错误", "账号已存在！")
                return
            r = "teacher" if r_text == "教师" else "student"
            user_data[acc] = {"pwd": pwd, "role": r, "status": 1}
            write_json(USER_DATA_FILE, user_data)
            self.refresh_user_list()
            messagebox.showinfo("成功", "用户新增完成！")
            add_win.destroy()

        self.create_btn(add_win, "确认新增", save_new_user, 150, 190, 100)

    # ---------------------- 4. 教师页面（课程管理、成绩管理） ----------------------
    def show_teacher_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("教师中心 - 教务系统")

        # 顶部导航
        top_card = self.create_card(self.root, 0, 0, 1000, 60)
        tk.Label(
            top_card, text=f"当前登录：{self.current_user}（教师）",
            font=("微软雅黑", 12), bg=CARD_COLOR
        ).place(x=20, y=15)
        self.create_btn(top_card, "修改密码", self.change_pwd, 750, 12, 90)
        self.create_btn(top_card, "退出登录", self.logout, 860, 12, 90, color=DANGER_COLOR)

        # 左侧功能菜单
        left_card = self.create_card(self.root, 20, 80, 140, 580)
        self.create_btn(left_card, "课程管理", self.show_course_tab, 20, 50, 100)
        self.create_btn(left_card, "成绩管理", self.show_score_tab, 20, 120, 100)

        # 右侧内容区
        self.right_card = self.create_card(self.root, 180, 80, 800, 580)
        self.show_course_tab()

    def show_course_tab(self):
        """教师-课程管理"""
        for w in self.right_card.winfo_children():
            w.destroy()
        tk.Label(self.right_card, text="我的课程管理", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        columns = ("课程编号", "课程名称", "授课教师", "最大人数", "已选人数")
        self.course_tree = ttk.Treeview(self.right_card, columns=columns, show="headings", height=16)
        for col in columns:
            self.course_tree.heading(col, text=col)
            self.course_tree.column(col, width=150, anchor="center")
        self.course_tree.place(x=20, y=50, width=750)
        self.refresh_course_list()

        self.create_btn(self.right_card, "新增课程", self.add_course, 120, 520, color=SUCCESS_COLOR)
        self.create_btn(self.right_card, "修改课程", self.edit_course, 240, 520)
        self.create_btn(self.right_card, "删除课程", self.del_course, 360, 520, color=DANGER_COLOR)

    def refresh_course_list(self):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        course_data = read_json(COURSE_DATA_FILE)
        for cid, info in course_data.items():
            self.course_tree.insert("", "end", values=(cid, info["name"], info["teacher"], info["max_num"], info["now_num"]))

    def add_course(self):
        win = tk.Toplevel(self.root)
        win.title("新增课程")
        win.geometry("380x220")
        win.configure(bg=BG_COLOR)
        win.grab_set()

        tk.Label(win, text="课程编号", bg=BG_COLOR).place(x=40, y=30)
        var_cid = tk.StringVar()
        ttk.Entry(win, textvariable=var_cid).place(x=120, y=30, width=200)

        tk.Label(win, text="课程名称", bg=BG_COLOR).place(x=40, y=80)
        var_cname = tk.StringVar()
        ttk.Entry(win, textvariable=var_cname).place(x=120, y=80, width=200)

        tk.Label(win, text="最大人数", bg=BG_COLOR).place(x=40, y=130)
        var_num = tk.StringVar()
        ttk.Entry(win, textvariable=var_num).place(x=120, y=130, width=200)

        def save():
            cid = var_cid.get().strip()
            cname = var_cname.get().strip()
            maxn = var_num.get().strip()
            if not cid or not cname or not maxn:
                messagebox.showwarning("提示", "信息不能为空！")
                return
            course_data = read_json(COURSE_DATA_FILE)
            if cid in course_data:
                messagebox.showerror("错误", "课程编号已存在！")
                return
            course_data[cid] = {"name": cname, "teacher": self.current_user, "max_num": int(maxn), "now_num": 0}
            write_json(COURSE_DATA_FILE, course_data)
            self.refresh_course_list()
            messagebox.showinfo("成功", "课程新增完成！")
            win.destroy()

        self.create_btn(win, "保存", save, 140, 170)

    def edit_course(self):
        select = self.course_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请选择课程！")
            return
        item = self.course_tree.item(select[0])
        cid = item["values"][0]
        course_data = read_json(COURSE_DATA_FILE)
        info = course_data[cid]

        win = tk.Toplevel(self.root)
        win.title("修改课程")
        win.geometry("380x220")
        win.configure(bg=BG_COLOR)
        win.grab_set()

        tk.Label(win, text="课程名称", bg=BG_COLOR).place(x=40, y=50)
        var_cname = tk.StringVar(value=info["name"])
        ttk.Entry(win, textvariable=var_cname).place(x=120, y=50, width=200)

        tk.Label(win, text="最大人数", bg=BG_COLOR).place(x=40, y=100)
        var_num = tk.StringVar(value=str(info["max_num"]))
        ttk.Entry(win, textvariable=var_num).place(x=120, y=100, width=200)

        def save():
            cname = var_cname.get().strip()
            maxn = var_num.get().strip()
            if not cname or not maxn:
                messagebox.showwarning("提示", "信息不能为空！")
                return
            course_data[cid]["name"] = cname
            course_data[cid]["max_num"] = int(maxn)
            write_json(COURSE_DATA_FILE, course_data)
            self.refresh_course_list()
            messagebox.showinfo("成功", "课程修改完成！")
            win.destroy()

        self.create_btn(win, "保存", save, 140, 150)

    def del_course(self):
        select = self.course_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请选择课程！")
            return
        item = self.course_tree.item(select[0])
        cid = item["values"][0]
        res = messagebox.askyesno("确认", f"确定删除课程 {cid}？")
        if res:
            course_data = read_json(COURSE_DATA_FILE)
            del course_data[cid]
            write_json(COURSE_DATA_FILE, course_data)
            self.refresh_course_list()
            messagebox.showinfo("成功", "课程已删除！")

    def show_score_tab(self):
        """教师-成绩管理"""
        for w in self.right_card.winfo_children():
            w.destroy()
        tk.Label(self.right_card, text="学生成绩录入/修改", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        columns = ("学生账号", "课程编号", "成绩")
        self.score_tree = ttk.Treeview(self.right_card, columns=columns, show="headings", height=16)
        for col in columns:
            self.score_tree.heading(col, text=col)
            self.score_tree.column(col, width=240, anchor="center")
        self.score_tree.place(x=20, y=50, width=750)
        self.refresh_score_list()

        self.create_btn(self.right_card, "录入成绩", self.add_score, 220, 520)
        self.create_btn(self.right_card, "修改成绩", self.edit_score, 340, 520)

    def refresh_score_list(self):
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        score_data = read_json(SCORE_DATA_FILE)
        for stu, c_dict in score_data.items():
            for cid, score in c_dict.items():
                self.score_tree.insert("", "end", values=(stu, cid, score))

    def add_score(self):
        win = tk.Toplevel(self.root)
        win.title("录入成绩")
        win.geometry("380x200")
        win.configure(bg=BG_COLOR)
        win.grab_set()

        tk.Label(win, text="学生账号", bg=BG_COLOR).place(x=40, y=30)
        var_stu = tk.StringVar()
        ttk.Entry(win, textvariable=var_stu).place(x=120, y=30, width=200)

        tk.Label(win, text="课程编号", bg=BG_COLOR).place(x=40, y=80)
        var_cid = tk.StringVar()
        ttk.Entry(win, textvariable=var_cid).place(x=120, y=80, width=200)

        tk.Label(win, text="成绩", bg=BG_COLOR).place(x=40, y=130)
        var_sc = tk.StringVar()
        ttk.Entry(win, textvariable=var_sc).place(x=120, y=130, width=200)

        def save():
            stu = var_stu.get().strip()
            cid = var_cid.get().strip()
            sc = var_sc.get().strip()
            if not stu or not cid or not sc:
                messagebox.showwarning("提示", "信息不能为空！")
                return
            score_data = read_json(SCORE_DATA_FILE)
            if stu not in score_data:
                score_data[stu] = {}
            score_data[stu][cid] = sc
            write_json(SCORE_DATA_FILE, score_data)
            self.refresh_score_list()
            messagebox.showinfo("成功", "成绩录入完成！")
            win.destroy()

        self.create_btn(win, "保存", save, 140, 160)

    def edit_score(self):
        select = self.score_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请选择记录！")
            return
        item = self.score_tree.item(select[0])
        stu, cid, old_sc = item["values"]

        win = tk.Toplevel(self.root)
        win.title("修改成绩")
        win.geometry("300x150")
        win.configure(bg=BG_COLOR)
        win.grab_set()

        tk.Label(win, text="新成绩", bg=BG_COLOR).place(x=40, y=40)
        var_sc = tk.StringVar(value=old_sc)
        ttk.Entry(win, textvariable=var_sc).place(x=100, y=40, width=160)

        def save():
            new_sc = var_sc.get().strip()
            if not new_sc:
                messagebox.showwarning("提示", "成绩不能为空！")
                return
            score_data = read_json(SCORE_DATA_FILE)
            score_data[stu][cid] = new_sc
            write_json(SCORE_DATA_FILE, score_data)
            self.refresh_score_list()
            messagebox.showinfo("成功", "成绩修改完成！")
            win.destroy()

        self.create_btn(win, "保存", save, 100, 90)

    # ---------------------- 5. 学生页面（选课、课表、查成绩） ----------------------
    def show_student_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("学生中心 - 教务系统")

        # 顶部导航
        top_card = self.create_card(self.root, 0, 0, 1000, 60)
        tk.Label(
            top_card, text=f"当前登录：{self.current_user}（学生）",
            font=("微软雅黑", 12), bg=CARD_COLOR
        ).place(x=20, y=15)
        self.create_btn(top_card, "修改密码", self.change_pwd, 750, 12, 90)
        self.create_btn(top_card, "退出登录", self.logout, 860, 12, 90, color=DANGER_COLOR)

        # 左侧菜单
        left_card = self.create_card(self.root, 20, 80, 140, 580)
        self.create_btn(left_card, "在线选课", self.show_select_tab, 20, 50, 100)
        self.create_btn(left_card, "我的课表", self.show_schedule_tab, 20, 120, 100)
        self.create_btn(left_card, "我的成绩", self.show_my_score_tab, 20, 190, 100)

        # 右侧内容区
        self.stu_right = self.create_card(self.root, 180, 80, 800, 580)
        self.show_select_tab()

    def show_select_tab(self):
        """学生-在线选课"""
        for w in self.stu_right.winfo_children():
            w.destroy()
        tk.Label(self.stu_right, text="在线选课中心", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        columns = ("课程编号", "课程名称", "授课教师", "剩余名额")
        self.select_tree = ttk.Treeview(self.stu_right, columns=columns, show="headings", height=16)
        for col in columns:
            self.select_tree.heading(col, text=col)
            self.select_tree.column(col, width=180, anchor="center")
        self.select_tree.place(x=20, y=50, width=750)
        self.refresh_select_course()

        self.create_btn(self.stu_right, "选择课程", self.select_course, 300, 520, color=SUCCESS_COLOR)

    def refresh_select_course(self):
        for item in self.select_tree.get_children():
            self.select_tree.delete(item)
        course_data = read_json(COURSE_DATA_FILE)
        for cid, info in course_data.items():
            rest = info["max_num"] - info["now_num"]
            self.select_tree.insert("", "end", values=(cid, info["name"], info["teacher"], rest))

    def select_course(self):
        select = self.select_tree.selection()
        if not select:
            messagebox.showwarning("提示", "请选择课程！")
            return
        item = self.select_tree.item(select[0])
        cid = item["values"][0]
        rest = int(item["values"][3])
        if rest <= 0:
            messagebox.showerror("提示", "该课程名额已满！")
            return

        select_data = read_json(SELECT_DATA_FILE)
        course_data = read_json(COURSE_DATA_FILE)
        stu = self.current_user

        # 判断是否已选
        if stu not in select_data:
            select_data[stu] = []
        if cid in select_data[stu]:
            messagebox.showwarning("提示", "您已选过该课程！")
            return

        # 选课
        select_data[stu].append(cid)
        course_data[cid]["now_num"] += 1
        write_json(SELECT_DATA_FILE, select_data)
        write_json(COURSE_DATA_FILE, course_data)
        self.refresh_select_course()
        messagebox.showinfo("成功", "选课完成！")

    def show_schedule_tab(self):
        """学生-我的课表"""
        for w in self.stu_right.winfo_children():
            w.destroy()
        tk.Label(self.stu_right, text="我的个人课表", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        columns = ("课程编号", "课程名称", "授课教师")
        self.sch_tree = ttk.Treeview(self.stu_right, columns=columns, show="headings", height=16)
        for col in columns:
            self.sch_tree.heading(col, text=col)
            self.sch_tree.column(col, width=240, anchor="center")
        self.sch_tree.place(x=20, y=50, width=750)

        select_data = read_json(SELECT_DATA_FILE)
        course_data = read_json(COURSE_DATA_FILE)
        stu = self.current_user
        if stu in select_data:
            for cid in select_data[stu]:
                info = course_data[cid]
                self.sch_tree.insert("", "end", values=(cid, info["name"], info["teacher"]))

    def show_my_score_tab(self):
        """学生-我的成绩"""
        for w in self.stu_right.winfo_children():
            w.destroy()
        tk.Label(self.stu_right, text="我的考试成绩", font=("微软雅黑", 14, "bold"), bg=CARD_COLOR).place(x=20, y=15)

        columns = ("课程编号", "课程名称", "成绩")
        self.score_stu_tree = ttk.Treeview(self.stu_right, columns=columns, show="headings", height=16)
        for col in columns:
            self.score_stu_tree.heading(col, text=col)
            self.score_stu_tree.column(col, width=240, anchor="center")
        self.score_stu_tree.place(x=20, y=50, width=750)

        score_data = read_json(SCORE_DATA_FILE)
        course_data = read_json(COURSE_DATA_FILE)
        stu = self.current_user
        if stu in score_data:
            for cid, sc in score_data[stu].items():
                cname = course_data[cid]["name"]
                self.score_stu_tree.insert("", "end", values=(cid, cname, sc))

# ===================== 程序入口 =====================
if __name__ == "__main__":
    root = tk.Tk()
    app = EduSystem(root)
    root.mainloop()