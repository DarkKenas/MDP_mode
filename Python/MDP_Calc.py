import pandas as pd
import Calc_to_bd
from bd_Rastr_scr import cur
from bd_Rastr_scr import bd
import bd_MDP_scr as bM
import numpy as np
# ------------------------------------------------
# Объект расчета МДП (полный отчет)


class MDP_data:
    # Создаём пустую таблицу
    def __init__(self, name, el, vt, It):
        self.am=len(el)
        self.am_vt=len(vt)
        self.It=It
        bM.new_tab(name)

    # Функция чтобы достать столбец данных
    def data(self, name, col):
        cur.execute(f"SELECT {col} FROM {name}")
        res = cur.fetchall()
        return res

    # Расчет ДП СУ (Steadystate stability - SS) в НР

    def P_SS(self):
        self.mass_P = self.data("Norm_mode", "P_sech")
        P_max = self.mass_P[-1][0]
        P_8per = P_max*0.92
        P_20per = P_max*0.8
        return P_max, P_8per, P_20per

    # Расчет ДП СУ в ПАР
    def P_SS_em(self):
        mass_P_norm = self.data("Norm_mode", "P_sech")
        am = self.am        # Количество НВ
        mass_P=[]
        # Работаем с каждым НВ отдельно
        for i in range(1, am+1):
            mass_P_one = self.data(f"RI_{i}", "P_sech")
            
            # Получаем ДП по СУ
            P_max_em = mass_P_one[-1][0]
            P_em_8per = P_max_em*0.92
            
            # Приведение ДП СУ ПАР к НР
            for j in mass_P_one:
                if j[0] >= P_em_8per:
                    # Номер итерации верхней границы
                    ind = mass_P_one.index(j)
                    down = mass_P_one[ind-1]
                    # Десятичная часть итерации
                    part_num = (P_em_8per-down[0])/(j[0]-down[0])
                    # Формула для приведения: x=i(b-a)+a, где x-привед. знач.;
                    # b и a-верх. и ниж. границы значений ДП НР, i-дес. часть итерации
                    P_em_orig = part_num * \
                        (mass_P_norm[ind][0]-mass_P_norm[ind-1][0])+mass_P_norm[ind-1][0]
                    break
            
            mass_P.append([P_max_em,P_em_8per,P_em_orig])
        return mass_P

    # Расчет ДП по АДТН в ПАР
    def P_I_em(self):
        
        mass_P_norm = self.data("Norm_mode", "P_sech")
        am = self.am        # Количество НВ
        am_vt = self.am_vt     # Количество контролируемых ветвей
        mass_P_I=[]                                           # Список ДП по АДТН для каждого НВ
        mass_Num_Vl=[]                                        # Массив номера ограничивающей ВЛ
        mass_I_max=[]                                         # Массив ограничивающего АДТН
        
        # Перебор по температурам
        for k in range(0,10):
            mass_P_RI=[]                                      # Промежуточные списки
            mass_Num_RVl=[]
            mass_RI_max=[]
            
            # Перебор по НВ
            for i in range(1, am+1):
                mass_P = self.data(f"RI_{i}", "P_sech")
                mid_P=[]                                      # Список ДП в соотвествии с каждой ветвью
                mid_I_max=[]
                
                
                # Перебор по Ветвям
                for j in range(1,am_vt+1):
                    mass_I_one = self.data(f"RI_{i}", f"VL{j}")
                    
                    P_I_orig = 100000
                    I_max = 0
                    # Нахождение ДП ПАР ВЛ в соответсвии с АДТН
                    for p in mass_I_one:
                        # Здесь p - Значение тока ветви
                    
                        # Сравниваем p с заданным АДТН
                        if p[0] >= self.It[j-1][k]:
                            # Номер итерации верхней границы
                            ind = mass_I_one.index(p)
                            down = mass_I_one[ind-1]
                            
                            # Если это последняя итерация утяжеления
                            if p == mass_I_one[-1]:
                                # Интерполяция до необходимого значения в последней итерации
                                # (То значение которое было бы без дробления шага Растром)
                                delta = (mass_P[-1][0]/(2*mass_P[-2][0]-mass_P[-3][0]))
                                part_num = (self.It[j-1][k]-down[0])/(p[0]/delta-down[0])
                            else:
                                part_num = (self.It[j-1][k]-down[0])/(p[0]-down[0])
                            
                            # Приведение
                            P_I_orig = part_num * \
                                (mass_P_norm[ind][0]-mass_P_norm[ind-1][0])+mass_P_norm[ind-1][0]
                            
                            # Контролируемое значение АДТН
                            I_max = self.It[j-1][k]
                            break
                        
                    mid_P.append(P_I_orig)
                    mid_I_max.append(I_max)
                    
                if len(mid_P)!=0:
                    mass_P_RI.append(min(mid_P))
                    index=mid_P.index(min(mid_P))
                    mass_Num_RVl.append(index)
                    mass_RI_max.append(mid_I_max[index])
                    
            if len(mass_P_RI)!=0:
                mass_P_I.append(mass_P_RI)
                mass_Num_Vl.append(mass_Num_RVl)
                mass_I_max.append(mass_RI_max)
        
        return [mass_P_I, mass_Num_Vl, mass_I_max]
    
    # Полный отчёт

    def full_rep(self, name):
        P_SS_mass = self.P_SS()
        P_SS_em_mass = self.P_SS_em()
        P_I_em_mass = self.P_I_em()[0]
        Num_Vl = self.P_I_em()[1]
        I_max = self.P_I_em()[2]
        am = 3
        bM.data_P_SS(name, P_SS_mass, P_SS_em_mass, P_I_em_mass, Num_Vl, I_max, am)



# Элементы отвечающие НВ
elements = [[51700109, 40303999], [52902023, 40303061],
            [51700222, 51700026]]
# Массив контролируемых ветвей [[VL1],[VL2],...]
vetvs = [[51700026, 51700222, 0], [40502010, 40502531, 0]]
I_set = [[1780,1711,1656,1587,1532,1449,1380,1297,1214,1118],
         [1774,1690,1609,1521,1430,1335,1234,1120,1013,890]]


MDP_data("Norm_scheme", elements, vetvs, I_set).full_rep("Norm_scheme")
# print(MDP_data("Norm_scheme").P_SS_em())
# print("Отчёт создан")

# check=MDP_data("Norm_scheme", elements, vetvs, I_set).P_I_em()
# print(check)

# Отправляем БД в Эксель
check=pd.read_sql("SELECT * FROM Norm_scheme",bM.bd)
check.to_excel(r'Файлы Excel/check.xlsx')