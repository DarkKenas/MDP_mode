from MDP_Calc import MDP_data
from Calc_to_bd import Calc_to_bd as calc
from Excel_scr import Full_rep as rep
import pandas as pd
import bd_MDP_scr as bM


# Исходные файлы
# Путь к файлу динамики
mode = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Динамика\Mode.rg2'
# Путь к файлу траектории
trajectory = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\траектория.ut2'
# Путь к файлу сечения
sech = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Центр - Северо-Запад.sch'

# Элементы отвечающие НВ
elements = [[51700109, 40303999], [52902023, 40303061],
            [51700222, 51700026]]

# Список контролируемых ветвей [[VL1],[VL2],...]
vetvs = [[51700026, 51700222, 0], [
    40502010, 40590507, 0], [40490354, 51700027, 0]]

# Список значений АДТН [[T1,T2,...][T1,T2,...]...]
I_set = [[1780, 1711, 1656, 1587, 1532, 1449, 1380, 1297, 1214, 1118],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890]]

I_time = [[1780, 1711, 1656, 1587, 1532, 1449, 1380, 1297, 1214, 1118],
          [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890],
          [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890]]

# Нерегулярные колебания
fluc = 150

# -------------------------------------------------------------
# Произвести расчет НР (nm) и/или ПАР (em)
# (Для необходимого расчета заменить "False" на "True")

calc("Norm_scheme", mode, trajectory, sech,
     elements, vetvs, False, nm=False, em=False)


# -------------------------------------------------------------
# Сформировать отчёт в эксель
# Здесь задать путь к файлу Эксель и необходимое название
path_excel = r'Файлы Excel/check2.xlsx'
name_tab = "Norm_scheme"

flag = False
if flag != False:
    MDP_data(name_tab, name_tab, elements, vetvs,
             I_set, I_time, fluc).full_rep(name_tab)

# --------------------------------------------------------------
# Ремонты

# Ремонт ВЛ 750 кВ Калининская АЭС - Ленинградская

# Отключаемые элементы
off_els = [51700109, 40303999]

# Элементы отвечающие НВ
elements = [[52902023, 40303061], [51700222, 51700026], [40502010, 40502531]]

# Список контролируемых ветвей [[VL1],[VL2],...]
vetvs = [[51700026, 51700222, 0], [
    40502010, 40590507, 0], [40490354, 51700027, 0]]

# Список значений АДТН [[T1,T2,...][T1,T2,...]...]
I_set = [[1780, 1711, 1656, 1587, 1532, 1449, 1380, 1297, 1214, 1118],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890]]

# --------------------------------------------------------------
# Расчет
name_tab = "Repair_1"
calc(name_tab, mode, trajectory, sech, elements,
     vetvs, off_els, nm=False, em=False)

# --------------------------------------------------------------
# Сформировать отчёт в эксель

flag = False
if flag != False:
    MDP_data(name_tab, name_tab, elements, vetvs,
             I_set, I_time, fluc).full_rep(name_tab)


# ---------------------------------------------------------------
# Ремонт ВЛ 750 кВ Белозерская - Ленинградская
# Отключаемые элементы
off_els = [52902023, 40303061]

# Элементы отвечающие НВ
elements = [[51700109, 40303999], [51700222, 51700026], [40502010, 40502531]]

# Список контролируемых ветвей [[VL1],[VL2],...]
vetvs = [[51700026, 51700222, 0], [
    40502010, 40590507, 0], [40490354, 51700027, 0]]

# Список значений АДТН [[T1,T2,...][T1,T2,...]...]
I_set = [[1780, 1711, 1656, 1587, 1532, 1449, 1380, 1297, 1214, 1118],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890],
         [1774, 1690, 1609, 1521, 1430, 1335, 1234, 1120, 1013, 890]]

# --------------------------------------------------------------
# Расчет
name_tab = "Repair_2"
calc(name_tab, mode, trajectory, sech, elements,
     vetvs, off_els, nm=False, em=False)

# -------------------------------------------------------------
# Сформировать отчёт в эксель

flag = False
if flag != False:
    MDP_data(name_tab, name_tab, elements, vetvs,
             I_set, I_time, fluc).full_rep(name_tab)


# -------------------------------------------------------------
# -------------------------------------------------------------
# Создание отчёта в Excel
name_tabs = "Norm_scheme"
rep(name_tabs, path_excel)
