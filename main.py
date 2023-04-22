from tkcalendar import DateEntry

from Entity.Models import Base, engine, Personal, Pc, Departments, Сontracts, Login_dates
from datetime import datetime, date
from sqlalchemy.orm import create_session, Session, joinedload
from sqlalchemy.orm import contains_eager, joinedload
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("1000x550")


def get_data():
    global results
    with Session(engine) as session:
        query = session.query(Personal).options(joinedload(Personal.department),
                                                joinedload(Personal.pc),
                                                joinedload(Personal.login_dates),
                                                joinedload(Personal.salary),
                                                joinedload(Personal.contracts))
        results = query.all()
        results = list(set(results))


def search_records():
    name = name_entry.get()
    last_name = last_name_entry.get()
    birth_date = birth_date_entry.get()
    department = department_entry.get()
    login = login_entry.get()
    email = email_entry.get()
    date_from = date_from_entry.get()
    date_to = date_to_entry.get()

    search.destroy()

    for record in my_tree.get_children():
        my_tree.delete(record)

    global count
    count = 0

    temp = []
    for record in results:
        if name.lower().__eq__(record.first_name.lower()) or last_name.lower().__eq__(
                record.last_name.lower()) or record.birth_date.__eq__(
                datetime.strptime(birth_date, '%d/%m/%Y')) or department.__eq__(
                record.department.department) or login.__eq__(record.login) or email.__eq__(
                record.email) or record.contracts.date_from.__eq__(
                datetime.strptime(date_from, '%d/%m/%Y')) or record.contracts.date_to.__eq__(
                datetime.strptime(date_to, '%d/%m/%Y')):
            temp.append(record)

    if temp.__len__() > 0:
        for record in temp:
            my_tree.insert(parent='', index='end',
                           iid=count, text='',
                           values=(record.first_name, record.last_name, record.birth_date, record.department.department,
                                   record.login, record.email, record.contracts.date_from, record.contracts.date_to))
            count += 1
    else:
        for record in results:
            my_tree.insert(parent='', index='end',
                           iid=count, text='',
                           values=(record.first_name, record.last_name, record.birth_date, record.department.department,
                                   record.login, record.email, record.contracts.date_from, record.contracts.date_to))
            count += 1


def lookup_records():
    global name_entry, last_name_entry, birth_date_entry, department_entry, login_entry, email_entry, date_from_entry, date_to_entry, search

    search = Toplevel(root)
    search.geometry("400x600")
    name_label = LabelFrame(search, text="Имя")
    name_label.pack(padx=3, pady=3)
    name_entry = Entry(name_label, font=("Times New Roman", 14))
    name_entry.pack(padx=10, pady=10)

    last_name_label = LabelFrame(search, text="Фамилия")
    last_name_label.pack(padx=3, pady=3)
    last_name_entry = Entry(last_name_label, font=("Times New Roman", 14))
    last_name_entry.pack(padx=10, pady=10)

    birth_date_label = LabelFrame(search, text="Дата рождения")
    birth_date_label.pack(padx=3, pady=3)
    birth_date_entry = DateEntry(birth_date_label, font=("Times New Roman", 14),  date_pattern='dd/mm/y')
    birth_date_entry.pack(padx=10, pady=10)

    department_label = LabelFrame(search, text="Название отдела")
    department_label.pack(padx=3, pady=3)
    department_entry = Entry(department_label, font=("Times New Roman", 14))
    department_entry.pack(padx=10, pady=10)

    login_label = LabelFrame(search, text="Логин")
    login_label.pack(padx=3, pady=3)
    login_entry = Entry(login_label, font=("Times New Roman", 14))
    login_entry.pack(padx=10, pady=10)

    email_label = LabelFrame(search, text="Почта")
    email_label.pack(padx=3, pady=3)
    email_entry = Entry(email_label, font=("Times New Roman", 14))
    email_entry.pack(padx=10, pady=10)

    date_from_label = LabelFrame(search, text="С")
    date_from_label.pack(padx=3, pady=3)
    date_from_entry = DateEntry(date_from_label, font=("Times New Roman", 14), date_pattern='dd/mm/y')
    date_from_entry.pack(padx=10, pady=10)

    date_to_label = LabelFrame(search, text="По")
    date_to_label.pack(padx=3, pady=3)
    date_to_entry = DateEntry(date_to_label, font=("Times New Roman", 14),  date_pattern='dd/mm/y')
    date_to_entry.pack(padx=10, pady=10)

    search_button = Button(search, text="Найти", command=search_records)
    search_button.pack(padx=3, pady=3)


def query_database():
    if 'results' not in locals():
        get_data()

    for record in my_tree.get_children():
        my_tree.delete(record)
    global count
    count = 0
    for record in results:
        my_tree.insert(parent='', index='end',
                       iid=count, text='',
                       values=(record.first_name, record.last_name, record.birth_date, record.department.department,
                               record.login, record.email, record.contracts.date_from, record.contracts.date_to))
        count += 1


if __name__ == '__main__':
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()
    tree_scroll.config(command=my_tree.yview)

    my_menu = Menu(root)
    root.config(menu=my_menu)
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
    search_menu.add_command(label="Search", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=query_database)

    my_tree['columns'] = (
        'first_name', 'last_name', 'birth_date', 'department', 'login', 'email', 'date_from', 'date_to')

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("first_name", anchor=CENTER, width=80)
    my_tree.column("last_name", anchor=CENTER, width=80)
    my_tree.column("birth_date", anchor=CENTER, width=90)
    my_tree.column("department", anchor=CENTER, width=150)
    my_tree.column("login", anchor=CENTER, width=80)
    my_tree.column("email", anchor=CENTER, width=160)
    my_tree.column("date_from", anchor=CENTER, width=80)
    my_tree.column("date_to", anchor=CENTER, width=80)

    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("first_name", text="Имя", anchor=CENTER)
    my_tree.heading("last_name", text="Фамилия", anchor=CENTER)
    my_tree.heading("birth_date", text="Дата рождения", anchor=CENTER)
    my_tree.heading("department", text="Подразделение", anchor=CENTER)
    my_tree.heading("login", text="Логин", anchor=CENTER)
    my_tree.heading("email", text="Почта", anchor=CENTER)
    my_tree.heading("date_from", text="С", anchor=CENTER)
    my_tree.heading("date_to", text="По", anchor=CENTER)

    query_database()

    root.mainloop()
