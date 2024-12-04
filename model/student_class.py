import sqlite3

class Student_ClassModel:
    def __init__(self, db_name="university.db"):
        self.conn = sqlite3.connect(db_name, timeout=10)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Sv_Lop(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MaSinhVien TEXT NOT NULL,
            MaLopHocPhan TEXT NOT NULL,
            FOREIGN KEY (MaSinhVien) REFERENCES SinhVien(MaSinhVien),
            FOREIGN KEY (MaLopHocPhan) REFERENCES LopHoc(MaLopHocPhan),
            UNIQUE (MaSinhVien, MaLopHocPhan) 
        );

        """)
        self.conn.commit()

    def add_student_class(self, ma_sinh_vien, ma_lop_hoc_phan):
        try:
            cursor = self.conn.execute("INSERT INTO Sv_Lop (MaSinhVien, MaLopHocPhan) VALUES (?, ?)",
                                       (ma_sinh_vien, ma_lop_hoc_phan))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def search_student_class(self, ma_sinh_vien):
        try:
            cursor = self.conn.execute("SELECT MaLopHocPhan FROM Sv_Lop WHERE MaSinhVien = ?",(ma_sinh_vien,))
            result = cursor.fetchone()
            class_list = []
            if result:
                class_list.append(result[0])
            return class_list
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def search_student_class_id(self, ma_sinh_vien, ma_hoc_phan):
        try:
            cursor = self.conn.execute("SELECT ID FROM Sv_Lop WHERE MaLopHocPhan = ? AND MaSinhVien = ?",(ma_hoc_phan, ma_sinh_vien,))
            result = cursor.fetchone()
            if result:
                return result[0]
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def fill_absent_list(self, absent_list):
        for absent in absent_list:
            id = absent["ID"]  # Lấy giá trị của trường ID
            try:
                cursor = self.conn.execute("SELECT MaSinhVien, MaLopHocPhan FROM Sv_Lop WHERE ID = ?",(id,))
                result = cursor.fetchone()
                if result:
                    absent["MaSinhVien"] = result[0]
                    absent["MaLopHocPhan"] = result[1] 
            except sqlite3.IntegrityError:
                return False
        self.conn.close()
                
