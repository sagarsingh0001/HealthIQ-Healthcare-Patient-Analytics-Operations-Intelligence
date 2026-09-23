import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

RISK_COLORS = {'Low': '#4caf50', 'Medium': '#ff9800', 'High': '#f44336'}
PALETTE = px.colors.qualitative.Safe


def monthly_visits_chart(monthly_df: pd.DataFrame):
    fig = px.line(
        monthly_df, x='month', y='visits',
        title='Monthly Patient Visits',
        markers=True,
        labels={'month': 'Month', 'visits': 'Number of Visits'},
    )
    fig.update_traces(line_color='#3b82d4', line_width=2)
    fig.update_layout(title_font_size=14)
    return fig


def department_bar(df: pd.DataFrame):
    counts = df['department'].value_counts().reset_index()
    counts.columns = ['department', 'visits']
    fig = px.bar(
        counts, x='visits', y='department', orientation='h',
        title='Visits by Department',
        labels={'visits': 'Number of Visits', 'department': ''},
        color='department', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig


def visit_type_pie(df: pd.DataFrame):
    counts = df['visit_type'].value_counts().reset_index()
    counts.columns = ['visit_type', 'count']
    fig = px.pie(
        counts, names='visit_type', values='count',
        title='Visit Type Distribution',
        color_discrete_sequence=['#3b82d4', '#f44336'],
    )
    fig.update_layout(title_font_size=14)
    return fig


def risk_distribution_bar(risk_df: pd.DataFrame):
    fig = px.bar(
        risk_df, x='risk', y='count',
        title='Readmission Risk Distribution',
        text='pct',
        labels={'risk': 'Risk Category', 'count': 'Number of Patients'},
        color='risk',
        color_discrete_map=RISK_COLORS,
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig


def cost_by_dept_bar(dept_df: pd.DataFrame):
    fig = px.bar(
        dept_df.sort_values('avg_cost'), x='avg_cost', y='department', orientation='h',
        title='Average Treatment Cost by Department',
        labels={'avg_cost': 'Avg Cost (USD)', 'department': ''},
        color='department', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    fig.update_xaxes(tickformat='$,.0f')
    return fig


def cost_by_treatment_bar(cost_df: pd.DataFrame):
    fig = px.bar(
        cost_df, x='treatment_type', y='avg_cost',
        title='Average Treatment Cost by Treatment Type',
        labels={'treatment_type': 'Treatment Type', 'avg_cost': 'Avg Cost (USD)'},
        color='treatment_type', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    fig.update_yaxes(tickformat='$,.0f')
    return fig


def los_by_dept_bar(dept_df: pd.DataFrame):
    fig = px.bar(
        dept_df.sort_values('avg_los'), x='avg_los', y='department', orientation='h',
        title='Average Length of Stay by Department',
        labels={'avg_los': 'Avg LOS (days)', 'department': ''},
        color='department', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig


def cost_vs_los_scatter(df: pd.DataFrame):
    sample = df.sample(min(1000, len(df)), random_state=42) if len(df) > 1000 else df
    fig = px.scatter(
        sample, x='length_of_stay_days', y='treatment_cost',
        color='department', opacity=0.5,
        title='Treatment Cost vs Length of Stay',
        labels={'length_of_stay_days': 'LOS (days)', 'treatment_cost': 'Treatment Cost (USD)'},
        color_discrete_sequence=PALETTE,
    )
    fig.update_yaxes(tickformat='$,.0f')
    fig.update_layout(title_font_size=14)
    return fig


def risk_by_dept_stacked(risk_dept_df: pd.DataFrame):
    fig = go.Figure()
    for risk, color in RISK_COLORS.items():
        if risk in risk_dept_df.columns:
            fig.add_trace(go.Bar(
                name=risk,
                x=risk_dept_df['department'],
                y=risk_dept_df[risk],
                marker_color=color,
            ))
    fig.update_layout(
        barmode='stack',
        title='Readmission Risk by Department (%)',
        xaxis_title='Department',
        yaxis_title='% of Patients',
        title_font_size=14,
    )
    return fig


def risk_by_age_grouped(risk_age_df: pd.DataFrame):
    fig = go.Figure()
    for risk, color in RISK_COLORS.items():
        if risk in risk_age_df.columns:
            fig.add_trace(go.Bar(
                name=risk,
                x=risk_age_df['age_group'],
                y=risk_age_df[risk],
                marker_color=color,
            ))
    fig.update_layout(
        barmode='group',
        title='Readmission Risk by Age Group (%)',
        xaxis_title='Age Group',
        yaxis_title='% of Patients',
        title_font_size=14,
    )
    return fig


def recovery_by_dept_bar(dept_df: pd.DataFrame):
    fig = px.bar(
        dept_df.sort_values('avg_recovery'), x='avg_recovery', y='department', orientation='h',
        title='Average Recovery Score by Department',
        labels={'avg_recovery': 'Avg Recovery Score', 'department': ''},
        color='department', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    fig.update_xaxes(range=[70, 76])
    return fig


def recovery_vs_risk_box(df: pd.DataFrame):
    fig = px.box(
        df, x='readmission_risk', y='recovery_score',
        category_orders={'readmission_risk': ['Low', 'Medium', 'High']},
        color='readmission_risk',
        color_discrete_map=RISK_COLORS,
        title='Recovery Score by Readmission Risk',
        labels={'readmission_risk': 'Risk Category', 'recovery_score': 'Recovery Score'},
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig


def age_distribution_bar(df: pd.DataFrame):
    age_order = ['18-30', '31-45', '46-60', '60+']
    counts = df['age_group'].value_counts().reindex(age_order, fill_value=0).reset_index()
    counts.columns = ['age_group', 'count']
    fig = px.bar(
        counts, x='age_group', y='count',
        title='Patient Distribution by Age Group',
        labels={'age_group': 'Age Group', 'count': 'Count'},
        color='age_group', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig


def region_distribution_bar(df: pd.DataFrame):
    counts = df['region'].value_counts().reset_index()
    counts.columns = ['region', 'count']
    fig = px.bar(
        counts, x='region', y='count',
        title='Patient Distribution by Region',
        labels={'region': 'Region', 'count': 'Count'},
        color='region', color_discrete_sequence=PALETTE,
    )
    fig.update_layout(showlegend=False, title_font_size=14)
    return fig
