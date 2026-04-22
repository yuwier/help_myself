import pandas as pd
from sqlalchemy import MetaData, Table, and_, exists, insert, literal_column, select


def load_file(engine, file_path, staging_table, file_type="csv"):
    """
    1) Прочитать CSV/XML
    2) Залить во временную таблицу staging_table
    """
    if file_type == "csv":
        df = pd.read_csv(file_path)
    elif file_type == "xml":
        df = pd.read_xml(file_path, xpath=".//record")
    else:
        raise ValueError("file_type must be 'csv' or 'xml'")

    df.columns = [c.lower().strip() for c in df.columns]
    df.to_sql(staging_table, engine, if_exists="replace", index=False, method="multi")


def move_rows(
    engine,
    source_table_name,
    target_table_name,
    col_map,
    unique_cols=None,
    where=None,
):
    """
    Перенос из source -> target.

    col_map: {"source_col": "target_col"}
    unique_cols: ["col1", "col2"] или None
    where: условие SQLAlchemy или None
    """
    meta = MetaData()
    src = Table(source_table_name, meta, autoload_with=engine)
    dst = Table(target_table_name, meta, autoload_with=engine)

    dst_cols = list(col_map.values())
    src_q = select(*[src.c[s].label(d) for s, d in col_map.items()])

    if where is not None:
        src_q = src_q.where(where)

    with engine.begin() as conn:
        if not unique_cols:
            stmt = insert(dst).from_select(dst_cols, src_q)
            return conn.execute(stmt)

        sq = src_q.distinct().subquery("sq")
        dup = and_(*[dst.c[c] == sq.c[c] for c in unique_cols])
        only_new = select(*[sq.c[c] for c in dst_cols]).where(
            ~exists(select(literal_column("1")).select_from(dst).where(dup))
        )
        stmt = insert(dst).from_select(dst_cols, only_new)
        return conn.execute(stmt)


# ---------------------------------------------------------
# ПРИМЕРЫ (копируйте и меняйте)
# ---------------------------------------------------------

# 1) services.csv -> services (только уникальные по code)
# load_file(engine, "assets/data/services.csv", "stg_services", file_type="csv")
# move_rows(
#     engine,
#     "stg_services",
#     "services",
#     {"code": "code", "service": "service", "price": "price"},
#     unique_cols=["code"],
# )

# 2) users.csv -> users (все строки)
# load_file(engine, "assets/data/users.csv", "stg_users", file_type="csv")
# move_rows(
#     engine,
#     "stg_users",
#     "users",
#     {
#         "id": "id",
#         "name": "name",
#         "login": "login",
#         "password": "password",
#         "ip": "ip",
#         "lastenter": "lastenter",
#         "services": "services",
#         "type": "type",
#     },
# )

# 3) blood.xml -> blood (все строки)
# load_file(engine, "assets/data/blood.xml", "stg_blood", file_type="xml")
# move_rows(
#     engine,
#     "stg_blood",
#     "blood",
#     {"id": "id", "patient": "patient", "barcode": "barcode", "date": "date"},
# )
