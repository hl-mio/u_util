# -*- coding: utf-8 -*-
# @Time    : 2024-04-15
# @PreTime : 2022-01-07
# @Author  : hlmio
import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from u_工具 import *



class 谷歌WebDriver(webdriver.Chrome):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def __del__(self):
        try:
            self.quit()
        except: pass

    def set隐式等待时间(self, 等待时间_秒=15):
        self.implicitly_wait(等待时间_秒)  # 查找元素时，元素若在加载，最多等待这个时间
    def set分辨率(self,x=1280,y=720,是否全屏=False):
        if 是否全屏:
            self.最大化或最小化浏览器(True)
            return
        self.set_window_size(x,y)
    def 最大化或最小化浏览器(self, 是否最大化=True):
        if 是否最大化:
            self.maximize_window()
        else:
            self.minimize_window()
    def 切换到第几个窗口_从1开始(self, number, 后等待几秒=1):
        all_hand = self.window_handles
        self.switch_to.window(all_hand[int(number)-1])
        if 后等待几秒:
            delay_x_s(1)

    def 鼠标移动到指定位置(self, element: WebElement, x=None, y=None, hover多少秒=None):
        if x and y:
            ActionChains(self).move_by_offset(x, y).perform()
        else:
            ActionChains(self).move_to_element(element).perform()
        if hover多少秒:
            delay_x_s(hover多少秒)
    def 左键单击(self, element: WebElement, 模拟鼠标点击=True, x=None, y=None, hover多少秒才单击=1.2):
        if 模拟鼠标点击:
            鼠标移动到指定位置(self, element, x, y, hover多少秒才单击)
            ActionChains(self).click().perform()
        else:
            element.click()
    def 左键单击_by_css(self, css_str, hover多少秒才单击=1.2):
        element = self.find_element_by_css_selector(css_str)
        return self.左键单击(element, hover多少秒才单击=hover多少秒才单击)
    def 左键单击_by_xpath(self, xpath_str, hover多少秒才单击=1.2):
        element = self.find_element_by_xpath(xpath_str)
        return self.左键单击(element, hover多少秒才单击=hover多少秒才单击)

class 火狐WebDriver():
    driver = None #type: webdriver.Firefox

    def __init__(self, profile):
        self.driver = webdriver.Firefox(firefox_profile=profile)

    def __del__(self):
        try:
            self.driver.quit()
        except: pass

    def set隐式等待时间(self, 等待时间_秒=15):
        self.driver.implicitly_wait(等待时间_秒)  # 查找元素时，元素若在加载，最多等待这个时间
    def set分辨率(self,x=1280,y=720,是否全屏=False):
        if 是否全屏:
            self.driver.最大化或最小化浏览器(True)
            return
        self.driver.set_window_size(x,y)
    def 最大化或最小化浏览器(self, 是否最大化=True):
        if 是否最大化:
            self.driver.maximize_window()
        else:
            self.driver.minimize_window()
    def 切换到第几个窗口_从1开始(self, number, 后等待几秒=1):
        all_hand = self.driver.window_handles
        self.driver.switch_to.window(all_hand[int(number)-1])
        if 后等待几秒:
            delay_x_s(1)

    def 鼠标移动到指定位置(self, element: WebElement, x=None, y=None, hover多少秒=None):
        if x and y:
            ActionChains(self.driver).move_by_offset(x, y).perform()
        else:
            ActionChains(self.driver).move_to_element(element).perform()
        if hover多少秒:
            delay_x_s(hover多少秒)
    def 左键单击(self, element: WebElement, 模拟鼠标点击=True, x=None, y=None, hover多少秒才单击=1.2):
        if 模拟鼠标点击:
            鼠标移动到指定位置(self.driver, element, x, y, hover多少秒才单击)
            ActionChains(self.driver).click().perform()
        else:
            element.click()
    def 左键单击_by_css(self, css_str, hover多少秒才单击=1.2):
        element = self.driver.find_element_by_css_selector(css_str)
        return self.driver.左键单击(element, hover多少秒才单击=hover多少秒才单击)
    def 左键单击_by_xpath(self, xpath_str, hover多少秒才单击=1.2):
        element = self.driver.find_element_by_xpath(xpath_str)
        return self.driver.左键单击(element, hover多少秒才单击=hover多少秒才单击)

    #region 为了兼容
    def find_element_by_css_selector(self, css_str):
        return self.driver.find_element_by_css_selector(css_str)
    def find_element_by_xpath(self, xpath_str):
        return self.driver.find_element_by_xpath(xpath_str)
    def implicitly_wait(self, time_to_wait):
        return self.driver.implicitly_wait(time_to_wait)
    def get(self, url):
        return self.driver.get(url)
    def refresh(self):
        return self.driver.refresh()
    #endregion


