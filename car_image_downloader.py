import requests
import json
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EX

from selenium.webdriver.common.by import By

# تنظیمات مرورگر
options = Options()

# برای لینوکس
# options.binary_location = "/usr/bin/chromium-browser"

# برای ویندوز
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# اجرا بدون پنجره
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


# ست برای جلوگیری از دانلود عکس تکراری
images_found = set()


# لیست اطلاعات عکس‌ها برای ذخیره در فایل json
meta_data = []


def download_car_image(image_src, car_name, counter):

    # چک کردن معتبر بودن لینک
    if not image_src:
        return False
    if image_src.startswith("data:"):
        return False
    if image_src in images_found:
        return False

    images_found.add(image_src)

    try:
        response = requests.get(image_src, headers=headers, timeout=10)

        # ساخت اطلاعات عکس برای فایل json
        item = {
            "filename": f"img{counter}.jpg",
            "label": f"{car_name}",
            "path": f"dataset/{car_name}/img{counter}.jpg",
        }

        meta_data.append(item)
        # ذخیره عکس در پوشه مربوطه
        with open(f"dataset/{car_name}/img{counter}.jpg", "wb") as f:
            f.write(response.content)

        return True

    except requests.exceptions.Timeout:
        print("The website did not respond.")

    except requests.exceptions.ConnectionError:
        print("No internet connection.")

    except requests.exceptions.HTTPError as e:
        print(f"Website error: {e}")

    return False


# آدرس صفحه هر مدل ماشین در دیوار
car_urls = {
    "206": "https://divar.ir/s/tehran/car?q=206",
    "207": "https://divar.ir/s/tehran/car?q=207",
    "405": "https://divar.ir/s/tehran/car?q=405",
    "504": "https://divar.ir/s/tehran/classic-car?q=504",
    "Peride": "https://divar.ir/s/tehran/car?q=%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF",
    "Samand_LX": "https://divar.ir/s/tehran/car?q=%D8%B3%D9%85%D9%86%D8%AF%20lx",
    "Samand_Soren": "https://divar.ir/s/tehran/car?q=%D8%B3%D9%85%D9%86%D8%AF%20%D8%B3%D9%88%D8%B1%D9%86",
    "Tara": "https://divar.ir/s/tehran/car?q=%D8%AA%D8%A7%D8%B1%D8%A7",
    "Dena": "https://divar.ir/s/tehran/car?q=%D8%AF%D9%86%D8%A7",
    "Rana": "https://divar.ir/s/tehran/car?q=%D8%B1%D8%A7%D9%86%D8%A7",
    "206_SD": "https://divar.ir/s/tehran/car?q=206%20sd",
    "L90": "https://divar.ir/s/tehran/car?q=l%2090",
}

if __name__ == "__main__":

    print("starting download...", end="\n\n")

    for name, url in car_urls.items():

        # ساخت پوشه مدل ماشین
        os.makedirs(f"dataset/{name}", exist_ok=True)

        driver.get(url)
        car_counter = 0

        time.sleep(2)

        # صبر کن تا عکس‌ها لود بشن
        try:
            wait = WebDriverWait(driver, 15)
            wait.until(
                EX.presence_of_element_located((By.CLASS_NAME, "kt-image-block__image"))
            )
        except:
            print(f"{name}: Page did not load")
            continue

        # اسکرول و دانلود عکس‌ها تا رسیدن به تعداد مورد نظر
        while car_counter < 200:

            prev_count = car_counter

            try:
                images = driver.find_elements(By.CLASS_NAME, "kt-image-block__image")

                for img in images:
                    img_src = img.get_attribute("src")

                    if not img_src:
                        img_src = img.get_attribute("data-src")

                    if download_car_image(img_src, name, car_counter):
                        car_counter += 1
            except:
                continue

            # اسکرول به پایین صفحه برای لود عکس‌های بیشتر
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # اگه عکس جدیدی پیدا نشد از این مدل بیا بیرون
            if prev_count == car_counter:
                break

        print(f"{name}: {car_counter} images downloaded")
        print(f"Moving to next model...", end="\n\n")

    print(f"Done! {len(images_found)} images found")

    # ذخیره اطلاعات عکس‌ها در فایل json
    with open(f"metadata.json", "w") as f:
        json.dump(meta_data, f, indent=4, sort_keys=True)

    driver.quit()
