class P_MDP_class:
    def __init__(self, mode, sech, trajectory):
        import win32com.client
        self.Rastr = win32com.client.Dispatch("Astra.Rastr")

        # Подгрузка используемых файлов
        self.Rastr.Load(0, mode, "")
        self.Rastr.Load(
            0, trajectory, r'C:\Users\bukre\OneDrive\Документы\RastrWin3\SHABLON\траектория утяжеления.ut2')
        self.Rastr.Load(
            0, sech, r'C:\Users\bukre\OneDrive\Документы\RastrWin3\SHABLON\сечения.sch')

        # Получаем данные P по сечению
        self.sechen = self.Rastr.Tables("sechen")
        self.psech = self.sechen.Cols("psech")

        # Получаем данные по узлам
        self.node = self.Rastr.Tables("node")
        self.sta_node = self.node.Cols("sta")     # Столбец вкл/откл.

        # Получаем данные по ветвям
        self.vetv = self.Rastr.Tables("vetv")
        self.i_max = self.vetv.Cols("i_max")

        self.Rastr.rgm('')
        # Обязательная инициализция значений утяжеления
        self.Rastr.step_ut("i")
        print("Файлы загружены\nНачинаю выполнение")

    # ОПРЕДЕЛЕНИЕ МДП ПО СТАТИЧЕСКОЙ УСТОЙЧИВОСТИ
    # Утяжеление исходного режима
    def norm_mode(self):
        mass_norm_P = []        # Массив значений P через сечение
        # Создание массива значений и занесение первого элемента
        mass_norm_P.append(self.psech.Z(0))

        # Переменная для проверки выполнения шага утяжеления
        check_norm = self.Rastr.step_ut('')
        if check_norm != 0:
            return ("Ошибка")
        mass_norm_P.append(self.psech.Z(0))

        # Цикл нахождения значений через сечение
        while check_norm == 0:
            check_norm = self.Rastr.step_ut('')
            mass_norm_P.append(self.psech.Z(0))
            # print(self.psech.Z(0))
        self.P_MDP_norm = round(self.psech.Z(0), 2)*0.8
        return [self.P_MDP_norm, mass_norm_P]

    # Утяжеление ПА
    def emerg_mode(self, element, vetv, controlled):

        # Массив значений для разных температур
        temp_mass = ["None"]*len(controlled)
        ind_vetv = []     # Массив индексов ветвей
        # Цикл определения индексов ветвей
        for i in vetv:
            self.vetv.SetSel("ip="+str(i[0]) +
                             "&iq=" + str(i[1]) + "&np="+str(i[2]))
            ind_vetv.append(self.vetv.FindNextSel(-1))

        # Отключение узлов
        for i in element:
            self.node.SetSel("ny="+str(i))
            # Получаем индексы узлов
            self.index = self.node.FindNextSel(-1)
            self.sta_node.SetZ(self.index, True)      # Отключаем их
        self.Rastr.rgm('')

        # Цикл утяжеления ПА режима
        mass_MDP_val = []
        # Создаём массив по МДП для дальнейшей выборки и нахождения шага. Добавляю нач. знач.
        mass_MDP_val.append(self.psech.Z(0))
        # print(self.psech.Z(0))

        # Здесь уже происходит первый шаг утяжеления и задаётся переменная для проверки работы
        check = self.Rastr.step_ut('')
        # print(self.psech.Z(0))
        mass_MDP_val.append(self.psech.Z(0))

        flag = [False]*len(controlled)

        # Цикл утяжеления ПА
        i_mass_num = []
        while check == 0:
            check = self.Rastr.step_ut('')
            mass_MDP_val.append(self.psech.Z(0))
            i_mass = []
            print(ind_vetv)

            for i in ind_vetv:
                i_mass.append(self.i_max.Z(i)*1000)
            i_mass_num.append(i_mass)

            print(self.psech.Z(0))

            l = 0
            for j in controlled:        # Перебор по температурам
                k = 0         # Порядковый номер ветви в массиве температур
                for i in ind_vetv:
                    # Сопоставление расчетной величины тока с заданной
                    if self.i_max.Z(i)*1000 >= j[k] and flag[l] == False:
                        # Верхняя граница искомого значения тока
                        i_max_up = self.i_max.Z(i)*1000
                        # Десятичная часть итерации искомого значения тока
                        part_num = (j[k]-i_mass_num[-2][k]) / \
                            (i_max_up-i_mass_num[-2][k])
                        ind_P_emerg_curr = mass_MDP_val.index(
                            # Порядковый номер этой итерации
                            self.psech.Z(0))
                        print(part_num)
                        flag[l] = True
                        temp_mass[l] = [part_num, ind_P_emerg_curr]
                        break
                    # Если НВ является контролируемой ветвью
                    if self.i_max.Z(i)*1000 == 0:
                        part_num = "Error1"
                        ind_P_emerg_curr = "Error1"
                        temp_mass[l] = [part_num, ind_P_emerg_curr]
                    k = k+1
                l = l+1

        a = 0
        for i in flag:
            if i == False:    # Если для каких то температур режим по стат. уст. разошёлся раньше чем по току
                part_num = "Error2"
                ind_P_emerg_curr = "Error2"
                temp_mass[a] = [part_num, ind_P_emerg_curr]
            a = a+1

        return [self.psech.Z(0)*0.92, mass_MDP_val, temp_mass]