# 1
def init_chrome(download_path=None, 隐式等待多少秒=None):
    options = webdriver.ChromeOptions()
    if download_path:
        mk(download_path)
        download_path = pwd(download_path)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_path}
        options.add_experimental_option('prefs', prefs)
    options.add_argument('-allow-running-insecure-content')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # driver = webdriver.Chrome(chrome_options=options)
    driver = 谷歌WebDriver(chrome_options=options)
    if 隐式等待多少秒:
        driver.implicitly_wait(隐式等待多少秒)
    return driver
def init_firefox(download_path=None, 隐式等待多少秒=None):
    profile = webdriver.FirefoxProfile()
    if download_path:
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", download_path)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference('browser.download.manager.focusWhenStarting', False)
    profile.set_preference('browser.download.manager.alertOnEXEOpen', False)
    profile.set_preference('browser.helperApps.alwaysAsk.force', False)

    文件类型 = "application/x-excel"
    profile.set_preference('browser.helperApps.neverAsk.openFile', 文件类型)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 文件类型)

    driver = 火狐WebDriver(profile)
    # driver = webdriver.Firefox(firefox_profile=profile)
    if 隐式等待多少秒:
        driver.set隐式等待时间(隐式等待多少秒)
        # driver.implicitly_wait(隐式等待多少秒)
    return driver


# 2
def 设置隐式等待时间(driver, 等待时间_秒=15):
    assert isinstance(driver, RemoteWebDriver)
    driver.implicitly_wait(等待时间_秒)  # 查找元素时，元素若在加载，最多等待这个时间
def 设置分辨率(driver,x=1280,y=720,是否全屏=False):
    if 是否全屏:
        最大化或最小化浏览器(driver,True)
        return
    driver.set_window_size(x,y)
def 最大化或最小化浏览器(driver, 是否最大化=True):
    if 是否最大化:
        driver.maximize_window()
    else:
        driver.minimize_window()
def 切换到第几个窗口_从1开始(driver, number, 后等待几秒=1):
    all_hand = driver.window_handles
    driver.switch_to.window(all_hand[int(number)-1])
    if 后等待几秒:
        delay_x_s(1)


# 3
def 鼠标移动到指定位置(driver, element :WebElement, x=None,y=None, hover多少秒=None):
    if x and y:
        ActionChains(driver).move_by_offset(x, y).perform()
    else:
        ActionChains(driver).move_to_element(element).perform()
    if hover多少秒:
        delay_x_s(hover多少秒)
def 左键单击(driver, element :WebElement, 模拟鼠标点击=True, x=None,y=None, hover多少秒才单击=1.2):
    if 模拟鼠标点击:
        鼠标移动到指定位置(driver, element, x,y ,hover多少秒才单击)
        ActionChains(driver).click().perform()
    else:
        element.click()
def 左键单击_by_css(driver, css_str, hover多少秒才单击=1.2):
    element = driver.find_element_by_css_selector(css_str)
    return 左键单击(driver, element, hover多少秒才单击=hover多少秒才单击)
def 左键单击_by_xpath(driver, xpath_str, hover多少秒才单击=1.2):
    element = driver.find_element_by_xpath(xpath_str)
    return 左键单击(driver, element, hover多少秒才单击=hover多少秒才单击)


# 其他
# 只允许文件夹内下载一个文件
def 等待下载完成(download_path, 预计有几个文件=1, 用来自动判断文件后缀的driver=None, timeout=60*30, 下载中文件的后缀=".crdownload", 等待间隔_秒=10, 几个计时点一组=3, 几组计时点换行=4):
    终点时间 = to_time_str(增加几分钟=timeout)
    driver = 用来自动判断文件后缀的driver
    if driver:
        if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
            下载中文件的后缀 = ".crdownload"
        if isinstance(driver, selenium.webdriver.firefox.webdriver.WebDriver):
            下载中文件的后缀 = ".part"

    计时点 = 计时点_生成器类(几个计时点一组, 几组计时点换行)
    print(f"// 一个点代表{等待间隔_秒}秒，一行{int(等待间隔_秒 * 几个计时点一组 * 几组计时点换行 / 60)}分钟")
    is_ok = False
    while not is_ok:
        if to_now_str() >= 终点时间:
            raise Exception("下载超时")

        delay_x_s(等待间隔_秒)
        print(next(计时点),end="")
        文件名数组 = ls(download_path)
        if len(文件名数组) == 0 or len(文件名数组) != 预计有几个文件:
            continue
        is_ok = True
        for 文件名 in 文件名数组:
            if 文件名.endswith(下载中文件的后缀):
                is_ok = False
                break
    print()
