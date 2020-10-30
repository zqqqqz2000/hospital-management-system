from tkinter import Tk
from tkinter import *
from tkinter import messagebox
import hashlib
from dao.login import Login as Login_dao
from global_var import DBSession


class Register:
    def __init__(self, root: Tk):
        self.root = root
        self.page = Frame(self.root)
        self.page.pack()

        self.root.title('注册')
        self.root.geometry('240x110')

        # 账号Frame
        username_frame = Frame(self.page)
        username_frame.pack(side=TOP)
        username_label = Label(username_frame, text='账号')
        username_label.pack(side=LEFT)
        self.username_var = StringVar()
        username_entry = Entry(username_frame, textvariable=self.username_var)
        username_entry.pack(side=LEFT)

        # 密码Frame
        password_frame = Frame(self.page)
        password_frame.pack(side=TOP)
        password_label = Label(password_frame, text='密码')
        password_label.pack(side=LEFT)
        self.password_var = StringVar()
        password_entry = Entry(password_frame, textvariable=self.password_var, show='*')
        password_entry.pack(side=LEFT)

        # 按钮Frame
        btn_frame = Frame(self.page)
        btn_frame.pack(side=TOP)
        # 注册按钮
        register_btn = Button(btn_frame, text='注册', command=self.register)
        register_btn.pack(side=LEFT, padx=5)
        # 登录按钮
        login_btn = Button(btn_frame, text='返回', command=self.back)
        login_btn.pack(side=LEFT, padx=5)

    def back(self):
        from view.login import Login
        self.page.destroy()
        Login(self.root)

    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        m = hashlib.md5()
        m.update(password.encode())
        pass_hash = m.hexdigest()

        session = DBSession()
        login_dao = Login_dao(
            username=username,
            password=pass_hash
        )
        try:
            session.add(login_dao)
            session.commit()
        except:
            messagebox.showerror("错误", "用户名已存在或不可为空!")
        else:
            messagebox.showinfo("成功", f"用户{username}已注册成功!")
        finally:
            session.close()
