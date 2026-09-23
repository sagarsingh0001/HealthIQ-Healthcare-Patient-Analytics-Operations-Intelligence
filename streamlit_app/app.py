import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

from data_loader import load_data, apply_filters
from analytics import (
    get_kpis, get_monthly_visits, get_dept_summary,
    get_risk_summary, get_cost_by_treatment, get_risk_by_dept, get_risk_by_age,
)
from charts import (
    monthly_visits_chart, department_bar, visit_type_pie, risk_distribution_bar,
    cost_by_dept_bar, cost_by_treatment_bar, los_by_dept_bar, cost_vs_los_scatter,
    risk_by_dept_stacked, risk_by_age_grouped, recovery_by_dept_bar,
    recovery_vs_risk_box, age_distribution_bar, region_distribution_bar,
)
from ml_predictor import model_available, predict

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title='HealthIQ — Patient Analytics',
    page_icon='🏥',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df_full = get_data()

# ─────────────────────────────────────────────
# Sidebar — navigation & filters
# ─────────────────────────────────────────────
with st.sidebar:
    st.title('🏥 HealthIQ')
    st.caption('Healthcare Patient Analytics')
    st.divider()

    pages = ['Dashboard', 'Patient Analysis', 'Cost & Operations', 'Risk Analysis']
    if model_available():
        pages.append('ML Prediction')

    page = st.radio('Navigate', pages)
    st.divider()
    st.subheader('Filters')

    min_date = df_full['visit_date'].min().date()
    max_date = df_full['visit_date'].max().date()
    date_range = st.date_input('Date Range', value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

    dept_options = sorted(df_full['department'].unique())
    selected_dept = st.multiselect('Department', dept_options)

    region_options = sorted(df_full['region'].unique())
    selected_region = st.multiselect('Region', region_options)

    gender_options = sorted(df_full['gender'].unique())
    selected_gender = st.multiselect('Gender', gender_options)

    age_options = ['18-30', '31-45', '46-60', '60+']
    selected_age = st.multiselect('Age Group', age_options)

    vt_options = sorted(df_full['visit_type'].unique())
    selected_vt = st.multiselect('Visit Type', vt_options)

    st.divider()
    st.caption('Jan – Jul 2022 | 5,000 visits')

# Apply filters
filters = {
    'department': selected_dept,
    'region': selected_region,
    'gender': selected_gender,
    'age_group': selected_age,
    'visit_type': selected_vt,
}
if len(date_range) == 2:
    filters['date_range'] = date_range

df = apply_filters(df_full.copy(), filters)

if len(df) == 0:
    st.warning('No data matches the selected filters. Please adjust the filters.')
    st.stop()

# ─────────────────────────────────────────────
# PAGE 1 — Dashboard
# ─────────────────────────────────────────────
if page == 'Dashboard':
    st.title('HealthIQ — Executive Dashboard')
    st.caption(f'Showing **{len(df):,}** of {len(df_full):,} visits')

    kpis = get_kpis(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Total Patients', f"{kpis['total_patients']:,}")
    c2.metric('Total Visits', f"{kpis['total_visits']:,}")
    c3.metric('Total Cost', f"${kpis['total_cost']:,.0f}")
    c4.metric('Avg Cost / Visit', f"${kpis['avg_cost']:,.0f}")

    c5, c6, c7 = st.columns(3)
    c5.metric('Avg Length of Stay', f"{kpis['avg_los']:.2f} days")
    c6.metric('Avg Recovery Score', f"{kpis['avg_recovery']:.2f}")
    c7.metric('High Risk %', f"{kpis['high_risk_pct']:.1f}%")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(monthly_visits_chart(get_monthly_visits(df)), use_container_width=True)
    with col2:
        st.plotly_chart(department_bar(df), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(visit_type_pie(df), use_container_width=True)
    with col4:
        st.plotly_chart(risk_distribution_bar(get_risk_summary(df)), use_container_width=True)

    st.divider()
    col_dl, _ = st.columns([1, 3])
    with col_dl:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('⬇ Download Filtered Dataset', csv, 'filtered_healthcare_data.csv', 'text/csv')

# ─────────────────────────────────────────────
# PAGE 2 — Patient Analysis
# ─────────────────────────────────────────────
elif page == 'Patient Analysis':
    st.title('Patient Analysis')
    st.caption(f'Showing **{len(df):,}** records')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(age_distribution_bar(df), use_container_width=True)
    with col2:
        gender_counts = df['gender'].value_counts().reset_index()
        gender_counts.columns = ['gender', 'count']
        import plotly.express as px
        fig_g = px.pie(gender_counts, names='gender', values='count',
                       title='Gender Distribution',
                       color_discrete_sequence=['#3b82d4', '#f44336'])
        st.plotly_chart(fig_g, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(region_distribution_bar(df), use_container_width=True)
    with col4:
        st.plotly_chart(department_bar(df), use_container_width=True)

    st.plotly_chart(visit_type_pie(df), use_container_width=True)

    st.divider()
    st.subheader('Patient Data Table')
    display_cols = ['patient_id', 'visit_date', 'age_group', 'gender', 'region',
                    'department', 'treatment_type', 'visit_type',
                    'length_of_stay_days', 'treatment_cost', 'recovery_score', 'readmission_risk']
    st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=350)

    csv = df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button('⬇ Download Patient Table', csv, 'patient_data.csv', 'text/csv')

# ─────────────────────────────────────────────
# PAGE 3 — Cost & Operations
# ─────────────────────────────────────────────
elif page == 'Cost & Operations':
    st.title('Cost & Operations')
    st.caption(f'Showing **{len(df):,}** records')

    kpis = get_kpis(df)
    c1, c2, c3 = st.columns(3)
    c1.metric('Avg Length of Stay', f"{kpis['avg_los']:.2f} days")
    c2.metric('Avg Treatment Cost', f"${kpis['avg_cost']:,.0f}")
    c3.metric('Total Treatment Cost', f"${kpis['total_cost']:,.0f}")

    st.divider()
    dept_df = get_dept_summary(df)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(cost_by_dept_bar(dept_df), use_container_width=True)
    with col2:
        st.plotly_chart(cost_by_treatment_bar(get_cost_by_treatment(df)), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(los_by_dept_bar(dept_df), use_container_width=True)
    with col4:
        vt_cost = df.groupby('visit_type')['treatment_cost'].mean().round(2).reset_index()
        vt_cost.columns = ['visit_type', 'avg_cost']
        import plotly.express as px
        fig_vt = px.bar(vt_cost, x='visit_type', y='avg_cost',
                        title='Average Cost by Visit Type',
                        labels={'visit_type': 'Visit Type', 'avg_cost': 'Avg Cost (USD)'},
                        color='visit_type',
                        color_discrete_sequence=['#3b82d4', '#f44336'])
        fig_vt.update_yaxes(tickformat='$,.0f')
        fig_vt.update_layout(showlegend=False)
        st.plotly_chart(fig_vt, use_container_width=True)

    st.plotly_chart(cost_vs_los_scatter(df), use_container_width=True)

    st.divider()
    st.subheader('Department Summary Table')
    st.dataframe(dept_df, use_container_width=True)

    csv = dept_df.to_csv(index=False).encode('utf-8')
    st.download_button('⬇ Download Department Analysis', csv, 'department_analysis.csv', 'text/csv')

# ─────────────────────────────────────────────
# PAGE 4 — Risk Analysis
# ─────────────────────────────────────────────
elif page == 'Risk Analysis':
    st.title('Risk Analysis')
    st.caption(f'Showing **{len(df):,}** records')

    risk_df = get_risk_summary(df)
    col1, col2, col3 = st.columns(3)
    for i, row in risk_df.iterrows():
        [col1, col2, col3][i].metric(
            f"{row['risk']} Risk",
            f"{row['count']:,}",
            f"{row['pct']:.1f}%"
        )

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(risk_distribution_bar(risk_df), use_container_width=True)
    with col2:
        st.plotly_chart(risk_by_dept_stacked(get_risk_by_dept(df)), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(risk_by_age_grouped(get_risk_by_age(df)), use_container_width=True)
    with col4:
        risk_vt = df.groupby(['visit_type', 'readmission_risk']).size().unstack(fill_value=0)
        for col in ['Low', 'Medium', 'High']:
            if col not in risk_vt.columns:
                risk_vt[col] = 0
        risk_vt_pct = (risk_vt.div(risk_vt.sum(axis=1), axis=0) * 100).round(2).reset_index()
        import plotly.graph_objects as go
        fig_vt = go.Figure()
        RISK_COLORS = {'Low': '#4caf50', 'Medium': '#ff9800', 'High': '#f44336'}
        for risk, color in RISK_COLORS.items():
            if risk in risk_vt_pct.columns:
                fig_vt.add_trace(go.Bar(name=risk, x=risk_vt_pct['visit_type'],
                                         y=risk_vt_pct[risk], marker_color=color))
        fig_vt.update_layout(barmode='stack', title='Risk by Visit Type (%)',
                              xaxis_title='Visit Type', yaxis_title='% of Patients')
        st.plotly_chart(fig_vt, use_container_width=True)

    st.plotly_chart(recovery_vs_risk_box(df), use_container_width=True)

    st.divider()
    st.subheader('Filtered Risk Table')
    risk_table = df[['patient_id', 'department', 'visit_type', 'age_group', 'region',
                     'readmission_risk', 'recovery_score', 'treatment_cost',
                     'length_of_stay_days']].reset_index(drop=True)
    st.dataframe(risk_table, use_container_width=True, height=350)

    csv = risk_table.to_csv(index=False).encode('utf-8')
    st.download_button('⬇ Download Risk Table', csv, 'risk_analysis.csv', 'text/csv')

# ─────────────────────────────────────────────
# PAGE 5 — ML Prediction (only if model exists)
# ─────────────────────────────────────────────
elif page == 'ML Prediction' and model_available():
    st.title('ML Risk Prediction')
    st.info(
        '**Model-predicted risk category** — '
        'This uses a Random Forest classifier trained on the healthcare dataset.'
    )
    st.warning(
        '⚠️ This prediction is for **educational and analytical purposes only** '
        'and is **not medical advice or a clinical diagnosis**.'
    )

    st.subheader('Enter Patient Details')
    col1, col2, col3 = st.columns(3)
    with col1:
        age_group = st.selectbox('Age Group', ['18-30', '31-45', '46-60', '60+'])
        gender = st.selectbox('Gender', ['Male', 'Female'])
        region = st.selectbox('Region', ['North', 'South', 'East', 'West'])
    with col2:
        department = st.selectbox('Department',
                                  ['Cardiology', 'General Medicine', 'Neurology',
                                   'Orthopedics', 'Pediatrics'])
        treatment_type = st.selectbox('Treatment Type',
                                      ['Medication', 'Observation', 'Surgery', 'Therapy'])
        visit_type = st.selectbox('Visit Type', ['Routine', 'Emergency'])
    with col3:
        los = st.slider('Length of Stay (days)', 0.0, 12.0, 4.0, 0.1)
        cost = st.number_input('Treatment Cost (USD)', min_value=0, max_value=150000,
                               value=55000, step=1000)
        recovery = st.slider('Recovery Score', 33, 100, 75)

    if st.button('🔍 Predict Risk', type='primary'):
        result = predict({
            'age_group': age_group,
            'gender': gender,
            'region': region,
            'department': department,
            'treatment_type': treatment_type,
            'visit_type': visit_type,
            'length_of_stay_days': los,
            'treatment_cost': cost,
            'recovery_score': recovery,
        })

        label = result['label']
        color_map = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        icon = color_map.get(label, '⚪')

        st.subheader(f'Predicted Risk: {icon} **{label}**')

        if result['probabilities']:
            st.markdown('**Predicted Probabilities:**')
            prob_cols = st.columns(len(result['probabilities']))
            for i, (cls, pct) in enumerate(sorted(result['probabilities'].items(),
                                                   key=lambda x: ['Low','Medium','High'].index(x[0]))):
                prob_cols[i].metric(f'{cls} Risk', f'{pct:.1f}%')

        st.caption(
            'Note: This model has moderate accuracy (~46%) due to the limited predictive '
            'signal in the dataset. Class imbalance (60% Low risk) affects results. '
            'Predictions should be interpreted with caution.'
        )
