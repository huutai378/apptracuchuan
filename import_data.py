import os
import sqlite3
import unicodedata
import openpyxl

def remove_accents(input_str):
    if not isinstance(input_str, str):
        input_str = str(input_str) if input_str is not None else ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D').lower().strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Bảng hồ sơ
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ho_so (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ho_ten TEXT,
        ho_ten_khong_dau TEXT,
        thong_tin_chi_tiet TEXT,
        thong_tin_khong_dau TEXT,
        ten_file TEXT
    )
''')

# 2. Bảng tài khoản (Bắt buộc cho main_3.py)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tai_khoan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
''')

# 3. Bảng lịch sử tra cứu
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lich_su_tra_cuu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        thoi_gian TEXT,
        user_tra_cuu TEXT,
        nguoi_yeu_cau TEXT,
        ghi_chu TEXT,
        tu_khoa TEXT,
        so_ket_qua INTEGER
    )
''')

# 4. Bảng thống kê
cursor.execute('''
    CREATE TABLE IF NOT EXISTS thong_ke (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loai_ho_so TEXT UNIQUE,
        so_luong INTEGER
    )
''')

# Thêm tài khoản mặc định (Admin: admin/admin | User: user/123)
cursor.execute("INSERT OR IGNORE INTO tai_khoan (username, password, role) VALUES ('admin', 'admin', 'admin')")
cursor.execute("INSERT OR IGNORE INTO tai_khoan (username, password, role) VALUES ('user', '123456', 'user')")

# Nạp dữ liệu Excel nếu có
data_dir = os.path.join(BASE_DIR, "data_raw")
target_dir = data_dir if os.path.exists(data_dir) else BASE_DIR
files = [f for f in os.listdir(target_dir) if f.endswith(('.xlsx', '.xls'))]

tong_so = 0
for file_name in files:
    file_path = os.path.join(target_dir, file_name)
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        count = 0
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            for row in sheet.iter_rows(values_only=True):
                if not row or not any(row):
                    continue
                row_text_list = [str(cell).strip() for cell in row if cell is not None]
                full_line = " | ".join(row_text_list)
                if not full_line:
                    continue
                
                ho_ten_val = row_text_list[0] if len(row_text_list) > 0 else "Chưa rõ"

                cursor.execute(
                    '''INSERT INTO ho_so 
                       (ho_ten, ho_ten_khong_dau, thong_tin_chi_tiet, thong_tin_khong_dau, ten_file) 
                       VALUES (?, ?, ?, ?, ?)''',
                    (
                        ho_ten_val[:100], 
                        remove_accents(ho_ten_val[:100]), 
                        full_line, 
                        remove_accents(full_line), 
                        file_name
                    )
                )
                count += 1
                tong_so += 1
        print(f"Đã nạp file {file_name}: {count} dòng")
    except Exception as e:
        print(f"Lỗi file {file_name}: {e}")

# Cập nhật bảng thống kê mẫu
cursor.execute("SELECT COUNT(*) FROM ho_so")
total_records = cursor.fetchone()[0]

cursor.execute("INSERT OR REPLACE INTO thong_ke (loai_ho_so, so_luong) VALUES ('Cai bắt buộc', ?)", (total_records,))
cursor.execute("INSERT OR REPLACE INTO thong_ke (loai_ho_so, so_luong) VALUES ('Cai tự nguyện', 0)")
cursor.execute("INSERT OR REPLACE INTO thong_ke (loai_ho_so, so_luong) VALUES ('Chuyển án', 0)")

conn.commit()
conn.close()
print("✅ KHỞI TẠO DATABASE HOÀN TẤT!")
