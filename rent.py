import threading
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

clicked = False
exit_flag = False
amount = 1


def try_click(browser):
    global exit_flag, clicked, amount

    if exit_flag or clicked:
        return

    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[" + formatted_time + "] Se incearca subscribe-ul...... (Incercarea #" + amount.__str__() + ")")

    browser.get("https://maaslandrelocation.nl/en/studio/y8e52qej/grote-gracht-maastricht")

    loginSpan = browser.find_element(By.XPATH,
                                     "/html/body/div[1]/header/section[1]/nav/div/ul/li/a/span")

    actions = ActionChains(browser)

    if loginSpan.text.lower() == "log in":
        actions.move_to_element(loginSpan).click().perform()

        mail = browser.find_element(By.XPATH, "//input[@type='email']")
        mail.clear()
        mail.send_keys("alex.cioc2004@gmail.com")

        password = browser.find_element(By.XPATH, "//input[@type='password']")
        password.clear()
        password.send_keys("ILoveSwaG123")

        sign_in_button = browser.find_element(By.XPATH, "//button[@type='submit']")
        WebDriverWait(browser, 4).until(EC.element_to_be_clickable(sign_in_button))
        sign_in_button.click()

        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[" + formatted_time + "] S-a efectuat log in.")

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                '#main-content > main > div > aside > section > div > ul > li > div.actions.viewing-registration-button > button')))

        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#main-content > main > div > aside > section > div > ul > li > div.actions.viewing-registration-button > button')))



        if button.text.lower() != "unregister from digital viewing":
            browser.get_screenshot_as_file("ss.png")

            button.click()
            clicked = True

            formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + formatted_time + "] !!!!!!!!!!Am dat subscribe!!!!!!!!!!!.")
            exit_flag = True
            browser.quit()

        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + formatted_time + "] Butonul are alt text.")
            amount += 1

    except Exception:
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[" + formatted_time + "] Nu s-a gasit butonul.")
        amount += 1


def input_listener():
    global exit_flag
    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            print("Scraperul s-a oprit.")
            exit_flag = True
            break


def main():
    global clicked, exit_flag

    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # browser = webdriver.Chrome()

    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    print("Se incarca...")

    while True:
        if clicked or exit_flag:
            break
        try_click(browser)
        time.sleep(random.uniform(1, 3))


if __name__ == '__main__':
    main()
