import os
import shutil
import sqlite3
import unicodedata
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_db = os.path.join(base_dir, 'database.db')
    asset_db = os.path.join(base_dir, 'assets', 'database.db')
    
    if os.path.exists(local_db):
        return local_db
    if os.path.exists(asset_db):
        return asset_db

    android_data = os.environ.get("ANDROID_DATA")
    if android_data:
        app_dir = os.path.join(android_data, "TraCuuApp")
        os.makedirs(app_dir, exist_ok=True)
        target_db = os.path.join(app_dir, 'database.db')
        
        if not os.path.exists(target_db) and os.path.exists(asset_db):
            shutil.copy2(asset_db, target_db)
        return target_db

    return local_db

def init_db_structure():
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tai_khoan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        
        cur.execute('''
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

        cur.execute('''
            CREATE TABLE IF NOT EXISTS ho_so (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ho_ten TEXT,
                ho_ten_khong_dau TEXT,
                thong_tin_chi_tiet TEXT,
                thong_tin_khong_dau TEXT,
                ten_file TEXT
            )
        ''')

        cur.execute("INSERT OR IGNORE INTO tai_khoan (username, password, role) VALUES ('admin', 'admin', 'admin')")
        cur.execute("INSERT OR IGNORE INTO tai_khoan (username, password, role) VALUES ('user', '123456', 'user')")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Lỗi khởi tạo DB: {e}")

def remove_accents(input_str):
    if not isinstance(input_str, str):
        input_str = str(input_str) if input_str is not None else ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D').lower().strip()

# Hàm chuẩn hóa hiển thị kết quả giống hệt hình ảnh minh họa
def format_result_line(index_stt, detail_str, file_src):
    if not detail_str:
        return f"[b]{index_stt}. Không có dữ liệu[/b]"
    
    parts = [p.strip() for p in str(detail_str).split('|') if p.strip()]
    
    stt_val = ""
    nam_val = ""
    ho_ten_val = ""
    nam_sinh_val = ""
    huyen_val = ""
    ghi_chu_val = ""

    # Trường hợp chuỗi có cấu trúc phân cách bởi dấu |
    if len(parts) >= 5:
        stt_val = parts[0]
        nam_val = parts[1]
        ho_ten_val = parts[2]
        nam_sinh_val = parts[3]
        huyen_val = parts[4]
        if len(parts) >= 6:
            ghi_chu_val = parts[5]
    elif len(parts) >= 3:
        ho_ten_val = parts[0]
        nam_sinh_val = parts[1]
        huyen_val = parts[2]
    else:
        ho_ten_val = detail_str

    # Dòng 1: STT. Họ và tên (Nguồn: ...)
    title_line = f"[b]{index_stt}. {ho_ten_val}[/b]"
    if file_src:
        title_line += f" [size=12sp][i](Nguồn: {file_src})[/i][/size]"

    # Dòng 2: Chi tiết thuộc tính
    detail_items = []
    if stt_val:
        detail_items.append(f"STT: {stt_val}")
    if nam_val:
        detail_items.append(f"Năm: {nam_val}")
    if ho_ten_val:
        detail_items.append(f"Họ và tên: {ho_ten_val}")
    if nam_sinh_val:
        detail_items.append(f"Năm sinh: {nam_sinh_val}")
    if huyen_val:
        detail_items.append(f"Huyện: {huyen_val}")
    if ghi_chu_val:
        detail_items.append(f"Ghi chú: {ghi_chu_val}")

    body_line = " | ".join(detail_items) if detail_items else detail_str
        
    return f"{title_line}\n{body_line}\n----------------------------------------"

KV = '''
<RootScreenManager>:
    LoginScreen:
        name: 'login'
    MainScreen:
        name: 'main'

<LoginScreen>:
    canvas.before:
        Color:
            rgba: 0.94, 0.95, 0.97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: ['24dp', '40dp', '24dp', '40dp']
        spacing: '16dp'

        Label:
            text: "HỆ THỐNG TRA CỨU HỒ SƠ"
            font_size: '20sp'
            bold: True
            color: 0.08, 0.25, 0.45, 1
            size_hint_y: None
            height: '40dp'

        Label:
            text: "ĐĂNG NHẬP"
            font_size: '16sp'
            bold: True
            color: 0.2, 0.2, 0.2, 1
            size_hint_y: None
            height: '30dp'

        TextInput:
            id: txt_user
            hint_text: "Tên đăng nhập"
            multiline: False
            font_size: '15sp'
            size_hint_y: None
            height: '46dp'
            padding: ['10dp', '12dp', '10dp', '8dp']

        TextInput:
            id: txt_pass
            hint_text: "Mật khẩu"
            password: True
            multiline: False
            font_size: '15sp'
            size_hint_y: None
            height: '46dp'
            padding: ['10dp', '12dp', '10dp', '8dp']

        Label:
            id: lbl_login_msg
            text: ""
            font_size: '13sp'
            color: 0.85, 0.25, 0.20, 1
            size_hint_y: None
            height: '24dp'

        Button:
            text: "ĐĂNG NHẬP"
            font_size: '16sp'
            bold: True
            size_hint_y: None
            height: '48dp'
            background_normal: ''
            background_color: 0.12, 0.53, 0.90, 1
            on_release: root.do_login()

        Widget:

<MainScreen>:
    canvas.before:
        Color:
            rgba: 0.94, 0.95, 0.97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        # Header
        BoxLayout:
            size_hint_y: None
            height: '52dp'
            padding: ['12dp', '0dp', '12dp', '0dp']
            canvas.before:
                Color:
                    rgba: 0.08, 0.25, 0.45, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "TRA CỨU HỒ SƠ"
                font_size: '17sp'
                bold: True
                color: 1, 1, 1, 1
                halign: 'left'
                text_size: self.size
                valign: 'middle'

            Button:
                id: btn_create_acc
                text: "TẠO TK"
                font_size: '12sp'
                bold: True
                size_hint: None, None
                size: '70dp', '36dp'
                pos_hint: {'center_y': 0.5}
                background_normal: ''
                background_color: 0.15, 0.68, 0.38, 1
                on_release: root.open_create_account_popup()

            Widget:
                size_hint_x: None
                width: '8dp'

            Button:
                text: "THOÁT"
                font_size: '12sp'
                bold: True
                size_hint: None, None
                size: '65dp', '36dp'
                pos_hint: {'center_y': 0.5}
                background_normal: ''
                background_color: 0.85, 0.25, 0.20, 1
                on_release: root.logout()

        # Vùng tra cứu
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '190dp'
            padding: ['12dp', '8dp', '12dp', '6dp']
            spacing: '8dp'

            TextInput:
                id: txt_search
                hint_text: "Nhập họ tên cần tra cứu..."
                font_size: '15sp'
                size_hint_y: None
                height: '46dp'
                multiline: False
                padding: ['10dp', '12dp', '10dp', '8dp']

            BoxLayout:
                size_hint_y: None
                height: '44dp'
                spacing: '8dp'

                TextInput:
                    id: txt_requester
                    hint_text: "Người yêu cầu (*)"
                    font_size: '14sp'
                    multiline: False
                    padding: ['8dp', '10dp', '8dp', '8dp']

                TextInput:
                    id: txt_note
                    hint_text: "Ghi chú (*)"
                    font_size: '14sp'
                    multiline: False
                    padding: ['8dp', '10dp', '8dp', '8dp']

            BoxLayout:
                size_hint_y: None
                height: '42dp'
                spacing: '8dp'

                Button:
                    text: "TÌM KIẾM"
                    font_size: '15sp'
                    bold: True
                    background_normal: ''
                    background_color: 0.12, 0.53, 0.90, 1
                    on_release: root.search_record()

                Button:
                    text: "XÓA NỘI DUNG"
                    font_size: '15sp'
                    bold: True
                    background_normal: ''
                    background_color: 0.85, 0.25, 0.20, 1
                    on_release: root.clear_search()

            Button:
                text: "XEM LỊCH SỬ TRA CỨU"
                font_size: '14sp'
                bold: True
                size_hint_y: None
                height: '38dp'
                background_normal: ''
                background_color: 0.55, 0.35, 0.75, 1
                on_release: root.show_history()

        # Kết quả tìm kiếm
        BoxLayout:
            orientation: 'vertical'
            padding: ['12dp', '2dp', '12dp', '6dp']
            
            Label:
                id: lbl_status
                text: "Sẵn sàng tra cứu."
                size_hint_y: None
                height: '24dp'
                font_size: '13sp'
                color: 0.3, 0.3, 0.3, 1
                halign: 'left'
                text_size: self.size
                markup: True

            ScrollView:
                do_scroll_x: False
                Label:
                    id: lbl_result
                    text: ""
                    font_size: '14sp'
                    color: 0.1, 0.1, 0.1, 1
                    size_hint_y: None
                    height: self.texture_size[1] + 20
                    text_size: self.width, None
                    markup: True

        # Thống kê
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '145dp'
            padding: ['12dp', '8dp', '12dp', '8dp']
            canvas.before:
                Color:
                    rgba: 0.88, 0.90, 0.94, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "[b]THỐNG KÊ HỒ SƠ PHÂN LOẠI[/b]"
                markup: True
                font_size: '14sp'
                size_hint_y: None
                height: '22dp'
                color: 0.1, 0.2, 0.3, 1

            Label:
                id: lbl_stats
                text: "Đang tải dữ liệu..."
                font_size: '13sp'
                color: 0.2, 0.2, 0.2, 1
                markup: True
                halign: 'left'
                valign: 'top'
                text_size: self.size
'''

class RootScreenManager(ScreenManager):
    pass

class LoginScreen(Screen):
    def do_login(self):
        user = self.ids.txt_user.text.strip()
        pwd = self.ids.txt_pass.text.strip()

        if not user or not pwd:
            self.ids.lbl_login_msg.text = "Vui lòng nhập đầy đủ Tài khoản & Mật khẩu!"
            return

        db_file = get_db_path()

        try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            cur.execute("SELECT role FROM tai_khoan WHERE username=? AND password=?", (user, pwd))
            row = cur.fetchone()
            conn.close()

            if row:
                role = row[0]
                main_screen = self.manager.get_screen('main')
                main_screen.logged_user = user
                main_screen.logged_role = role
                main_screen.setup_user_permissions()
                self.ids.lbl_login_msg.text = ""
                self.manager.current = 'main'
            else:
                self.ids.lbl_login_msg.text = "Tài khoản hoặc mật khẩu không chính xác!"
        except Exception as e:
            self.ids.lbl_login_msg.text = f"Lỗi đăng nhập: {e}"

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logged_user = ""
        self.logged_role = ""

    def setup_user_permissions(self):
        if self.logged_role == 'admin':
            self.ids.btn_create_acc.opacity = 1
            self.ids.btn_create_acc.disabled = False
        else:
            self.ids.btn_create_acc.opacity = 0
            self.ids.btn_create_acc.disabled = True

        self.ids.lbl_status.text = "Sẵn sàng tra cứu."
        self.load_statistics()

    def get_db(self):
        return sqlite3.connect(get_db_path())

    def load_statistics(self):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            
            # 1. Tổng toàn bộ
            cur.execute("SELECT COUNT(*) FROM ho_so")
            total_all = cur.fetchone()[0]

            # 2. Đếm Chuyển án (ghi chú / nội dung chứa từ 'chuyển án')
            cur.execute("SELECT COUNT(*) FROM ho_so WHERE LOWER(thong_tin_chi_tiet) LIKE '%chuyển án%' OR LOWER(thong_tin_chi_tiet) LIKE '%chuyen an%'")
            c_chuyen_an = cur.fetchone()[0]

            # 3. Đếm Cai tự nguyện (ghi chú chứa từ 'tự nguyện')
            cur.execute("SELECT COUNT(*) FROM ho_so WHERE LOWER(thong_tin_chi_tiet) LIKE '%tự nguyện%' OR LOWER(thong_tin_chi_tiet) LIKE '%tu nguyen%'")
            c_tu_nguyen = cur.fetchone()[0]

            # 4. Cai bắt buộc = Còn lại
            c_bat_buoc = max(0, total_all - c_chuyen_an - c_tu_nguyen)

            conn.close()

            lines = [
                f"• [b]Chuyển án[/b]: {c_chuyen_an:,} hồ sơ",
                f"• [b]Cai tự nguyện[/b]: {c_tu_nguyen:,} hồ sơ",
                f"• [b]Cai bắt buộc[/b]: {c_bat_buoc:,} hồ sơ",
                f"-> [b]TỔNG CỘNG: {total_all:,} hồ sơ[/b]"
            ]
            self.ids.lbl_stats.text = "\n".join(lines)
        except Exception as e:
            self.ids.lbl_stats.text = f"Lỗi đọc thống kê: {e}"

    def search_record(self):
        raw_keyword = self.ids.txt_search.text.strip()
        requester = self.ids.txt_requester.text.strip()
        note = self.ids.txt_note.text.strip()

        if not requester and not note:
            self.ids.lbl_status.text = "[color=#c0392b]Bạn cần nhập thêm Người yêu cầu hoặc ghi chú[/color]"
            return

        if not raw_keyword:
            self.ids.lbl_status.text = "Vui lòng nhập từ khóa/họ tên cần tra cứu!"
            return

        kw_kd = remove_accents(raw_keyword)
        
        try:
            conn = self.get_db()
            cur = conn.cursor()
            
            query = '''
                SELECT ho_ten, thong_tin_chi_tiet, ten_file 
                FROM ho_so 
                WHERE ho_ten_khong_dau LIKE ? 
                   OR ho_ten LIKE ? 
                   OR thong_tin_khong_dau LIKE ? 
                   OR thong_tin_chi_tiet LIKE ?
                LIMIT 100
            '''
            cur.execute(query, (f"%{kw_kd}%", f"%{raw_keyword}%", f"%{kw_kd}%", f"%{raw_keyword}%"))
            rows = cur.fetchall()

            count = len(rows)

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute('''
                INSERT INTO lich_su_tra_cuu (thoi_gian, user_tra_cuu, nguoi_yeu_cau, ghi_chu, tu_khoa, so_ket_qua)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (now_str, self.logged_user, requester, note, raw_keyword, count))
            conn.commit()
            conn.close()

            self.ids.lbl_status.text = f"Tìm thấy {count} kết quả cho '{raw_keyword}':"

            if count == 0:
                self.ids.lbl_result.text = "[color=#c0392b]Không tìm thấy hồ sơ phù hợp.[/color]"
            else:
                out = []
                for i, r in enumerate(rows, 1):
                    detail_str = r[1]
                    file_src = r[2] if r[2] else ""
                    card = format_result_line(i, detail_str, file_src)
                    out.append(card)
                self.ids.lbl_result.text = "\n\n".join(out)
        except Exception as e:
            self.ids.lbl_status.text = f"Lỗi truy vấn: {e}"

    def show_history(self):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            cur.execute("SELECT thoi_gian, user_tra_cuu, nguoi_yeu_cau, ghi_chu, tu_khoa, so_ket_qua FROM lich_su_tra_cuu ORDER BY id DESC LIMIT 50")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                self.ids.lbl_result.text = "Chưa có lịch sử tra cứu nào."
                return

            out = ["[b]=== LỊCH SỬ TRA CỨU (50 lượt gần nhất) ===[/b]\n"]
            for i, r in enumerate(rows, 1):
                out.append(
                    f"[b]{i}. [{r[0]}][/b] User: [color=#1F4E78]{r[1]}[/color] | Từ khóa: '{r[4]}' -> Kết quả: {r[5]}\n"
                    f"   • Người YC: {r[2]} | Ghi chú: {r[3]}"
                )
            self.ids.lbl_result.text = "\n\n".join(out)
            self.ids.lbl_status.text = f"Đã tải {len(rows)} lượt lịch sử."
        except Exception as e:
            self.ids.lbl_status.text = f"Lỗi tải lịch sử: {e}"

    def open_create_account_popup(self):
        content = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        txt_u = TextInput(hint_text="Tên đăng nhập mới", multiline=False, font_size='14sp', size_hint_y=None, height='40dp')
        txt_p = TextInput(hint_text="Mật khẩu", password=True, multiline=False, font_size='14sp', size_hint_y=None, height='40dp')
        lbl_msg = Label(text="", font_size='12sp', color=(1, 0, 0, 1), size_hint_y=None, height='20dp')
        btn_save = Button(text="TẠO TÀI KHOẢN", font_size='14sp', bold=True, size_hint_y=None, height='40dp', background_normal='', background_color=(0.15, 0.68, 0.38, 1))

        content.add_widget(txt_u)
        content.add_widget(txt_p)
        content.add_widget(lbl_msg)
        content.add_widget(btn_save)

        popup = Popup(title='TẠO TÀI KHOẢN USER MỚI', content=content, size_hint=(0.85, 0.45))

        def create_user(instance):
            u = txt_u.text.strip()
            p = txt_p.text.strip()
            if not u or not p:
                lbl_msg.text = "Vui lòng nhập tên và mật khẩu!"
                return
            try:
                conn = self.get_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO tai_khoan (username, password, role) VALUES (?, ?, 'user')", (u, p))
                conn.commit()
                conn.close()
                popup.dismiss()
                self.ids.lbl_status.text = f"[color=#27ae60]✔ Đã tạo thành công tài khoản User: {u}[/color]"
            except Exception as e:
                lbl_msg.text = f"Lỗi: Tên đăng nhập đã tồn tại!"

        btn_save.bind(on_release=create_user)
        popup.open()

    def clear_search(self):
        self.ids.txt_search.text = ""
        self.ids.txt_requester.text = ""
        self.ids.txt_note.text = ""
        self.ids.lbl_status.text = "Sẵn sàng tra cứu."
        self.ids.lbl_result.text = ""

    def logout(self):
        self.manager.get_screen('login').ids.txt_user.text = ""
        self.manager.get_screen('login').ids.txt_pass.text = ""
        self.manager.current = 'login'

class TraCuuApp(App):
    def build(self):
        init_db_structure()
        Builder.load_string(KV)
        sm = RootScreenManager()
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    TraCuuApp().run()
