#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.insert(0,"../")

from bs4 import BeautifulSoup
from utils.deques import codes_deque, start_codes_deque, pagination_urls_deque
from config import DATA_PATH, MAIN_PAGE_DATA_PATH, MCC_DATA_PATH, SEARCH_PAGE_DATA_PATH
from config import SHORT_SLEEP, LONG_SLEEP
from config import MAIN_URL, headers, MAX_RESULT_ON_SEARCH_PAGE

import requests
from time import sleep 

search_url_template = "https://mcc-codes.ru/search?extended=1&m={code}&sortBy=date&sortDir=desc&page={page_num}"
start_search_url_template = "https://mcc-codes.ru/search?extended=true&o=&m={code}&q=&c=&a="

def request_and_save_html(url, path):
    response = requests.get(url, headers=headers)
    html = response.text
    with open(path, "w", encoding='utf-8') as file:
        file.write(html)
    return html

def parse_code_pages(codes_deque):
    i = 0
    while codes_deque:
        code = codes_deque[0]
        request_and_save_html(url = MAIN_URL + f"/{code}", path= f"{MCC_DATA_PATH}\\{code}_page_html.txt")

        codes_deque.popleft() #удаляем код из очереди
        i+=1
        print(i, code) #принтуем итерацию
        sleep(SHORT_SLEEP if i%100 else LONG_SLEEP) #ставим задержку, и на каждой 100 итерации даем длинный таймаут

def parse_search_urls(start_codes_deque):
    i = 0
    while start_codes_deque:
        code, amount_marketplaces = start_codes_deque[0]
        url = start_search_url_template.format(code=code)
        start_page = 1

        search_page_html = request_and_save_html(url=url, path=SEARCH_PAGE_DATA_PATH + f"\\{code}_page_{start_page}_html.txt")
        start_codes_deque.popleft()
        print(i, url)
        sleep(SHORT_SLEEP)


        if amount_marketplaces > MAX_RESULT_ON_SEARCH_PAGE:    
            search_page_soup_obj = BeautifulSoup(search_page_html, "lxml")
            total_pages = int(search_page_soup_obj.find('ul', class_="pagination").find_all('li')[-2].a.text)

            #пишем урлы в очередь
            for page_num in range(1,total_pages+1):
                pagination_url = search_url_template.format(code=code, page_num=page_num)
                pagination_urls_deque.append((page_num, code, pagination_url))
            print(len(pagination_urls_deque))


            while pagination_urls_deque:
                page_num, code, pagination_url = pagination_urls_deque[0]

                request_and_save_html(url=pagination_url,path=SEARCH_PAGE_DATA_PATH + f"\\{code}_page_{page_num}_html.txt")

                pagination_urls_deque.popleft() #убираем из очереди pagination_url
                print(i,pagination_url)
                print(len(pagination_urls_deque))
                i+=1
                sleep(SHORT_SLEEP if i%100 else LONG_SLEEP)

        i+=1
        sleep(SHORT_SLEEP if i%100 else LONG_SLEEP)





