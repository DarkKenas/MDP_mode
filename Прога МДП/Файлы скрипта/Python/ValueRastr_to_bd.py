# РАСЧЕТ РАСТРА
def Calc_to_bd(name, mode, trajectory, sech, el, vts, off_els, norm_mode, emerge_mode):
    
    import sqlite3 as sl
    import bd_Rastr_scr
    from Calc_Rastr import Rastr_Calc_class
    
    # ------------------------------------------------
    # Функция получения данных исходного режима в БД

    def norm_F():
        print("Расчет исходного режима")
        # Называем каждую ветвь
        j = 1
        name_vetvs = []
        for vl in vts:
            name_vetvs.append("VL"+str(j))
            j = j+1
        # Добавляем столбцы тока ветвей в таблицу БД
        bd_Rastr_scr.new_tab(name, name_vetvs)
        # Расчёт ПАР
        P_I_one_mass = Rastr_Calc_class(
            mode, sech, trajectory).calc_mode(vts, False, off_els)
        # Занесение значений в БД
        print(f"{name} - Выполнен")
        bd_Rastr_scr.data_P(name, P_I_one_mass[0])
        bd_Rastr_scr.data_I(name, P_I_one_mass[1], name_vetvs)
        
    # ------------------------------------------------
    # Функция получения данных ПА режима в БД

    def emerg_F():
        print("Расчет ПА режима с НВ")
        k = 1
        for i in el:
            print("Обработка НВ")
            name_em = name+"_RI_"+str(k)
            # Называем каждую ветвь
            j = 1
            name_vetvs = []
            for vl in vts:
                name_vetvs.append("VL"+str(j))
                j = j+1
            # Добавляем столбцы тока ветвей в таблицу БД
            bd_Rastr_scr.new_tab(name_em, name_vetvs)
            # Расчёт ПАР
            P_I_one_mass = Rastr_Calc_class(
                mode, sech, trajectory).calc_mode(vts, i, off_els)
            # Занесение значений в БД
            print(f"{name_em} - Выполнен")
            bd_Rastr_scr.data_P(name_em, P_I_one_mass[0])
            bd_Rastr_scr.data_I(name_em, P_I_one_mass[1], name_vetvs)
            k += 1
    
    if norm_mode == True:
        norm_F()
    if emerge_mode == True:
        emerg_F()