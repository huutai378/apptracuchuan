[app]

# Tên ứng dụng
title = App Chuan Tra Cuu

# Tên package (không dấu, viết thường, liền nhau)
package.name = appchantracuu

# Domain
package.domain = org.tai

# Các định dạng file đưa vào APK
source.include_exts = py,png,jpg,kv,atlas,db

# Thư mục mã nguồn
source.dir = .

# Các thư mục/file nhúng kèm quan trọng
source.include_patterns = assets/*,database.db,data_raw/*

# Tên file icon (logo)
icon.filename = %(source.dir)s/logo.png

# Phiên bản
version = 1.0

# Các thư viện Python bắt buộc
requirements = python3,kivy,sqlite3

# Màn hình hiển thị dọc
orientation = portrait

# Quyền ứng dụng
android.permissions = INTERNET

# Cấu hình SDK/NDK tương thích
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a

# Tự động chấp nhận bản quyền Android SDK để không bị lỗi
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
