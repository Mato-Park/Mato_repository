import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

# options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument('window-size=1020x1080')
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36')

browser = webdriver.Chrome()
browser.maximize_window()

url = 'http://www.naver.com/'
browser.get(url)

elem = browser.find_element_by_class_name('input_text')
elem.click()

# 1. 날씨
elem.send_keys('날씨')
elem.send_keys(Keys.ENTER)

soup = BeautifulSoup(browser.page_source, 'lxml')
weather = soup.find('div', attrs = {'class': 'weather_area _mainArea'})
weather_times = weather.find('ul', attrs = {'class': 'list_area'}).find_all('li')

curr_temp = weather.find('span', attrs = {'class': 'todaytemp'}).get_text()


print('='*5,'[오늘의 날씨]','='*5)
print('현재 기온: {}'.format(curr_temp + weather.find('span', attrs = {'class': 'tempmark'}).get_text()[2].strip()))
print('최저/최고 기온: {}'.format(weather.find('span', attrs = {'class': 'merge'}).get_text().strip()))
print('체감온도: {}'.format(weather.find('span', attrs = {'class': 'sensible'}).find('em').get_text()))
print(weather.find('span', attrs = {'class': 'rainfall'}).get_text().strip())
print('[시간대별 날씨]')
for w_time in weather_times:
    times = w_time.find('dd', attrs = {'class': 'item_time'}).get_text().strip()
    temp = w_time.find('dd', attrs = {'class': 'weather_item _dotWrapper'}).get_text().strip()[0:-1]
    rain = w_time.find('dd', attrs = {'class': 'item_condition'}).get_text().strip()
    print(f'시간: {times},', f'기온: {temp},', f'날씨: {rain}')

# 2. 헤드라인 뉴스
browser.get(url)
browser.find_element_by_class_name('link_news').click()

soup = BeautifulSoup(browser.page_source, 'lxml')

head_news = soup.find('div', attrs = {'class': 'hdline_flick_item'})
main_news = head_news.find('p', attrs = {'class': 'hdline_flick_tit'}).get_text()
news_list = soup.find('ul', attrs = {'class': 'hdline_article_list'}).find_all('li')

print('\n')
print('='*5,'[오늘의 메인 뉴스]','='*5)
print(main_news)
print('  (링크: https://news.naver.com/{})'.format(head_news.a['href']))

print('\n')
print('='*5,'[헤드라인 뉴스]','='*5)
for idx, news in enumerate(news_list):
    print(str(idx + 1)+'.', news.find('div', attrs = {'class': 'hdline_article_tit'}).get_text().strip())
    print('  (링크: https://news.naver.com/{})'.format(news.a['href']))

# url = browser.current_url
# browser.get(url)

category = soup.find('span', attrs = {'class': 'category_ranking'})
category_list = category.get_text().strip().split(' ')
class_list = ['pol', 'eco', 'soc', 'lif', 'wor', 'sci']


for idx, cate in enumerate(category_list):
    browser.find_element_by_xpath(f'//*[@id="right.ranking_tab_10{idx}"]').click()

    soup = BeautifulSoup(browser.page_source, 'lxml')
    news_list = soup.find('ul', attrs = {'class': 'section_list_ranking'}).find_all('li')

    print('\n')
    print('='*5,'[가장 많이 본 뉴스 - {}]'.format(category_list[idx]),'='*5)
    for idx2, news in enumerate(news_list):
        print(str(idx2 + 1)+'.', news.find('a', attrs = {'class': 'nclicks(rig.rank{})'.format(class_list[idx])}).get_text().strip())
        print('  (링크: https://news.naver.com/{}'.format(news.a['href']))


# 4. 채용공고 메일(잡코리아)
browser.get(url)
browser.find_element_by_xpath('//*[@id="account"]/a').click()
tag_id = browser.find_element_by_id('id')
tag_pw = browser.find_element_by_id('pw')

# 자동입력 방지 어떻게...
tag_id.click()
pyperclip.copy('*')
tag_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

tag_pw.click()
pyperclip.copy('*')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

browser.find_element_by_id('log.login').click()
time.sleep(1)

browser.find_element_by_class_name('nav').click()
time.sleep(1)

soup = BeautifulSoup(browser.page_source, 'lxml')

mail_list = soup.find('ol', attrs = {'class': 'mailList sender_context'}).find_all('div', attrs = {'class': 'subject'})

for idx, mail in enumerate(mail_list):
    mail_txt = mail.get_text()
    if '채용정보' not in mail_txt:
        continue
    else:
        xpath = browser.find_element_by_xpath('//*[@id="list_for_view"]/ol/li[{}]/div/div[2]/a[1]/span/strong'.format(idx+1))
        # //*[@id="list_for_view"]/ol/li[5]/div/div[2]/a[1]/span/strong: li[idx] 저기에 인덱스를 넣어줘서 처리하면 될듯 함
        break

xpath.click()
time.sleep(1)

soup = BeautifulSoup(browser.page_source, 'lxml')

job_list = soup.find_all('td', attrs = {'width': '578'})

print('='*30,'오늘의 채용정보','='*30, '\n')
for idx, job in enumerate(job_list):
    corporate = job.find('td', attrs={'width': '468'}).get_text().strip()
    due_date = job.find('td', attrs={'align': 'right', 'width': '110'}).get_text().strip()
    contents = job.find('td', attrs={'style': "font-family: '맑은 고딕'; font-size:20px; color:#333; line-height:30px; letter-spacing:-1px;"}).get_text().strip()
    subcontents = job.find('td', attrs={'height': '30','style': "font-family: '맑은 고딕'; font-size:16px; color:#666;"}).get_text().strip()


    print(str(idx + 1)+'.', corporate, "   '{}'".format(due_date))
    print('   ', contents, ' ({})'.format(subcontents))
    print('   (링크: {})'.format(job.a['href']),'\n')

# 5. 해외축구 기사(스포츠)
url = 'https://www.naver.com'
browser.get(url)

browser.find_element_by_xpath('//*[@id="NM_NEWSSTAND_HEADER"]/div[2]/a[3]').click()
browser.find_element_by_xpath('//*[@id="_sports_lnb_menu"]/div/ul[1]/li[5]/a').click()

soup = BeautifulSoup(browser.page_source, 'lxml')
sport_news = soup.find('ol', attrs = {'class': 'news_list'}).find_all('li')

print('='*30, '오늘의 해외축구 뉴스(Naver)', '='*30, '\n')
for idx, news in enumerate(sport_news):
    print(str(idx + 1)+'.', news.find('a', attrs = {'class': 'link_news_end'}).get_text().strip())
    print('  (링크: https://sports.news.naver.com{}'.format(news.a['href']))

browser.quit()

