import requests
from lxml import etree
import re
import os
import pickle

class casService(object):
    def __init__(self,svr_session):
        self.cas_url = ""
        self.svr_session = svr_session  #service_session
        self.session = requests.session() #cas session
        # self.load_cascookies_from_file() #使用已有的cas-cookie(如果有的话)
        self.headers = {
                "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8",
                "Accept-Language": "zh_CN",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
            }
    def Login(self,serviceUrl = "",username = None,password = None):        
        response = self.svr_session.get(url=serviceUrl, headers = self.headers, allow_redirects=False)
        if response.status_code == 200:
            return True
        self.cas_url = response.headers["Location"]    
        cas_url = response.headers["Location"]
        cas_response = self.svr_session.get(cas_url, headers = self.headers, allow_redirects = False)
        if cas_response.status_code == 200:#登录界面
            if username == None or password == None:
                print("cas_cookie not valid")
                username = input("plase input username:")
                password = input("plase input password:")
            loginhtml = etree.HTML(cas_response.text)
            execution_value = loginhtml.xpath("//input[@name='execution']/@value")
            # lt_value = loginhtml.xpath("//div[@id='bottom']/input[@name='lt']/@value")
            auth_data =  {                
                "_eventId" : "submit",                
                "execution" : execution_value[0],
                "username" : username,
                "password" : password,                
                "loginType" : 1,
                "submit": "登  录"
            }
            auth_response = self.svr_session.post(self.cas_url,data = auth_data, headers = self.headers, allow_redirects = False)
            if auth_response.status_code == 302:
                url_with_ticket = auth_response.headers["Location"]
                confirm_response = self.session.get(url = url_with_ticket, headers = self.headers, allow_redirects = True)
                if confirm_response.status_code == 200:
                    print("logon on success")
                    # self.write_cascookies_to_file()
                    return requests.utils.dict_from_cookiejar(self.session.cookies)
                else:
                    print("logon on failed")
            else:
                print('auth failed')
                return False

    # def load_cascookies_from_file(self):
    #     if os.path.exists("cas_cookies.dat"):
    #         with open("cas_cookies.dat", 'rb') as f:
    #             self.session.cookies.update(pickle.load(f))
    # def write_cascookies_to_file(self):
    #     with open("cas_cookies.dat",'wb') as f:
    #         pickle.dump(self.session.cookies,f)        

