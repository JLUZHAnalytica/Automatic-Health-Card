from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def getWeb():
    '''配置web浏览器'''
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Galaxy S5"}
    capabilities = DesiredCapabilities.CHROME
    capabilities['loggingPrefs'] = {'browser': 'ALL'}
    # options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制desired_capabilities=capabilities,
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 更换头部
    options.add_argument(
        'user-agent=mozilla/5.0 (iphone; cpu iphone os 5_1_1 like mac os x) applewebkit/534.46 (khtml, like gecko) mobile/9b206 micromessenger/5.0')
    # 禁用图片
    # 禁止图片和css加载
    # "profile.managed_default_content_settings.images": 2,
    prefs = {'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)
    # #添加代理
    # ip,port = '127.0.0.1','8080'
    # options.add_argument(('--proxy-server=http://{}:{}'.format(ip,port)))#有的博客写的是'--proxy-server=http://'，就目前我的电脑来看的话需要把http://去掉就可以用，他会自己加的
    # options.add_argument('-headless')  # 无头参数
    # options.headless = True
    web = webdriver.Chrome(options=options)
    url = "https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/jkxxcj.jsp"
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    web.set_page_load_timeout(30)
    web.set_script_timeout(30)  # 这两种设置都进行才有效
    web.get(url)
    # web.add_cookie({'name': 'JSESSIONID','path': '/','value': cookies})
    return web


def get_cookie(username, password):
    web = getWeb()
    time.sleep(2)
    user = web.find_element_by_id("username")
    user.send_keys("{}".format(username))
    passwd = web.find_element_by_id("password")
    passwd.send_keys("{}".format(password))
    btn = web.find_element_by_id("passbutton")
    btn.click()
    time.sleep(2)
    print(web.get_cookies())
    cookie = web.get_cookies()[0]['value']
    web.quit()
    return cookie
