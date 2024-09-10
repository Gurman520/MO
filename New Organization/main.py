from tkinter import Tk, messagebox, Toplevel, Menu, N, NO, W, END, NS
from tkinter.ttk import Label, Entry, Button, Treeview, Style, Scrollbar
from fdb import connect as fdb_conn  # функция подлкючения к БД

name_icon = "./icon.ico"

version = "v0.1.4"

about = (
    "Программа для внесения и просмотра списка организаций в которых работают пациенты, проходящие мед. и проф. осмотры.\n"
    "Работает на базе Арена (Разработка КОМИАЦ)\n"
    "\nРазработчик Сулима Р.И. Инженер-программист отдела АСУ ГАУЗ ККБСМП\nEmail: sulima.ri@kkbsmp.ru\n"
    "При ошибках обращаться в отдел АСУ Телефон: 25-04-33\n"
    f"Версия программы: {version}")

error_mes = ("К сожалению запись не была добавлена. Возникла техническая ошибка.\n"
             "Пожалуйста, обратитьс в отдел АСУ по телефону: 25-04-33")

# Функция для установления соединения с базой данных Firebird
def connect_to_database():
    '''
    Конект с БД
    :return: Соединение и курсор
    '''
    conn = fdb_conn(
        dsn='10.2.0.69:d:\\arena\db\\arena.gdb',
        user='sysdba',
        password='masterkey'
    )
    cursor = conn.cursor()
    return conn, cursor


# Функция для выполнения SQL-запроса
def execute_query(cursor, query):
    '''
    Функция производящая сам запрос на получение данных из бд
    :param cursor:
    :param query:
    :return:
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# Функция для вставки новой строки в таблицу
def insert_record(conn, cursor, org_name):
    '''
    Функция внесения новой записи в таблицу
    :param conn:
    :param cursor:
    :param org_name:
    :return:
    '''
    _, number = get_query(conn, cursor)
    cursor.execute("INSERT INTO N_KMR (KMR, NMR) VALUES (?, ?)", (number + 1, org_name))
    conn.commit()


def get_query(conn, cursor):
    '''
    Функция получения всех записей из таблицы
    :param conn: Параметр Коннекта
    :param cursor: Параметр Курсор
    :return: Возвращает все записи в исходном виде и второым параметром возвращает количество записей в таблице
    '''
    result = ''
    try:
        query = 'SELECT * FROM N_KMR'
        result = execute_query(cursor, query)
    except:
        messagebox.showinfo("Ошибка", error_mes)
        conn.close()
    return result, len(result)

# Функция вывода таблицы
def show_table():
    conn, cursor = connect_to_database()
    records, _ = get_query(conn, cursor)
    conn.close()

    top = Toplevel()
    top.title("Таблица записей")
    top.geometry("450x400")
    top.iconbitmap(name_icon)

    table = Treeview(top, height=22)
    table.grid(column=0, row=0, sticky=N, pady=2)
    table["columns"] = ("Порядковый номер", "Название организаций")
    table.column("#0", width=0, stretch=NO)
    table.column("Порядковый номер", anchor=W, width=115)
    table.column("Название организаций", anchor=W, width=300)
    table.heading("#0", text="", anchor=W)
    table.heading("Порядковый номер", text="Порядковый номер", anchor=W)
    table.heading("Название организаций", text="Название организации", anchor=W)

    for record in records:
        table.insert("", END, values=(record[0], record[2]))

    ys = Scrollbar(top, orient="vertical", command=table.yview)
    ys.grid(column=1, row=0, sticky=NS)
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)

    table["yscrollcommand"] = ys.set

    style = Style()
    style.theme_use("default")
    style.map("Treeview")


# Функция обработки нажатия кнопки добавления записи
def add_record():
    org_name = entry_org_name.get()

    if not org_name:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните название организации.")
        return

    confirmation = messagebox.askokcancel("Подтверждение",
                                          f"Вы уверены, что хотите добавить запись организации '{org_name}'?")

    if confirmation:
        conn, cursor = connect_to_database()
        try:
            insert_record(conn, cursor, org_name)
        except:
            messagebox.showinfo("Ошибка", error_mes)
            conn.close()
        else:
            conn.close()
        messagebox.showinfo("Успех", "Новая запись успешно добавлена в таблицу!")


def about_click():
    messagebox.showinfo("О программе", about)


# def exit_click(root):
#     root.destroy()


# Создание графического интерфейса
root = Tk()
root.iconbitmap(name_icon)
root.title("Добавление записи в базу данных")
root.geometry("400x400")
main_menu = Menu()

main_menu.add_cascade(label="Выход", command=root.destroy)
main_menu.add_cascade(label="О программе", command=about_click)

label_org_name = Label(root, text="Введите название организации:", font=("Times New Roman", 16))
label_org_name.pack()
entry_org_name = Entry(root, width=40, font=("Times New Roman", 14))
entry_org_name.pack()

btn_add_record = Button(root, text="Добавить запись", command=add_record)
btn_add_record.pack(ipadx=20, ipady=10, padx=5, pady=5)

btn_show_table = Button(root, text="Показать таблицу", command=show_table)
btn_show_table.pack(ipadx=14, ipady=6, padx=5, pady=3)

root.config(menu=main_menu)

entry_org_name.focus()
st = Style()
st.theme_use('alt')

root.mainloop()
