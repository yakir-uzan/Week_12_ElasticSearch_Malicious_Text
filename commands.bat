@echo off
echo 🚀 יצירת סביבה וירטואלית...
python -m venv .venv

echo 🔄 הפעלת הסביבה...
call .venv\Scripts\activate

echo 📦 התקנת תלויות...
pip install --upgrade pip
pip install -r requirements.txt

echo 🧠 הרצת תהליך ההעשרה ואינדוקס...
python main.py

echo 🛰️ הרצת FastAPI...
uvicorn api.app:app --reload

pause
