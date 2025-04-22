import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from datetime import datetime

# Хук для создания скриншотов при неудачах тестов
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Сохранение скриншотов при неудачах тестов."""
    if call.when == 'call' and call.excinfo is not None:
        driver = item.funcargs.get('driver')
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join("screenshots", f"{item.nodeid.replace('::', '_')}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Скриншот сохранен: {screenshot_path}")

# Фикстура для инициализации WebDriver
@pytest.fixture(scope="function")
def driver():
    """Инициализация WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Без графического интерфейса (можно убрать, если нужно отображение)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    yield driver  # Передаем драйвер в тест

    # После теста закрываем браузер
    driver.quit()

# Фикстура для ожидания явных ожиданий, если нужно
@pytest.fixture
def wait(driver):
    """Возвращаем webdriver для использования в тестах с явными ожиданиями."""
    return driver
