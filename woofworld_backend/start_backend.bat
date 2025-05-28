@echo off
echo Starting WoofWorld Backend Server...
cd "C:\Project\Pemograman Web\WoofWorld\woofworld_backend"
call conda activate woofworld
echo Environment activated
pserve development.ini --reload
pause
