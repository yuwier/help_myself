#  загрузка ------
class LabWindow(QDialog):
	def __init__(self):
		super().__init__()

		loader = QUiLoader()
		file = QFile('./app/login.ui')
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, self)
		file.close()


# пароль ------------
	def toggle_password(self):
		field = self.ui.passwordLineEdit

		if field.echoMode() == QLineEdit.Password:
			field.setEchoMode(QLineEdit.Normal)
		else:
			field.setEchoMode(QLineEdit.Password)


# капча ------------
def generate_captcha(self):
	image = ImageCaptcha()
	self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
	image.write(self.captcha_text, 'captcha.png')

	self.ui.captchaImageLabel.setPixmap(QPixmap('captcha.png'))
	self.ui.captchaUpdateButton.show()
	self.ui.captchaTextLabel.setText('Введите капчу')


# стили -------------


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(r'sources\logo.png'))
font = QFont('Comic Sans MS')
app.setFont(font)
app.setStyleSheet(
	"""
QWidget {
	background-color: white;
	font-family: 'Comic Sans MS';
	color: rgb(73, 140,81);
	font-size: 14px;
}

QPushButton {
	background-color: rgb(118, 227, 131);
	padding: 6px;
	border-radius: 6px;
}

QPushButton:pressed {
	background-color: rgb(73, 140,81);
}

QLabel {
	color: rgb(73, 140,81);
}
	"""
)
lab_window = LabWindow()
app.exec()

# выгрузка истории входа -------



# --- автоматический ввод

stmt = select(func.max(my_table.c.id))

self.next_id = get_last_tube_id() + 1
self.ui.tubeLineEdit.setPlaceholderText(str(self.next_id))
self.ui.tubeLineEdit.returnPressed.connect(self.handle_tube)


def handle_tube(self):
    text = self.ui.tubeLineEdit.text().strip()

    # если ничего не ввели → берём подсказку
    if text == "":
        tube_id = self.next_id
    else:
        if not text.isdigit():
            self.ui.errorLabel.setText("Введите число")
            return
        tube_id = int(text)



    # проверка на дубликат
    if tube_exists(tube_id):
        self.ui.errorLabel.setText("Такой номер уже есть")
        return

    self.ui.errorLabel.setText(f"Номер принят: {tube_id}")


# ------------------------------------------
# ------------------------------------------
# Заполнение из БД
def load_patients(self):
    self.ui.patientComboBox.clear()

    patients = get_all_patients()  # [(id, fio), ...]

    for p in patients:
        self.ui.patientComboBox.addItem(p[1], p[0])  # текст + id

    self.ui.patientComboBox.addItem("➕ Добавить пациента")
    
# Обработка выбора
self.ui.patientComboBox.currentIndexChanged.connect(self.handle_patient)
def handle_patient(self, index):
    text = self.ui.patientComboBox.currentText()

    if text == "➕ Добавить пациента":
        self.open_add_patient_dialog()
        

# ТАБЛИЦЫ ------------------------------
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlTableModel

class UsersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Users")
        self.resize(1000, 600)

        self.table = QTableView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        # PostgreSQL connection
        self.db = QSqlDatabase.addDatabase("QPSQL", "pg_users_conn")
        self.db.setHostName("127.0.0.1")
        self.db.setPort(5432)
        self.db.setDatabaseName("lab_db")
        self.db.setUserName("postgres")
        self.db.setPassword("your_password")

        if not self.db.open():
            raise RuntimeError(self.db.lastError().text())

        # Load table into QTableView
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("users")   # schema.table при необходимости: public.users
        self.model.select()

        self.table.setModel(self.model)
