# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 12:52:12 2021

@author: chels
"""

from sqlalchemy import create_engine
import sqlalchemy

import pandas as pd

MYSQL_HOSTNAME = '40.117.148.146'
MYSQL_USER = 'DBA'
MYSQL_PASSWORD = 'ahi2021'
MYSQL_DATABASE = 'e2e'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)

print(engine.table_names())

csvfile = pd.read_csv('https://raw.githubusercontent.com/chelseatwan/datasets/main/H1N1_Flu_Vaccines.csv')
csvfile.to_sql('h1n1', con=engine, if_exists='append')