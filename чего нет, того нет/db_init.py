from sqlalchemy import Column, Table, String, Integer, ForeignKey, MetaData
from sqlalchemy import create_engine, insert, select, update, delete, inspect
import pandas as pd
import lxml

DB_NAME = 'postgres'
DB_USERNAME = 'postgres'
DB_PASSWORD = '92votefu'
HOST = 'localhost'
PORT = '5432'

engine = create_engine(f'postgresql+psycopg2://{DB_NAME}:{DB_PASSWORD}@{HOST}:{PORT}')
metadata = MetaData()


def create_db():
	DB_NAME = 'TEST'
	stmt = f'CREATE DATABASE {DB_NAME}'
	with engine.connect() as conn:
		try:
			conn.execute(stmt)
			print('База данных создана')
		except:
			print('База данных уже существует')


engine = create_engine(f'postgresql+psycopg2://{DB_NAME}:{DB_PASSWORD}@{HOST}:{PORT}')

table1 = None 
table2 = None


def create_tables():
	is_tables_in_bd = inspect(engine).get_table_names()

	if is_tables_in_bd:
		table1 = Table('table1',
					metadata,
					Column('col1', Integer, primary_key=True),
					Column('col2', String))
		table2 = Table('table2',
					metadata,
					Column('col1', Integer, primary_key=True),
					Column('col3', Integer, ForeignKey('table1.col1')))
	
		metadata.create_all()


def import_data(data_path: str, table, data_type: str):
	if data_type == 'csv':
		df = pd.read_csv(data_path)
	if data_type == 'xml':
		df = pd.read_xml(data_path)

	data = df.to_dict(orient='records')

	with engine.connect() as conn:
		is_data_in_table = conn.execute(select(table).limit(1)).first()

		if not is_data_in_table:
			conn.execute(insert(table), data) 
			conn.commit()
