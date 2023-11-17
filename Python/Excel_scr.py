def Full_rep(name, path):
    import bd_MDP_scr as bM
    import pandas as pd
    import openpyxl as px

    file = px.load_workbook(path)
    name_sheet1 = file.get_sheet_names()[0]
    sheet1 = file.get_sheet_by_name(name_sheet1)

    # Занесение данных по всем схемам
    cnct = pd.read_sql(f"SELECT * FROM {name}", bM.bd)
    with pd.ExcelWriter(path, mode="a", if_sheet_exists="overlay") as writer:
        cnct.to_excel(writer, sheet_name=name_sheet1, startrow=3)

    # Очистка заголовков из БД
    for i in range(0, len(sheet1[4])):
        sheet1[4][i].value = None
    sheet1.merge_cells('B4:T4')
    sheet1['B4'] = "Нормальная схема"
    file.save(path)
