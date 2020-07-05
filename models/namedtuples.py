from collections import namedtuple

MCC_code = namedtuple("MCC_code", 'id MCC mcc_name mcc_group mcc_update_date')
MCC_description = namedtuple("MCC_desccription", "id MCC category_name_eng mcc_description amount_marketplacements")
Company_info = namedtuple("Company_info", "id MCC company_name company_code yandex_map last_update adress")