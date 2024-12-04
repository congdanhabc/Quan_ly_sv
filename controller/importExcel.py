from model.student import StudentModel
from model.student_class import Student_ClassModel
from model.class_study import ClassModel
from model.schedule import ScheduleModel

import pandas as pd 
import re
from datetime import datetime


def update_sv_from_excel(excel_file, ma_lop_hoc_phan):
    df = pd.read_excel(excel_file, skiprows = 11)
    df["Mã sinh viên"] = df["Mã sinh viên"].fillna(0).astype(int).astype(str)
    date_columns = df.filter(regex=r'\d{2}/\d{2}/\d{4}').columns
    for index, row in df.iterrows():
        if row["Mã sinh viên"] == "0": continue
        ngay_sinh = row["Ngày sinh"].strftime('%d/%m/%Y')
        student_model = StudentModel()
        student_model.add_student(row["Mã sinh viên"], row["Họ đệm"] + " " + row["Tên"], row["Giới tính"], ngay_sinh)

        student_class = Student_ClassModel()
        ID = student_class.add_student_class(row["Mã sinh viên"],ma_lop_hoc_phan)

        for col in date_columns:
            date =  datetime.strptime(col.split(" - ")[2], "%d/%m/%Y").date().strftime('%d/%m/%Y')
            trang_thai = row[col]
            if pd.isna(trang_thai):
                trang_thai = "C"
            schedule_model = ScheduleModel()
            schedule_model.add_lich_hoc(ID, date, trang_thai)




def update_class_form_excel(excel_file):
    class_model = ClassModel()
    df = pd.read_excel(excel_file, skiprows=4, nrows=6)
    hoc_ky = df.iloc[0, 2]
    co_so = df.iloc[1, 2]
    ma_lop_hoc_phan = df.iloc[2, 2]
    ten_mon_hoc = df.iloc[3, 2]
    ten_mon_hoc = re.sub(r"\(.*?\)", "", ten_mon_hoc).strip()
    phong = df.iloc[4, 2]
    class_model.add_class(ma_lop_hoc_phan, hoc_ky, co_so, ten_mon_hoc, phong)
    return ma_lop_hoc_phan


def import_excel(excel_file):
    ma_lop_hoc_phan = update_class_form_excel(excel_file)
    update_sv_from_excel(excel_file, ma_lop_hoc_phan)
