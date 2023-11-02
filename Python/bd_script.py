import sqlite3 as sl

# Создание и/или подключение файла БД
bd = sl.connect("Python//data.db")
cur=bd.cursor()
# Создание новой таблицы и стобцов


def new_tab(name, vetv=False):
    with bd:
        # Создание таблицы
        table = "CREATE TABLE if not exists "+name+" (P_sech);"
        bd.execute(table)
        
        cur.execute('PRAGMA table_info(Norm_mode)')     # Получаем выборку всех имеющихся столбцов
        cols = cur.fetchall()                           # Забираем все столбцы в переменную
        # Добавление столбцов по току контролируемых ветвей, если только их ещё нет
        print(vetv)
        if vetv!=False:
            for vl in vetv:
                flag=False
                for c in cols:
                    if vl==c[1]:
                        flag=True
                if flag==False:
                    col = 'AlTER TABLE '+name+' ADD COLUMN '+vl
                    bd.execute(col)

# Функции вноса данных
# Значения P
def data_P(name,mass_P):
    with bd:
        # Предварительная очистка таблицы
        bd.execute("DELETE FROM "+name)
        # Вносим данные в БД
        new_data_P="INSERT INTO "+name+" (P_sech) values(?)"
        bd.executemany(new_data_P,mass_P)
        
# Значения I
def data_I(name,vetv,mass_I):
        for vl in vetv:
            new_data_I="INSERT INTO "+name+" ("+vl+") values(?)"
        bd.executemany(new_data_I,mass_I)
