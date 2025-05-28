@echo off
cd /d "C:\Project\Pemograman Web\WoofWorld\woofworld_backend"
echo Starting WoofWorld Backend Server with CORS fixes...
python -m pserve development.ini --reload
pause
