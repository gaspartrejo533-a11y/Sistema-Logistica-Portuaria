@echo off
title Sistema de Gestion de Logistica Portuaria

echo ==========================================
echo   SISTEMA DE GESTION LOGISTICA PORTUARIA
echo ==========================================
echo.

echo Iniciando microservicio AUTH...
start "AUTH - Puerto 5001" cmd /k "cd /d ""%~dp0backend\auth"" && py app.py"

timeout /t 2 /nobreak >nul

echo Iniciando microservicio CATALOG...
start "CATALOG - Puerto 5002" cmd /k "cd /d ""%~dp0backend\catalog"" && py app.py"

timeout /t 2 /nobreak >nul

echo Iniciando microservicio OPERATIONS...
start "OPERATIONS - Puerto 5003" cmd /k "cd /d ""%~dp0backend\operations"" && py app.py"

timeout /t 2 /nobreak >nul

echo Iniciando API GATEWAY...
start "GATEWAY - Puerto 5000" cmd /k "cd /d ""%~dp0backend\gateway"" && py app.py"

echo.
echo ==========================================
echo   SERVICIOS INICIADOS
echo   Gateway:    http://127.0.0.1:5000
echo   Auth:       http://127.0.0.1:5001
echo   Catalog:    http://127.0.0.1:5002
echo   Operations: http://127.0.0.1:5003
echo ==========================================
echo.
pause
