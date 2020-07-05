#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0,"../")

import re
from bs4 import BeautifulSoup
from utils.deques import codes_deque, start_codes_deque
from config import MAIN_PAGE_DATA_PATH, MCC_DATA_PATH, DATA_PATH, SEARCH_PAGE_DATA_PATH

from models.db import engine, meta, all_mcc, mcc_description, company_info
from models.namedtuples import MCC_code, MCC_description, Company_info

def extract_and_save_db_main_page():
    """
    Читает файл с HTML страницы со всеми кодами,
    записывает в таблицу mcc_code данные, 
    наполняет очередь code_deque кодами для парсинга
    """
    with open(MAIN_PAGE_DATA_PATH + "\main_page_html.txt", "r", encoding='utf-8') as file:
        main_page_html = file.read()

    main_page_soup = BeautifulSoup(main_page_html, "lxml")
    main_page_soup.find("table", id_="all-mcc-table")
    table_rows = main_page_soup.find("table", id="all-mcc-table").tbody.find_all('tr')

    for table_row in table_rows:
        mcc_code = table_row.find("a").b.text
        mcc_name = table_row.find_all("td")[1].b.text
        mcc_group = table_row.find_all("td")[2].text if table_row.find_all("td")[2].text else None
        mcc_update_date = table_row.find_all("td")[-1].text
        current_code = MCC_code(None, mcc_code, mcc_name, mcc_group, mcc_update_date)
        engine.execute(all_mcc.insert().values(current_code))
        codes_deque.append(mcc_code)

def extract_and_save_db_mcc_desc(file_name):
    """
    Очищает данные со страниц кодов.
    Принимает на вход имя файла с HTML,
    записывает в базу описания кодов и количество торговых точек,
    наполняет очередь start_codes_deque, для дальнейшего парсинга компаний

    """
    with open(f"{MCC_DATA_PATH}\\{file_name}", "r", encoding='utf-8') as file:
        mcc_html = file.read()
        
    mcc_soup_obj = BeautifulSoup(mcc_html, "lxml")
    
    mcc_desc = (mcc_soup_obj
                       .find("p", class_="mb-3")
                       .text.replace("\n", " ")
                       .replace("Описание: ", " ")
                       .strip() 
                       if mcc_soup_obj.find("p", class_="mb-3") else None
                      )                            
    amount_marketplacements = int(re.findall("\d+", 
                                             mcc_soup_obj
                                             .find("div", id="navbarCard")
                                             .find("a", href="#points")
                                             .text)[0]
                                 )
    
    category_name_eng = (mcc_soup_obj.find("div", class_= "h5 text-primary mb-3").text 
                         if mcc_soup_obj.find("div", class_= "h5 text-primary mb-3") else None)
    
    if amount_marketplacements:
        start_codes_deque.append((file_name.strip('_page_html.txt'), amount_marketplacements))
    
    current_mcc = MCC_description(None, file_name.strip('_page_html.txt'), 
                                           category_name_eng,
                                           mcc_desc,
                                           amount_marketplacements
                                          )
    
    engine.execute(mcc_description.insert().values(current_mcc))

def extract_and_save_db_company_info(file_name):
    """
    Парсинг данных о компаниях,
    принимает на вход файл,
    записывает данные в таблицу company_info
    """
    with open(SEARCH_PAGE_DATA_PATH + f"\\{file_name}", "r", encoding='utf-8') as file:
        search_data_html = file.read()
    search_soup_odj = BeautifulSoup(search_data_html, "lxml")
    table_rows = search_soup_odj.find("div", class_="table-responsive").tbody.find_all("tr")
    
    for row in table_rows:
        company_name = row.b.text
        company_code = row.find("span", class_ = "text-uppercase text-muted d-none d-md-inline noSmartLink").text if \
                                         row.find("span", class_ = "text-uppercase text-muted d-none d-md-inline noSmartLink") else None
        yandex_map_href = row.find("a", class_="search-map")['href'] if row.find("a", class_="search-map") else None
        last_update = row.find_all("td")[-1].text
        adress = row.find("span", class_="mlink").text
        
        current_company = Company_info(None, file_name.split("_")[0], 
                                       company_name, company_code, 
                                       yandex_map_href, 
                                       last_update, 
                                       adress)
        engine.execute(company_info.insert().values(current_company))
            
        
       




