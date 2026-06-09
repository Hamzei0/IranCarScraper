import pytest

from car_image_downloader import download_car_image, images_found


def test_empty_src():
    resurt = download_car_image(None, "206", 1)
    assert resurt == False


def test_data_src():
    result = download_car_image("data:image/png;base64,abc123", "206", 1)
    assert result == False


def test_double_img():
    src = "https://s100.divarcdn.com/static/photo/neda/webp_thumbnail/21SYtUmmrvBy09IpWCkLgQ/59e0198c-edb5-47ba-afc8-714ab41119d5.webp"

    images_found.clear()

    first_img = download_car_image(src, "206", 2)
    second_img = download_car_image(src, "206", 3)

    assert first_img == True
    assert second_img == False


def test_invalid_src():
    images_found.clear()
    result = download_car_image("https://invalid_url.com", "206", 1)
    assert result == False
