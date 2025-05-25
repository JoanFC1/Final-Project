import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from functions import (
    human_delay, human_typing, random_mouse_movements,
    random_scrolls, random_pause_between_actions, wait_for_download
)

os.environ['PATH'] += r";C:/SeleniumDrivers"

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument(
    f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,115)}.0.{random.randint(4000,5000)}.100 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)
action = ActionChains(driver)

stealth_js = (
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    "window.navigator.chrome = { runtime: {} };"
    "Object.defineProperty(navigator, 'languages', {get: () => ['es-ES','es']});"
    "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});"
)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})

USER = os.getenv('SABI_USER', 'u1972741')
PASS = os.getenv('SABI_PASS', 'Jo@n2002')  # INSERTAR CONTRASEÑA SEGURA

try:
    driver.get('https://biblioapps.udg.edu/bases_dades_az.html')
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    time.sleep(human_delay())
    random_scrolls(driver)
    random_mouse_movements(action)
    random_pause_between_actions()

    link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='oa-sabiinforma']")))
    random_scrolls(driver)
    random_mouse_movements(action)
    link.click()
    time.sleep(human_delay())

    driver.switch_to.window(driver.window_handles[-1])
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    time.sleep(human_delay())
    random_scrolls(driver)
    random_mouse_movements(action)
    u_elem = wait.until(EC.visibility_of_element_located((By.ID, 'edit-name')))
    human_typing(u_elem, USER)
    time.sleep(human_delay())
    p_elem = driver.find_element(By.ID, 'edit-pass')
    human_typing(p_elem, PASS)
    time.sleep(human_delay())
    random_mouse_movements(action)
    p_elem.send_keys(Keys.RETURN)
    wait.until(lambda d: 'Shibboleth.sso' not in d.current_url)

    main_handle = driver.current_window_handle
    input("Presiona ENTER para iniciar las exportaciones...")

    total = 39682
    step = 50
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'sabi')
    for start in range(8401, total + 1, step):
        end_range = min(start + step - 1, total)
        random_pause_between_actions()
        random_scrolls(driver)
        random_mouse_movements(action)

        export_btn = wait.until(EC.element_to_be_clickable((
            By.ID,
            'm_ContentControl_ContentContainer1_ctl00_FixedContent_Headerbarreport1_ctl00_iconExport'
        )))
        random_scrolls(driver)
        random_mouse_movements(action)
        export_btn.click()
        time.sleep(human_delay())

        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.presence_of_element_located((By.ID, 'exportRange')))
        f1 = driver.find_element(By.NAME, 'RANGEFROM')
        random_mouse_movements(action)
        f1.click(); f1.clear(); human_typing(f1, str(start)); time.sleep(human_delay())
        f2 = driver.find_element(By.NAME, 'RANGETO')
        random_mouse_movements(action)
        f2.click(); f2.clear(); human_typing(f2, str(end_range)); time.sleep(human_delay())
        sep = driver.find_element(By.ID, 'chSeparatedFiles')
        random_mouse_movements(action); sep.click(); time.sleep(human_delay())
        confirm_btn = driver.find_element(By.ID, 'ctl00_ContentContainer1_ctl00_ButtonsContent_ExportOptionsBottomButtons_OkLabel')
        random_mouse_movements(action); confirm_btn.click()

        downloaded = wait_for_download(download_dir)
        if downloaded:
            print(f"Rango {start}-{end_range} descargado: {downloaded}")
            ci = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[src*="close_btn.gif"]')))
            random_scrolls(driver)
            random_mouse_movements(action)
            ci.click()
            print("Ventana cerrada.")
            driver.switch_to.window(main_handle)
        else:
            print(f"Falló descarga rango {start}-{end_range}")
            break

finally:
    driver.quit()
