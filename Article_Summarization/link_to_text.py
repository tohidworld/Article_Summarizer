from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def link_to_text(url):
    try:
        option = webdriver.ChromeOptions()
        #option.add_experimental_option("debuggerAddress","localhost:9222")
        '''user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        option.add_argument(f'user-agent={user_agent}')
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("--disable-blink-features=AutomationControlled")'''
        # for headless
        '''option.headless = True
        option.add_argument("--window-size=1004,708")
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--allow-running-insecure-content')
        option.add_argument("--disable-extensions")
        option.add_argument("--proxy-server='direct://'")
        option.add_argument("--proxy-bypass-list=*")
        option.add_argument("--start-maximized")
        option.add_argument('--disable-gpu')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--no-sandbox')'''
        #url = 'https://timesofindia.indiatimes.com/india/pm-modi-replies-to-motion-of-thanks-on-presidents-address-in-rajya-sabha/articleshow/89423079.cms'
        #r = requests.get(url, allow_redirects=True)
        #url = 'https://www.indiatoday.in/india/story/five-congress-mlas-announce-to-join-npp-nda-meghalaya-1910352-2022-02-08'
        wd = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        wd.get(url)
        htmlContent = wd.page_source
        wd.close
        soup = BeautifulSoup(htmlContent, 'html.parser')
        #print(soup)
        p = soup.find_all('p')
        title = soup.find('title').text.strip()
        #print(title)
        body = title
        for para in p:
            if len(para.text) >70:
                para = para.text.strip()
                #print(para)
                #(len(para.text))
                body = body + '\n' + para
        #print(text)
        body = str(body)
        status = 0
    except Exception as e:
        body = str(e)
        status = 1
    return status, body