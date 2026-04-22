import pandas as pd
import json
import pandas as pd

def clean_patients():
	df = pd.read_xml('./assets/data/patients.xml', parser='lxml')

	name_parts = df['full_name'].str.split(expand=True)
	df['first_name'] = name_parts[0]
	df['last_name'] = name_parts[1]
	df['middle_name'] = ''

	df = df.drop(columns=['full_name'])
	df.to_xml('./assets/data/patients_cleaned.xml', parser='lxml', index=False)

# ------

def clean_users():
	df = pd.read_csv('./assets/data/users.csv', parser='csv')

	name_parts = df['name'].str.split(expand=True)
	df['first_name'] = name_parts[0]
	df['last_name'] = name_parts[1]
	df['middle_name'] = ''

	df = df.drop(columns=['name'])
	df.to_csv('./assets/data/users_cleaned.csv', parser='csv', index=False)

# -----

from sqlalchemy import insert, select


def ins_codes_users(conn, users_services):
	df = pd.read_csv("./assets/data/users.csv", usecols=["id", "services"])
	rows = []
	for user_id, raw_services in zip(df["id"], df["services"]):
		for item in json.loads(raw_services):
			rows.append(
				{
					"user_id": int(user_id),
					"service_code": int(item["code"]),
				}
			)

	# один execute на все строки (быстрее и проще)
	conn.execute(insert(users_services), rows)

def ins_accountants():
	pass

# -----

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



# -----
def col_to_date():
	df = pd.read_csv("./assets/data/users.csv")

	# Если формат MM/DD/YYYY (2/10/2020 = Feb 10, 2020)
	df["lastenter"] = pd.to_datetime(df["lastenter"], format=r"%m/%d/%Y").dt.date

	rows = df[["id", "login", "lastenter"]].to_dict(orient="records")
	conn.execute(insert(users), rows)  # users.c.lastenter должен быть Date


# -----
def stmts():
	stmt = insert(user_address).from_select([user_address.c.user_id, user_address.c.address_id], select(users.c.id, addresses.c.id).select_from(users.join(addresses, users.c.id == addresses.c.user_id)))

	stmt = insert(to_table).from_select([to_table.c.col1, to_table.c.col2], select(from_table1.c.col1, from_table2.c.col2).select_from(from_table1.join(from_table2, from_table1.c.id == from_table2.c.from_table1_id)))