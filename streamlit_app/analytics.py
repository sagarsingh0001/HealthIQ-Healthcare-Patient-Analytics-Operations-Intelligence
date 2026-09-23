import pandas as pd


def get_kpis(df: pd.DataFrame) -> dict:
    """Calculate top-level KPI metrics."""
    high_risk_count = (df['readmission_risk'] == 'High').sum()
    return {
        'total_patients': df['patient_id'].nunique(),
        'total_visits': len(df),
        'total_cost': df['treatment_cost'].sum(),
        'avg_cost': df['treatment_cost'].mean(),
        'avg_los': df['length_of_stay_days'].mean(),
        'avg_recovery': df['recovery_score'].mean(),
        'high_risk_pct': (high_risk_count / len(df) * 100) if len(df) > 0 else 0,
    }


def get_monthly_visits(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly visit counts."""
    monthly = (
        df.groupby(df['visit_date'].dt.to_period('M'))
        .size()
        .reset_index(name='visits')
    )
    monthly['month'] = monthly['visit_date'].astype(str)
    return monthly[['month', 'visits']]


def get_dept_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Department-level summary."""
    return (
        df.groupby('department')
        .agg(
            visits=('patient_id', 'count'),
            avg_cost=('treatment_cost', 'mean'),
            total_cost=('treatment_cost', 'sum'),
            avg_los=('length_of_stay_days', 'mean'),
            avg_recovery=('recovery_score', 'mean'),
        )
        .round(2)
        .reset_index()
        .sort_values('visits', ascending=False)
    )


def get_risk_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Risk distribution counts and percentages."""
    risk_order = ['Low', 'Medium', 'High']
    risk_counts = df['readmission_risk'].value_counts().reindex(risk_order, fill_value=0).reset_index()
    risk_counts.columns = ['risk', 'count']
    risk_counts['pct'] = (risk_counts['count'] / len(df) * 100).round(1) if len(df) > 0 else 0
    return risk_counts


def get_cost_by_treatment(df: pd.DataFrame) -> pd.DataFrame:
    """Average cost by treatment type."""
    return (
        df.groupby('treatment_type')['treatment_cost']
        .mean()
        .round(2)
        .reset_index()
        .sort_values('treatment_cost', ascending=False)
        .rename(columns={'treatment_cost': 'avg_cost'})
    )


def get_risk_by_dept(df: pd.DataFrame) -> pd.DataFrame:
    """Risk distribution by department."""
    risk_dept = (
        df.groupby(['department', 'readmission_risk'])
        .size()
        .unstack(fill_value=0)
    )
    for col in ['Low', 'Medium', 'High']:
        if col not in risk_dept.columns:
            risk_dept[col] = 0
    risk_dept_pct = risk_dept.div(risk_dept.sum(axis=1), axis=0) * 100
    return risk_dept_pct[['Low', 'Medium', 'High']].round(2).reset_index()


def get_risk_by_age(df: pd.DataFrame) -> pd.DataFrame:
    """Risk distribution by age group."""
    age_order = ['18-30', '31-45', '46-60', '60+']
    risk_age = (
        df.groupby(['age_group', 'readmission_risk'])
        .size()
        .unstack(fill_value=0)
    )
    for col in ['Low', 'Medium', 'High']:
        if col not in risk_age.columns:
            risk_age[col] = 0
    risk_age_pct = risk_age.div(risk_age.sum(axis=1), axis=0) * 100
    return risk_age_pct[['Low', 'Medium', 'High']].round(2).reindex(age_order).reset_index()
