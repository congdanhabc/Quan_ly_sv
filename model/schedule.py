import sqlite3
from datetime import datetime

class ScheduleModel:
    def __init__(self, db_name="university.db"):
        self.conn = sqlite3.connect(db_name, timeout=10)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS LichHoc(
        LichHoc_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID INTEGER NOT NULL,
        NgayHoc DATE NOT NULL,
        TrangThai TEXT NOT NULL,
        FOREIGN KEY (ID) REFERENCES Sv_Lop(ID),
        UNIQUE (ID, NgayHoc)  -- Ràng buộc UNIQUE trên cặp ID và NgayHoc
        );
        """)
        self.conn.commit()

    def add_lich_hoc(self, id, ngay_hoc, trang_thai):
        try:
            self.conn.execute("INSERT INTO LichHoc (ID, NgayHoc, TrangThai) VALUES (?, ?, ?)",
                              (id, ngay_hoc, trang_thai))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def search_schedule(self, id):
        try:
            cursor = self.conn.execute("SELECT NgayHoc, TrangThai FROM LichHoc WHERE ID = ?",(id,))
            results = cursor.fetchall()
            sorted_results = sorted(results, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
            schedule_list = []
            for result in sorted_results:
                schedule_list.append({
                "NgayHoc": result[0],
                "TrangThai": result[1],
            })
            return schedule_list
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.close()

    def get_absent_list(self):
        query = """
        SELECT 
            ID,
            (SUM(CASE WHEN TrangThai = 'P' THEN 1 ELSE 0 END) + SUM(CASE WHEN TrangThai = 'K' THEN 1 ELSE 0 END)) AS SoBuoi,
             ROUND((CAST(SUM(CASE WHEN TrangThai IN ('P', 'K') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100, 2) AS ThoiLuong
        FROM 
            LichHoc
        GROUP BY 
            ID
        HAVING 
            SoBuoi > 0
        """
        cursor = self.conn.execute(query)
        results = cursor.fetchall()
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        absent_list = []        
        for row in sorted_results:
            absent = {
                "ID": row[0],
                "MaSinhVien": "",
                "TenSinhVien": "",
                "MaLopHocPhan": "",
                "TenMonHoc": "",
                "SoBuoi": row[1],
                "ThoiLuong": row[2],
                "EmailSinhVien": "",
                "EmailPhuHuynh": "",
                "EmailGVCN": "",
                "EmailTBM": ""
            }
            absent_list.append(absent)
        return absent_list