import requests
import random
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            https = tds[6].text.strip()
            if(https == 'yes'):
                host = f"{ip}:{port}"
                proxies.append(host)
        except IndexError:
            continue
    return proxies

def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxies)
    httpproxy = "http://" + proxy
    newProxies = {"http": httpproxy, "https": httpproxy}

    session.proxies.update(newProxies)
    return session

def getProxy():
    proxies = get_free_proxies()
    proxy = random.choice(proxies)
    httpproxy = "http://" + proxy
    newProxies = {"http": httpproxy, "https": httpproxy}

    return httpproxy

def getURL(url):
    getDone=False
    while (not getDone):
        proxies=get_free_proxies()
        s = get_session(proxies)
        try:
            strip = s.get(url)
            return strip
            getDone=True
        except Exception as e:
            print("Problem")
            continue

def getChromeDriver(url):
    getDone = False
    while (not getDone):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % getProxy())
            chrome_options.add_argument("--enable-javascript")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            getDone = True
        except Exception as e:
            print("Problem")
            continue

def getFirefoxDriver(url):
    myProxy = getProxy()
    print(myProxy)
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'httpsProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '' # set this value as desired
        })
    driver = webdriver.Firefox(proxy=proxy)
    driver.get(url)