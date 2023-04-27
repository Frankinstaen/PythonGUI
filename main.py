from tkcalendar import DateEntry
from tkinter import ttk

from Entity.Models import engine, Personal, Pc, Departments, Сontracts, Login_dates
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from tkinter import *

root = Tk()
root.geometry("300x150")


def init_third():
    def get_data():
        global results
        with Session(engine) as session:
            query = session.query(Personal).options(joinedload(Personal.department),
                                                    joinedload(Personal.salary))
            results = query.all()
            results = list(set(results))

    def validate_values():
        search_records()

    def lookup_records():
        global name_entry, last_name_entry, department_entry, month_from_entry, month_to_entry, year_entry, search

        search = Toplevel(third_window)
        search.geometry("400x450")
        style = ttk.Style(search)
        style.theme_use('alt')
        style.configure('TEntry,TButton', background="#D3D3D3",
                        foreground="black",
                        fieldbackground="#D3D3D3")
        name_label = LabelFrame(search, text="Имя")
        name_label.pack(padx=3, pady=3)
        name_entry = ttk.Entry(name_label, font=("Times New Roman", 14))
        name_entry.pack(padx=10, pady=10)

        last_name_label = LabelFrame(search, text="Фамилия")
        last_name_label.pack(padx=3, pady=3)
        last_name_entry = ttk.Entry(last_name_label, font=("Times New Roman", 14))
        last_name_entry.pack(padx=10, pady=10)

        department_label = LabelFrame(search, text="Название отдела")
        department_label.pack(padx=3, pady=3)
        department_entry = ttk.Entry(department_label, font=("Times New Roman", 14))
        department_entry.pack(padx=10, pady=10)

        month_label = LabelFrame(search, text="Месяц с/по")
        month_label.pack(padx=3, pady=3)
        month_from_entry = ttk.Entry(month_label, font=("Times New Roman", 14))
        month_to_entry = ttk.Entry(month_label, font=("Times New Roman", 14))
        month_from_entry.pack(padx=10, pady=10)
        month_to_entry.pack(padx=10, pady=10)

        year_label = LabelFrame(search, text="Год")
        year_label.pack(padx=3, pady=3)
        year_entry = ttk.Entry(year_label, font=("Times New Roman", 14))
        year_entry.pack(padx=10, pady=10)

        search_button = ttk.Button(search, text="Найти", command=validate_values)
        search_button.pack(padx=3, pady=3)

        global answer
        answer = Label(search, text='')
        answer.pack(pady=20)

    def query_database():
        if 'results' not in locals():
            get_data()

        for record in my_tree.get_children():
            my_tree.delete(record)
        global count
        count = 0
        average_salary = 0
        for record in results:
            for item in record.salary:
                average_salary += item.salary
            average_salary = round(average_salary/record.salary.__len__(), 2)
            my_tree.insert(parent='', index='end',
                           iid=count, text='',
                           values=(record.first_name, record.last_name, record.department.department, average_salary))
            for item in record.salary:
                my_tree.insert(count, index=END, values=(item.month, item.year, item.salary))
            average_salary = 0
            count += 1

    root.withdraw()
    third_window = Tk()
    third_window.geometry("650x450")
    style = ttk.Style(third_window)
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    tree_frame = Frame(third_window)
    tree_frame.pack(pady=10)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=450)
    my_tree.pack(expand=1, fill=BOTH)
    tree_scroll.config(command=my_tree.yview)

    my_menu = Menu(third_window)
    third_window.config(menu=my_menu)
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Опции", menu=search_menu)
    search_menu.add_command(label="Найти", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Сбросить", command=query_database)

    my_tree['columns'] = (
        'first_name', 'last_name', 'department', 'average_salary')

    my_tree.column("#0", width=150, stretch=NO)
    my_tree.column("first_name", anchor=CENTER, width=80)
    my_tree.column("last_name", anchor=CENTER, width=80)
    my_tree.column("department", anchor=CENTER, width=150)
    my_tree.column("average_salary", anchor=CENTER, width=100)

    my_tree.heading("#0", text="Зарплата по месяцам", anchor=CENTER)
    my_tree.heading("first_name", text="Имя", anchor=CENTER)
    my_tree.heading("last_name", text="Фамилия", anchor=CENTER)
    my_tree.heading("department", text="Отдел", anchor=CENTER)
    my_tree.heading("average_salary", text="Средняя зарплата", anchor=CENTER)
    query_database()
    third_window.protocol("WM_DELETE_WINDOW", lambda: (root.deiconify(), third_window.destroy()))

    def search_records():
        name = name_entry.get()
        last_name = last_name_entry.get()
        department = department_entry.get()
        month_from = month_from_entry.get()
        month_to = month_to_entry.get()
        year = year_entry.get()

        search.destroy()

        for record in my_tree.get_children():
            my_tree.delete(record)

        global count
        count = 0

        temp = []
        for record in results:
            if name != '' and last_name != '' and department != ''and month_from != '' and month_to != '' and year != '' and month_from.isnumeric() and month_to.isnumeric() and year.isnumeric():
                if name.lower().__eq__(record.first_name.lower()):
                    if last_name.lower().__eq__(record.last_name.lower()):
                        if department.__eq__(record.department.department):
                            if int(month_to).__eq__(record.salary.__len__()) and int(month_from) < record.salary.__len__():
                                if int(year).__eq__(record.salary[0].year):
                                    temp.append(record)
                                    break
        if temp.__len__() == 0:
            if month_from != '' and month_to != '' and month_from.isnumeric() and month_to.isnumeric():
                print("Ищет по месяцам")
                temp = results
            else:
                if year != '' and year.isnumeric():
                    print("Ищет по ф, и, отдел, год")
                    for record in results:
                        if name.lower().__eq__(record.first_name.lower()) or last_name.lower().__eq__(
                                record.last_name.lower()) or department.__eq__(record.login) or int(year).__eq__(record.salary[0].year):
                            temp.append(record)
                else:
                    print("Ищет по ф, и, отдел")
                    for record in results:
                        if name.lower().__eq__(record.first_name.lower()) or last_name.lower().__eq__(
                                record.last_name.lower()) or department.__eq__(record.department.department):
                            temp.append(record)

        if temp.__len__() > 0:
            if name != '' and last_name != '' and department != '' and month_from != '' and month_to != '' and year != '' and month_from.isnumeric() and month_to.isnumeric() and year.isnumeric():
                print("Полная отрисовка")
                count = 0
                average_salary = 0
                for record in temp:
                    for item in record.salary:
                        average_salary += item.salary
                    average_salary = round(average_salary / record.salary.__len__(), 2)
                    my_tree.insert(parent='', index='end',
                                   iid=count, text='',
                                   values=(
                                       record.first_name, record.last_name, record.department.department,
                                       average_salary))
                    for item in record.salary:
                        my_tree.insert(count, index=END, values=(item.month, item.year, item.salary))
                    average_salary = 0
                    count += 1
            else:
                if month_from != '' and month_to != '' and month_from.isnumeric() and month_to.isnumeric():
                    print("Вошел в отрисовку по месяцам")
                    count = 0
                    average_salary = 0
                    for record in results:
                        for item in record.salary:
                            if int(month_from) <= item.month <= int(month_to):
                                average_salary += item.salary
                        average_salary = round(average_salary / (int(month_to) - int(month_from) + 1), 2)
                        my_tree.insert(parent='', index='end',
                                       iid=count, text='',
                                       values=(record.first_name, record.last_name, record.department.department, average_salary))
                        for item in record.salary:
                            if int(month_from) <= item.month <= int(month_to):
                                my_tree.insert(count, index=END, values=(item.month, item.year, item.salary))
                        average_salary = 0
                        count += 1
                else:
                    print("Вошел в отрисовку по ф, и, подразделению, году")
                    count = 0
                    average_salary = 0
                    for record in temp:
                        for item in record.salary:
                            average_salary += item.salary
                        average_salary = round(average_salary / record.salary.__len__(), 2)
                        my_tree.insert(parent='', index='end',
                                       iid=count, text='',
                                       values=(
                                           record.first_name, record.last_name, record.department.department, average_salary))
                        for item in record.salary:
                            my_tree.insert(count, index=END, values=(item.month, item.year, item.salary))
                        average_salary = 0
                        count += 1
        else:
            print("Ничего не нашел, полная отрисовка")
            count = 0
            average_salary = 0
            for record in results:
                for item in record.salary:
                    average_salary += item.salary
                average_salary = round(average_salary / record.salary.__len__(), 2)
                my_tree.insert(parent='', index='end',
                               iid=count, text='',
                               values=(
                               record.first_name, record.last_name, record.department.department, average_salary))
                for item in record.salary:
                    my_tree.insert(count, index=END, values=(item.month, item.year, item.salary))
                average_salary = 0
                count += 1

def init_second():
    def get_data():
        global results
        with Session(engine) as session:
            query = session.query(Personal).options(joinedload(Personal.pc),
                                                    joinedload(Personal.login_dates))
            results = query.all()
            results = list(set(results))

    def lookup_records():
        global name_entry, last_name_entry, login_entry, search

        search = Toplevel(second_window)
        search.geometry("400x250")
        style = ttk.Style(search)
        style.theme_use('alt')
        style.configure('TEntry,TButton', background="#D3D3D3",
                        foreground="black",
                        fieldbackground="#D3D3D3")
        name_label = LabelFrame(search, text="Имя")
        name_label.pack(padx=3, pady=3)
        name_entry = ttk.Entry(name_label, font=("Times New Roman", 14))
        name_entry.pack(padx=10, pady=10)

        last_name_label = LabelFrame(search, text="Фамилия")
        last_name_label.pack(padx=3, pady=3)
        last_name_entry = ttk.Entry(last_name_label, font=("Times New Roman", 14))
        last_name_entry.pack(padx=10, pady=10)

        login_label = LabelFrame(search, text="Логин")
        login_label.pack(padx=3, pady=3)
        login_entry = ttk.Entry(login_label, font=("Times New Roman", 14))
        login_entry.pack(padx=10, pady=10)

        search_button = ttk.Button(search, text="Найти", command=search_records)
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
                           values=(record.first_name, record.last_name, record.login, record.pc.pc_id,
                                   record.pc.pc_serial, record.pc.pc_mac, record.pc.pc_ip))
            for item in record.login_dates:
                my_tree.insert(count, index=END, values=(item.date_time))
            count += 1

    root.withdraw()
    second_window = Tk()
    second_window.geometry("1200x450")
    style = ttk.Style(second_window)
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    tree_frame = Frame(second_window)
    tree_frame.pack(pady=10)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=450)
    my_tree.pack(expand=1, fill=BOTH)
    tree_scroll.config(command=my_tree.yview)

    my_menu = Menu(second_window)
    second_window.config(menu=my_menu)
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Опции", menu=search_menu)
    search_menu.add_command(label="Найти", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Сбросить", command=query_database)

    my_tree['columns'] = (
        'first_name', 'last_name', 'login', 'pc_id', 'pc_serial', 'pc_mac', 'pc_ip', 'date_time')

    my_tree.column("#0", width=80, stretch=NO)
    my_tree.column("first_name", anchor=CENTER, width=80)
    my_tree.column("last_name", anchor=CENTER, width=80)
    my_tree.column("login", anchor=CENTER, width=150)
    my_tree.column("pc_id", anchor=CENTER, width=200)
    my_tree.column("pc_serial", anchor=CENTER, width=200)
    my_tree.column("pc_mac", anchor=CENTER, width=200)
    my_tree.column("pc_ip", anchor=CENTER, width=200)

    my_tree.heading("#0", text="Даты входов", anchor=CENTER)
    my_tree.heading("first_name", text="Имя", anchor=CENTER)
    my_tree.heading("last_name", text="Фамилия", anchor=CENTER)
    my_tree.heading("login", text="Логин", anchor=CENTER)
    my_tree.heading("pc_id", text="ID ПК", anchor=CENTER)
    my_tree.heading("pc_serial", text="Серийный номер", anchor=CENTER)
    my_tree.heading("pc_mac", text="Мак-адрес", anchor=CENTER)
    my_tree.heading("pc_ip", text="Айпи-адрес", anchor=CENTER)
    query_database()
    second_window.protocol("WM_DELETE_WINDOW", lambda: (root.deiconify(), second_window.destroy()))

    def search_records():
        name = name_entry.get()
        last_name = last_name_entry.get()
        login = login_entry.get()

        search.destroy()

        for record in my_tree.get_children():
            my_tree.delete(record)

        global count
        count = 0

        temp = []
        for record in results:
            if name != '' and last_name != '' and login != '':
                if name.lower().__eq__(record.first_name.lower()):
                    print(name)
                    if last_name.lower().__eq__(record.last_name.lower()):
                        print(last_name)
                        if login.__eq__(record.login):
                            temp.append(record)
                            break

        if temp.__len__() == 0:
            for record in results:
                if name.lower().__eq__(record.first_name.lower()) or last_name.lower().__eq__(
                        record.last_name.lower()) or login.__eq__(record.login):
                    temp.append(record)

        if temp.__len__() > 0:
            print("параметры поиска нашлись, поиск по ним")
            for record in temp:
                my_tree.insert(parent='', index='end',
                               iid=count, text='',
                               values=(record.first_name, record.last_name, record.login, record.pc.pc_id,
                                       record.pc.pc_serial, record.pc.pc_mac, record.pc.pc_ip))
                for item in record.login_dates:
                    my_tree.insert(count, index=END, values=(item.date_time))
                count += 1
        else:
            print("параметры поиска не нашлись, полная отрисовка")
            for record in results:
                my_tree.insert(parent='', index='end',
                               iid=count, text='',
                               values=(record.first_name, record.last_name, record.login, record.pc.pc_id,
                                       record.pc.pc_serial, record.pc.pc_mac, record.pc.pc_ip))
                for item in record.login_dates:
                    my_tree.insert(count, index=END, values=(item.date_time))
                count += 1


def init_first():
    def get_data():
        global results
        with Session(engine) as session:
            query = session.query(Personal).options(joinedload(Personal.department),
                                                    joinedload(Personal.contracts))
            results = query.all()
            results = list(set(results))

    def lookup_records():
        global name_entry, last_name_entry, birth_date_entry, department_entry, login_entry, email_entry, date_from_entry, date_to_entry, search

        search = Toplevel(first_window)
        search.geometry("400x610")
        style = ttk.Style(search)
        style.theme_use('alt')
        style.configure('TEntry,TButton', background="#D3D3D3",
                        foreground="black",
                        fieldbackground="#D3D3D3")
        name_label = LabelFrame(search, text="Имя")
        name_label.pack(padx=3, pady=3)
        name_entry = ttk.Entry(name_label, font=("Times New Roman", 14))
        name_entry.pack(padx=10, pady=10)

        last_name_label = LabelFrame(search, text="Фамилия")
        last_name_label.pack(padx=3, pady=3)
        last_name_entry = ttk.Entry(last_name_label, font=("Times New Roman", 14))
        last_name_entry.pack(padx=10, pady=10)

        birth_date_label = LabelFrame(search, text="Дата рождения")
        birth_date_label.pack(padx=3, pady=3)
        birth_date_entry = DateEntry(birth_date_label, font=("Times New Roman", 14), date_pattern='dd/mm/y')
        birth_date_entry.pack(padx=10, pady=10)

        department_label = LabelFrame(search, text="Название отдела")
        department_label.pack(padx=3, pady=3)
        department_entry = ttk.Entry(department_label, font=("Times New Roman", 14))
        department_entry.pack(padx=10, pady=10)

        login_label = LabelFrame(search, text="Логин")
        login_label.pack(padx=3, pady=3)
        login_entry = ttk.Entry(login_label, font=("Times New Roman", 14))
        login_entry.pack(padx=10, pady=10)

        email_label = LabelFrame(search, text="Почта")
        email_label.pack(padx=3, pady=3)
        email_entry = ttk.Entry(email_label, font=("Times New Roman", 14))
        email_entry.pack(padx=10, pady=10)

        date_from_label = LabelFrame(search, text="С")
        date_from_label.pack(padx=3, pady=3)
        date_from_entry = DateEntry(date_from_label, font=("Times New Roman", 14), date_pattern='dd/mm/y')
        date_from_entry.pack(padx=10, pady=10)

        date_to_label = LabelFrame(search, text="По")
        date_to_label.pack(padx=3, pady=3)
        date_to_entry = DateEntry(date_to_label, font=("Times New Roman", 14), date_pattern='dd/mm/y')
        date_to_entry.pack(padx=10, pady=10)

        search_button = ttk.Button(search, text="Найти", command=search_records)
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

    root.withdraw()
    first_window = Tk()
    first_window.geometry("870x450")
    style = ttk.Style(first_window)
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    tree_frame = Frame(first_window)
    tree_frame.pack(pady=10)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=450)
    my_tree.pack()
    tree_scroll.config(command=my_tree.yview)

    my_menu = Menu(first_window)
    first_window.config(menu=my_menu)
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Опции", menu=search_menu)
    search_menu.add_command(label="Найти", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Сбросить", command=query_database)

    my_tree['columns'] = (
        'first_name', 'last_name', 'birth_date', 'department', 'login', 'email', 'date_from', 'date_to')

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("first_name", anchor=CENTER, width=80)
    my_tree.column("last_name", anchor=CENTER, width=80)
    my_tree.column("birth_date", anchor=CENTER, width=90)
    my_tree.column("department", anchor=CENTER, width=150)
    my_tree.column("login", anchor=CENTER, width=80)
    my_tree.column("email", anchor=CENTER, width=200)
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
    first_window.protocol("WM_DELETE_WINDOW", lambda: (root.deiconify(), first_window.destroy()))

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
            if name != '' and last_name != '' and department != '' and login != '' and email != '':
                if name.lower().__eq__(record.first_name.lower()):
                    print(name)
                    if last_name.lower().__eq__(record.last_name.lower()):
                        print(last_name)
                        if record.birth_date.__eq__(datetime.strptime(birth_date, '%d/%m/%Y')):
                            print(birth_date)
                            if department.__eq__(record.department.department):
                                print(department)
                                if login.__eq__(record.login):
                                    print(login)
                                    if email.__eq__(record.email):
                                        print(email)
                                        if record.contracts.date_from.__eq__(datetime.strptime(date_from, '%d/%m/%Y')):
                                            print(date_from)
                                            if record.contracts.date_to.__eq__(datetime.strptime(date_to, '%d/%m/%Y')):
                                                print(date_to)
                                                temp.append(record)
                                                break

        if temp.__len__() == 0:
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
            print("Отрисовка по найденным параметрам")
            for record in temp:
                my_tree.insert(parent='', index='end',
                               iid=count, text='',
                               values=(
                                   record.first_name, record.last_name, record.birth_date, record.department.department,
                                   record.login, record.email, record.contracts.date_from, record.contracts.date_to))
                count += 1
        else:
            print("Полная отрисовка")
            for record in results:
                my_tree.insert(parent='', index='end',
                               iid=count, text='',
                               values=(
                                   record.first_name, record.last_name, record.birth_date, record.department.department,
                                   record.login, record.email, record.contracts.date_from, record.contracts.date_to))
                count += 1


if __name__ == '__main__':
    style = ttk.Style(root)
    style.theme_use('alt')
    style.configure('TButton', background="#D3D3D3",
                    foreground="black",
                    fieldbackground="#D3D3D3")

    buttonFirst = ttk.Button(root, text="Первый пункт", command=init_first)
    buttonFirst.pack(padx=10, pady=10)
    buttonSecond = ttk.Button(root, text="Второй пункт", command=init_second)
    buttonSecond.pack(padx=10, pady=10)
    buttonThird = ttk.Button(root, text="Третий пункт", command=init_third)
    buttonThird.pack(padx=10, pady=10)

    root.mainloop()
