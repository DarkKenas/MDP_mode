class Rastr_Calc_class:
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
        return mass_norm_P

    # Утяжеление ПА
    def emerg_mode(self, element, vetv):
        print("Обработка НВ")
        # Массив значений для разных температур
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

        # Создание необходимых массивов
        mass_emerg_P = []
        I_mass = []

        # Занесение первых значенией P, I, step
        mass_emerg_P.append(self.psech.Z(0))
        for i in ind_vetv:
            mini = []
            mini.append(self.i_max.Z(i)*1000)
            I_mass.append(mini)

        # Функция заполнения значений тока для каждой ветви
        def I_mass_func():
            k = 0
            for i in ind_vetv:
                I_mass[k].append(self.i_max.Z(i)*1000)
                k = k+1

        # Здесь уже происходит первый шаг утяжеления и задаётся переменная для проверки работы
        check = self.Rastr.step_ut('')
        if check != 0:
            return ("Ошибка")
        mass_emerg_P.append(self.psech.Z(0))
        I_mass_func()
        

        # Цикл утяжеления ПА
        while check == 0:
            check = self.Rastr.step_ut('')
            mass_emerg_P.append(self.psech.Z(0))
            I_mass_func()

        return [mass_emerg_P, I_mass]
