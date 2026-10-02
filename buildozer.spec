[app]

# (str) Title of your application
title = Tra Cuu App

# (str) Package name
package.name = tracuuapp

# (str) Package domain (needed for android packaging)
package.domain = org.tracuu

# [QUAN TRỌNG] Thư mục chứa mã nguồn (dấu chấm nghĩa là thư mục hiện tại)
source.dir = .

# (list) Source files to include (thêm các định dạng file anh dùng)
source.include_exts = py,png,jpg,kv,atlas,db

# (list) Application requirements
requirements = python3,kivy,cython==0.29.36

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Supported orientations
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin
