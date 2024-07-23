import base64
import sys

from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import argparse
import requests

from Utils.config import ConfigManager, write_plugin_data
from Utils.logger import log
from Utils.notify import send_notification, beat_once

config = ConfigManager().data_obj


# ChromeDriverManager().install()
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
browser = Chrome(options=option)


# browser = webdriver.Chrome()

def save_cookie():
    if not config.preference.auto_save_cookies:
        return
    config.account[0].cookies = str(base64.b64encode(json.dumps(browser.get_cookies()).encode('utf-8')), 'utf-8')
    write_plugin_data()


def loginUsePasswd():
    browser.get("https://www.tsdm39.com/member.php?mod=logging&action=login")
    browser.find_element('xpath', '//input[@name="username"]').send_keys(config.account[0].username)
    browser.find_element('xpath', '//input[@name="password"]').send_keys(config.account[0].passwd)
    sleep(1)
    count = 0
    while True:
        sleep(1)
        if browser.current_url.endswith('forum.php'):
            print("ss")
            break
        else:
            print("dnmd快验证")
        # try:
        #     # element1 = browser.find_element_by_xpath('//span[text()="动画"]')
        #     # element1 = browser.find_element_by_xpath('//a[text()="修改密码"]')
        # except NoSuchElementException as e:
        #     print("dnmd快验证")
        # else:
        #     print("ss")
        #     break
    browser.get("https://www.tsdm39.com/forum.php")
    save_cookie()


def loginUseCookie():
    browser.get("https://www.tsdm39.com/forum.php")
    browser.delete_all_cookies()
    cookies_list = json.loads(str(base64.b64decode(config.account[0].cookies), 'utf-8'))
    for cookie in cookies_list:
        browser.add_cookie(cookie)
    browser.refresh()
    save_cookie()


def sign_in(browser: WebDriver):
    browser.get("https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign")
    sleep(0.5)
    browser.execute_script('Icon_selected("kx")')
    sleep(0.2)
    browser.find_element("xpath", "//input[@type='radio' and @name='qdmode' and @value='3']").click()
    sleep(0.2)
    browser.find_element("xpath", "//img[contains(@src, 'qdtb.gif')]").click()
    sleep(3)


def ad_single_click(browser: WebDriver, element):
    browser.execute_script('jq.post("plugin.php?id=np_cliworkdz:work",{ act:"clickad"},function(data){});')
    # element.click()
    # time.sleep(1)
    # og, popup = browser.window_handles[0], browser.window_handles[1]
    # browser.switch_to.window(popup)
    # browser.close()
    # browser.switch_to.window(og)


def wads(browser: WebDriver):
    browser.get("https://www.tsdm39.com/plugin.php?id=np_cliworkdz:work")
    sleep(1)
    for i in browser.find_elements("xpath", "//*[starts-with(@id,'np_advid')]"):
        ad_single_click(browser, i)
        sleep(1.5)
    browser.execute_script('document.getcre.submit()')
    # browser.find_element("xpath", '//*[@id="stopad"]/a').click()
    sleep(3)


parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", help="Execute sign_in function")
parser.add_argument("-a", action="store_true", help="Execute wads function")
parser.add_argument("-p", action="store_true", help="Login use password")
args = parser.parse_args()

isExit = False
retry_time = 0

log.info("开始运行")

if args.p or config.preference.login_use_password or not config.account[0].cookies:
    loginUsePasswd()
else:
    loginUseCookie()

if args.s:
    sign_in(browser)
    send_notification("task finish", "Finish tsdm_signin")
    beat_once()
if args.a:
    wads(browser)
    send_notification("task finish", "Finish tsdm_wads")
    beat_once()

save_cookie()

browser.close()
sys.exit(0)
