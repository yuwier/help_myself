# У нас есть объекты:
# loginLineEdit
# passwordLineEdit
# loginButton
# togglePasswordButton
# errorLabel
import sys
import os

from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QSizePolicy
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer

from captcha.image import ImageCaptcha
from PySide6.QtGui import QPixmap, QIcon, QFont
import random 
import string

from db.connect import check_user, get_role

USER_ID = 0

class LabWindow(QDialog):
	def __init__(self):
		super().__init__()

# ------ Загрузка --------
		loader = QUiLoader()
		file = QFile('./app/login.ui')
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, self)
		file.close()

		self.timer = QTimer()

		self.ui.setWindowIcon(QIcon(r'sources\logo.png'))
		self.ui.setWindowTitle('Авторизация')

		self.ui.setMinimumSize(600, 400)
		self.ui.resize(900, 600)


# ------ Окно авторизации --------
		self.failed_attempts = 0
		self.ui.captchaImageLabel.hide()
		self.ui.captchaLineEdit.hide()
		self.ui.captchaTextLabel.hide()
		self.ui.captchaUpdateButton.hide()
		self.captcha_text = ''

		self.ui.stackedWidget.setCurrentIndex(0)

		self.ui.loginButton.clicked.connect(self.login)
		self.ui.togglePasswordButton.clicked.connect(self.toggle_password)
		self.ui.captchaImageLabel.setScaledContents(True)
		self.ui.captchaUpdateButton.clicked.connect(self.generate_captcha)



		self.login_status = False

		self.ui.show()

# ------ Окно админа --------
# ------ Окно лаборанта --------
# ------ Окно лаборанта-исследователя --------
# ------ Окно бухгалтера --------

# ------ Окно авторизации --------
	def toggle_password(self):
		field = self.ui.passwordLineEdit

		if field.echoMode() == QLineEdit.Password:
			field.setEchoMode(QLineEdit.Normal)
		else:
			field.setEchoMode(QLineEdit.Password)

	def block_login(self):
		self.ui.loginButton.setEnabled(False)
		QTimer.singleShot(10, lambda: self.ui.loginButton.setEnabled(True))

	def login(self):
		login = self.ui.loginLineEdit.text()
		password = self.ui.passwordLineEdit.text()

		if self.failed_attempts >= 1:
			if self.ui.captchaLineEdit.text() != self.captcha_text:
				self.ui.errorLabel.setText('Неверный ввод капчи. Продолжите через 10 секунд')
				self.block_login()
				self.generate_captcha()
				return

		result = check_user(login, password)

		if result == True:
			self.ui.errorLabel.setText('Успешный вход')
			self.login_status = True
			global USER_ID
			USER_ID = login
			self.ui.stackedWidget.setCurrentIndex(get_role(USER_ID))
		else:
			self.ui.errorLabel.setText(result)
			self.failed_attempts += 1
			
			if self.failed_attempts == 1:
				self.ui.captchaImageLabel.show()
				self.ui.captchaLineEdit.show()
				self.generate_captcha()

	def generate_captcha(self):
		image = ImageCaptcha()
		self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
		image.write(self.captcha_text, 'captcha.png')

		self.ui.captchaImageLabel.setPixmap(QPixmap('captcha.png'))
		self.ui.captchaUpdateButton.show()
		self.ui.captchaTextLabel.setText('Введите капчу')


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

print(USER_ID)


# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

def toggle_password(self):
    field = self.ui.passwordLineEdit

    if field.echoMode() == field.Password:
        field.setEchoMode(field.Normal)
    else:
        field.setEchoMode(field.Password)


def generate_captcha(self):
    image = ImageCaptcha()

    self.captcha_text = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=4)
    )

    image.write(self.captcha_text, "captcha.png")

    self.ui.captchaImageLabel.setPixmap(QPixmap("captcha.png"))



