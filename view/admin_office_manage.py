from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from global_var import DBSession
from dao.office import Office
from typing import *


class AdminOfficeManage:
    def __init__(self, root: Tk):
        self.offices = []
        # 读入所有科室
        self.root = root
        self.page = Frame(self.root)
        self.page.pack()

        self.root.title('科室管理')
        self.root.geometry('260x370')

        # 科室名Frame
        office_name_frame = Frame(self.page)
        office_name_frame.pack(side=TOP)
        office_name_label = Label(office_name_frame, text='科室名称')
        office_name_label.pack(side=LEFT)
        self.office_name_var = StringVar()
        office_name_entry = Entry(office_name_frame, textvariable=self.office_name_var)
        office_name_entry.pack(side=LEFT)

        # 科室地址Frame
        office_addr_frame = Frame(self.page)
        office_addr_frame.pack(side=TOP)
        office_addr_label = Label(office_addr_frame, text='科室地址')
        office_addr_label.pack(side=LEFT)
        self.office_addr_var = StringVar()
        office_addr_entry = Entry(office_addr_frame, textvariable=self.office_addr_var)
        office_addr_entry.pack(side=LEFT)

        # 科室电话Frame
        office_tele_frame = Frame(self.page)
        office_tele_frame.pack(side=TOP)
        office_tele_label = Label(office_tele_frame, text='科室电话')
        office_tele_label.pack(side=LEFT)
        self.office_tele_var = StringVar()
        office_addr_entry = Entry(office_tele_frame, textvariable=self.office_tele_var)
        office_addr_entry.pack(side=LEFT)

        # 提交按钮
        btn_frame = Frame(self.page)
        commit_button = Button(btn_frame, text='提交', command=self.insert_office)
        commit_button.pack(side=LEFT)
        commit_button = Button(btn_frame, text='修改', command=self.change)
        commit_button.pack(side=LEFT)
        btn_frame.pack(side=TOP)

        # 表格
        self.tb = ttk.Treeview(self.page, columns=('0', '1', '2', '3'), show="headings")
        self.tb.column("0", width=50, anchor='center')
        self.tb.column("1", width=50, anchor='center')
        self.tb.column("2", width=80, anchor='center')
        self.tb.column("3", width=80, anchor='center')
        self.tb.heading("0", text="id")
        self.tb.heading("1", text="名称")
        self.tb.heading("2", text="地址")
        self.tb.heading("3", text="电话")
        self.tb.bind('<ButtonRelease-1>', self.tb_bind)
        self.tb.pack(side=TOP)
        self.refresh_table()

        # 返回按钮
        return_button = Button(self.page, text='返回', command=self.back)
        return_button.pack(side=TOP)

    def change(self):
        name = self.office_name_var.get()
        session = DBSession()
        office: Optional[Office] = session.query(Office).filter_by(
            office_name=name
        ).first()
        if office:
            office.office_address = self.office_addr_var.get()
            office.office_telephone = self.office_tele_var.get()
            session.commit()
            messagebox.showinfo('成功', '修改科室信息成功')
        else:
            messagebox.showerror('找不到科室', f'找不到名为 {name} 的科室.')
        session.close()
        self.refresh_table()

    def back(self):
        from view.menu import ChoiceMenu
        self.page.destroy()
        ChoiceMenu(self.root)

    def tb_bind(self, event):
        id_ = None
        for item in self.tb.selection():
            item_text = self.tb.item(item, "values")
            id_ = item_text[0]
        if id_:
            session = DBSession()
            try:
                o: Office = session.query(Office).filter_by(id=id_).first()
                session.delete(o)
                session.commit()
            except:
                messagebox.showerror('错误', '该科室已被病房或医生绑定')
            session.close()
        self.refresh_table()

    def refresh_table(self):
        for item in self.tb.get_children():
            self.tb.delete(item)
        session = DBSession()
        offices: List[Office] = session.query(Office).filter().all()
        self.offices = [{
            'id': office.id,
            'office_name': office.office_name,
            'office_address': office.office_address,
            'office_telephone': office.office_telephone
        } for office in offices]
        session.close()
        for office in self.offices:
            self.tb.insert("", 0, values=[
                office['id'],
                office['office_name'],
                office['office_address'],
                office['office_telephone'],
            ])

    def insert_office(self):
        session = DBSession()
        try:
            office = Office(
                office_name=self.office_name_var.get(),
                office_address=self.office_addr_var.get(),
                office_telephone=self.office_tele_var.get()
            )
            session.add(office)
            session.commit()
            messagebox.showinfo('成功', '新建科室成功!')
        except Exception as _:
            messagebox.showerror('失败', '新建科室失败，科室已存在')
        session.close()
        self.refresh_table()
