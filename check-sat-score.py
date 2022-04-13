from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

def check_scores(config):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(10)

    try:
        print("Initializing...")

        driver.get("https://studentscores.collegeboard.org/viewscore")

        login = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div[3]/div/div/div[3]/div[1]/div[1]/div/div/div/a")
        login.click()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "idp-discovery-username")))

        username = driver.find_element(by=By.ID, value="idp-discovery-username")
        username.send_keys(config["username"])

        cont_button = driver.find_element(by=By.ID, value="idp-discovery-submit")
        cont_button.click()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "okta-signin-password")))

        print("Logging in....")

        passwd = driver.find_element(by=By.ID, value="okta-signin-password")
        passwd.send_keys(config["password"])

        cont_button = driver.find_element(by=By.ID, value="okta-signin-submit")
        cont_button.click()

        print("Looking up scores....")

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "score")))
        elements = driver.find_elements(by=By.CLASS_NAME, value="score")

        for el in elements:
            score = el.get_attribute('innerHTML')
            if int(score)>1000:
                print(f'Score: {score}')
            else:
                print(f' * {score}')
    finally:
        driver.quit()

def main():
    with open('student.json') as conf_file:
        config = json.load(conf_file)
    check_scores(config)

if __name__=='__main__':
    main()
