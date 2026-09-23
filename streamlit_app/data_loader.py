import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'cleaned_healthcare_data.csv')


def load_data() -> pd.DataFrame:
    """Load the cleaned healthcare dataset."""
    df = pd.read_csv(DATA_PATH, parse_dates=['visit_date'])
    return df


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply sidebar filters to the dataframe."""
    if filters.get('department'):
        df = df[df['department'].isin(filters['department'])]
    if filters.get('region'):
        df = df[df['region'].isin(filters['region'])]
    if filters.get('gender'):
        df = df[df['gender'].isin(filters['gender'])]
    if filters.get('age_group'):
        df = df[df['age_group'].isin(filters['age_group'])]
    if filters.get('visit_type'):
        df = df[df['visit_type'].isin(filters['visit_type'])]
    if filters.get('date_range'):
        start, end = filters['date_range']
        df = df[(df['visit_date'].dt.date >= start) & (df['visit_date'].dt.date <= end)]
    return df
