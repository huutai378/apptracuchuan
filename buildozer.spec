[app]
title = App Chuan Tra Cuu
package.name = appchantracuu
package.domain = org.tai
source.include_exts = py,png,jpg,kv,atlas,db
source.dir = .
source.include_patterns = assets/*,database.db,data_raw/*
icon.filename = %(source.dir)s/logo.png
version = 1.0
requirements = python3,kivy,sqlite3
orientation = portrait
android.permissions = INTERNET

# Cấu hình SDK/NDK tương thích
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
