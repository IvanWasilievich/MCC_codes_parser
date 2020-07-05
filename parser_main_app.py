from collections import deque
from config import MAIN_PAGE_DATA_PATH, MCC_DATA_PATH, SEARCH_PAGE_DATA_PATH
from config import MAIN_URL
from config import TEST_MODE, TEST_CODES
from models.db import engine, meta
import os
from utils.deques import codes_deque, start_codes_deque
from utils.parsehtml import request_and_save_html, parse_code_pages, parse_search_urls
from utils.processinghtml import extract_and_save_db_main_page, extract_and_save_db_mcc_desc, extract_and_save_db_company_info

if __name__ == "__main__":
    if TEST_MODE:
        print("TEST MODE")
    meta.create_all(engine)
    print("db engine created")

    #запрос к общей таблице кодов, разбор, запись в базу, наполнение очереди codes_deque
    print("STAGE 1: parse all codes")
    request_and_save_html(url=MAIN_URL, path = MAIN_PAGE_DATA_PATH + "\main_page_html.txt")
    print("save to db all code...")
    extract_and_save_db_main_page()
    print("codes saved")

    #запрос к страницам кодов и разбор, запись в базу наполнение очереди start_codes_deque на парсинг
    print("STAGE 2: parse codes pages")
    print("parse codes pages...")
    if TEST_MODE:
        codes_deque = deque(TEST_CODES)
    parse_code_pages(codes_deque)
    print("save to db codes description...")
    code_page_files = os.listdir(MCC_DATA_PATH)
    for file_name in code_page_files:
        extract_and_save_db_mcc_desc(file_name)
    print("codes description saved")

    #запрос к страницам расщиренного поиска и пагинации, 
    #запись в базу данных о компаниях, использует промежуточную очередь pagination_urls_deque для хранения урлов из пагинации
    print("STAGE 3: parse companies")
    print("parse search pages...")
    parse_search_urls(start_codes_deque)
    print("save to db company info...")
    search_page_files = os.listdir(SEARCH_PAGE_DATA_PATH)
    for file_name in search_page_files:
        extract_and_save_db_company_info(file_name)
    print("company info saved")
    print("Fin!")