from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions


# 定义webdriver打开窗口的大小的函数
# 选用开发者模式，创建一个浏览器对象，可避免被检测到是selenium模拟浏览器
option = ChromeOptions()
# 解决登录出现滑动验证的参数
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)
# driver.implicitly_wait(10)


def open_func(target_url: str) -> None:
    driver.get(target_url)
    driver.maximize_window()


def find_by_id(id: str) -> object:
    try:
        login_tag = driver.find_element_by_id(id)
        return login_tag
    except:
        return None


def find_by_xpath(xpath: str) -> object:
    try:
        xpath_tag = driver.find_element_by_xpath(xpath)
        return xpath_tag
    except:
        return None


def click_func(obj: object) -> None:
    try:
        obj.click()
    except Exception as e:
        print("点击按钮出错！")


def login(url: str, username: str, password: str, logined_user:str) -> None:
    """
    淘宝网站的登录。如果有安全验证，需要手工输入验证码。
    :param url 登陆地址
    :param username 用户名
    :param password 登陆密码
    :param logined_user 登陆成功后的用户名称
    """
    URLS = url
    open_func(URLS)
    login_tag = find_by_xpath('/html/body/div[1]/div[1]/div/ul[1]/li[2]/div[1]/div[1]/a[1]')
    # 点击登录
    login_tag.click()
    sleep(1)
    # 跳转到登录页面, 查找用户名、密码的登录
    find_by_id('fm-login-id').send_keys(username)
    find_by_id('fm-login-password').send_keys(password)
    sleep(1)
    # 点击登录
    login_btn = find_by_xpath('/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[4]/button')
    click_func(login_btn)
    sleep(1)
    # 判断登录以后是否需要账户安全验证
    is_Validator = find_by_id('otherValidator')
    if is_Validator:
        is_Validator.click()
        # sleep(1)
        driver.switch_to.frame(0)
        validator_button = find_by_xpath('//*[@id="content"]/div/ol/li[1]/a')
        click_func(validator_button)
        # 点击按钮获取验证码
        yzm_btn = find_by_xpath('//*[@id="J_GetCode"]')
        click_func(yzm_btn)
        # 停留20秒，手工输入验证码
        sleep(20)
        if find_by_xpath('//*[@id="submitBtn"]').is_displayed():
            validator_commit = find_by_xpath('//*[@id="submitBtn"]')
            click_func(validator_commit)
    # 点击淘宝图片，进入首页
    taobao = driver.find_element_by_css_selector('body > div.cup.J_Cup.search-fixed > div > div > div.tbh-logo.J_Module.tb-pass > div > h1 > a')
    click_func(taobao)
    # 查找登录名用户是否为对应的用户名,判断是否登陆成功
    handles_list = driver.window_handles
    driver.switch_to.window(handles_list[1])
    if logined_user in driver.page_source:
        print(True)
    else:
        print(False)

def buy_goods(kw: str, goodid: str, paywords: list) -> None:
    """
    购买商品
    :param kw 商品关键词
    :param goodid 目标商品id
    :param paywords 付款密码
    """
    # 输入搜索的商品
    find_by_id('q').send_keys(kw)
    # 确定搜索
    search_commit = find_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button')
    click_func(search_commit)
    sleep(1)
    # 获取对应的商品，通过id来定位
    book_list = find_by_id(goodid)
    click_func(book_list)
    # 下单-因为新开了窗口，需要将driver对象进行切换到新窗口进行操作
    all_handles = driver.window_handles
    driver.switch_to.window(all_handles[-1])
    sleep(1)
    # driver.switch_to.fream(handles_list[1])
    # 购买点击按钮
    J_LinkBuy = find_by_id('J_LinkBuy')
    click_func(J_LinkBuy)
    sleep(1)
    # 点击提交按钮
    buy_btn = driver.find_element_by_css_selector('#submitOrderPC_1 > div > a')
    click_func(buy_btn)
    sleep(3)

    # 获取付款密码的输入框
    pwd_info = driver.find_elements_by_css_selector('#payPassword_container > div > i')
    for i in range(len(pwd_info)):
        ActionChains(driver).click(pwd_info[i]).perform()
        find_by_xpath('//*[@id="payPassword_rsainput"]').send_keys(paywords[i])

    # 确认付款
    buy_submit = find_by_id('J_authSubmit')
    click_func(buy_submit)

if __name__ == "__main__":
    url = 'https://tb.alicdn.com/snapshot/index.html'
    user = 'XXXXXXX'
    password = 'xxxxxxx'
    logined_user = 'XXXXXXX'
    paywords = ['*', '*', '*', '*', '*', '*'] # * 代表支付密码
    kw = 'selenium书籍'
    goodid = 'J_Itemlist_TLink_599744663919'
    login(url, user, password, logined_user)
    buy_goods(kw, goodid, paywords)
    # 退出·
    driver.quit()
