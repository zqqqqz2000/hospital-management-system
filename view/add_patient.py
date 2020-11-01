from tkinter import *
from typing import *
from tkinter import ttk
from tkinter import messagebox
from global_var import DBSession
from dao.office import Office
from dao.doctor import Doctor
from dao.room import Room
from dao.patient import Patient


class AddPatient:
    def __init__(self, root: Tk):
        self.patients = []
        # 数据库查询所有科室
        session = DBSession()
        offices: List[Office] = session.query(Office).filter().all()
        doctors: List[Doctor] = session.query(Doctor).filter().all()
        rooms: List[Room] = session.query(Room).filter().all()
        self.offices = [
            {
                'id': office.id,
                'name': office.office_name
            }
            for office in offices]
        # 查询所有医生
        self.doctors = [
            {
                'id': doctor.id,
                'name': doctor.name
            }
            for doctor in doctors]
        # 查询所有病房
        self.rooms = [
            {
                'id': room.id,
                'room_number': room.room_number
            }
            for room in rooms]
        session.close()
        self.root = root
        self.page = Frame(self.root)
        self.page.pack()

        self.root.title('病人管理')
        self.root.geometry('500x480')

        # 姓名Frame
        name_frame = Frame(self.page)
        name_frame.pack(side=TOP)
        name_label = Label(name_frame, text='姓名')
        name_label.pack(side=LEFT)
        self.name_var = StringVar()
        name_entry = Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side=LEFT)

        # 病历号Frame
        history_number_frame = Frame(self.page)
        history_number_frame.pack(side=TOP)
        history_number_label = Label(history_number_frame, text='病历号')
        history_number_label.pack(side=LEFT)
        self.history_number_var = StringVar()
        history_number_entry = Entry(history_number_frame, textvariable=self.history_number_var)
        history_number_entry.pack(side=LEFT)

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

        # 主治医生Frame
        doctor_frame = Frame(self.page)
        doctor_frame.pack(side=TOP)
        doctor_label = Label(doctor_frame, text='主治医生')
        doctor_label.pack(side=LEFT)
        self.doctor_var = StringVar()
        self.doctor_com = ttk.Combobox(doctor_frame, textvariable=self.doctor_var)
        self.doctor_com['value'] = [doctor['name'] for doctor in self.doctors]
        self.doctor_com.pack(side=LEFT)

        # 所属科室Frame
        office_name_frame = Frame(self.page)
        office_name_frame.pack(side=TOP)
        office_name_label = Label(office_name_frame, text='科室')
        office_name_label.pack(side=LEFT)
        self.office_name_var = StringVar()
        self.office_name_com = ttk.Combobox(office_name_frame, textvariable=self.office_name_var)
        self.office_name_com['value'] = [office['name'] for office in self.offices]
        self.office_name_com.pack(side=LEFT)

        # 病房号Frame
        room_frame = Frame(self.page)
        room_frame.pack(side=TOP)
        room_label = Label(room_frame, text='病房号')
        room_label.pack(side=LEFT)
        self.room_var = StringVar()
        self.room_com = ttk.Combobox(room_frame, textvariable=self.room_var)
        self.room_com['value'] = [room['room_number'] for room in self.rooms]
        self.room_com.pack(side=LEFT)

        # 诊断Frame
        dig_frame = Frame(self.page)
        dig_frame.pack(side=TOP)
        dig_label = Label(dig_frame, text='诊断')
        dig_label.pack(side=LEFT)
        self.dig_var = StringVar()
        dig_entry = Entry(dig_frame, textvariable=self.dig_var)
        dig_entry.pack(side=LEFT)

        # 提交按钮
        btn_frame = Frame(self.page)
        commit_button = Button(btn_frame, text='提交', command=self.insert_patient)
        commit_button.pack(side=LEFT)
        commit_button = Button(btn_frame, text='修改', command=self.change)
        commit_button.pack(side=LEFT)
        btn_frame.pack(side=TOP)

        # 表格
        self.tb = ttk.Treeview(self.page, columns=('0', '1', '2', '3', '4', '5', '6', '7', '8'), show="headings")
        self.tb.column("0", width=50, anchor='center')
        self.tb.column("1", width=50, anchor='center')
        self.tb.column("2", width=80, anchor='center')
        self.tb.column("3", width=80, anchor='center')
        self.tb.column("4", width=80, anchor='center')
        self.tb.column("5", width=80, anchor='center')
        self.tb.column("6", width=80, anchor='center')
        self.tb.column("7", width=80, anchor='center')
        self.tb.column("8", width=80, anchor='center')
        self.tb.heading("0", text="id")
        self.tb.heading("1", text="医生")
        self.tb.heading("2", text="房号")
        self.tb.heading("3", text="科室")
        self.tb.heading("4", text="病例号")
        self.tb.heading("5", text="姓名")
        self.tb.heading("6", text="性别")
        self.tb.heading("7", text="年龄")
        self.tb.heading("8", text="诊断结果")
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
                p: Patient = session.query(Patient).filter_by(id=id_).first()
                session.delete(p)
                session.commit()
            except:
                messagebox.showerror('错误', '该病人已被其他关系绑定')
            session.close()
        self.refresh_table()

    def refresh_table(self):
        for item in self.tb.get_children():
            self.tb.delete(item)
        session = DBSession()
        patients: List[Tuple[Patient, str, str, str]] = session.query(
            Patient,
            Doctor.name,
            Room.room_number,
            Office.office_name
        ).filter(
            Patient.did == Doctor.id,
            Patient.rid == Room.id,
            Patient.oid == Office.id
        ).all()
        self.patients = [{
            'id': patient[0].id,
            'doctor': patient[1],
            'room_number': patient[2],
            'office_name': patient[3],
            'history_number': patient[0].history_number,
            'name': patient[0].name,
            'gender': '男' if patient[0].gender else '女',
            'age': patient[0].age,
            'diagnose': patient[0].diagnose
        } for patient in patients]
        session.close()
        for patient in self.patients:
            self.tb.insert("", 0, values=[
                patient['id'],
                patient['doctor'],
                patient['room_number'],
                patient['office_name'],
                patient['history_number'],
                patient['name'],
                patient['gender'],
                patient['age'],
                patient['diagnose'],
            ])

    def back(self):
        from view.menu import ChoiceMenu
        self.page.destroy()
        ChoiceMenu(self.root)

    def insert_patient(self):
        session = DBSession()
        oids = [office['id'] for office in self.offices if office['name'] == self.office_name_var.get()]
        dids = [doctor['id'] for doctor in self.doctors if doctor['name'] == self.doctor_var.get()]
        rids = [room['id'] for room in self.rooms if room['room_number'] == self.room_var.get()]
        gender = self.gender_var.get()
        try:
            patient = Patient(
                did=dids[0],
                rid=rids[0],
                oid=oids[0],
                history_number=self.history_number_var.get(),
                name=self.name_var.get(),
                gender=gender,
                age=self.age_var.get(),
                diagnose=self.dig_var.get()
            )
            messagebox.showinfo('成功', '新建患者成功!')
            session.add(patient)
        except Exception as _:
            messagebox.showinfo('失败', '新建患者失败')
        session.commit()
        session.close()
        self.refresh_table()

    def change(self):
        session = DBSession()
        oids = [office['id'] for office in self.offices if office['name'] == self.office_name_var.get()]
        dids = [doctor['id'] for doctor in self.doctors if doctor['name'] == self.doctor_var.get()]
        rids = [room['id'] for room in self.rooms if room['room_number'] == self.room_var.get()]
        gender = self.gender_var.get()
        patient: Patient = session.query(Patient).filter_by(
            history_number=self.history_number_var.get()
        ).first()
        try:
            if patient:
                patient.did = dids[0]
                patient.rid = rids[0]
                patient.oid = oids[0]
                patient.name = self.name_var.get()
                patient.gender = gender
                patient.age = self.age_var.get()
                patient.diagnose = self.dig_var.get()
                messagebox.showinfo('成功', '修改病人信息成功')
            else:
                messagebox.showerror('错误', '找不到病人')
        except Exception as _:
            messagebox.showinfo('失败', '修改病人信息失败')
        session.commit()
        session.close()
        self.refresh_table()
