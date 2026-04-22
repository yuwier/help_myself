USERNAME = 'postgres'
PASSWORD = '92votefu'
DB_NAME = 'train'

from sqlalchemy import create_engine
from sqlalchemy import select, text
import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy import MetaData, String, Integer, Table, Column, ForeignKey, Boolean


def create_db(db_name):
	engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:5432/postgres")

	with engine.connect() as conn:
		try:
			conn.execution_options(isolation_level='AUTOCOMMIT')
			conn.execute(text(f'CREATE DATABASE {db_name}'))
			print(f'База данных {db_name} создана')
		except:
			print(f'База данных {db_name} уже существует')

create_db(DB_NAME)


engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:5432/{DB_NAME}")


metadata = MetaData()

users = Table('users',
			  metadata,
			  Column('id', Integer, primary_key=True),
			  Column('name', String))

addresses = Table('addresses',
				 metadata,
				 Column('id', Integer, primary_key=True),
				 Column('user_id', Integer, ForeignKey('users.id')),
				 Column('city', String))

user_address = Table('user_address',
				  metadata,
				  Column('id', Integer, primary_key=True),
				  Column('user_id', Integer, ForeignKey('users.id')),
				  Column('address_id', Integer, ForeignKey('addresses.id')))

metadata.drop_all(engine)
metadata.create_all(engine)
print('Таблицы созданы')


def import_in_table(file_path, table, engine, type):
	if type == 'csv':
		df = pd.read_csv(file_path)
	elif type == 'xml':
		df = pd.read_xml(file_path)
	else:
		print('Неверный тип файла')

	data = df.to_dict(orient='records')

	with engine.connect() as conn:
		result = conn.execute(select(table).limit(1))
		if result.first() is None:
			conn.execute(insert(table), data)
			conn.commit()
		else:
			print('Таблица', table, 'уже была заполнена ранее')

import_in_table('./sources/train_users.csv', users, engine, 'csv')
print('Произведен импорт users')
import_in_table('./sources/train_addresses.xml', addresses, engine, 'xml')
print('Произведен импорт addresses')


with engine.connect() as conn:
	result = conn.execute(select(users))
	print(result.mappings().all())
	result = conn.execute(select(addresses))
	print(result.mappings().all())


print('Попытка переноса столбцов из таблиц в другую')
with engine.begin() as conn:
	stmt = insert(user_address).from_select([user_address.c.user_id, user_address.c.address_id], select(users.c.id, addresses.c.id).select_from(users.join(addresses, users.c.id == addresses.c.user_id)))

	stmt = insert(to_table).from_select([to_table.c.col1, to_table.c.col2], select(from_table1.c.col1, from_table2.c.col2).select_from(from_table1.join(from_table2, from_table1.c.id == from_table2.c.from_table1_id)))

	conn.execute(stmt)

	stmt = select(addresses).where(addresses.c.user_id == 1)
	result = conn.execute(stmt)
	rows = result.fetchall()

	for row in rows:
		print(row)


def check_user(login: str, password: str):
	"""
	Проверяет пользователя. Существование логина в базе данных. Правильный ли пароль
	"""
	if (login != None) and (password != None):
		with engine.connect() as conn:
			try:
				login_stmt = select(users.c.id).where(users.c.name==login)
				result = conn.execute(login_stmt)
				user_id = result.first()[0]
			except:
				return 'Пользователя с таким логином не существует'

			password_stmt = select(addresses.c.city).where(addresses.c.user_id==user_id)
			result = conn.execute(password_stmt)
			user_password = result.first()[0]

		if password == user_password:
			return True
		else:
			return get_captcha()
		
def get_captcha():
	"""
	Запускаем капчу и пишем, что пароль неверный
	"""
	pass

def get_role(user_id):
	with engine.connect() as conn:
		stmt = select(users.c.id).where(users.c.name==user_id)
		result = conn.exec(stmt)
		role = result.first()[0]

		return role


# -