# 🚗 Iran Car Scraper

اسکریپتی برای دانلود تصاویر ۱۲ مدل ماشین ایرانی از سایت دیوار.
برای هر مدل حداقل ۲۰۰ عکس دانلود میشود.

------

## 📁 ساختار پروژه
project/
├── car_image_downloader.py
├── augmentation.py
├── test_car_image_downloader.py
├── README.md
├── requirements.txt
└── dataset/
    ├── 206/
    ├── 207/
    ├── 405/
    └── ...

------

## ⚙️ پیش‌نیازها
- Python 3.10+
- Chrome browser

------

## 🚀 نصب و راه‌اندازی

git clone نام ریپازیتوری
cd repo-name

ساخت محیط مجازی:

python3 -m venv venv
source venv/bin/activate

در ویندوز:

venv\Scripts\activate

نصب dependencies:

pip install -r requirements.txt

اجرای اسکریپت:

python3 car_image_downloader.py

پس از اتمام، تصاویر در پوشه dataset ذخیره میشوند.

> **نکته:** اگر تعداد تصاویر یک مدل در دیوار کمتر از ۲۰۰ تا باشد، اسکریپت به صورت خودکار به مدل بعدی میرود.

------

## ✏️ تغییر تعداد عکس‌ها

برای تغییر تعداد عکس‌های هر مدل، در فایل `car_image_downloader.py` این خط را پیدا کنید:

while car_counter < 200:

و عدد ۲۰۰ را به تعداد دلخواه تغییر دهید.

------

## 🖼️ Data Augmentation

برای ساخت دیتاست augmented:

python3 augmentation.py

پس از اتمام، تصاویر در پوشه dataset_augmented ذخیره میشوند.

------

## 🧪 اجرای تست‌ها

pytest test_car_image_downloader.py -v

------

# ⚠️ نکته برای کاربران ویندوز

در فایل `car_image_downloader.py` این خط را پیدا کنید:

options.binary_location = "/usr/bin/chromium-browser"

و آن را به این تغییر دهید:

options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"