# ------------------------------------------------
# Объект расчета МДП (полный отчет)


class MDP_data:
    # Создаём пустую таблицу
    def __init__(self, name, em_name, el, vt, It, Itt, fluc):

        from bd_Rastr_scr import cur
        import bd_MDP_scr as bM
        self.cur = cur
        self.bM = bM
        self.am = len(el)
        self.am_vt = len(vt)
        self.It = It
        self.Itt = Itt
        self.em_name = em_name
        self.fl = fluc          # НК
        bM.new_tab(name)

    # Функция чтобы достать столбец данных

    def data(self, name, col):
        self.cur.execute(f"SELECT {col} FROM {name}")
        res = self.cur.fetchall()
        return res

    # Расчет ДП СУ (Steadystate stability - SS) в НР

    def P_SS(self, em_name):
        self.mass_P = self.data(em_name, "P_sech")
        P_max = self.mass_P[-1][0]
        P_8per = P_max*0.92
        P_20per = P_max*0.8 - self.fl
        return P_max, P_8per, P_20per

    # Расчет ДП по ДДТН/АДТН в НР
    def P_I_nm(self, em_name, I_check):

        # Получаем список значений P нормального режима
        mass_P_norm = self.data(em_name, "P_sech")
        am_vt = self.am_vt     # Количество контролируемых ветвей

        # Список P ДДТН/АДТН
        mass_P = []
        mass_I = []
        mass_Num_Vl = []

        # Перебор по температурам
        for k in range(0, 10):
            # Промежуточные списки
            mass_P_Vl = []
            mass_P_I_Vl = []

            # Перебор по Ветвям
            for j in range(1, am_vt+1):
                mass_I_one = self.data(em_name, f"VL{j}")

                # Это значения, чтобы заполнять пустые места в списках
                P_orig = 100000
                I_max = 0

                # Нахождение ДП ПАР ВЛ в соответсвии с АДТН
                for p in mass_I_one:
                    # Здесь p - Значение тока ветви

                    # Сравниваем p с заданным АДТН
                    if p[0] >= I_check[j-1][k]:

                        # Номер итерации верхней границы
                        ind = mass_I_one.index(p)
                        down = mass_I_one[ind-1]
                        # Находим десятичную часть необходимой итерации
                        part_num = (I_check[j-1][k]-down[0])/(p[0]-down[0])

                        # Переходим к значениям P
                        P_orig = part_num * \
                            (mass_P_norm[ind][0]-mass_P_norm[ind-1]
                             [0]) + mass_P_norm[ind-1][0]
                        # Контролируемое значение АДТН
                        I_max = I_check[j-1][k]
                        break

                mass_P_Vl.append(P_orig)
                mass_P_I_Vl.append(I_max)

            mass_P.append(min(mass_P_Vl))
            index = mass_P_Vl.index(min(mass_P_Vl))
            mass_I.append(mass_P_I_Vl[index])
            mass_Num_Vl.append(index)

        return [mass_P, mass_Num_Vl, mass_I]

    # Расчет ДП СУ в ПАР

    def P_SS_em(self, em_name):
        mass_P_norm = self.data(em_name, "P_sech")
        am = self.am        # Количество НВ
        mass_P = []
        # Работаем с каждым НВ отдельно
        for i in range(1, am+1):
            mass_P_one = self.data(f"{em_name}_RI_{i}", "P_sech")

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
                        (mass_P_norm[ind][0]-mass_P_norm[ind-1]
                         [0])+mass_P_norm[ind-1][0]
                    break

            mass_P.append([P_max_em, P_em_8per, P_em_orig-self.fl])
        return mass_P

    # Расчет ДП по АДТН в ПАР
    def P_I_em(self, em_name):

        mass_P_norm = self.data(em_name, "P_sech")
        am = self.am        # Количество НВ
        am_vt = self.am_vt     # Количество контролируемых ветвей
        # Список ДП по АДТН для каждого НВ
        mass_P_I = []
        # Массив номера ограничивающей ВЛ
        mass_Num_Vl = []
        # Массив ограничивающего АДТН
        mass_I_max = []

        # Перебор по температурам
        for k in range(0, 10):
            mass_P_RI = []                                      # Промежуточные списки
            mass_Num_RVl = []
            mass_RI_max = []

            # Перебор по НВ
            for i in range(1, am+1):
                mass_P = self.data(f"{em_name}_RI_{i}", "P_sech")
                # Список ДП в соотвествии с каждой ветвью
                mid_P = []
                mid_I_max = []

                # Перебор по Ветвям
                for j in range(1, am_vt+1):
                    mass_I_one = self.data(f"{em_name}_RI_{i}", f"VL{j}")

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
                                delta = (
                                    mass_P[-1][0]/(2*mass_P[-2][0]-mass_P[-3][0]))
                                part_num = (
                                    self.It[j-1][k]-down[0])/(p[0]/delta-down[0])
                            else:
                                part_num = (
                                    self.It[j-1][k]-down[0])/(p[0]-down[0])

                            # Приведение
                            P_I_orig = part_num * \
                                (mass_P_norm[ind][0]-mass_P_norm[ind-1]
                                 [0])+mass_P_norm[ind-1][0]

                            # Контролируемое значение АДТН
                            I_max = self.It[j-1][k]
                            break

                    mid_P.append(P_I_orig)
                    mid_I_max.append(I_max)

                mass_P_RI.append(min(mid_P))
                index = mid_P.index(min(mid_P))
                mass_Num_RVl.append(index)
                mass_RI_max.append(mid_I_max[index])

            mass_P_I.append(mass_P_RI)
            mass_Num_Vl.append(mass_Num_RVl)
            mass_I_max.append(mass_RI_max)

        return [mass_P_I, mass_Num_Vl, mass_I_max]

    # Определние минимального МДП с/без ПА
    def MDP(self, name):
        # Получение данных из БД
        MDP = []
        MDP_em = []
        with self.bM.bd:
            for i in range(-5, 45, 5):
                # Формируем МДП без ПА
                MDP_em_mid = []
                # Получаем массивы данных
                self.bM.cur.execute(f"""SELECT P_I FROM {
                                    name} WHERE Temp=?""", (i,))
                P_I = self.bM.cur.fetchall()
                self.bM.cur.execute(f"""SELECT P_em_orig_8per FROM {
                                    name} WHERE Temp=?""", (i,))
                P_orig = self.bM.cur.fetchall()
                # Заносим значения Pдав и Pадтн для каждого НВ
                k = 0
                for j in P_I:
                    if j[0] != None:
                        MDP_em_mid.append(min(j[0], P_orig[k][0]))
                    k += 1
                MDP_em.append(min(MDP_em_mid))

                # Формируем МДП с ПА
                MDP_mid = []
                self.bM.cur.execute(f"""SELECT P_I_long FROM {
                                    name} WHERE Temp=?""", (i,))
                if self.bM.cur.fetchone()[0] != None:
                    MDP_mid.append(self.bM.cur.fetchone()[0])
                self.bM.cur.execute(f"""SELECT P_20per FROM {
                                    name} WHERE Temp=?""", (i,))
                MDP_mid.append(self.bM.cur.fetchone()[0])
                MDP.append(min(MDP_mid))
        return MDP, MDP_em
    # Полный отчёт

    def full_rep(self, name):
        # Получаем все рассчитанные значения
        P_SS_mass = self.P_SS(self.em_name)
        P_SS_em_mass = self.P_SS_em(self.em_name)
        P_I_em_mass = self.P_I_em(self.em_name)[0]
        Num_Vl = self.P_I_em(self.em_name)[1]
        I_max = self.P_I_em(self.em_name)[2]
        P_I_max = self.P_I_nm(self.em_name, self.It)
        P_I_time = self.P_I_nm(self.em_name, self.It)
        am = self.am    # Количество НВ
        # Занесение значений в БД
        self.bM.data_P_SS(name, P_I_time, P_I_max, P_SS_mass, P_SS_em_mass,
                          P_I_em_mass, Num_Vl, I_max, am, self.fl)

        # Получаем значения МДП
        MDP = self.MDP(name)
        self.bM.MDP(name, MDP)
        print("Отчёт создан")