def login(self):
    login = self.ui.loginLineEdit.text()
    password = self.ui.passwordLineEdit.text()

    # если уже есть капча — проверяем
    if self.failed_attempts >= 1:
        if self.ui.captchaLineEdit.text() != self.captcha_text:
            self.ui.errorLabel.setText("Неверная капча")
            return

    cursor = self.db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE login=? AND password=?",
        (login, password)
    )

    user = cursor.fetchone()

    if user:
        self.accept()
    else:
        self.failed_attempts += 1
        self.ui.errorLabel.setText("Неверные данные")

        # после первой ошибки включаем капчу
        if self.failed_attempts == 1:
            self.generate_captcha()
            self.ui.captchaImageLabel.show()
            self.ui.captchaLineEdit.show()



from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        file = QFile("login.ui")  # имя твоего файла
        file.open(QFile.ReadOnly)

        self.ui = loader.load(file, self)

        file.close()

        # пример подключения кнопки
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        print(self.ui.loginLineEdit.text())


app = QApplication([])
window = LoginWindow()
window.show()
app.exec()


from PySide6.QtCore import QTimer

# --- запуск после успешного входа ---
def start_session(self):
    self.time_left = 600  # 10 минут
    self.timer = QTimer()
    self.timer.timeout.connect(self.tick)
    self.timer.start(1000)


# --- каждую секунду ---
def tick(self):
    self.time_left -= 1

    # отображение времени
    m = self.time_left // 60
    s = self.time_left % 60
    self.ui.timerLabel.setText(f"{m:02d}:{s:02d}")

    # предупреждение за 5 минут
    if self.time_left == 300:
        self.ui.errorLabel.setText("Осталось 5 минут")

    # конец сессии
    if self.time_left <= 0:
        self.timer.stop()
        self.ui.errorLabel.setText("Сеанс завершён")
        self.ui.close()

        # блокировка на 1 минуту
        self.block_login(60)


# --- универсальная блокировка ---
def block_login(self, seconds):
    self.ui.loginButton.setEnabled(False)
    QTimer.singleShot(seconds * 1000,
                      lambda: self.ui.loginButton.setEnabled(True))


# --- использовать после ошибки капчи ---
def captcha_failed(self):
    self.ui.errorLabel.setText("Неверная капча")
    self.block_login(10)
    
# --- автоматический ввод
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
    

# ---------
# ---------
# ---------
# загружаем из списка

# 👉 Заполнение из БД
def load_patients(self):
    self.ui.patientComboBox.clear()

    patients = get_all_patients()  # [(id, fio), ...]

    for p in patients:
        self.ui.patientComboBox.addItem(p[1], p[0])  # текст + id

    self.ui.patientComboBox.addItem("➕ Добавить пациента")
    
# 👉 Обработка выбора
self.ui.patientComboBox.currentIndexChanged.connect(self.handle_patient)
def handle_patient(self, index):
    text = self.ui.patientComboBox.currentText()

    if text == "➕ Добавить пациента":
        self.open_add_patient_dialog()
        
# 🚀 2. Модальное окно (добавление пациента)
# 👉 Класс окна
from PySide6.QtWidgets import QDialog

class AddPatientDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        file = QFile('add_patient.ui')
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        self.ui.saveButton.clicked.connect(self.save)
        
# 👉 Сохранение
def save(self):
    fio = self.ui.fioLineEdit.text()
    birth = self.ui.birthDateEdit.text()
    passport = self.ui.passportLineEdit.text()
    phone = self.ui.phoneLineEdit.text()
    email = self.ui.emailLineEdit.text()
    policy = self.ui.policyLineEdit.text()

    insurance_type = self.ui.insuranceTypeComboBox.currentText()
    company = self.ui.companyComboBox.currentText()

    add_patient(
        fio, birth, passport,
        phone, email, policy,
        insurance_type, company
    )

    self.accept()  # закрыть окно
    
