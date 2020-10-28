from tkinter import *
from typing import *
from tkinter import ttk
from tkinter import messagebox
from global_var import DBSession
from dao.office import Office
from dao.room import Room


class AddRoom:
    def __init__(self, root: Tk):
        self.rooms = []
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

        self.root.title('病房管理')
        self.root.geometry('260x360')

        # 病房号Frame
        room_number_frame = Frame(self.page)
        room_number_frame.pack(side=TOP)
        room_number_label = Label(room_number_frame, text='病房号')
        room_number_label.pack(side=LEFT)
        self.room_number_var = StringVar()
        room_number_entry = Entry(room_number_frame, textvariable=self.room_number_var)
        room_number_entry.pack(side=LEFT)

        # 床位数Frame
        room_bed_number_frame = Frame(self.page)
        room_bed_number_frame.pack(side=TOP)
        room_bed_number_label = Label(room_bed_number_frame, text='床位数')
        room_bed_number_label.pack(side=LEFT)
        self.room_bed_number_var = StringVar()
        room_bed_number_entry = Entry(room_bed_number_frame, textvariable=self.room_bed_number_var)
        room_bed_number_entry.pack(side=LEFT)

        # 所属科室Frame
        office_name_frame = Frame(self.page)
        office_name_frame.pack(side=TOP)
        office_name_label = Label(office_name_frame, text='所属科室')
        office_name_label.pack(side=LEFT)
        self.office_name_var = StringVar()
        self.office_name_com = ttk.Combobox(office_name_frame, textvariable=self.office_name_var)
        self.office_name_com['value'] = [office['name'] for office in self.offices]
        self.office_name_com.pack(side=LEFT)

        # 提交按钮
        commit_button = Button(self.page, text='提交', command=self.insert_room)
        commit_button.pack(side=TOP)
        # 表格
        self.tb = ttk.Treeview(self.page, columns=('0', '1', '2', '3'), show="headings")
        self.tb.column("0", width=50, anchor='center')
        self.tb.column("1", width=50, anchor='center')
        self.tb.column("2", width=80, anchor='center')
        self.tb.column("3", width=80, anchor='center')
        self.tb.heading("0", text="id")
        self.tb.heading("1", text="病房号")
        self.tb.heading("2", text="床位数")
        self.tb.heading("3", text="所属科室")
        self.tb.bind('<ButtonRelease-1>', self.tb_bind)
        self.tb.pack(side=TOP)
        # self.refresh_table()
        # 返回按钮
        return_button = Button(self.page, text='返回', command=self.back)
        return_button.pack(side=TOP)
        self.refresh_table()

    def tb_bind(self, event):
        id_ = None
        for item in self.tb.selection():
            item_text = self.tb.item(item, "values")
            id_ = item_text[0]
        if id_:
            session = DBSession()
            try:
                r: Room = session.query(Room).filter_by(id=id_).first()
                session.delete(r)
                session.commit()
            except:
                messagebox.showerror('错误', '该科室已被病房或医生绑定')
            session.close()
        self.refresh_table()

    def refresh_table(self):
        for item in self.tb.get_children():
            self.tb.delete(item)
        session = DBSession()
        rooms: List[Tuple] = session.query(Room, Office.office_name).join(Office).filter().all()
        self.rooms = [{
            'id': room[0].id,
            'room_number': room[0].room_number,
            'bed_number': room[0].bed_number,
            'office_name': room[1]
        } for room in rooms]
        session.commit()
        session.close()
        print(self.rooms)
        for room in self.rooms:
            self.tb.insert("", 0, values=[
                room['id'],
                room['room_number'],
                room['bed_number'],
                room['office_name'],
            ])

    def back(self):
        from view.menu import ChoiceMenu
        self.page.destroy()
        ChoiceMenu(self.root)

    def insert_room(self):
        session = DBSession()
        oids = [office['id'] for office in self.offices if office['name'] == self.office_name_var.get()]
        try:
            room = Room(
                room_number=self.room_number_var.get(),
                bed_number=int(self.room_bed_number_var.get()),
                oid=oids[0]
            )
            messagebox.showinfo('成功', '新建病房成功!')
            session.add(room)
        except Exception as _:
            messagebox.showinfo('失败', '新建病房失败')
        session.commit()
        session.close()
        self.refresh_table()
