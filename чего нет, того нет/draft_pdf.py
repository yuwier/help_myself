import pandas as pd
import matplotlib.pyplot as plt
from weasyprint import HTML

# ====== настройки ======
REPORT_TYPE = "both"  # "table", "graph", "both"

# ====== тестовые данные ======
data = [
    {"patient": "Иванов", "service": "Анализ крови", "price": 100},
    {"patient": "Иванов", "service": "МРТ", "price": 500},
    {"patient": "Петров", "service": "Анализ крови", "price": 100},
    {"patient": "Сидоров", "service": "УЗИ", "price": 300},
]

df = pd.DataFrame(data)

# ====== агрегация ======
summary = df.groupby("patient")["price"].sum().reset_index()

# ====== CSV ======
df.to_csv("report.csv", index=False)

# ====== график ======
plt.figure()
summary.plot(kind="bar", x="patient", y="price", legend=False)
plt.title("Сумма по пациентам")
plt.savefig("chart.png")
plt.close()

# ====== HTML генерация ======
table_html = f"""
<h2>Таблица</h2>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Пациент</th><th>Сумма</th></tr>
{''.join(f"<tr><td>{row['patient']}</td><td>{row['price']}</td></tr>" for _, row in summary.iterrows())}
</table>
"""

graph_html = """
<h2>График</h2>
<img src="chart.png" width="500">
"""

# выбираем формат
if REPORT_TYPE == "table":
    content = table_html
elif REPORT_TYPE == "graph":
    content = graph_html
else:
    content = table_html + graph_html

# ====== финальный HTML ======
html = f"""
<h1>Счет страховой компании</h1>
<p>Период: 01.01.2024 - 31.01.2024</p>

{content}

<h3>Итого: {summary['price'].sum()}</h3>
"""

# ====== PDF ======
HTML(string=html).write_pdf("report.pdf")

print("Готово: report.pdf и report.csv")