# 🚀 3. Открытие окна
def open_add_patient_dialog(self):
    dialog = AddPatientDialog()

    if dialog.exec():  # модальное окно
        self.load_patients()  # обновляем список
        

self.ui.insuranceTypeComboBox.addItems([
    "ОМС",
    "ДМС"
])

self.ui.companyComboBox.addItems([
    "РЕСО",
    "СОГАЗ",
    "АльфаСтрахование"
])



# ---------- таблица с пользователями, взаимодействие в виджете

# =========================
# SQLALCHEMY CORE: FETCH USERS (FILTER + PAGINATION)
# =========================

def fetch_users(conn, limit=20, offset=0, search=None):
    # Базовый SELECT из таблицы users
    stmt = select(users)

    # Если есть строка поиска — добавляем фильтр по username и email
    if search:
        stmt = stmt.where(
            users.c.username.ilike(f"%{search}%") |
            users.c.email.ilike(f"%{search}%")
        )

    # Пагинация: ограничиваем количество записей и сдвиг
    stmt = stmt.limit(limit).offset(offset)

    # Выполняем запрос и возвращаем результат
    return conn.execute(stmt).fetchall()


# =========================
# QTABLEMODEL: ОТОБРАЖЕНИЕ ДАННЫХ В UI
# =========================

from PySide6.QtCore import QAbstractTableModel, Qt

class UserTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        # Храним данные, пришедшие из БД
        self._data = data or []

        # Заголовки таблицы
        self._headers = ["ID", "Username", "Email"]

    def update(self, data):
        # Полное обновление модели (быстро и безопасно для Qt)
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def rowCount(self, parent=None):
        # Количество строк = количество записей
        return len(self._data)

    def columnCount(self, parent=None):
        # У нас 3 поля: id, username, email
        return 3

    def data(self, index, role):
        # Проверка корректности индекса
        if not index.isValid():
            return None

        row = self._data[index.row()]

        # Отображаем данные только в режиме DisplayRole
        if role == Qt.DisplayRole:
            return [
                row.id,
                row.username,
                row.email
            ][index.column()]

    def headerData(self, section, orientation, role):
        # Заголовки колонок
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]


# =========================
# CONTROLLER: ЛОГИКА АДМИНКИ (ПОИСК + ПАГИНАЦИЯ)
# =========================

class UsersController:
    def __init__(self, conn, model: UserTableModel):
        # SQLAlchemy connection
        self.conn = conn

        # Qt model
        self.model = model

        # Параметры пагинации
        self.limit = 20
        self.offset = 0

        # Текущий фильтр
        self.search = None

    def load(self):
        # Загружаем данные из БД с текущими параметрами
        data = fetch_users(
            self.conn,
            limit=self.limit,
            offset=self.offset,
            search=self.search
        )

        # Обновляем UI модель
        self.model.update(data)

    def set_search(self, text):
        # Устанавливаем фильтр и сбрасываем пагинацию
        self.search = text
        self.offset = 0
        self.load()

    def next_page(self):
        # Следующая страница
        self.offset += self.limit
        self.load()

    def prev_page(self):
        # Предыдущая страница (не уходим в отрицательные значения)
        self.offset = max(0, self.offset - self.limit)
        self.load()


# =========================
# ПОДКЛЮЧЕНИЕ К UI (Qt Designer)
# =========================

# Инициализация модели
self.model = UserTableModel()

# Привязка модели к таблице
self.tableViewUsers.setModel(self.model)

# Контроллер (логика приложения)
self.controller = UsersController(conn, self.model)

# Первая загрузка данных
self.controller.load()


# =========================
# СИГНАЛЫ (МИНИМАЛЬНО И БЫСТРО)
# =========================

# Поиск
self.btnSearch.clicked.connect(
    lambda: self.controller.set_search(self.lineEditSearch.text())
)

# Пагинация вперед
self.btnNext.clicked.connect(self.controller.next_page)

# Пагинация назад
self.btnPrev.clicked.connect(self.controller.prev_page)