import sqlite3 as sl
import bd_script
from Calc_Rastr import Rastr_Calc_class


# Исходные файлы
# Путь к файлу динамики
path_mode = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Динамика\Mode.rg2'
# Путь к файлу траектории
path_trajectory = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\траектория.ut2'
# Путь к файлу сечения
path_sech = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Центр - Северо-Запад.sch'

# Элементы отвечающие НВ
elements = [[51700109, 40303999], [52902023, 40303061],
            [51700222, 51700026]]
# Массив контролируемых ветвей [[VL1],[VL2],...]
vetvs = [[51700026, 51700222, 0], [40502010, 40502531, 0]]

# РАСЧЕТ РАСТРА

# ------------------------------------------------
# Функция получения данных исходного режима


def norm_F():
    print("Расчет исходного режима")
    norm_P_mass = Rastr_Calc_class(
        path_mode, path_sech, path_trajectory).norm_mode()
    # Занесение значений в БД
    bd_script.new_tab("Norm_mode")
    bd_script.data_P("Norm_mode", norm_P_mass)

# ------------------------------------------------
# Функция получения данных ПА режима


def emerg_F():
    print("Расчет ПА режима с НВ")
    k = 1
    for i in elements:
        name = "RI_"+str(k)
        # Называем каждую ветвь
        j = 1
        name_vetvs = []
        for vl in vetvs:
            name_vetvs.append("VL"+str(j))
            j = j+1
        bd_script.new_tab(name, name_vetvs)
        P_I_one_mass = Rastr_Calc_class(
            path_mode, path_sech, path_trajectory).emerg_mode(i, vetvs)
        if k == 3:
            print(P_I_one_mass[1])
        # Занесение значений в БД
        print(name)
        bd_script.data_P(name, P_I_one_mass[0])
        bd_script.data_I(name, P_I_one_mass[1], name_vetvs)
        k += 1
