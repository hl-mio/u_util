import time

from u_工具 import delay_x_s, ls, 计时点_生成器类
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver



def 左键单击(driver, element :WebElement, 模拟鼠标点击=True, x=None,y=None, hover多少秒=1.2):
    if 模拟鼠标点击:
        鼠标移动到指定位置(driver, element, x,y ,hover多少秒)
        ActionChains(driver).click().perform()
    else:
        element.click()

def 鼠标移动到指定位置(driver, element :WebElement, x=None,y=None, hover多少秒=None):
    if x and y:
        ActionChains(driver).move_by_offset(x, y).perform()
    else:
        ActionChains(driver).move_to_element(element).perform()
    if hover多少秒:
        delay_x_s(hover多少秒)


# 只允许文件夹内下载一个文件
def 等待下载完成(download_path, 下载中文件的后缀=".part", 等待间隔_秒=10, 几个计时点一组=3, 几组计时点换行=4):
    计时点 = 计时点_生成器类(几个计时点一组, 几组计时点换行)
    print(f"# 一个点代表{等待间隔_秒}秒，一行{int(等待间隔_秒 * 几个计时点一组 * 几组计时点换行 / 60)}分钟")
    空文件夹次数 = 0
    is_ok = False
    while not is_ok:
        delay_x_s(等待间隔_秒)
        print(next(计时点),end="")
        文件名数组 = ls(download_path)
        if len(文件名数组) == 0:
            空文件夹次数+=1
            continue
        is_ok = True
        for 文件名 in 文件名数组:
            if 文件名.endswith(下载中文件的后缀):
                is_ok = False
                break
        if 空文件夹次数 > int(60/等待间隔_秒) * 10:
            raise Exception("空文件过久，疑似未触发下载")
    print()
    time.sleep(2)



# 切换浏览器窗口 number为第几个窗口 从0开始
def switchingWindow(browser, number):
    all_hand = browser.window_handles
    browser.switch_to.window(all_hand[number])
    time.sleep(1)


def 设置隐式等待时间(driver, 等待时间_秒=15):
    driver.implicitly_wait(等待时间_秒)  # 查找元素时，元素若在加载，最多等待这个时间


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
    profile.set_preference('general.useragent.override','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')

    driver = webdriver.Firefox(firefox_profile=profile)
    if 隐式等待多少秒:
        driver.implicitly_wait(隐式等待多少秒)
    return driver


def init_chrome(download_path=None, 隐式等待多少秒=None):
    options = webdriver.ChromeOptions()
    if download_path:
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_path}
        options.add_experimental_option('prefs', prefs)
    options.add_argument('-allow-running-insecure-content')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(chrome_options=options)
    if 隐式等待多少秒:
        driver.implicitly_wait(隐式等待多少秒)
    return driver
