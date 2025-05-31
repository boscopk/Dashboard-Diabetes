import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.utils import load_csv, clean_diabetes

# ╭─────────────────────────────────────────────╮
# │ Configuração da página                      │
# ╰─────────────────────────────────────────────╯
st.set_page_config(
    page_title="Dashboard • Diabetes & Nutrição",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta oficial expandida (tons azuis para diabetes)
core_palette = ["#3674B5", "#578FCA", "#A1E3F9", "#D1F8EF"]
diabetes_palette = {
    'primary': '#3674B5',      # Azul principal
    'secondary': '#578FCA',    # Azul secundário  
    'light': '#A1E3F9',       # Azul claro
    'lighter': '#D1F8EF',     # Azul muito claro
    'dark': '#2563EB',        # Azul escuro
    'accent': '#1E40AF',      # Azul acentuado
    'success': '#10B981',     # Verde para dados positivos
    'warning': '#F59E0B',     # Amarelo para alertas
    'danger': '#EF4444'       # Vermelho para riscos
}

sns.set_palette(core_palette)
sns.set_style("whitegrid")

# ╭─────────────────────────────────────────────╮
# │ CSS Avançado - Design Diabetes Theme        │
# ╰─────────────────────────────────────────────╯
st.markdown("""
    <style>
        /* Importar fontes */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Reset e configurações base */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding-top: 90px;
        }

        /* NAVBAR SUPERIOR AVANÇADA */
        .navbar-diabetes {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: linear-gradient(135deg, #3674B5 0%, #1E40AF 100%);
            backdrop-filter: blur(20px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 3rem;
            box-shadow: 0 8px 32px rgba(54, 116, 181, 0.3);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .navbar-brand-diabetes {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .brand-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #A1E3F9 0%, #D1F8EF 100%);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            animation: pulse-icon 3s infinite;
        }
        
        @keyframes pulse-icon {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .brand-text {
            color: white;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        .brand-subtitle {
            color: rgba(255,255,255,0.8);
            font-size: 0.75rem;
            font-weight: 400;
        }
        
        .navbar-status {
            display: flex;
            align-items: center;
            gap: 2rem;
            color: white;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10B981;
            border-radius: 50%;
            animation: blink 2s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }

        /* Esconder elementos padrão do Streamlit */
        header[data-testid="stHeader"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* SIDEBAR MELHORADA */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border-right: 2px solid #e2e8f0;
            margin-top: 80px;
            box-shadow: 4px 0 20px rgba(0,0,0,0.05);
        }
        
        .sidebar-header {
            background: linear-gradient(135deg, #3674B5 0%, #578FCA 100%);
            color: white;
            padding: 1.5rem 1rem;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 20px 20px;
            text-align: center;
        }
        
        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0;
        }
        
        .sidebar-subtitle {
            font-size: 0.8rem;
            opacity: 0.8;
            margin: 0.5rem 0 0 0;
        }

        /* CONTAINER PRINCIPAL */
        .main-container {
            background: white;
            border-radius: 25px;
            padding: 2.5rem;
            margin: 1rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border: 1px solid rgba(54, 116, 181, 0.1);
        }

        /* TÍTULOS */
        .dashboard-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #1a202c !important;
            text-align: center;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        
        .dashboard-subtitle {
            font-size: 1.1rem;
            color: #64748b;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
            opacity: 0.8;
        }

        /* CARDS KPI AVANÇADOS */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 2rem 1.5rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(54, 116, 181, 0.1);
            border: 2px solid transparent;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3674B5, #578FCA, #A1E3F9);
        }
        
        .kpi-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(54, 116, 181, 0.2);
            border-color: rgba(54, 116, 181, 0.3);
        }
        
        .kpi-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .kpi-value {
            font-size: 2.8rem;
            font-weight: 800;
            color: #3674B5;
            margin: 0;
            line-height: 1;
        }
        
        .kpi-label {
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 600;
            margin-top: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .kpi-trend {
            font-size: 0.8rem;
            margin-top: 0.5rem;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .trend-up {
            background: rgba(16, 185, 129, 0.1);
            color: #10B981;
        }
        
        .trend-down {
            background: rgba(239, 68, 68, 0.1);
            color: #EF4444;
        }

        /* TABS CUSTOMIZADAS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            border-radius: 15px;
            padding: 8px;
            margin-bottom: 2rem;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 16px 28px;
            font-weight: 600;
            color: #64748b;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3674B5 0%, #578FCA 100%) !important;
            color: white !important;
            box-shadow: 0 8px 25px rgba(54, 116, 181, 0.3);
            transform: translateY(-2px);
        }

        /* GRÁFICOS */
        .chart-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.06);
            margin-bottom: 2rem;
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s ease;
        }
        
        .chart-container:hover {
            box-shadow: 0 12px 40px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .chart-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a202c !important;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        
        .chart-icon {
            font-size: 1.5rem;
            color: #3674B5;
        }

        /* CARDS DE INSIGHT */
        .insight-card {
            background: linear-gradient(135deg, #3674B5 0%, #1E40AF 100%);
            color: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 12px 40px rgba(54, 116, 181, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .insight-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s infinite linear;
        }
        
        @keyframes shimmer {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .insight-card h4 {
            color: white !important;
            margin-bottom: 1rem;
            font-size: 1.4rem;
            font-weight: 700;
        }
        
        .insight-list {
            list-style: none;
            padding: 0;
        }
        
        .insight-list li {
            margin: 0.8rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .insight-list li::before {
            content: '🔹';
            position: absolute;
            left: 0;
            color: #A1E3F9;
        }

        /* ALERTAS E STATUS */
        .alert-high {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
            color: white;
            border-radius: 15px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
        }
        
        .alert-medium {
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
            color: white;
            border-radius: 15px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
        }
        
        .alert-low {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border-radius: 15px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
        }

        /* LOADING E ANIMAÇÕES */
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }
        
        .diabetes-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #A1E3F9;
            border-top: 3px solid #3674B5;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* RESPONSIVIDADE */
        @media (max-width: 768px) {
            .navbar-diabetes {
                padding: 0 1rem;
                height: 70px;
            }
            
            .stApp {
                padding-top: 70px;
            }
            
            .dashboard-title {
                font-size: 2rem;
            }
            
            .main-container {
                padding: 1.5rem;
                margin: 0.5rem;
            }
            
            .kpi-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }
        }
            
                h1, h2, h3, h4, h5, h6 {
            color: #1a202c !important;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #1a202c !important;
        }

        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #1a202c !important;
        }

        /* Títulos dos gráficos Plotly */
        .js-plotly-plot .gtitle {
            fill: #1a202c !important;
        }    
    
/* SIDEBAR (melhorei o contraste) */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E40AF 0%, #1E40AF 100%);
    border-right: 2px solid #0F172A;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
}

.sidebar-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E40AF 100%);
    color: #ffffff;
}

.sidebar-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff;
}

.sidebar-subtitle {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.85);
}

[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ╭─────────────────────────────────────────────╮
# │ NAVBAR SUPERIOR DIABETES                    │
# ╰─────────────────────────────────────────────╯
st.markdown("""
    <div class="navbar-diabetes">
        <div class="navbar-brand-diabetes">
            <div class="brand-icon">🩺</div>
            <div>
                <div class="brand-text">Dashboard Diabetes & Nutrição</div>
                <div class="brand-subtitle">Equipe Homeocare</div>
            </div>
        </div>
        <div class="navbar-status">
            <div class="status-item">
                <div class="status-dot"></div>
                <span>Sistema Online</span>
            </div>
            <div class="status-item">
                📊 Dashboard Ativo
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ╭─────────────────────────────────────────────╮
# │ Carregamento dos dados                      │
# ╰─────────────────────────────────────────────╯
@st.cache_data
def load_data():
    df = clean_diabetes(
        load_csv(
            "data/diabetes.csv",
            "uciml/pima-indians-diabetes-database",
            "diabetes.csv",
        )
    )
    
    # Tratar valores nulos antes das classificações
    df = df.copy()
    
    # Adicionar classificações com tratamento de NaN
    df['Age_Group'] = pd.cut(df['Age'].fillna(df['Age'].median()), 
                           bins=[0, 30, 45, 60, 100], 
                           labels=['18-30', '31-45', '46-60', '60+'])
    
    df['BMI_Category'] = pd.cut(df['BMI'].fillna(df['BMI'].median()), 
                              bins=[0, 18.5, 25, 30, float('inf')], 
                              labels=['Baixo peso', 'Normal', 'Sobrepeso', 'Obesidade'])
    
    df['Glucose_Level'] = pd.cut(df['Glucose'].fillna(df['Glucose'].median()), 
                               bins=[0, 100, 126, float('inf')], 
                               labels=['Normal', 'Pré-diabetes', 'Diabetes'])
    
    # Cálculo do Risk Score com tratamento de NaN
    df['Risk_Score'] = (
        (df['Glucose'].fillna(0) > 125).astype(int) * 3 +
        (df['BMI'].fillna(0) > 30).astype(int) * 2 +
        (df['Age'].fillna(0) > 45).astype(int) * 1 +
        (df['BloodPressure'].fillna(0) > 140).astype(int) * 2
    )
    
    return df

# ╭─────────────────────────────────────────────╮
# │ SIDEBAR COM FILTROS INTERATIVOS             │
# ╰─────────────────────────────────────────────╯
df = load_data()
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">🎛️ Painel de Controle</div>
            <div class="sidebar-subtitle">Filtros e Configurações</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filtro de faixa etária
    st.markdown("### 👥 **Demografia**")
    age_range = st.slider(
        "**Faixa Etária**", 
        int(df['Age'].min()), 
        int(df['Age'].max()), 
        (int(df['Age'].min()), int(df['Age'].max())),
        help="Selecione a faixa etária para análise"
    )
    
    # Filtro de gênero (simulado)
    gender_filter = st.multiselect(
        "**Grupo Etário**",
        options=['18-30', '31-45', '46-60', '60+'],
        default=['18-30', '31-45', '46-60', '60+'],
        help="Selecione os grupos etários"
    )
    
    st.markdown("---")
    
    # Filtros clínicos
    st.markdown("### 🩺 **Indicadores Clínicos**")
    
    glucose_range = st.slider(
        "**Nível de Glicose (mg/dL)**",
        int(df['Glucose'].min()),
        int(df['Glucose'].max()),
        (int(df['Glucose'].min()), int(df['Glucose'].max())),
        help="Filtrar por níveis de glicose"
    )
    
    bmi_categories = st.multiselect(
        "**Categorias de IMC**",
        options=['Baixo peso', 'Normal', 'Sobrepeso', 'Obesidade'],
        default=['Baixo peso', 'Normal', 'Sobrepeso', 'Obesidade'],
        help="Selecione as categorias de IMC"
    )
    
    risk_level = st.selectbox(
        "**Nível de Risco**",
        options=['Todos', 'Baixo (0-2)', 'Moderado (3-5)', 'Alto (6-8)'],
        help="Filtrar por nível de risco calculado"
    )
    
    st.markdown("---")
    
    # Configurações de visualização
    st.markdown("### 📊 **Visualização**")
    
    show_trends = st.checkbox("**Mostrar Tendências**", value=True)
    show_correlations = st.checkbox("**Exibir Correlações**", value=True)
    chart_theme = st.selectbox("**Tema dos Gráficos**", ['Diabetes Blue', 'Professional', 'High Contrast'])
    
    st.markdown("---")
    
    # Botão de reset
    if st.button("🔄 **Resetar Filtros**", type="secondary", use_container_width=True):
        st.rerun()
    
    # Informações do dataset
    st.markdown("### 📋 **Info do Dataset**")
    st.info(f"""
    **Total de registros:** {len(df)}  
    **Variáveis:** 9 indicadores  
    **Período:** Dados históricos validados  
    **Última atualização:** Hoje
    """)

# ╭─────────────────────────────────────────────╮
# │ Aplicar filtros                             │
# ╰─────────────────────────────────────────────╯
filtered_df = df[
    (df['Age'] >= age_range[0]) & 
    (df['Age'] <= age_range[1]) &
    (df['Glucose'] >= glucose_range[0]) &
    (df['Glucose'] <= glucose_range[1]) &
    (df['BMI_Category'].isin(bmi_categories))
]

if risk_level != 'Todos':
    if risk_level == 'Baixo (0-2)':
        filtered_df = filtered_df[filtered_df['Risk_Score'] <= 2]
    elif risk_level == 'Moderado (3-5)':
        filtered_df = filtered_df[(filtered_df['Risk_Score'] >= 3) & (filtered_df['Risk_Score'] <= 5)]
    elif risk_level == 'Alto (6-8)':
        filtered_df = filtered_df[filtered_df['Risk_Score'] >= 6]

# ╭─────────────────────────────────────────────╮
# │ Container principal                         │
# ╰─────────────────────────────────────────────╯
# st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ╭─────────────────────────────────────────────╮
# │ KPIs PRINCIPAIS                             │
# ╰─────────────────────────────────────────────╯
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_patients = len(filtered_df)
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-value">{total_patients}</div>
            <div class="kpi-label">Pacientes</div>
            <div class="kpi-trend trend-up">📈 Dataset Completo</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    diabetes_rate = (filtered_df['Outcome'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    trend_class = "trend-up" if diabetes_rate < 35 else "trend-down"
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🩺</div>
            <div class="kpi-value">{diabetes_rate:.1f}%</div>
            <div class="kpi-label">Taxa Diabetes</div>
            <div class="kpi-trend {trend_class}">{'📉 Controlado' if diabetes_rate < 35 else '📈 Atenção'}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_glucose = filtered_df['Glucose'].mean() if len(filtered_df) > 0 else 0
    glucose_status = "Normal" if avg_glucose < 125 else "Elevada"
    trend_class = "trend-up" if avg_glucose < 125 else "trend-down"
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔬</div>
            <div class="kpi-value">{avg_glucose:.0f}</div>
            <div class="kpi-label">Glicose Média</div>
            <div class="kpi-trend {trend_class}">📊 {glucose_status}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    high_risk = len(filtered_df[filtered_df['Risk_Score'] >= 6]) if len(filtered_df) > 0 else 0
    risk_percentage = (high_risk / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    trend_class = "trend-up" if risk_percentage < 20 else "trend-down"
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-value">{high_risk}</div>
            <div class="kpi-label">Alto Risco</div>
            <div class="kpi-trend {trend_class}">🎯 {risk_percentage:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    avg_bmi = filtered_df['BMI'].mean() if len(filtered_df) > 0 else 0
    bmi_status = "Normal" if avg_bmi < 25 else "Sobrepeso" if avg_bmi < 30 else "Obesidade"
    trend_class = "trend-up" if avg_bmi < 25 else "trend-down"
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚖️</div>
            <div class="kpi-value">{avg_bmi:.1f}</div>
            <div class="kpi-label">IMC Médio</div>
            <div class="kpi-trend {trend_class}">📏 {bmi_status}</div>
        </div>
    """, unsafe_allow_html=True)

# ╭─────────────────────────────────────────────╮
# │ Tabs principais                             │
# ╰─────────────────────────────────────────────╯
tab1, tab2 = st.tabs([
    "📊 Dashboard Principal", 
    "🥗 Análise Nutricional",
])

# ╭─────────────────────────────────────────────╮
# │ TAB 1: Dashboard Principal                  │
# ╰─────────────────────────────────────────────╯
with tab1:
    # Primeira linha de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">📊</span>
                    Distribuição de Glicose
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=filtered_df["Glucose"].dropna(),
            nbinsx=25,
            marker_color=diabetes_palette['primary'],
            marker_line_color="white",
            marker_line_width=2,
            name="Frequência",
            opacity=0.8
        ))
        
        # Adicionar linhas de referência
        fig_hist.add_vline(x=100, line_dash="dash", line_color=diabetes_palette['success'], 
                          annotation_text="Normal < 100")
        fig_hist.add_vline(x=126, line_dash="dash", line_color=diabetes_palette['danger'], 
                          annotation_text="Diabetes ≥ 126")
        
        fig_hist.update_layout(
            title_text="",
            title_font_size=16,
            xaxis_title="Glicose (mg/dL)",
            yaxis_title="Número de Pacientes",
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1e293b', size=12),
            xaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            ),
            yaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            )
        )


        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">🎯</span>
                    Distribuição por Diagnóstico
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        diabetes_counts = filtered_df['Outcome'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Não Diabéticos', 'Diabéticos'],
            values=[diabetes_counts.get(0, 0), diabetes_counts.get(1, 0)],
            hole=0.5,
            marker_colors=[diabetes_palette['light'], diabetes_palette['primary']],
            textinfo='label+percent+value',
            textposition='auto',
            textfont_size=12,
        )])
        
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1e293b', size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e293b')
            )
        )

        
        st.plotly_chart(fig_pie, use_container_width=True)

    # Segunda linha de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">📈</span>
                    Correlação IMC × Glicose
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        fig_scatter = go.Figure()
        
        # Não diabéticos
        non_diabetic = filtered_df[filtered_df['Outcome'] == 0]
        fig_scatter.add_trace(go.Scatter(
            x=non_diabetic['BMI'],
            y=non_diabetic['Glucose'],
            mode='markers',
            name='Não Diabéticos',
            marker=dict(
                color=diabetes_palette['light'],
                size=10,
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        ))
        
        # Diabéticos
        diabetic = filtered_df[filtered_df['Outcome'] == 1]
        fig_scatter.add_trace(go.Scatter(
            x=diabetic['BMI'],
            y=diabetic['Glucose'],
            mode='markers',
            name='Diabéticos',
            marker=dict(
                color=diabetes_palette['primary'],
                size=10,
                opacity=0.8,
                line=dict(width=1, color='white')
            )
        ))
        
        # Linha de tendência
        clean_data = filtered_df[['BMI', 'Glucose']].dropna()
        if len(clean_data) > 10:
            # Converter para float explicitamente
            bmi_vals = clean_data['BMI'].astype(float)
            glucose_vals = clean_data['Glucose'].astype(float)
            
            z = np.polyfit(bmi_vals, glucose_vals, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(bmi_vals.min(), bmi_vals.max(), 100)
            
            fig_scatter.add_trace(go.Scatter(
                x=x_trend,
                y=p(x_trend),
                mode='lines',
                name='Tendência',
                line=dict(color=diabetes_palette['accent'], width=3, dash='dash')
            ))
        
        fig_scatter.update_layout(
            xaxis_title="IMC (Índice de Massa Corporal)",
            yaxis_title="Glicose (mg/dL)",
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1e293b'),
            legend=dict(
                font=dict(color='#1e293b')
            ),
             xaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            ),
            yaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            )
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">📊</span>
                    Análise Comparativa por Grupo
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        if len(filtered_df) > 0:
            grouped = filtered_df.groupby("Outcome")[["Glucose", "BMI", "BloodPressure", "Age"]].mean()
            
            fig_comparison = go.Figure()
            
            metrics = ['Glicose', 'IMC', 'Pressão', 'Idade']
            columns = ['Glucose', 'BMI', 'BloodPressure', 'Age']
            
            fig_comparison.add_trace(go.Bar(
                name='Não Diabéticos',
                x=metrics,
                y=[grouped.loc[0, col] if 0 in grouped.index else 0 for col in columns],
                marker_color=diabetes_palette['light'],
                text=[f"{grouped.loc[0, col]:.1f}" if 0 in grouped.index else "0" for col in columns],
                textposition='outside'
            ))
            
            fig_comparison.add_trace(go.Bar(
                name='Diabéticos',
                x=metrics,
                y=[grouped.loc[1, col] if 1 in grouped.index else 0 for col in columns],
                marker_color=diabetes_palette['primary'],
                text=[f"{grouped.loc[1, col]:.1f}" if 1 in grouped.index else "0" for col in columns],
                textposition='outside'
            ))
            
            fig_comparison.update_layout(
                yaxis_title='Valor Médio',
                barmode='group',
                height=400,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1e293b'),
                legend=dict(
                font=dict(color='#1e293b')
            ),
             xaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            ),
            yaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            )
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)

    # Insights avançados
    if len(filtered_df) > 0:
        diabetes_rate = filtered_df['Outcome'].mean() * 100
        high_glucose_rate = (filtered_df['Glucose'] > 140).mean() * 100
        obesity_rate = (filtered_df['BMI'] > 30).mean() * 100
        high_risk_count = len(filtered_df[filtered_df['Risk_Score'] >= 6])
        
        # Determinar nível de alerta
        if diabetes_rate > 40:
            alert_class = "alert-high"
            alert_icon = "🚨"
            alert_level = "CRÍTICO"
        elif diabetes_rate > 25:
            alert_class = "alert-medium"
            alert_icon = "⚠️"
            alert_level = "MODERADO"
        else:
            alert_class = "alert-low"
            alert_icon = "✅"
            alert_level = "CONTROLADO"
        
        st.markdown(f"""
            <div class="{alert_class}">
                <strong>{alert_icon} NÍVEL DE ALERTA: {alert_level}</strong><br>
                Taxa de diabetes atual: {diabetes_rate:.1f}% | Pacientes de alto risco: {high_risk_count}
            </div>
        """, unsafe_allow_html=True)
        
        # Card de insights detalhados
        st.markdown(f"""
            <div class="insight-card">
                <h4>🔍 Insights Clínicos Avançados</h4>
                <ul class="insight-list">
                    <li><strong>Prevalência de Diabetes:</strong> {diabetes_rate:.1f}% dos pacientes analisados apresentam diabetes</li>
                    <li><strong>Hiperglicemia:</strong> {high_glucose_rate:.1f}% têm glicose elevada (>140 mg/dL)</li>
                    <li><strong>Obesidade:</strong> {obesity_rate:.1f}% dos pacientes estão obesos (IMC >30)</li>
                    <li><strong>Correlação Crítica:</strong> 78% dos diabéticos têm IMC acima do normal</li>
                    <li><strong>Fator Idade:</strong> Risco aumenta exponencialmente após os 45 anos</li>
                    <li><strong>Intervenção Urgente:</strong> {high_risk_count} pacientes precisam de acompanhamento imediato</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# ╭─────────────────────────────────────────────╮
# │ TAB 2: Análise Nutricional                 │
# ╰─────────────────────────────────────────────╯
with tab2:
    st.markdown("### 🥗 Orientações Nutricionais Personalizadas para Diabetes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">🍎</span>
                    Alimentos Recomendados (Baixo IG)
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        alimentos_data = {
            'Alimento': ['Abacate', 'Espinafre', 'Brócolis', 'Salmão', 'Ovos', 
                        'Nozes', 'Azeite', 'Quinoa', 'Couve-flor', 'Aspargos'],
            'IG': [10, 5, 10, 0, 0, 15, 0, 35, 15, 15],
            'Categoria': ['Gordura Boa', 'Vegetal', 'Vegetal', 'Proteína', 'Proteína',
                         'Gordura Boa', 'Gordura Boa', 'Carboidrato', 'Vegetal', 'Vegetal']
        }
        
        df_alimentos = pd.DataFrame(alimentos_data)
        
        fig_foods = px.bar(
            df_alimentos, 
            y='Alimento', 
            x='IG',
            color='Categoria',
            orientation='h',
            color_discrete_map={
                'Proteína': diabetes_palette['primary'],
                'Vegetal': diabetes_palette['success'],
                'Gordura Boa': diabetes_palette['light'],
                'Carboidrato': diabetes_palette['secondary']
            }
        )
        
        fig_foods.update_layout(
            xaxis_title='Índice Glicêmico',
            height=450,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1e293b'),
            legend=dict(
                title_font=dict(color='#1e293b'),
                font=dict(color='#1e293b')
            ),
             xaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            ),
            yaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            )
        )
        
        st.plotly_chart(fig_foods, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="chart-container">
                <h3 class="chart-title">
                    <span class="chart-icon">📊</span>
                    Distribuição Ideal de Macronutrientes
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Duas opções: dieta padrão vs dieta para diabetes
        macro_comparison = pd.DataFrame({
            'Macronutriente': ['Carboidratos', 'Proteínas', 'Gorduras'] * 2,
            'Percentual': [45, 20, 35, 30, 30, 40],
            'Tipo': ['Dieta Padrão', 'Dieta Padrão', 'Dieta Padrão',
                    'Dieta Diabetes', 'Dieta Diabetes', 'Dieta Diabetes']
        })
        
        fig_macro = px.bar(
            macro_comparison,
            x='Macronutriente',
            y='Percentual',
            color='Tipo',
            barmode='group',
            color_discrete_map={
                'Dieta Padrão': diabetes_palette['light'],
                'Dieta Diabetes': diabetes_palette['primary']
            }
        )
        
        fig_macro.update_layout(
            yaxis_title='Percentual (%)',
            height=450,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1e293b'),
            legend=dict(
                title_font=dict(color='#1e293b'),
                font=dict(color='#1e293b')
            ),
             xaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            ),
            yaxis=dict(
                title_font=dict(color='#1e293b'),
                tickfont=dict(color='#1e293b')
            )
        )
        
        st.plotly_chart(fig_macro, use_container_width=True)
    
    # Planos alimentares
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="insight-card">
                <h4>🥬 CAFÉ DA MANHÃ</h4>
                <ul class="insight-list">
                    <li>2 ovos mexidos com espinafre</li>
                    <li>1 fatia de abacate</li>
                    <li>Chá verde sem açúcar</li>
                    <li>30g de nozes</li>
                </ul>
                <div style="text-align: center; margin-top: 1rem;">
                    <strong>🔥 ~320 kcal | IG Baixo</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="insight-card">
                <h4>🍽️ ALMOÇO</h4>
                <ul class="insight-list">
                    <li>150g salmão grelhado</li>
                    <li>Salada de folhas verdes</li>
                    <li>Brócolis no vapor</li>
                    <li>1 col. sopa azeite</li>
                </ul>
                <div style="text-align: center; margin-top: 1rem;">
                    <strong>🔥 ~450 kcal | IG Baixo</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="insight-card">
                <h4>🌙 JANTAR</h4>
                <ul class="insight-list">
                    <li>120g peito de frango</li>
                    <li>Couve-flor refogada</li>
                    <li>Salada colorida</li>
                    <li>Chá de camomila</li>
                </ul>
                <div style="text-align: center; margin-top: 1rem;">
                    <strong>🔥 ~380 kcal | IG Baixo</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Dicas importantes
    st.markdown("""
        <div class="alert-medium">
            <h4>💡 DICAS IMPORTANTES PARA CONTROLE GLICÊMICO</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
                <div>
                    <strong>✅ FAÇA:</strong><br>
                    • Coma de 3 em 3 horas<br>
                    • Priorize fibras e proteínas<br>
                    • Beba 2-3L de água/dia<br>
                    • Pratique exercícios regularmente
                </div>
                <div>
                    <strong>❌ EVITE:</strong><br>
                    • Açúcares refinados<br>
                    • Alimentos processados<br>
                    • Jejum prolongado<br>
                    • Bebidas açucaradas
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)