import sqlite3 as sl

# Создание и/или подключение файла БД
bd = sl.connect("DataBase//MDP_data.db")
cur = bd.cursor()
# Создание новой таблицы и стобцов
def new_tab(name):
    with bd:
        # Создание таблицы
        table = f"""CREATE TABLE if not exists {name}
        (Temp, P_max_orig, P_8per, P_20per, name_RI TEXT, P_I, VL TEXT, I_max, P_max_em, P_em_8per, P_em_orig_8per)"""
        bd.execute(table)

# ------------------------------------------------
# Функции вноса данных
# Значения P

def data_P_SS(name, mass_P, mass_P_em, P_I_em, Num_Vl, I_max, am):
    with bd:
        # Предварительная чистка таблицы
        cur.execute("DELETE FROM "+name)
        add=f"INSERT INTO {name} (Temp, P_max_orig, P_8per, P_20per, P_I, VL, I_max, P_max_em, P_em_8per, P_em_orig_8per) VALUES (?,?,?,?,?,?,?,?,?,?)"
        # Заносим все строки температур НВ раз
        k=0
        for t in range(-5,45,5):
            for i in range(0,am):
                if P_I_em[k][i]==100000:
                    cur.execute(add,(t, *mass_P, None, None, None,*mass_P_em[i]))
                else:
                    cur.execute(add,(t, *mass_P, P_I_em[k][i], Num_Vl[k][i], I_max[k][i],*mass_P_em[i]))
            k+=1