@echo on

set PYTHONPATH=%CD%;%PYTHONPATH%

call .venv\Scripts\activate.bat

set DATA=--add-data "assets/ui/login.ui;assets/ui" --add-data "db/database.db;db" --add-data "app/images;app/images"

pyinstaller --onefile --windowed %DATA% src/laboratory_app.py