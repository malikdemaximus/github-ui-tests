import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def test_github_search(driver):
    # Шаг 1: Открыть сайт GitHub
    driver.get("https://github.com/")

    # Шаг 2: Найти строку поиска и ввести запрос
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("selenium")  # Вводим запрос
    search_box.send_keys(Keys.RETURN)  # Нажимаем Enter для поиска

    # Шаг 3: Проверить, что результаты поиска появились
    time.sleep(2)
    assert "selenium" in driver.title.lower()

    # Шаг 4: Проверить, что на странице есть ссылки на репозитории
    repo_links = driver.find_elements(By.CSS_SELECTOR, "a.v-align-middle")
    assert len(repo_links) > 0, "Не найдено репозиториев в результатах поиска"

    # Шаг 5: Перейти по одному из репозиториев и проверить его заголовок
    repo_links[0].click()
    time.sleep(2)
    assert "selenium" in driver.title.lower()

    # Шаг 6: Проверить наличие кнопки 'Star' и 'Fork'
    star_button = driver.find_element(By.CSS_SELECTOR, ".btn-sm.btn-primary")
    fork_button = driver.find_element(By.CSS_SELECTOR, ".btn.sm.Btn")

    assert star_button.is_displayed(), "Кнопка 'Star' не найдена на странице"
    assert fork_button.is_displayed(), "Кнопка 'Fork' не найдена на странице"

    # Шаг 7: Проверка фильтра репозиториев
    filter_dropdown = driver.find_element(By.XPATH, '//summary[@aria-label="Type filter menu"]')
    filter_dropdown.click()
    time.sleep(1)
    assert driver.find_element(By.XPATH, "//button[text()='Repositories']").is_displayed()

    # Шаг 8: Прокрутка страницы вниз для проверки
    actions = ActionChains(driver)
    actions.move_to_element(repo_links[0]).perform()
    time.sleep(2)

    # Шаг 9: Подтверждение, что страница загрузилась корректно
    assert driver.find_element(By.XPATH, "//div[@class='repository-content']").is_displayed(), "Не удалось загрузить контент страницы"

    # Шаг 10: Закрыть браузер
    driver.quit()


def test_github_navigation(driver):
    # Шаг 1: Открыть сайт GitHub
    driver.get("https://github.com/")

    # Шаг 2: Перейти на страницу Sign Up
    sign_up_button = driver.find_element(By.LINK_TEXT, "Sign up")
    sign_up_button.click()

    # Шаг 3: Проверить, что мы на странице регистрации
    time.sleep(2)
    assert "Join GitHub" in driver.title

    # Шаг 4: Закрыть браузер
    driver.quit()


def test_github_footer_links(driver):
    # Шаг 1: Открыть сайт GitHub
    driver.get("https://github.com/")

    # Шаг 2: Проверить ссылки в подвале
    footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a")
    assert len(footer_links) > 0, "Нет ссылок в подвале страницы"
    for link in footer_links:
        assert link.is_displayed(), f"Ссылка {link.text} не отображается"

    # Шаг 3: Закрыть браузер
    driver.quit()
