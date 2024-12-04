import sqlite3

class ClassModel:
    def __init__(self, db_name="university.db"):
        self.conn = sqlite3.connect(db_name, timeout=10)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS LopHoc (
            MaLopHocPhan TEXT PRIMARY KEY,
            HocKy TEXT NOT NULL,
            CoSo TEXT NOT NULL,
            TenMonHoc TEXT NOT NULL,
            Phong TEXT NOT NULL,
            EmailTBM TEXT DEFAULT 'tbm43215@gmail.com'

        )
        """)
        self.conn.commit()

    def add_class(self, ma_lop_hoc_phan, hoc_ky, co_so, ten_mon_hoc, phong):
        try:
            self.conn.execute("INSERT INTO LopHoc (MaLopHocPhan, HocKy, CoSo, TenMonHoc, Phong) VALUES (?, ?, ?, ?, ?)",(ma_lop_hoc_phan, hoc_ky, co_so, ten_mon_hoc, phong))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def get_class(self, ma_lop_hoc_phan):
        cursor = self.conn.execute("SELECT * FROM LopHoc WHERE MaLopHocPhan = ?", (ma_lop_hoc_phan,))
        class_info = cursor.fetchone()
        if class_info:
            class_dict = {
                "MaLopHocPhan": class_info[0],
                "HocKy": class_info[1],
                "CoSo": class_info[2],
                "TenMonHoc": class_info[3],
                "Phong": class_info[4]
            }
            return class_dict
        return None

    def update_class(self, ma_lop_hoc_phan, hoc_ky, co_so, ten_mon_hoc, lop_hoc):
        self.conn.execute("UPDATE LopHoc SET HocKy = ?, CoSo = ?, TenMonHoc = ?, LopHoc = ? WHERE MaLopHocPhan = ?",
                          (hoc_ky, co_so, ten_mon_hoc, lop_hoc, ma_lop_hoc_phan))
        self.conn.commit()
        return True

    def delete_class(self, ma_lop_hoc_phan):
        self.conn.execute("DELETE FROM LopHoc WHERE MaLopHocPhan = ?", (ma_lop_hoc_phan,))
        self.conn.commit()
        return True
    
    def fill_absent_list(self, absent_list):
        for absent in absent_list:
            MaLop = absent["MaLopHocPhan"]  # Lấy giá trị của trường ID
            try:
                cursor = self.conn.execute("SELECT TenMonHoc, EmailTBM FROM LopHoc WHERE MaLopHocPhan = ?",( MaLop,))
                result = cursor.fetchone()
                if result:
                    absent["TenMonHoc"] = result[0]
                    absent["EmailTBM"] = result[1]
            except sqlite3.IntegrityError:
                return False
        self.conn.close()

