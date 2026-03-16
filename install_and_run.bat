@echo off
chcp 65001 >nul
title Strava Setup - World's Toughest Mudder

echo ============================================================
echo   STRAVA SETUP - World's Toughest Mudder Trainingsplan
echo ============================================================
echo.

:: Prüfe ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python gefunden! Starte direkt...
    goto :run_script
)

:: Python nicht gefunden - Installation anbieten
echo Python ist nicht installiert. Es wird benoetigt.
echo.
echo Moechtest du Python jetzt automatisch installieren?
echo (Einmalig noetig, dauert ca. 2-3 Minuten)
echo.
choice /C JN /M "Python installieren? (J=Ja / N=Nein)"
if %errorlevel% == 2 (
    echo.
    echo Bitte installiere Python manuell von: https://www.python.org/downloads/
    echo Wichtig: Beim Installieren "Add Python to PATH" anhaeken!
    pause
    exit /b 1
)

echo.
echo Versuche automatische Installation via Windows Package Manager...
winget install --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements

if %errorlevel% neq 0 (
    echo.
    echo Automatische Installation nicht moeglich.
    echo Oeffne python.org im Browser...
    start https://www.python.org/downloads/
    echo.
    echo Bitte:
    echo 1. Python herunterladen und installieren
    echo 2. Beim Setup "Add Python to PATH" anhaeken!
    echo 3. Danach diese Datei nochmal doppelklicken
    pause
    exit /b 1
)

echo.
echo Python erfolgreich installiert!
echo.

:run_script
echo Starte Strava-Verbindung...
echo.
python get_token_local.py

if %errorlevel% neq 0 (
    echo.
    echo Fehler beim Ausfuehren. Bitte melde dich bei Claude.
    pause
    exit /b 1
)
