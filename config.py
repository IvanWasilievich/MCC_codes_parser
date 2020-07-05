import random


DATA_PATH ='data'
MAIN_PAGE_DATA_PATH = DATA_PATH + '\mainpage_data'
MCC_DATA_PATH = DATA_PATH + '\mcc_codes_data'
SEARCH_PAGE_DATA_PATH = DATA_PATH + '\search_page_data'

MAIN_URL = 'https://mcc-codes.ru/code'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

MAX_RESULT_ON_SEARCH_PAGE = 20

SHORT_SLEEP = random.randint(1, 2)
LONG_SLEEP = random.randint(10, 15)

SQL_ALCHEMY_URI = 'sqlite:///test.db'
ALCHEMY_ECHO_FLAG = False

TEST_MODE = True
TEST_CODES = ["0742","0780","5999", "5912"]
