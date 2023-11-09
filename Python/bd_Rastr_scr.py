import sqlite3 as sl

# Создание и/или подключение файла БД
bd = sl.connect("DataBase//Rastr_data.db")
cur = bd.cursor()
# Создание новой таблицы и стобцов


def new_tab(name, vetv=False):
    with bd:
        # Создание таблицы
        table = "CREATE TABLE if not exists "+name+" (id,P_sech);"
        bd.execute(table)

        # Получаем выборку всех имеющихся столбцов
        cur.execute(f'PRAGMA table_info({name})')
        # Забираем все столбцы в переменную
        cols = cur.fetchall()
        # Добавление столбцов по току контролируемых ветвей, если только их ещё нет
        if vetv != False:
            for vl in vetv:
                flag = False
                for c in cols:
                    if vl == c[1]:
                        flag = True
                if flag == False:
                    col = 'AlTER TABLE '+name+' ADD COLUMN '+vl
                    bd.execute(col)


# ------------------------------------------------
# Функции вноса данных
# Значения P


def data_P(name, mass_P):
    with bd:
        # Предварительная чистка таблицы
        bd.execute("DELETE FROM "+name)
        # Список индексов
        ind = [(x,) for x in range(1, len(mass_P)+1)]
        # Вносим индексы значений
        new_data_ind = "INSERT INTO "+name+" (id) values(?)"
        bd.executemany(new_data_ind, ind)
        # Обновляем значения P
        for i in ind:
            bd.execute(f"UPDATE {name} SET P_sech=? WHERE id={i[0]}", (mass_P[i[0]-1],))

# ------------------------------------------------
# Значения I
# Данную функцию необходимо выполнять после функции data_P
# Потому, что в data_P создаются строки и задаются к ним индексы,
# А в этой функции происходит обновление (а не добавление) данных по току


def data_I(name, mass_I, vetv):
    with bd:
        # Выборка всех ID
        cur.execute(f"SELECT id FROM {name}")
        ind = cur.fetchall()
        k = 0
        # Обновление данных I в ветвях
        for vl in vetv:
            for i in ind:
                bd.execute(f"UPDATE {name} SET {vl}= ? WHERE id={i[0]}", (mass_I[k][i[0]-1],))
            k += 1
