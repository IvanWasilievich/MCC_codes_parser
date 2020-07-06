#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.insert(0,"../")

from config import ALCHEMY_ECHO_FLAG, SQL_ALCHEMY_URI
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, MetaData


engine = create_engine(SQL_ALCHEMY_URI, echo = ALCHEMY_ECHO_FLAG)
meta = MetaData()


all_mcc = Table(
   'all_mcc', meta, 
   Column('MCC', String, primary_key = True), 
   Column('mcc_group', String),
   Column('mcc_update_date', String)
)

mcc_description = Table(
   'mcc_desc', meta, 
   Column('MCC', String, primary_key = True), 
   Column('category_name_eng', String),
   Column('mcc_description', String),
   Column('amount_marketplacements', Integer)   
)

company_info = Table(
   'company_info', meta, 
   Column('id', String, primary_key = True), 
   Column('MCC', String), 
   Column('company_name', String),
   Column('company_code', String),
   Column('yandex_map', String),
   Column('last_update', String),
   Column('adress', String)
)







