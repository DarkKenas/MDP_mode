import sqlite3 as sl
import numpy as np

# Создание и/или подключение файла БД
bd = sl.connect("DataBase//MDP_data.db")
cur = bd.cursor()
# Создание новой таблицы и стобцов


def new_tab(name):
    with bd:
        # Создание таблицы
        table = f"""CREATE TABLE if not exists {name}
        (Temp, P_I_long, VL_time, I_time, P_I_max, VL_max, I_max_nm, P_max_orig, P_8per, P_20per, name_RI,
        P_I, VL, I_max, P_max_em, P_em_8per, P_em_orig_8per, MDP, MDP_em)"""
        bd.execute(table)

# ------------------------------------------------
# Функции вноса данных
# Значения P


def data_P_SS(name, P_I_time, P_I_max, mass_P, mass_P_em, P_I_em, Num_Vl, I_max, am, fl):
    with bd:
        # Предварительная чистка таблицы
        cur.execute("DELETE FROM "+name)
        # Скрипт для добавления строки
        add = f"""INSERT INTO {name} (Temp, P_I_long, VL_time, I_time, P_I_max,
                  VL_max, I_max_nm, P_max_orig, P_8per, P_20per, P_I, VL,
                  I_max, P_max_em, P_em_8per, P_em_orig_8per) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        # Заносим все строки температур НВ раз
        k = 0
        for t in range(-5, 45, 5):
            for i in range(0, am):
                cur.execute(
                    add, (t, P_I_time[0][k]-fl, P_I_time[1][k], P_I_time[2][k],
                          P_I_max[0][k]-fl, P_I_max[1][k], P_I_max[2][k],
                          *mass_P, P_I_em[k][i]-fl, Num_Vl[k][i], I_max[k][i], *mass_P_em[i]))
            k += 1

        # Корректируем значения где была заглушка
        update_P_long = f"""UPDATE {name} SET P_I_long=? WHERE P_I_long=?"""
        cur.execute(update_P_long, (None, 100000-fl))
        update_P_max = f"""UPDATE {name} SET P_I_max=? WHERE P_I_max=?"""
        cur.execute(update_P_max, (None, 100000-fl))
        update_P = f"""UPDATE {name} SET P_I=? WHERE P_I=?"""
        cur.execute(update_P, (None, 100000-fl))

        update_VL_time = f"""UPDATE {name}
            SET VL_time=?, I_time=? WHERE I_time=?"""
        cur.execute(update_VL_time, (None, None, 0))
        update_VL_I_max = f"""UPDATE {
            name} SET VL_max=?, I_max_nm=? WHERE I_max_nm=?"""
        cur.execute(update_VL_I_max, (None, None, 0))
        update_VL_I = f"""UPDATE {name} SET VL=?, I_max=? WHERE I_max=?"""
        cur.execute(update_VL_I, (None, None, 0))


def MDP(name, MDP_mass):
    with bd:
        k = 0
        for t in range(-5, 45, 5):
            update_MDP = f"""UPDATE {name}
                SET MDP=?, MDP_em=? WHERE Temp=?"""
            cur.execute(
                update_MDP, (MDP_mass[0][k], MDP_mass[1][k], t))
            k += 1
