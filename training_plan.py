"""
World's Toughest Mudder Trainingsplan Generator
Ziel: 28. Juli 2026 - mindestens 100km, Ziel 75 Meilen (120km / 15 Runden)
Jede Runde ≈ 8km mit Hindernissen und ca. 50-80m Höhenunterschied
"""
from datetime import date, timedelta


RACE_DATE = date(2026, 7, 28)
TODAY = date(2026, 3, 16)
WEEKS_TO_RACE = (RACE_DATE - TODAY).days // 7

# WTM Runden-Details
LOOP_KM = 8.0
TARGET_MIN_KM = 100
TARGET_GOAL_KM = 120  # 75 Meilen
TARGET_MIN_LOOPS = int(TARGET_MIN_KM / LOOP_KM)  # 12 Runden
TARGET_GOAL_LOOPS = int(TARGET_GOAL_KM / LOOP_KM)  # 15 Runden


def generate_plan(current_weekly_run_km: float, current_long_run_km: float) -> list:
    """
    Generiert einen Wochenplan basierend auf aktuellem Fitnessniveau.
    Phasen:
      Wochen 1-4:  Aufbau Grundausdauer
      Wochen 5-8:  Volumenblock
      Wochen 9-12: Spezifität (Nacht, Hindernisse, Rucksack)
      Wochen 13-16: Peak & Simulation
      Wochen 17-18: Taper
    """
    weeks = []
    start = TODAY

    for w in range(1, WEEKS_TO_RACE + 1):
        week_start = start + timedelta(weeks=w - 1)
        week_end = week_start + timedelta(days=6)

        if w <= 4:
            phase = "Grundausdauer"
            long_run = min(current_long_run_km + (w * 2), 25)
            weekly_km = current_weekly_run_km * (1 + w * 0.08)
            focus = [
                "Zone-2 Dauerläufe",
                "Kraft (Körpergewicht: Burpees, Pull-ups, Dips)",
                "Langer Lauf am Wochenende",
            ]
        elif w <= 8:
            phase = "Volumenaufbau"
            long_run = min(25 + (w - 4) * 3, 40)
            weekly_km = current_weekly_run_km * (1.3 + (w - 4) * 0.07)
            focus = [
                "Doppeleinheiten 1x/Woche (Morgen + Abend)",
                "Trail-Laufen mit Höhenmetern",
                "Hindernistechnik (Monkey Bars, Walls, Carries)",
                "Langer Lauf + Rucksack (5kg)",
            ]
        elif w <= 12:
            phase = "Spezifität"
            long_run = min(40 + (w - 8) * 2, 48)
            weekly_km = current_weekly_run_km * 1.6
            focus = [
                "Nachtlauf (mind. 1x/Woche nach 22 Uhr)",
                "Kaltwasser-Exposition (Eisbad / kalte Dusche)",
                "Back-to-Back Läufe (Sa + So je 20-25km)",
                "Hindernisparcours simulieren",
                "Mentale Härtung",
            ]
        elif w <= 16:
            phase = "Peak & Simulation"
            long_run = 48 if w < 15 else 52
            weekly_km = current_weekly_run_km * 1.7
            focus = [
                "24h Simulation (mind. 1x): 6-8 Stunden kontinuierliches Laufen",
                "Ausrüstung testen (Neopren, Schuhe, Beleuchtung)",
                "Nutrition-Strategie üben (alle 45min essen/trinken)",
                "Schlafentzug-Training",
            ]
        else:
            phase = "Taper"
            long_run = max(20, 52 - (w - 16) * 10)
            weekly_km = current_weekly_run_km * (1.0 - (w - 16) * 0.3)
            focus = [
                "Volumen stark reduzieren (60-70%)",
                "Intensität beibehalten",
                "Ausrüstung finalisieren",
                "Schlaf priorisieren",
            ]

        weeks.append({
            "week": w,
            "phase": phase,
            "start": week_start.strftime("%d.%m."),
            "end": week_end.strftime("%d.%m.%Y"),
            "target_long_run_km": round(long_run, 1),
            "target_weekly_km": round(weekly_km, 1),
            "focus": focus,
        })

    return weeks


def print_plan(weeks: list, stats: dict = None):
    print("\n" + "=" * 70)
    print("  WORLD'S TOUGHEST MUDDER - TRAININGSPLAN")
    print(f"  Renntag: 28. Juli 2026 | Noch {WEEKS_TO_RACE} Wochen")
    print(f"  Mindestziel: {TARGET_MIN_LOOPS} Runden ({TARGET_MIN_KM}km)")
    print(f"  Hauptziel:   {TARGET_GOAL_LOOPS} Runden ({TARGET_GOAL_KM}km / 75 Meilen)")
    print("=" * 70)

    if stats:
        print(f"\nDein aktuelles Level (aus Strava):")
        print(f"  Ø Wochenkilometer Laufen: {stats['avg_weekly_km_run']:.1f} km")
        print(f"  Längster Lauf:            {stats['longest_run_km']:.1f} km")
        print(f"  Gesamthöhenmeter (6 Mo):  {stats['total_elevation_m']:,.0f} m")

    current_phase = None
    for w in weeks:
        if w["phase"] != current_phase:
            current_phase = w["phase"]
            print(f"\n{'─'*70}")
            print(f"  PHASE: {current_phase.upper()}")
            print(f"{'─'*70}")

        print(f"\n  Woche {w['week']:2d} ({w['start']} - {w['end']})")
        print(f"    Langer Lauf: {w['target_long_run_km']} km")
        print(f"    Wochenziel:  {w['target_weekly_km']} km")
        print(f"    Fokus:")
        for f in w["focus"]:
            print(f"      • {f}")

    print("\n" + "=" * 70)
    print("  WÖCHENTLICHE STRUKTUR (Beispiel)")
    print("=" * 70)
    print("""
  Mo: Kraft + Mobilität (60-90min)
  Di: Intervalle / Tempolauf (10-15km)
  Mi: Mittellanger Lauf Zone 2 (12-18km)
  Do: Kraft + Schwimmen/Kalt-Exposition
  Fr: Kurz & locker (8-10km) oder Ruhe
  Sa: LANGER LAUF (mit Rucksack, Trails)
  So: Back-to-Back Lauf (15-20km) oder aktive Erholung
  """)

    print("=" * 70)
    print("  HINDERNISTYPISCHE KRAFTÜBUNGEN (3x/Woche)")
    print("=" * 70)
    print("""
  • Monkey Bar Progressionen (Grip-Stärke)
  • Farmers Carry (20-30kg, 50m)
  • Sandbag Carries
  • Pull-ups & Muscle-ups
  • Burpees (WTM-Standard: 30 Burpees pro verfehltem Hindernis)
  • Cold Water Immersion (2-3x/Woche kalt duschen)
  • Box Jumps & Sprints
  """)


if __name__ == "__main__":
    # Beispielwerte - werden aus Strava-Analyse übernommen
    plan = generate_plan(
        current_weekly_run_km=40,
        current_long_run_km=20
    )
    print_plan(plan)
