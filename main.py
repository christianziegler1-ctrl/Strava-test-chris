"""
Hauptprogramm: Strava-Analyse + WTM Trainingsplan
"""
from strava_data import fetch_activities, analyze_activities, print_analysis
from training_plan import generate_plan, print_plan


def main():
    print("=" * 60)
    print("  WORLD'S TOUGHEST MUDDER - ANALYSE & TRAININGSPLAN")
    print("=" * 60)

    # 1. Strava-Daten laden
    print("\nLade Strava-Aktivitäten (letzte 6 Monate)...")
    activities = fetch_activities(months_back=6)

    # 2. Analysieren
    stats = analyze_activities(activities)
    print_analysis(stats)

    # 3. Trainingsplan basierend auf echten Daten
    print("\nErstelle personalisierten Trainingsplan...")
    plan = generate_plan(
        current_weekly_run_km=max(stats["avg_weekly_km_run"], 10),
        current_long_run_km=max(stats["longest_run_km"], 10),
    )
    print_plan(plan, stats=stats)


if __name__ == "__main__":
    main()
