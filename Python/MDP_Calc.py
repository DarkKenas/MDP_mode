from MDP_Calc_func import P_MDP_class

# Исходные файлы
# Путь к файлу динамики
path_mode = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Динамика\Mode.rg2'
# Путь к файлу траектории
path_trajectory = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\траектория.ut2'
# Путь к файлу сечения
path_sech = r'C:\Users\bukre\OneDrive\Рабочий стол\ОДУ\Расчет МДП тест\Rastr\Центр - Северо-Запад.sch'

elements = [[51700109, 40303999], [52902023, 40303061],
            [51700222, 51700026]]      # Элементы отвечающие НВ
# Массив контролируемых ветвей
vetvs = [[51700026, 51700222, 0], [40502010, 40502531, 0]]
controlled = [[1532, 1430], [1449, 1335]]     # Значения АДТН

# Осуществление утяжеления исходного режима


def norm_mode_calc():
    P_norm_mode = P_MDP_class(path_mode, path_sech,
                              path_trajectory).norm_mode()
    return P_norm_mode

# norm_calc=norm_mode_calc(path_mode,path_sech,path_trajectory)
# print("Значение МДП в исходном режиме с 20% запасом по статической устойчивости:\n"+str(norm_calc[0]))


# Осуществление утяжеления ПА режима для каждого НВ
# Функция нахождения ДП по каждому НВ (по стат. уст. с 8%  и по току)
def enum_elements_emerg(P_norm_mode=False):

    # Проверка и расчет исходного режима, если он не был осуществлен ранее
    if P_norm_mode == False:
        P_norm_mode = P_MDP_class(
            path_mode, path_sech, path_trajectory).norm_mode()

    MDP_mass = []
    # Выполняем функцию утяжеления для каждого НВ
    for i in elements:
        Mdp = P_MDP_class(path_mode, path_sech, path_trajectory).emerg_mode(
            i, vetvs, controlled)      # Массив для  одного элемента
        MDP_mass.append(Mdp)        # Результат - массив МДП ПА
    print(MDP_mass)

    # Приведение к мощности исходного режима
    P_norm_emerg_mass = []
    P_temp_mass = []
    for i in MDP_mass:  # Перебор массива по НВ
        k = 0
        for j in i[1]:  # Перебор значений ДП в отдельном НВ по статической устойчивости
            if j >= i[0] and k != 0:
                part_num_emerg = (i[0]-k)/(j-k)   # Десятичная часть итерации
                ind_emerg = i[1].index(j)     # Номер итерации верхней границы
                # Формула для приведения: x=i(b-a)+a, где x-привед. знач.; b и a-верх. и ниж. границы значений ДП, i-дес. часть итерации
                P_norm_emerg = part_num_emerg * \
                    (P_norm_mode[1][ind_emerg]-P_norm_mode[1]
                     [ind_emerg-1])+P_norm_mode[1][ind_emerg-1]
                P_norm_emerg_mass.append(round(P_norm_emerg, 2))
                break
            k = j

        # Приведение ДП по току к исходному режиму
        p = 0
        P_norm_emerg_current_mass = []
        while p < len(controlled):
            if type(i[2][p][1]) is int:
                P_norm_emerg_current = i[2][p][0]*(
                    P_norm_mode[1][i[2][p][1]]-P_norm_mode[1][i[2][p][1]-1])+P_norm_mode[1][i[2][p][1]-1]
                P_norm_emerg_current_mass.append(
                    round(P_norm_emerg_current, 2))
            else:
                P_norm_emerg_current_mass.append("Ошибка")
            p = p+1
        P_temp_mass.append(P_norm_emerg_current_mass)
    return [P_norm_emerg_mass, P_temp_mass]

# P_emerg=enum_elements_emerg()
# print("Массив приведенных значений МДП НВ по стат. устойчивости:\n"+str(P_emerg[0]))
# print("Массив приведенных значений МДП НВ по току (НВ->[Т1,Т2]):\n"+str(P_emerg[1]))


# Функиця выборки минимального ДП по каждой температуре
def min_P():
    norm_calc = norm_mode_calc()
    emerg_calc = enum_elements_emerg(norm_calc)

    Min_P_mass_temp = []
    l = 0
    while l < len(controlled):    # Перебор по температурам
        middle_mass = []
        for k in emerg_calc[1]:     # Перебор НВ
            middle_mass.append(k[l])

        # Удаление элементов ("Ошибка") из массива
        emerg_current_calc = [j for j in middle_mass if type(j) != str]
        # Минимальный ДП по конкретной температуре
        Min_P_mass = min(
            [norm_calc[0], min(emerg_calc[0]), min(emerg_current_calc)])
        Min_P_mass_temp.append(Min_P_mass)
        l = l+1
    return Min_P_mass_temp


min_MDP = min_P()
print("Минимальное значени ДП:\n"+str(min_MDP))

print("Выполнение закончил")
