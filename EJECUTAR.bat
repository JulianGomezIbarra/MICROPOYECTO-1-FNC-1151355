@echo off
title Conversor a Forma Normal de Chomsky - UFPS
echo ========================================================
echo   Iniciando Conversor de Gramaticas a FNC (UFPS)
echo ========================================================
if exist "%~dp0Chomsky_FNC.exe" (
    start "" "%~dp0Chomsky_FNC.exe"
) else if exist "%~dp0dist\Chomsky_FNC.exe" (
    start "" "%~dp0dist\Chomsky_FNC.exe"
) else (
    python "%~dp0main.py"
)
