@echo off
SETLOCAL
cls
echo 💠 ======================================================
echo 💠       NEXLY ELITE LEARNING ECOSYSTEM
echo 💠 ======================================================
echo.

echo 🛡️  Checking for Database Migrations...
python manage.py migrate --noinput

echo.
echo 🚀  Launching Core Server at http://127.0.0.1:8000/
echo 💡  (Press CTRL+C to stop)
echo.

python manage.py runserver
