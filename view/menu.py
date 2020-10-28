from tkinter import *
from view.add_room import AddRoom
from view.admin_office_manage import AdminOfficeManage


class ChoiceMenu:
    def __init__(self, root: Tk):
        self.root = root
        self.page = Frame(self.root)
        self.page.pack()

        self.root.title('操作菜单')
        self.root.geometry('260x230')

        pres_button = Button(self.page, text='病人信息', width=60, command=self.redirect2patient)
        pres_button.pack(side=TOP, pady=5)

        doc_button = Button(self.page, text='医生信息', width=60, command=self.direct2doctor)
        doc_button.pack(side=TOP, pady=5)

        room_button = Button(self.page, text='病房信息', width=60, command=self.direct2add_room)
        room_button.pack(side=TOP, pady=5)

        admin_office_button = Button(self.page, text='科室信息', width=60, command=self.direct2admin_office)
        admin_office_button.pack(side=TOP, pady=5)

        back_button = Button(self.page, text='返回', width=60, command=self.direct2admin)
        back_button.pack(side=TOP, pady=5)

    def direct2admin_office(self):
        self.page.destroy()
        AdminOfficeManage(self.root)

    def direct2add_room(self):
        self.page.destroy()
        AddRoom(self.root)

    def direct2admin(self):
        from view.login import Login
        self.page.destroy()
        Login(self.root)

    def direct2doctor(self):
        from view.add_doctor import AddDoctor
        self.page.destroy()
        AddDoctor(self.root)

    def redirect2patient(self):
        from view.add_patient import AddPatient
        self.page.destroy()
        AddPatient(self.root)
