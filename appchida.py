import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Análisis Bursátil - Mercado Mexicano", layout="wide")

# Título principal
st.title("📊 Análisis Bursátil - Mercado Mexicano")

# Lista de tickers válidos para el mercado mexicano
lista_tickers = [
    "WALMEX.MX", "AMXB.MX", "CEMEXCPO.MX", "LABB.MX", "CUERVO.MX", "FUNO11.MX",
    "TRAXIONA.MX", "GMEXICOB.MX", "KIMBERA.MX", "KOFUBL.MX", "GFNORTEO.MX", "VOLARA.MX",
    "BBAJIOO.MX", "ALSEA.MX", "Q.MX", "GENTERA.MX", "BOLSAA.MX", "DLRTRAC15.MX", "NAFTRACISHRS.MX"
]

# Barra lateral para entrada de usuario
st.sidebar.header("Selección de Empresa")
ticker_input = st.sidebar.selectbox("Selecciona un ticker:", lista_tickers)
st.sidebar.markdown("*Estos tickers corresponden a empresas que cotizan en la Bolsa Mexicana de Valores.*")

# Diccionario de nombres completos de las empresas mexicanas para mostrar info adicional
empresas_info = {
    "WALMEX.MX": "Walmart de México y Centroamérica",
    "AMXB.MX": "América Móvil",
    "CEMEXCPO.MX": "CEMEX",
    "LABB.MX": "Genomma Lab Internacional",
    "CUERVO.MX": "Becle (José Cuervo)",
    "FUNO11.MX": "Fibra Uno",
    "TRAXIONA.MX": "Grupo Traxión",
    "GMEXICOB.MX": "Grupo México",
    "KIMBERA.MX": "Kimberly-Clark de México",
    "KOFUBL.MX": "Coca-Cola FEMSA",
    "GFNORTEO.MX": "Grupo Financiero Banorte",
    "VOLARA.MX": "Controladora Vuela Compañía de Aviación (Volaris)",
    "BBAJIOO.MX": "Banco del Bajío",
    "ALSEA.MX": "Alsea",
    "Q.MX": "Quálitas Controladora",
    "GENTERA.MX": "Gentera",
    "BOLSAA.MX": "Grupo Bolsa Mexicana de Valores",
    "DLRTRAC15.MX": "DLRTRAC15 (ETF que sigue al dólar)",
    "NAFTRACISHRS.MX": "NAFTRAC (ETF que sigue al IPC)"
}

# Función para traducir texto al español usando deep_translator
@st.cache_data(ttl=3600)  # Cachear traducciones por 1 hora
def translate_to_spanish(text):
    if not text or text == 'No disponible':
        return "No hay descripción disponible."
    
    try:
        # Dividimos el texto en fragmentos más pequeños para evitar límites de la API
        max_length = 5000  # Google Translate tiene un límite aproximado de 5000 caracteres
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        translated_parts = []
        for part in parts:
            # Usar GoogleTranslator de deep_translator
            translation = GoogleTranslator(source='auto', target='es').translate(part)
            translated_parts.append(translation)
        
        return " ".join(translated_parts)
    except Exception as e:
        st.warning(f"No se pudo traducir la descripción: {str(e)}")
        return text  # Devolver el texto original si hay error

# Función para calcular CAGR (Compound Annual Growth Rate)
def calculate_cagr(initial_value, final_value, years):
    if initial_value <= 0 or years <= 0:
        return 0
    return (final_value / initial_value) ** (1 / years) - 1

# Función para verificar si el ticker es válido
@st.cache_data(ttl=3600)  # Cachear datos por 1 hora
def is_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Solo verificamos si podemos acceder a la información básica
        info = stock.info
        return 'longName' in info
    except:
        return False

# Función para obtener datos de la empresa
@st.cache_data(ttl=3600)  # Cachear datos por 1 hora
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        
        # Extraer la información necesaria en un diccionario
        info_dict = {}
        info = stock.info
        for key in ['longName', 'sector', 'industry', 'longBusinessSummary']:
            info_dict[key] = info.get(key, '')
        
        # Obtener datos históricos de los últimos 5 años
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5*365)
        hist_data = stock.history(start=start_date, end=end_date)
        
        # Convertir a DataFrame para asegurar serialización
        hist_data_df = pd.DataFrame(hist_data)
        
        return info_dict, hist_data_df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return {}, pd.DataFrame()

