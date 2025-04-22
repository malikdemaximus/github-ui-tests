import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert


def test_github_login_page(driver):
    # Шаг 1: Открыть страницу входа в GitHub
    driver.get("https://github.com/login")

    # Шаг 2: Проверить, что форма входа отображается
    username_field = driver.find_element(By.ID, "login_field")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.NAME, "commit")

    assert username_field.is_displayed(), "Поле для имени пользователя не отображается"
    assert password_field.is_displayed(), "Поле для пароля не отображается"
    assert login_button.is_displayed(), "Кнопка входа не отображается"

    # Шаг 3: Попытаться войти с неправильным паролем
    username_field.send_keys("wrong_user")
    password_field.send_keys("wrong_password")
    login_button.click()

    time.sleep(2)  # Подождем немного, чтобы увидеть ошибку

    # Шаг 4: Проверка на наличие ошибки при неправильном логине
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash-error")
    assert error_message.is_displayed(), "Сообщение об ошибке при неправильном логине не отображается"

    # Шаг 5: Закрыть браузер
    driver.quit()


def test_github_profile_page(driver):
    # Шаг 1: Открыть страницу профиля (нужно быть залогиненным)
    driver.get("https://github.com/login")
    username_field = driver.find_element(By.ID, "login_field")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.NAME, "commit")
    
    username_field.send_keys("your_username")  # Введите свой логин
    password_field.send_keys("your_password")  # Введите свой пароль
    login_button.click()

    time.sleep(2)

    driver.get("https://github.com/your_username")  # Переходим на свою страницу профиля

    # Шаг 2: Проверка, что имя профиля отображается
    profile_name = driver.find_element(By.CSS_SELECTOR, ".p-name")
    assert profile_name.is_displayed(), "Имя профиля не отображается на странице"

    # Шаг 3: Проверка наличия репозиториев на странице профиля
    repos_section = driver.find_elements(By.CSS_SELECTOR, ".pinned-repositories .repo")
    assert len(repos_section) > 0, "Не отображаются репозитории в разделе 'Pinned Repositories'"

    # Шаг 4: Закрыть браузер
    driver.quit()


def test_github_logout(driver):
    # Шаг 1: Открыть страницу GitHub и войти в аккаунт
    driver.get("https://github.com/login")
    username_field = driver.find_element(By.ID, "login_field")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.NAME, "commit")
    
    username_field.send_keys("your_username")  # Введите свой логин
    password_field.send_keys("your_password")  # Введите свой пароль
    login_button.click()

    time.sleep(2)

    # Шаг 2: Ожидаем и нажимаем на кнопку "Sign out"
    profile_icon = driver.find_element(By.CSS_SELECTOR, ".avatar-user")
    profile_icon.click()
    time.sleep(1)
    logout_button = driver.find_element(By.CSS_SELECTOR, "button.dropdown-item.js-sign-out-button")
    logout_button.click()

    # Шаг 3: Проверить, что на странице снова есть кнопка "Sign up"
    time.sleep(2)
    assert driver.find_element(By.LINK_TEXT, "Sign up").is_displayed(), "После выхода не отображается кнопка 'Sign up'"

    # Шаг 4: Закрыть браузер
    driver.quit()
