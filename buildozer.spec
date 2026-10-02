[app]

# (str) Title of your application
title = Tra Cuu App

# (str) Package name
package.name = tracuuapp

# (str) Package domain (needed for android packaging)
package.domain = org.tracuu

# Thư mục chứa mã nguồn
source.dir = .

# Các định dạng file đi kèm
source.include_exts = py,png,jpg,kv,atlas,db

# Phiên bản ứng dụng
version = 1.0

# Các thư viện Python cần thiết
requirements = python3,kivy,cython==0.29.36

# Quyền truy cập mạng
android.permissions = INTERNET

# [QUAN TRỌNG] Sử dụng NDK r23b và API 31 để chống lỗi biên dịch phút chót
android.api = 31
android.minapi = 21
android.ndk = 23b
android.accept_sdk_license = True

# Chỉ định kiến trúc chip 64-bit phổ biến
android.archs = arm64-v8a

# Hướng màn hình ứng dụng
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin
