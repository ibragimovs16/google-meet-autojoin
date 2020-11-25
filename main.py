from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options

from time import sleep

from datetime import datetime as dt

import json

""" Настройки браузера"""
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1
})


def import_settings() -> dict:
    """ Функция импортирования настроек """

    with open("settings.json", 'r+') as f:
        return json.load(f)


def meet_login(driver) -> None:
    """ Функция авторизации """

    driver.find_element_by_class_name("NPEfkd").click()

    for i in range(2):
        settings = import_settings()
        data = settings['login'] if i == 0 else settings['password']
        driver.find_element_by_class_name("whsOnd").send_keys(data)
        driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        sleep(1)

    sleep(5)


def disable_mic_and_cam(driver) -> None:
    """ Функция отключения микрофона и веб-камеры """

    settings = import_settings()
    if settings['DISABLE_MIC'] is True:
        driver.find_element_by_class_name("sUZ4id").click()
    if settings['DISABLE_CAM'] is True:
        driver.find_element_by_class_name("GOH7Zb").click()


def join(driver) -> None:
    """ Функция входа на встречу """

    try:
        meet_login(driver)
        disable_mic_and_cam(driver)

        sleep(1)

        driver.find_element_by_class_name("NPEfkd").click()
    except Exception:
        print("Неверно указаны данные для входа в settings.json или неверная ссылка в schedule.json")
        driver.close()


def main() -> None:
    """ Основная функция с планировщиком """

    print("Скрипт запущен.")

    with open("schedule.json", 'r+') as f:
        schedule = json.load(f)

    while True:
        for item in schedule:
            if item['start'][0] == dt.now().isoweekday():
                if item['start'][1] == dt.now().hour and item['start'][2] == dt.now().minute and dt.now().second == 0:
                    url = item['url']
                    end_time = item['end']

                    sleep(1)

                    print("Выполняется вход...")

                    driver = wd.Chrome(options=options)
                    driver.get(url)
                    join(driver)

                    while True:
                        if end_time[0] == dt.now().hour and end_time[1] == dt.now().minute and dt.now().second == 0:
                            driver.close()
                            print("Встреча законилась.")
                            break


if __name__ == '__main__':
    main()
