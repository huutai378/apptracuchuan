[app]

# Tên ứng dụng hiển thị trên điện thoại
title = App Chuan Tra Cuu

# Tên package (viết thường, liền nhau)
package.name = appchantracuu

# Domain của bạn
package.domain = org.tai

# Các định dạng file cần đưa vào APK (đã bao gồm 'png' và 'db')
source.include_exts = py,png,jpg,kv,atlas,db

# Thư mục chứa mã nguồn
source.dir = .

# Các thư mục/file dữ liệu cần nhúng kèm
source.include_patterns = assets/*,database.db,data_raw/*

# Tên file logo chính xác của bạn trên GitHub
icon.filename = %(source.dir)s/logo.png

# Phiên bản ứng dụng
version = 1.0

# Các thư viện Python ứng dụng sử dụng
requirements = python3,kivy

# Màn hình hiển thị (portrait: dọc)
orientation = portrait

# Quyền truy cập Internet (nếu app cần)
android.permissions = INTERNET

# Cấu hình API Android mục tiêu
android.api = 33
android.minapi = 21
android.sdk = 20
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
