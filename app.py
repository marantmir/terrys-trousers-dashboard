import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página e tema visual
st.set_page_config(
    page_title="Terry's Trousers - Financial Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (DESIGN PREMIUM DARK) ---
st.markdown("""
    <style>
    /* Alterar fundo da aplicação e fontes */
    .stApp {
        background-color: #0E1117;
        color: #ECF0F1;
    }
    
    /* Customização dos Cards de Métrica */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #00F2FE !important; /* Ciano Neon */
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8A9A86 !important;
    }
    
    /* Estilização da Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #161A24 !important;
        border-right: 1px solid #2D3748;
    }
    
    /* Headers customizados */
    h1 {
        font-weight: 800 !important;
        background: -webkit-linear-gradient(#00F2FE, #4FACFE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 20px;
    }
    
    h3 {
        color: #A0AEC0 !important;
        font-weight: 600 !important;
    }
    
    /* Customização de Tabelas */
    .dataframe {
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DADOS INICIAIS ---
dados_iniciais = {
    'Product Category': ['Classic Chinos', 'Slim-Fit Denim', 'Corduroy Slacks', 'Baggy Cargo', 'Wool Dress Trousers'],
    'Orders': [120, 200, 85, 450, 110],
    'AOV': [85.0, 110.0, 95.0, 140.0, 125.0],
    'Return Rate': [0.20, 0.28, 0.20, 0.36, 0.30],
    'Cost Per Return': [12.50, 14.00, 12.50, 15.00, 13.50]
}

df_base = pd.DataFrame(dados_iniciais)
df_base['Gross Revenue'] = df_base['Orders'] * df_base['AOV']
df_base['Returns (Units)'] = (df_base['Orders'] * df_base['Return Rate']).round().astype(int)
df_base['Total Return Cost'] = df_base['Returns (Units)'] * df_base['Cost Per Return']
df_base['Net Revenue'] = df_base['Gross Revenue'] - df_base['Total Return Cost']

lucro_liquido_original = df_base['Net Revenue'].sum()

# --- SIDEBAR (CONTROLES COM CORES DE DESTAQUE) ---
st.sidebar.markdown("<h2 style='color:#00F2FE; font-size:1.5rem; font-weight:700;'>🎛️ Centro de Comando</h2>", unsafe_allow_html=True)
st.sidebar.write("Ajuste as estratégias operacionais em tempo real:")
st.sidebar.markdown("---")

# Mudança 1: Baggy Cargo
st.sidebar.markdown("<b style='color:#4FACFE;'>1. Linha Baggy Cargo</b>", unsafe_allow_html=True)
aplicar_m1 = st.sidebar.toggle("Ativar correção de Fit/Tamanho", value=True, key="m1")
taxa_retorno_cargo = df_base.loc[3, 'Return Rate']
if aplicar_m1:
    taxa_retorno_cargo = st.sidebar.slider("Nova Taxa de Devolução Cargo (%)", min_value=10, max_value=36, value=20) / 100

st.sidebar.markdown("---")

# Mudança 2: Slim-Fit Denim
st.sidebar.markdown("<b style='color:#4FACFE;'>2. Linha Slim-Fit Denim</b>", unsafe_allow_html=True)
aplicar_m2 = st.sidebar.toggle("Otimizar Logística Reversa", value=True, key="m2")
custo_retorno_denim = df_base.loc[1, 'Cost Per Return']
taxa_retorno_denim = df_base.loc[1, 'Return Rate']
if aplicar_m2:
    taxa_retorno_denim = st.sidebar.slider("Nova Taxa de Devolução Denim (%)", min_value=15, max_value=28, value=22) / 100
    custo_retorno_denim = st.sidebar.slider("Redução Custo de Coleta ($)", min_value=10.0, max_value=14.0, value=11.50)

st.sidebar.markdown("---")

# Mudança 3: Escalar Eficientes
st.sidebar.markdown("<b style='color:#4FACFE;'>3. Escalar Produtos Eficientes</b>", unsafe_allow_html=True)
aplicar_m3 = st.sidebar.toggle("Redirecionar Tráfego (Chinos/Corduroy)", value=False, key="m3")
aumento_pedidos = 0
if aplicar_m3:
    aumento_pedidos = st.sidebar.slider("Impulsionar Pedidos (%)", min_value=0, max_value=100, value=40) / 100

# --- CÁLCULOS DO CENÁRIO SIMULADO ---
df_simulado = df_base.copy()
df_simulado.loc[3, 'Return Rate'] = taxa_retorno_cargo
df_simulado.loc[1, 'Return Rate'] = taxa_retorno_denim
df_simulado.loc[1, 'Cost Per Return'] = custo_retorno_denim

if aplicar_m3:
    df_simulado.loc[0, 'Orders'] = int(df_simulado.loc[0, 'Orders'] * (1 + aumento_pedidos))
    df_simulado.loc[2, 'Orders'] = int(df_simulado.loc[2, 'Orders'] * (1 + aumento_pedidos))

df_simulado['Gross Revenue'] = df_simulado['Orders'] * df_simulado['AOV']
df_simulado['Returns (Units)'] = (df_simulado['Orders'] * df_simulado['Return Rate']).round().astype(int)
df_simulado['Total Return Cost'] = df_simulado['Returns (Units)'] * df_simulado['Cost Per Return']
df_simulado['Net Revenue'] = df_simulado['Gross Revenue'] - df_simulado['Total Return Cost']

lucro_liquido_simulado = df_simulado['Net Revenue'].sum()
variacao_lucro = lucro_liquido_simulado - lucro_liquido_original
percentual_ganho = (variacao_lucro / lucro_liquido_original) * 100

# --- LAYOUT PRINCIPAL ---
st.title("Terry's Trousers • Calculadora de Lucro Interativa")

# KPIs do Topo com design de painel financeiro
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Lucro Líquido Base", value=f"${lucro_liquido_original:,.2f}")
with kpi2:
    cor_delta = "normal" if variacao_lucro >= 0 else "inverse"
    st.metric(label="Lucro Líquido Projetado", value=f"${lucro_liquido_simulado:,.2f}", delta=f"+${variacao_lucro:,.2f}")
with kpi3:
    st.metric(label="Eficiência de Lucro Marginal", value=f"{percentual_ganho:.1f}%", delta=f"{percentual_ganho:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# --- GRÁFICO CUSTOMIZADO PLOTLY (DESIGN EXECUTIVO) ---
st.subheader("📊 Impacto no Lucro Líquido por Categoria de Produto")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_base['Product Category'],
    y=df_base['Net Revenue'],
    name='Cenário Inicial',
    marker_color='#26A69A', # Verde Pastel
    opacity=0.6
))
fig.add_trace(go.Bar(
    x=df_simulado['Product Category'],
    y=df_simulado['Net Revenue'],
    name='Cenário Otimizado',
    marker_color='#00F2FE' # Neon Ciano
))

fig.update_layout(
    barmode='group',
    template='plotly_dark',
    background_color='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor='#2D3748', title="Lucro Líquido ($)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=10, b=10)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- SEÇÃO DE TABELAS COMPARATIVAS ---
st.subheader("📋 Auditoria de Métricas (Original vs Simulado)")

df_vis_original = df_base[['Product Category', 'Orders', 'Return Rate', 'Total Return Cost', 'Net Revenue']].copy()
df_vis_original['Return Rate'] = (df_vis_original['Return Rate'] * 100).map('{:.1f}%'.format)

df_vis_simulado = df_simulado[['Product Category', 'Orders', 'Return Rate', 'Total Return Cost', 'Net Revenue']].copy()
df_vis_simulado['Return Rate'] = (df_vis_simulado['Return Rate'] * 100).map('{:.1f}%'.format)

c1, c2 = st.columns(2)
with c1:
    st.write("📉 **Performance Operacional Atual**")
    st.dataframe(
        df_vis_original.style.format({'Total Return Cost': '${:,.2f}', 'Net Revenue': '${:,.2f}'}),
        use_container_width=True,
        hide_index=True
    )

with c2:
    st.write("🚀 **Projeção com Alavancas Ativadas**")
    st.dataframe(
        df_vis_simulado.style.format({'Total Return Cost': '${:,.2f}', 'Net Revenue': '${:,.2f}'}),
        use_container_width=True,
        hide_index=True
    )