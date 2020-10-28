from tkinter import *
from tkinter import messagebox
from typing import *

from dao.doctor import Doctor
from dao.office import Office
from dao.patient import Patient
from dao.room import Room
from global_var import DBSession


class Tor:
    def __init__(self, root):
        self.root = root
        self.root.title('游客查询')
        self.root.geometry('240x120')

        self.page = Frame(self.root)
        self.page.pack()

        patient_label = Label(self.page, text="病人:")
        patient_label.grid(row=1, column=1)
        self.patient_variable = Variable()
        patient_entry = Entry(self.page, textvariable=self.patient_variable)
        patient_entry.placeholder = "输入病历号"
        patient_entry.var = self.patient_variable
        self.patient_variable.set(patient_entry.placeholder)
        patient_entry.bind("<Button-1>", self.placeholder_handler)
        patient_entry.grid(row=1, column=2)
        patient_button = Button(self.page, text="查询", command=self.search_for_patient)
        patient_button.grid(row=1, column=3)

        doctor_label = Label(self.page, text="医生:")
        doctor_label.grid(row=2, column=1)
        self.doctor_variable = Variable()
        doctor_entry = Entry(self.page, textvariable=self.doctor_variable)
        doctor_entry.placeholder = "输入工号"
        doctor_entry.var = self.doctor_variable
        self.doctor_variable.set(doctor_entry.placeholder)
        doctor_entry.bind("<Button-1>", self.placeholder_handler)
        doctor_entry.grid(row=2, column=2)
        doctor_button = Button(self.page, text="查询", command=self.search_for_doctor)
        doctor_button.grid(row=2, column=3)

        room_label = Label(self.page, text="病房:")
        room_label.grid(row=3, column=1)
        self.room_variable = Variable()
        room_entry = Entry(self.page, textvariable=self.room_variable)
        room_entry.placeholder = "输入病房号"
        room_entry.var = self.room_variable
        self.room_variable.set(room_entry.placeholder)
        room_entry.bind("<Button-1>", self.placeholder_handler)
        room_entry.grid(row=3, column=2)
        room_button = Button(self.page, text="查询")
        room_button.grid(row=3, column=3)

        office_label = Label(self.page, text="科室:")
        office_label.grid(row=3, column=1)
        self.office_variable = Variable()
        office_entry = Entry(self.page, textvariable=self.office_variable)
        office_entry.placeholder = "科室名"
        office_entry.var = self.office_variable
        self.office_variable.set(office_entry.placeholder)
        office_entry.bind("<Button-1>", self.placeholder_handler)
        office_entry.grid(row=3, column=2)
        office_button = Button(self.page, text="查询", command=self.search_for_office)
        office_button.grid(row=3, column=3)

        back_btn = Button(self.page, text='返回上页', command=self.back)
        back_btn.grid(row=4, column=2)

    @staticmethod
    def placeholder_handler(event):
        widget = event.widget
        var: Variable = widget.var
        if var.get() == widget.placeholder:
            var.set('')

    def back(self):
        from view.login import Login
        self.page.destroy()
        Login(self.root)

    def search_for_patient(self):
        his_number = self.patient_variable.get()
        session = DBSession()
        patient: Optional[Tuple[Patient, str, str, str]] = session.query(
            Patient,
            Doctor.name,
            Room.room_number,
            Office.office_name
        ).filter(
            Patient.did == Doctor.id,
            Patient.rid == Room.id,
            Patient.oid == Office.id,
            Patient.history_number == his_number
        ).first()
        if patient:
            patient_dir = {
                'id': patient[0].id,
                'doctor': patient[1],
                'room_number': patient[2],
                'office_name': patient[3],
                'history_number': patient[0].history_number,
                'name': patient[0].name,
                'gender': '男' if patient[0].gender else '女',
                'age': patient[0].age,
                'diagnose': patient[0].diagnose}
            messagebox.showinfo('病人', '\n'.join(map(lambda i: f'{i[0]}: {i[1]}', patient_dir.items())))
        else:
            messagebox.showerror('错误', '找不到该病历号的病人!')
        session.close()

    def search_for_doctor(self):
        doctor_work_num = self.doctor_variable.get()
        session = DBSession()
        doctor: Optional[Tuple] = session.query(Doctor, Office.office_name).join(Office).filter(
            Doctor.work_number == doctor_work_num
        ).first()
        if doctor:
            doctor_dict = {
                'id': doctor[0].id,
                'work_number': doctor[0].work_number,
                'name': doctor[0].name,
                'gender': '男' if doctor[0].gender else '女',
                'age': doctor[0].age,
                'title': doctor[0].title,
                'office_name': doctor[1]
            }
            messagebox.showinfo('医生', '\n'.join(map(lambda i: f'{i[0]}: {i[1]}', doctor_dict.items())))
        else:
            messagebox.showerror('错误', '找不到医生!')
        session.close()

    def search_for_office(self):
        office_name = self.office_variable.get()
        session = DBSession()
        office: Optional[Office] = session.query(Office).filter(
            Office.office_name == office_name
        ).first()
        if office:
            office_dict = {
                'id': office.id,
                'office_name': office.office_name,
                'office_address': office.office_address,
                'office_telephone': office.office_telephone
            }
            messagebox.showinfo('医生', '\n'.join(map(lambda i: f'{i[0]}: {i[1]}', office_dict.items())))
        else:
            messagebox.showerror('错误', '找不到科室!')
        session.close()
