from fdb import connect as fdb_conn  # функция подлкючения к БД
from tkinter import messagebox
from messages import error_mes


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
