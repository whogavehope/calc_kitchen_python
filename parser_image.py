import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# === НАСТРОЙКИ ===
URL = "https://sidak.ru/catalog/complect/kuhni_sidak/"
OUTPUT_FOLDER = "images_sidak_full"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Заголовки для скачивания
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Запуск браузера (headless = без окна)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

print("🚀 Запускаем браузер...")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    print(f"🌐 Открываем {URL}")
    driver.get(URL)

    # Ждём появления хотя бы одной секции (например, заголовка)
    print("⏳ Ждём загрузки контента...")
    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Кухонные шкафы')]"))
        )
        print("✅ Контент частично загружен")
    except TimeoutException:
        print("⚠️ Заголовки не найдены — продолжаем без ожидания")

    # === КЛИКАЕМ ВСЕ КНОПКИ «Показать ещё» ===
    print("🖱️ Ищем и нажимаем все кнопки «Показать ещё»...")
    click_count = 0
    while True:
        try:
            # Ищем ВСЕ кнопки с текстом «Показать ещё» (может быть несколько на странице)
            buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Показать ещё')]")
            if not buttons:
                print("🔚 Кнопок «Показать ещё» больше нет")
                break

            # Кликаем по первой найденной кнопке
            btn = buttons[0]
            print(f"  → Нажимаю: {btn.text.strip()}")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", btn)
            click_count += 1

            # Ждём появления новых картинок (хотя бы +1 <img>)
            wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "img")) > 10)
            time.sleep(1)  # дать отрисоваться

        except (TimeoutException, NoSuchElementException) as e:
            print(f"⚠️ Остановка: {e}")
            break
        except Exception as e:
            print(f"❌ Ошибка при нажатии: {e}")
            break

    print(f"✅ Всего нажато кнопок: {click_count}")

    # === ПОЛУЧАЕМ ФИНАЛЬНЫЙ HTML ===
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Находим ВСЕ изображения
    img_tags = soup.find_all('img', src=True)
    print(f"🖼️ Найдено <img> тегов: {len(img_tags)}")

    # Скачиваем уникальные
    saved = 0
    seen = set()

    for i, img in enumerate(img_tags, 1):
        src = img.get('data-src') or img.get('src', '').strip()
        if not src:
            continue

        img_url = urljoin(URL, src)
        if img_url in seen:
            continue
        seen.add(img_url)

        # Фильтр: пропускаем data:image, svg, пиксели
        if any(x in img_url for x in ['data:image', 'blank', '1x1', 'spacer', '.svg']):
            continue

        # Имя файла
        name = os.path.basename(urlparse(img_url).path)
        if not name or '.' not in name:
            name = f"img_{i}.jpg"
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        path = os.path.join(OUTPUT_FOLDER, name)

        try:
            print(f"{len(seen):2}. {name}")
            res = requests.get(img_url, headers=headers, timeout=10)
            res.raise_for_status()
            with open(path, 'wb') as f:
                f.write(res.content)
            saved += 1
        except Exception as e:
            print(f"   ❌ {type(e).__name__}")

    print(f"\n🎉 Всего сохранено: {saved} изображений")
    print(f"📁 В папке: {os.path.abspath(OUTPUT_FOLDER)}")

finally:
    driver.quit()