# Función para crear gráfico de precios
def create_price_chart(data, company_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Precio de Cierre', line=dict(color='#2E86C1', width=2)))
    
    fig.update_layout(
        title=f'Precios de {company_name} (Últimos 5 Años)',
        xaxis_title='Fecha',
        yaxis_title='Precio de Cierre Ajustado (MXN)',
        template='plotly_white',
        height=500,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all", label="Todo")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    return fig

# Función para calcular y mostrar métricas de rendimiento
def show_performance_metrics(data, company_name):
    # Calcular rendimientos diarios
    data['Daily Return'] = data['Close'].pct_change()
    
    # Obtener precios para diferentes períodos
    try:
        current_price = data['Close'].iloc[-1]
        price_1y_ago = data['Close'].iloc[-252] if len(data) >= 252 else data['Close'].iloc[0]
        price_3y_ago = data['Close'].iloc[-756] if len(data) >= 756 else data['Close'].iloc[0]
        price_5y_ago = data['Close'].iloc[-1260] if len(data) >= 1260 else data['Close'].iloc[0]
        
        # Calcular CAGRs
        cagr_1y = calculate_cagr(price_1y_ago, current_price, 1)
        cagr_3y = calculate_cagr(price_3y_ago, current_price, 3)
        cagr_5y = calculate_cagr(price_5y_ago, current_price, 5)
        
        # Calcular volatilidad anualizada (desviación estándar de rendimientos diarios * sqrt(252))
        daily_std = np.std(data['Daily Return'].dropna())
        annualized_std = daily_std * np.sqrt(252)
        
        # Crear dataframe para tabla de rendimientos
        returns_data = {
            'Período': ['1 año', '3 años', '5 años'],
            'Rendimiento Anualizado': [f"{cagr_1y:.2%}", f"{cagr_3y:.2%}", f"{cagr_5y:.2%}"]
        }
        
        returns_df = pd.DataFrame(returns_data)
        
        # Mostrar tabla de rendimientos
        st.header(f"📈 Rendimientos Anualizados de {company_name}")
        st.markdown("Este cálculo considera el precio al inicio y al final del periodo para determinar el rendimiento anualizado.")
        st.table(returns_df)
        
        # Mostrar medida de riesgo
        st.header("🔎 Análisis de Riesgo")
        st.markdown(f"**Volatilidad anualizada:** {annualized_std:.2%}")
        st.markdown("""
        La volatilidad anualizada es una medida del riesgo basada en la desviación estándar de los rendimientos diarios, 
        multiplicada por la raíz cuadrada de 252 (número aproximado de días de trading en un año). 
        Este valor representa la dispersión de los rendimientos respecto a su media.
        """)
        
    except Exception as e:
        st.error(f"Error al calcular métricas de rendimiento: {e}")

# Área principal - Mostrar datos si el ticker es válido
if ticker_input:
    with st.spinner(f'Cargando información de {ticker_input}...'):
        # Verificar si el ticker seleccionado es válido
        if is_valid_ticker(ticker_input):
            # Obtener datos
            info, hist_data = get_stock_data(ticker_input)
            
            if info and not hist_data.empty:
                # Información de la empresa
                company_ref = ticker_input.replace(".MX", "")
                company_name = info.get('longName', empresas_info.get(ticker_input, ticker_input))
                sector = info.get('sector', 'No disponible')
                industry = info.get('industry', 'No disponible')
                description_en = info.get('longBusinessSummary', 'No hay descripción disponible.')
                
                # Traducir sector, industria y descripción al español
                with st.spinner('Traduciendo información al español...'):
                    description_es = translate_to_spanish(description_en)
                    sector_es = translate_to_spanish(sector) if sector != 'No disponible' else sector
                    industry_es = translate_to_spanish(industry) if industry != 'No disponible' else industry
                
                # Contenedor para información de empresa
                company_container = st.container()
                with company_container:
                    st.header(f"🏢 {company_name} ({ticker_input})")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Sector:** {sector_es}")
                    with col2:
                        st.markdown(f"**Industria:** {industry_es}")
                    
                    st.subheader("Descripción de la Empresa")
                    st.markdown(description_es)
                
                # Gráfico de precios
                chart_container = st.container()
                with chart_container:
                    if not hist_data.empty:
                        price_chart = create_price_chart(hist_data, company_name)
                        st.plotly_chart(price_chart, use_container_width=True)
                    else:
                        st.warning("No se pudieron cargar datos históricos para este ticker.")
                
                # Métricas de rendimiento
                metrics_container = st.container()
                with metrics_container:
                    if not hist_data.empty:
                        show_performance_metrics(hist_data, company_name)
                    else:
                        st.warning("No se pudieron calcular métricas de rendimiento debido a la falta de datos.")
            else:
                st.error("No se pudieron obtener datos para este ticker.")
        else:
            st.error("Ticker inválido o no se pudo establecer conexión con Yahoo Finance.")

# Información adicional en la barra lateral
st.sidebar.markdown("---")
st.sidebar.subheader("Acerca de esta aplicación")
st.sidebar.markdown("""
Esta aplicación permite analizar datos bursátiles de empresas que cotizan en la Bolsa Mexicana de Valores.
Los datos se obtienen a través de Yahoo Finance.

Funcionalidades:
- Visualización de información fundamental de la empresa
- Gráfico de precios históricos
- Cálculo de rendimientos anualizados (CAGR)
- Análisis de riesgo (volatilidad)
""")

# Información del mercado mexicano
st.sidebar.markdown("---")
st.sidebar.subheader("Mercado Mexicano")
st.sidebar.markdown("""
La Bolsa Mexicana de Valores (BMV) es la segunda bolsa de valores más grande 
de Latinoamérica después de la Bolsa de São Paulo. La moneda utilizada es el peso mexicano (MXN).

El principal índice bursátil es el S&P/BMV IPC (Índice de Precios y Cotizaciones), 
que agrupa a las 35 empresas más líquidas del mercado mexicano.
""")

# Mostrar hora de actualización
st.sidebar.markdown("---")
st.sidebar.markdown(f"*Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*")