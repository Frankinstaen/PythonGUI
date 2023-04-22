from Entity.Models import Base, engine, Personal, Pc, Departments, Сontracts, Login_dates
from sqlalchemy import select
from sqlalchemy.orm import create_session, Session, joinedload
from sqlalchemy.orm import contains_eager, joinedload
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("1000x550")


def query_database():
    with Session(engine) as session:
        query = session.query(Personal).options(joinedload(Personal.department),
                                                joinedload(Personal.pc),
                                                joinedload(Personal.login_dates),
                                                joinedload(Personal.salary),
                                                joinedload(Personal.contracts))
        results = query.all()
        results = list(set(results))

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
