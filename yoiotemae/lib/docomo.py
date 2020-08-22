from .sensor import Sensor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

class Docomo(Sensor):

  def __init__(self, arg):
    self.argnum = 2

    self.docomo_id = arg[0]
    self.docomo_pw = arg[1]

  def getLog(self, docomo_id, docomo_pw):

    # Selenium用オプション
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--headless")

    driver = webdriver.Chrome(options=op)
    driver.get('https://www.nttdocomo.co.jp/auth/cgi/mltdomanidlogin?rl=https%3A%2F%2Fwww.nttdocomo.co.jp%2Fmydocomo%2F')

    # ID入力
    id = driver.find_element_by_id("Di_Uid")
    id.send_keys(docomo_id)

    # 「次へ」クリック
    login_button = driver.find_element_by_name("subForm")
    login_button.click()

    time.sleep(7)
    #print(driver.page_source)

    # PW入力
    password = driver.find_element_by_id("Di_Pass")
    password.send_keys(docomo_pw)

    print(driver.page_source)

    # 「ログイン」クリック
    login_button = driver.find_element_by_name("subForm")
    login_button.click()

    # 通信量のページへ遷移
    driver.get("https://www.nttdocomo.co.jp/mydocomo/data/")

    time.sleep(7)

    ret = []
    total = 0;
    elements = driver.find_elements_by_class_name('data-list-inner')
    for ele in elements:
        tel = ele.find_element_by_class_name('mydcm_data_data-09')
        cost = ele.find_element_by_class_name('mydcm_data_data-10-1')
        total += float(cost.text)
        ret.append({"tel": tel.text,  'cost': cost.text})
    return total, ret

  def get(self):
    #if docomo_id is None:
    #    sys.exit(1)
    #if docomo_pw is None:
    #    sys.exit(1)

    total, mount = self.getLog(self.docomo_id, self.docomo_pw)
    return [total]

