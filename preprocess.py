import pandas as pd
import numpy as np

def load_and_clean_data():

    # ── LOAD BOTH DATASETS ──────────────────────────────
    df_worker = pd.read_csv('data/sleep_lifestyle.csv')
    df_student = pd.read_csv('data/student_depression.csv')

    # ── CLEAN WORKER DATASET ────────────────────────────
    df_worker = df_worker.rename(columns={
        'Age': 'age',
        'Gender': 'gender',
        'Occupation': 'occupation',
        'Sleep Duration': 'sleep_hours',
        'Quality of Sleep': 'sleep_quality',
        'Physical Activity Level': 'physical_activity',
        'Stress Level': 'stress_level',
        'BMI Category': 'bmi',
        'Sleep Disorder': 'sleep_disorder'
    })

    # Add category column
    df_worker['category'] = 'Worker'

    # Fill missing sleep disorder with None
    df_worker['sleep_disorder'] = df_worker['sleep_disorder'].fillna('None')

    # Create depression column from sleep disorder
    df_worker['depression'] = df_worker['sleep_disorder'].apply(
        lambda x: 1 if x in ['Insomnia', 'Sleep Apnea'] else 0
    )

    # Keep useful columns only
    df_worker = df_worker[[
        'age', 'gender', 'occupation', 'category',
        'sleep_hours', 'sleep_quality', 'stress_level',
        'physical_activity', 'bmi', 'sleep_disorder', 'depression'
    ]]

    # ── CLEAN STUDENT DATASET ───────────────────────────
    df_student = df_student.rename(columns={
        'Age': 'age',
        'Gender': 'gender',
        'Profession': 'occupation',
        'Sleep Duration': 'sleep_duration_range',
        'Work/Study Hours': 'work_study_hours',
        'Academic Pressure': 'academic_pressure',
        'Work Pressure': 'work_pressure',
        'Financial Stress': 'financial_stress',
        'Family History of Mental Illness': 'family_history',
        'Depression': 'depression',
        'Dietary Habits': 'dietary_habits',
        'Have you ever had suicidal thoughts ?': 'suicidal_thoughts'
    })

    # Add category column
    df_student['category'] = 'Student'

    # Convert sleep range to numeric hours
    sleep_map = {
        "'Less than 5 hours'": 4.5,
        "'5-6 hours'": 5.5,
        "'7-8 hours'": 7.5,
        "'More than 8 hours'": 9.0,
        'Others': 6.0
    }
    df_student['sleep_hours'] = df_student['sleep_duration_range'].map(sleep_map).fillna(6.0)

    # Convert financial stress to numeric
    df_student['financial_stress'] = pd.to_numeric(
        df_student['financial_stress'], errors='coerce'
    ).fillna(0)

    # Add stress level from academic + work pressure average
    df_student['stress_level'] = (
        (df_student['academic_pressure'] + df_student['work_pressure']) / 2
    ).round(1)

    # Add missing columns with default values
    df_student['sleep_quality'] = df_student['sleep_hours'].apply(
        lambda x: 8 if x >= 7 else (6 if x >= 5.5 else 4)
    )
    df_student['physical_activity'] = 50
    df_student['bmi'] = 'Normal'
    df_student['sleep_disorder'] = df_student['depression'].apply(
        lambda x: 'Insomnia' if x == 1 else 'None'
    )

    # Keep useful columns only
    df_student = df_student[[
        'age', 'gender', 'occupation', 'category',
        'sleep_hours', 'sleep_quality', 'stress_level',
        'physical_activity', 'bmi', 'sleep_disorder', 'depression'
    ]]

    # ── MERGE BOTH DATASETS ─────────────────────────────
    df = pd.concat([df_worker, df_student], ignore_index=True)

    # ── CREATE AGE GROUPS ───────────────────────────────
    bins = [0, 18, 25, 35, 50, 100]
    labels = ['Teen', 'Young Adult', 'Adult', 'Mid-Age', 'Senior']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

    # ── CREATE RISK LEVEL ───────────────────────────────
    def assign_risk(row):
        score = 0
        if row['sleep_hours'] < 5:    score += 3
        elif row['sleep_hours'] < 6:  score += 1
        if row['stress_level'] >= 7:  score += 3
        elif row['stress_level'] >= 5: score += 2
        if row['sleep_quality'] <= 4: score += 2
        if row['depression'] == 1:    score += 3
        if score >= 7:   return 'High'
        elif score >= 4: return 'Medium'
        else:            return 'Low'

    df['risk_level'] = df.apply(assign_risk, axis=1)

    # ── CLEAN UP ────────────────────────────────────────
    df = df.dropna(subset=['age', 'sleep_hours', 'stress_level'])
    df['age'] = df['age'].astype(int)
    df = df.reset_index(drop=True)

    return df