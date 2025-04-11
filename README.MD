# Análisis Bursátil - Mercado Mexicano

## Descripción

Esta aplicación de Streamlit permite analizar datos bursátiles de empresas que cotizan en la Bolsa Mexicana de Valores (BMV). Proporciona información fundamental, gráficos de precios históricos, cálculo de rendimientos anualizados y análisis de riesgo para una selección de las empresas más importantes del mercado mexicano.

## Características principales

- 📊 **Visualización de precios históricos**: Gráficos interactivos con datos de los últimos 5 años
- 📈 **Análisis de rendimiento**: Cálculo de rendimientos anualizados (CAGR) para diferentes períodos
- 🔎 **Métricas de riesgo**: Cálculo de volatilidad anualizada
- 🏢 **Información empresarial**: Resumen de la empresa, sector e industria en español
- 🌐 **Traducción automática**: Conversión de la información obtenida en inglés a español

## Requisitos previos

- Python 3.8 o superior (compatible con Python 3.13)
- Las dependencias listadas en `requirements.txt`

## Instalación

1. Clone este repositorio:
   ```
   git clone https://github.com/tu-usuario/analisis-bursatil-mexico.git
   cd analisis-bursatil-mexico
   ```

2. Cree un entorno virtual e instale las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ejecute la aplicación:
   ```
   streamlit run app.py
   ```

## Uso

1. Seleccione un ticker de la lista desplegable en la barra lateral izquierda
2. La aplicación mostrará:
   - Información general de la empresa
   - Gráfico de precios históricos con controles interactivos
   - Tabla de rendimientos anualizados para períodos de 1, 3 y 5 años
   - Análisis de riesgo con volatilidad anualizada

## Empresas incluidas

La aplicación incluye una selección de empresas relevantes del mercado mexicano, incluyendo:

- Walmart de México (WALMEX.MX)
- América Móvil (AMXB.MX)
- CEMEX (CEMEXCPO.MX)
- Grupo México (GMEXICOB.MX)
- Banorte (GFNORTEO.MX)
- Volaris (VOLARA.MX)
- Y muchas más...

También incluye ETFs importantes como NAFTRAC (que sigue al IPC) y DLRTRAC (que sigue al dólar).

## Estructura del código

- `appchida.py`: Archivo principal de la aplicación
- `requirements.txt`: Lista de dependencias
- `README.md`: Documentación del proyecto

## Tecnologías utilizadas

- **Streamlit**: Framework para la creación de aplicaciones web de ciencia de datos
- **yfinance**: API para obtener datos financieros de Yahoo Finance
- **Pandas**: Análisis y manipulación de datos
- **Plotly**: Visualización interactiva de datos
- **deep_translator**: Traducción de textos de inglés a español

## Notas importantes

- Los datos se obtienen en tiempo real a través de la API de Yahoo Finance
- La aplicación utiliza caché para mejorar el rendimiento y reducir las solicitudes a la API
- Las traducciones se realizan mediante la librería deep_translator

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntase libre de enviar pull requests o abrir issues para mejorar la aplicación.

## Licencia

Este proyecto está bajo la licencia MIT.