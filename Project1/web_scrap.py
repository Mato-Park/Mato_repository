import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import csv
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
browser.maximize_window()

url = 'https://www.youtube.com/channel/UCn9mJ4htO64-1osMWYu9k5Q'
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'lxml')

browser.find_element_by_xpath('//*[@id="tabsContent"]/paper-tab[2]/div').click()

# soup = BeautifulSoup(browser.page_source, 'lxml')
# a = soup.find('div', attrs = {'class': 'ytp-ad-player-overlay-instream-info'}) # 광고가 뜨는 경우 이걸로 체크
#
# if a:
#     print('commercial')
#     time.sleep(7)
#     browser.find_element_by_class_name('ytp-ad-skip-button-container').click()
# else:
#     print('none')
#
# soup = BeautifulSoup(browser.page_source, 'lxml')
#
# vid_time = soup.find('span', attrs = {'class': 'ytp-time-duration'}).get_text()
# hash = soup.find('yt-formatted-string', attrs = {'class': 'super-title style-scope ytd-video-primary-info-renderer'}).get_text()
# title = soup.find('yt-formatted-string', attrs = {'class': 'style-scope ytd-video-primary-info-renderer'}).get_text()
# show_cnt = soup.find('span', attrs = {'class': 'view-count style-scope yt-view-count-renderer'}).get_text()
# upload_date = soup.find('div', attrs = {'id': 'date', 'class': 'style-scope ytd-video-primary-info-renderer'}).get_text()[1:]
# like_cnt = soup.find('yt-formatted-string', attrs = {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})['aria-label']
# dislike_cnt = soup.find_all('yt-formatted-string', attrs = {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})[1]['aria-label']
# comments_cnt =  soup.find('yt-formatted-string', attrs = {'class': 'count-text style-scope ytd-comments-header-renderer'}).get_text()
#
#
# browser.find_element_by_css_selector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button').click()

filename = '이스타TV.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)

col_title = '제목 비디오시간 해쉬태그 조회수 업로드날짜 좋아요수 싫어요수 댓글수'.split(' ')
writer.writerow(col_title)
f.close()

i = 1
while i < 10:
    time.sleep(2)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    a = soup.find('div', attrs={'class': 'ytp-ad-player-overlay-instream-info'})  # 광고가 뜨는 경우 이걸로 체크

    try:
        if a:
            time.sleep(6)
            browser.find_element_by_class_name('ytp-ad-skip-button-container').click()
    except NoSuchElementException as e:
        print(e)


    browser.execute_script('window.scrollTo(0, 400)')
    time.sleep(0.5)

    soup = BeautifulSoup(browser.page_source, 'lxml')

    vid_time = soup.find('span', attrs={'class': 'ytp-time-duration'}).get_text()
    hash = soup.find('yt-formatted-string',
                     attrs={'class': 'super-title style-scope ytd-video-primary-info-renderer'}).get_text()
    title = soup.find('yt-formatted-string', attrs={'class': 'style-scope ytd-video-primary-info-renderer'}).get_text()
    show_cnt = soup.find('span', attrs={'class': 'view-count style-scope yt-view-count-renderer'}).get_text()
    upload_date = soup.find('div',
                            attrs={'id': 'date', 'class': 'style-scope ytd-video-primary-info-renderer'}).get_text()[1:]
    like_cnt = soup.find('yt-formatted-string',
                         attrs={'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})[
        'aria-label']
    dislike_cnt = soup.find_all('yt-formatted-string',
                                attrs={'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text'})[1][
        'aria-label']
    comments_cnt = soup.find('yt-formatted-string', attrs={'class': 'count-text style-scope ytd-comments-header-renderer'}).get_text()
    b = browser.find_element_by_css_selector(
        '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button')

    f = open(filename, 'a', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)

    row = [title, vid_time, hash, show_cnt, upload_date, like_cnt, dislike_cnt, comments_cnt]
    writer.writerow(row)
    f.close()

    b.click()

    # if b:
    #     b.click()
    # else:
    #     break

    i += 1






