from tkinter import *
from typing import *
from tkinter import ttk
from tkinter import messagebox
from global_var import DBSession
from dao.office import Office
from dao.doctor import Doctor
from dao.room import Room


class AddDoctor:
    def __init__(self, root: Tk):
        self.doctors = []
        # 数据库查询所有科室
        session = DBSession()
        offices: List[Office] = session.query(Office).filter().all()
        self.offices = [
            {
                'id': office.id,
                'name': office.office_name
            }
            for office in offices]
        self.root = root
        self.page = Frame(self.root)
        self.page.pack()

        self.root.title('医生管理')
        self.root.geometry('500x430')

        # 工号Frame
        work_number_frame = Frame(self.page)
        work_number_frame.pack(side=TOP)
        work_number_label = Label(work_number_frame, text='工号')
        work_number_label.pack(side=LEFT)
        self.work_number_var = StringVar()
        work_number_entry = Entry(work_number_frame, textvariable=self.work_number_var)
        work_number_entry.pack(side=LEFT)

        # 姓名Frame
        name_frame = Frame(self.page)
        name_frame.pack(side=TOP)
        name_label = Label(name_frame, text='姓名')
        name_label.pack(side=LEFT)
        self.name_var = StringVar()
        name_entry = Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side=LEFT)

        # 性别Frame
        gender_frame = Frame(self.page)
        gender_frame.pack(side=TOP)
        gender_label = Label(gender_frame, text='性别')
        gender_label.pack(side=LEFT)
        self.gender_var = IntVar()
        r1 = Radiobutton(gender_frame, variable=self.gender_var, value=0, text="女")
        r2 = Radiobutton(gender_frame, variable=self.gender_var, value=1, text="男")
        r1.pack(side=LEFT)
        r2.pack(side=LEFT)

        # 年龄Frame
        age_frame = Frame(self.page)
        age_frame.pack(side=TOP)
        age_label = Label(age_frame, text='年龄')
        age_label.pack(side=LEFT)
        self.age_var = StringVar()
        age_entry = Entry(age_frame, textvariable=self.age_var)
        age_entry.pack(side=LEFT)

        # 职称Frame
        title_frame = Frame(self.page)
        title_frame.pack(side=TOP)
        title_label = Label(title_frame, text='职称')
        title_label.pack(side=LEFT)
        self.title_var = StringVar()
        self.title_com = ttk.Combobox(title_frame, textvariable=self.title_var)
        self.title_com['value'] = ['主任', '副主任', '主治医师', '副院长', '院长']
        self.title_com.pack(side=LEFT)

        # 所属科室Frame
        office_name_frame = Frame(self.page)
        office_name_frame.pack(side=TOP)
        office_name_label = Label(office_name_frame, text='科室')
        office_name_label.pack(side=LEFT)
        self.office_name_var = StringVar()
        self.office_name_com = ttk.Combobox(office_name_frame, textvariable=self.office_name_var)
        self.office_name_com['value'] = [office['name'] for office in self.offices]
        self.office_name_com.pack(side=LEFT)

        # 提交按钮
        btn_frame = Frame(self.page)
        commit_button = Button(btn_frame, text='提交', command=self.insert_doctor)
        commit_button.pack(side=LEFT)
        commit_button = Button(btn_frame, text='修改', command=self.change)
        commit_button.pack(side=LEFT)
        btn_frame.pack(side=TOP)

        # 表格
        self.tb = ttk.Treeview(self.page, columns=('0', '1', '2', '3', '4', '5', '6'), show="headings")
        self.tb.column("0", width=50, anchor='center')
        self.tb.column("1", width=50, anchor='center')
        self.tb.column("2", width=80, anchor='center')
        self.tb.column("3", width=80, anchor='center')
        self.tb.column("4", width=80, anchor='center')
        self.tb.column("5", width=80, anchor='center')
        self.tb.column("6", width=80, anchor='center')
        self.tb.heading("0", text="id")
        self.tb.heading("1", text="工号")
        self.tb.heading("2", text="姓名")
        self.tb.heading("3", text="性别")
        self.tb.heading("4", text="年龄")
        self.tb.heading("5", text="职称")
        self.tb.heading("6", text="科室")
        self.tb.bind('<ButtonRelease-1>', self.tb_bind)
        self.tb.pack(side=TOP)
        self.refresh_table()

        # 返回
        return_button = Button(self.page, text='返回', command=self.back)
        return_button.pack(side=TOP)

    def tb_bind(self, event):
        id_ = None
        for item in self.tb.selection():
            item_text = self.tb.item(item, "values")
            id_ = item_text[0]
        if id_:
            session = DBSession()
            try:
                d: Doctor = session.query(Doctor).filter_by(id=id_).first()
                session.delete(d)
                session.commit()
            except:
                messagebox.showerror('错误', '该医生已被病人绑定')
            session.close()
        self.refresh_table()

    def refresh_table(self):
        for item in self.tb.get_children():
            self.tb.delete(item)
        session = DBSession()
        doctors: List[Tuple] = session.query(Doctor, Office.office_name).join(Office).filter().all()
        self.doctors = [{
            'id': doctor[0].id,
            'work_number': doctor[0].work_number,
            'name': doctor[0].name,
            'gender': '男' if doctor[0].gender else '女',
            'age': doctor[0].age,
            'title': doctor[0].title,
            'office_name': doctor[1]
        } for doctor in doctors]
        session.close()
        for doctor in self.doctors:
            self.tb.insert("", 0, values=[
                doctor['id'],
                doctor['work_number'],
                doctor['name'],
                doctor['gender'],
                doctor['age'],
                doctor['title'],
                doctor['office_name'],
            ])

    def back(self):
        from view.menu import ChoiceMenu
        self.page.destroy()
        ChoiceMenu(self.root)

    def change(self):
        session = DBSession()
        oids = [office['id'] for office in self.offices if office['name'] == self.office_name_var.get()]
        gender = self.gender_var.get()
        doctor: Doctor = session.query(Doctor).filter_by(
            work_number=self.work_number_var.get()
        ).first()
        try:
            if doctor:
                doctor.name = self.name_var.get()
                doctor.gender = gender
                doctor.age = self.age_var.get()
                doctor.title = self.title_var.get()
                doctor.oid = oids[0]
                session.commit()
                messagebox.showinfo('成功', '修改医生信息成功!')
            else:
                messagebox.showerror('错误', '找不到医生')
        except Exception as _:
            messagebox.showinfo('失败', '新建医生失败')
        session.close()
        self.refresh_table()

    def insert_doctor(self):
        session = DBSession()
        oids = [office['id'] for office in self.offices if office['name'] == self.office_name_var.get()]
        gender = self.gender_var.get()
        try:
            room = Doctor(
                work_number=self.work_number_var.get(),
                name=self.name_var.get(),
                gender=gender,
                age=self.age_var.get(),
                title=self.title_var.get(),
                oid=oids[0]
            )
            session.add(room)
            session.commit()
            messagebox.showinfo('成功', '新建医生成功!')
        except Exception as _:
            messagebox.showerror('失败', '新建医生失败，医生可能已存在')
        session.close()
        self.refresh_table()
