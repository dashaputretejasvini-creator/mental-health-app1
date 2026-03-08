def calculate_risk(sleep_hours, stress_level, sleep_quality,
                   work_study_hours=0, physical_activity=50):

    score = 0
    factors = []

    # ── SLEEP HOURS ──────────────────────────────────
    if sleep_hours < 5:
        score += 3
        factors.append("🔴 Very low sleep ({:.1f}h) — major risk".format(sleep_hours))
    elif sleep_hours < 6:
        score += 2
        factors.append("🟠 Low sleep ({:.1f}h)".format(sleep_hours))
    elif sleep_hours < 7:
        score += 1
        factors.append("🟡 Slightly low sleep ({:.1f}h)".format(sleep_hours))
    else:
        factors.append("🟢 Sleep hours are healthy ({:.1f}h)".format(sleep_hours))

    # ── STRESS LEVEL ─────────────────────────────────
    if stress_level >= 8:
        score += 3
        factors.append("🔴 Very high stress ({}/10) — major risk".format(stress_level))
    elif stress_level >= 6:
        score += 2
        factors.append("🟠 High stress ({}/10)".format(stress_level))
    elif stress_level >= 4:
        score += 1
        factors.append("🟡 Moderate stress ({}/10)".format(stress_level))
    else:
        factors.append("🟢 Stress level is low ({}/10)".format(stress_level))

    # ── SLEEP QUALITY ─────────────────────────────────
    if sleep_quality <= 4:
        score += 2
        factors.append("🔴 Poor sleep quality ({}/10)".format(sleep_quality))
    elif sleep_quality <= 6:
        score += 1
        factors.append("🟠 Average sleep quality ({}/10)".format(sleep_quality))
    else:
        factors.append("🟢 Good sleep quality ({}/10)".format(sleep_quality))

    # ── WORK/STUDY HOURS ──────────────────────────────
    if work_study_hours > 10:
        score += 3
        factors.append("🔴 Overworking ({}h/day) — major risk".format(work_study_hours))
    elif work_study_hours > 8:
        score += 2
        factors.append("🟠 High work/study hours ({}h/day)".format(work_study_hours))
    elif work_study_hours > 6:
        score += 1
        factors.append("🟡 Moderate work/study hours ({}h/day)".format(work_study_hours))
    else:
        factors.append("🟢 Work/study hours are balanced ({}h/day)".format(work_study_hours))

    # ── PHYSICAL ACTIVITY ─────────────────────────────
    if physical_activity < 30:
        score += 2
        factors.append("🔴 Very low physical activity")
    elif physical_activity < 50:
        score += 1
        factors.append("🟠 Low physical activity")
    else:
        factors.append("🟢 Physical activity is good")

    # ── RISK LEVEL ────────────────────────────────────
    if score >= 8:
        risk_level = "High"
    elif score >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Sort factors — most critical first
    factors_sorted = (
        [f for f in factors if "🔴" in f] +
        [f for f in factors if "🟠" in f] +
        [f for f in factors if "🟡" in f] +
        [f for f in factors if "🟢" in f]
    )

    return score, risk_level, factors_sorted
