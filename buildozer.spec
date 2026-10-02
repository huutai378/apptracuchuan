[app]

# (str) Title of your application
title = Tra Cuu App

# (str) Package name
package.name = tracuuapp

# (str) Package domain (needed for android packaging)
package.domain = org.tracuu

# (list) Source files to include (let it include python files, kv files, images, and database if you use one)
source.include_exts = py,png,jpg,kv,atlas,db

# (list) Source files to exclude (optional)
source.exclude_exts = spec

# (list) List of directory to exclude (optional)
source.exclude_dirs = tests, bin, .git, .github

# (list) List of inclusions
# source.include_patterns = assets/*, images/*.png

# (str) Application versioning
version = 0.1

# (list) Application requirements
# [QUAN TRỌNG] Giữ danh sách gọn gàng để tránh lỗi biên dịch C/C++
requirements = python3,kivy,cython==0.29.36

# (str) Custom source folders for requirements
#requirements.source.kivy = ../../../kivy

# (list) Permissions
android.permissions = INTERNET

# (list) Features
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
# android.sdk = 20

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) Use adb to push files and debug
android.debug_gable = False

# (str) Supported orientations
orientation = portrait

# (list) The orientation to support
# supported.orientations = landscape,portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
# android.presplash_color = #FFFFFF

# (list) List of services to declare
# android.services = 

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1

# (str) Path to build artifact, storage, the root of buildozer
bin_dir = ./bin

# (str) Path to build output (default is .buildozer)
# build_dir = .build_dir

# (str) Output path for android build
# android.output_dir = .
