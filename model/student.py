import sqlite3
from datetime import datetime


class StudentModel:
    def __init__(self, db_name="university.db"):
        self.conn = sqlite3.connect(db_name, timeout=10)
        self.create_table()
        self.student = None

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS SinhVien (
            MaSinhVien TEXT PRIMARY KEY,
            HoTen TEXT NOT NULL,
            GioiTinh TEXT NOT NULL,
            NgaySinh DATE NOT NULL,
            EmailSinhVien TEXT DEFAULT 'no email',
            EmailPhuHuynh TEXT DEFAULT 'no email',
            EmailGVCN TEXT DEFAULT 'gvcn482@gmail.com'
        )
        """)
        self.conn.commit()


    def search_student(self, name):
        cursor = self.conn.execute("SELECT MaSinhVien, HoTen, GioiTinh, NgaySinh FROM SinhVien WHERE HoTen LIKE ?", (f"%{name}%",))
        result = cursor.fetchall()
        students = []
        for i, student in enumerate(result, start=1):
            students.append({
                "STT": i,
                "MaSinhVien": student[0],
                "HoTen": student[1],
                "GioiTinh": student[2],
                "NgaySinh": student[3]
            })
        return students
    
    def add_student(self, ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh):
        try:
            self.conn.execute("INSERT INTO SinhVien (MaSinhVien, HoTen, GioiTinh, NgaySinh) VALUES (?, ?, ?, ?)",(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def get_student(self, ma_sinh_vien):
        try:
            cursor = self.conn.execute("SELECT * FROM SinhVien WHERE MaSinhVien = ?", (ma_sinh_vien,))
            result = cursor.fetchone()
            if result:
                self.student = {
                    "MaSinhVien": result[0],
                    "HoTen": result[1],
                    "GioiTinh": result[2],
                    "NgaySinh": result[3],
                    "EmailSinhVien": result[4],
                    "EmailPhuHuynh": result[5],
                    "EmailGVCN": result[6]
                }
            return self.student
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def update_student(self, ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, EmailSinhVien, EmailPhuHuynh, EmailGVCN):
        try:
            self.conn.execute("UPDATE SinhVien SET HoTen = ?, GioiTinh = ?, NgaySinh = ?, EmailSinhVien = ?, EmailPhuHuynh = ?, EmailGVCN = ? WHERE MaSinhVien = ?",(ho_ten, gioi_tinh, ngay_sinh, EmailSinhVien, EmailPhuHuynh, EmailGVCN, ma_sinh_vien,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def delete_student(self, ma_sinh_vien):
        try:
            self.conn.execute("DELETE FROM SinhVien WHERE MaSinhVien = ?", (ma_sinh_vien,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def fill_absent_list(self, absent_list):
        for absent in absent_list:
            MaSV = absent["MaSinhVien"]  # Lấy giá trị của trường ID
            try:
                cursor = self.conn.execute("SELECT HoTen, EmailSinhVien, EmailPhuHuynh, EmailGVCN FROM SinhVien WHERE MaSinhVien = ?",(MaSV,))
                result = cursor.fetchone()
                if result:
                    absent["TenSinhVien"] = result[0]
                    absent["EmailSinhVien"] = result[1]
                    absent["EmailPhuHuynh"] = result[2]
                    absent["EmailGVCN"] = result[3]
            except sqlite3.IntegrityError:
                return False
        self.conn.close()