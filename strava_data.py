"""
Strava Aktivitätsdaten abrufen und analysieren.
"""
import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from strava_auth import get_valid_access_token

load_dotenv()

CACHE_FILE = "activities_cache.json"
BASE_URL = "https://www.strava.com/api/v3"


def fetch_activities(months_back: int = 6, use_cache: bool = True) -> list:
    """Holt alle Aktivitäten der letzten X Monate von Strava."""
    if use_cache and os.path.exists(CACHE_FILE):
        print(f"Lade Aktivitäten aus Cache ({CACHE_FILE})...")
        with open(CACHE_FILE) as f:
            return json.load(f)

    token = get_valid_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    after_ts = int((datetime.now() - timedelta(days=30 * months_back)).timestamp())

    activities = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/athlete/activities",
            headers=headers,
            params={"after": after_ts, "per_page": 100, "page": page},
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        activities.extend(batch)
        print(f"  Seite {page}: {len(batch)} Aktivitäten geladen")
        page += 1

    with open(CACHE_FILE, "w") as f:
        json.dump(activities, f, indent=2)

    print(f"Gesamt: {len(activities)} Aktivitäten")
    return activities


def analyze_activities(activities: list) -> dict:
    """Analysiert die Aktivitäten und gibt eine Zusammenfassung zurück."""
    stats = {
        "total": len(activities),
        "by_type": {},
        "weekly_volume": {},
        "longest_run_km": 0,
        "longest_ride_km": 0,
        "total_elevation_m": 0,
        "avg_weekly_km_run": 0,
        "avg_weekly_km_ride": 0,
    }

    weekly_run_km = {}
    weekly_ride_km = {}

    for act in activities:
        sport = act.get("sport_type", act.get("type", "Unknown"))
        dist_km = act.get("distance", 0) / 1000
        elev = act.get("total_elevation_gain", 0)
        date = datetime.fromisoformat(act["start_date"][:10])
        week = date.strftime("%Y-W%V")

        stats["by_type"][sport] = stats["by_type"].get(sport, 0) + 1
        stats["total_elevation_m"] += elev

        if sport in ("Run", "TrailRun", "VirtualRun"):
            stats["longest_run_km"] = max(stats["longest_run_km"], dist_km)
            weekly_run_km[week] = weekly_run_km.get(week, 0) + dist_km
        elif sport in ("Ride", "VirtualRide", "MountainBikeRide", "GravelRide"):
            stats["longest_ride_km"] = max(stats["longest_ride_km"], dist_km)
            weekly_ride_km[week] = weekly_ride_km.get(week, 0) + dist_km

    if weekly_run_km:
        stats["avg_weekly_km_run"] = sum(weekly_run_km.values()) / len(weekly_run_km)
        stats["weekly_volume"]["run"] = weekly_run_km
    if weekly_ride_km:
        stats["avg_weekly_km_ride"] = sum(weekly_ride_km.values()) / len(weekly_ride_km)
        stats["weekly_volume"]["ride"] = weekly_ride_km

    return stats


def print_analysis(stats: dict):
    """Gibt die Analyse lesbar aus."""
    print("\n" + "=" * 60)
    print("  STRAVA ANALYSE - WORLD'S TOUGHEST MUDDER VORBEREITUNG")
    print("=" * 60)
    print(f"\nGesamte Aktivitäten analysiert: {stats['total']}")
    print("\nAktivitäten nach Typ:")
    for sport, count in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {sport:<25} {count:>4} Einheiten")
    print(f"\nLängster Lauf:       {stats['longest_run_km']:.1f} km")
    print(f"Längste Radfahrt:    {stats['longest_ride_km']:.1f} km")
    print(f"Gesamthöhenmeter:    {stats['total_elevation_m']:,.0f} m")
    print(f"\nDurchschnittliches Wochenvolumen:")
    print(f"  Laufen:  {stats['avg_weekly_km_run']:.1f} km/Woche")
    print(f"  Radeln:  {stats['avg_weekly_km_ride']:.1f} km/Woche")


if __name__ == "__main__":
    print("Lade Strava-Daten...")
    activities = fetch_activities(months_back=6)
    stats = analyze_activities(activities)
    print_analysis(stats)
