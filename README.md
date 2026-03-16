# World's Toughest Mudder - Strava Analyse & Trainingsplan

**Renntag:** 28. Juli 2026
**Ziel:** Mindestens 100km (12 Runden), Hauptziel 75 Meilen / 120km (15 Runden)

## Setup

### 1. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 2. Strava API App erstellen
1. Gehe zu [strava.com/settings/api](https://www.strava.com/settings/api)
2. Erstelle eine App (Name & Website können beliebig sein)
3. Kopiere **Client ID** und **Client Secret**

### 3. .env Datei anlegen
```bash
cp .env.example .env
# Trage Client ID und Client Secret in .env ein
```

### 4. Einmalige Authentifizierung
```bash
python strava_auth.py
```
Folge den Anweisungen, um deinen Refresh Token zu erhalten und in `.env` einzutragen.

### 5. Analyse & Trainingsplan starten
```bash
python main.py
```

## Programm-Übersicht

| Datei | Beschreibung |
|-------|-------------|
| `strava_auth.py` | OAuth2 Authentifizierung mit Strava |
| `strava_data.py` | Aktivitätsdaten abrufen & analysieren |
| `training_plan.py` | WTM Trainingsplan Generator |
| `main.py` | Hauptprogramm (Analyse + Plan) |

## Trainingsplan-Phasen

| Phase | Wochen | Fokus |
|-------|--------|-------|
| Grundausdauer | 1-4 | Aerobe Basis, Kraft |
| Volumenaufbau | 5-8 | Höhere Wochenkilometer, Trail |
| Spezifität | 9-12 | Nacht, Kälte, Hindernisse |
| Peak & Simulation | 13-16 | 24h Simulation, Ausrüstung |
| Taper | 17-18 | Volumenreduktion, Erholung |
