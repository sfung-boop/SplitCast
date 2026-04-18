
# ==============================================================
# ⚙️ CONFIGURACIÓN E IMPORTACIONES
# ==============================================================
import streamlit as st
import pandas as pd
import io
import zipfile
import time

st.set_page_config(
    page_title="SplitCast",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==============================================================
# 🎨 ESTILOS PERSONALIZADOS (Dark Glassmorphism)
# ==============================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
  }

  /* Fondo degradado oscuro */
  .stApp {
      background: linear-gradient(135deg, #0f0c29 0%, #1a1040 50%, #24243e 100%);
      min-height: 100vh;
  }

  /* Tarjetas glassmorphism */
  .glass-card {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 20px;
      backdrop-filter: blur(12px);
  }

  /* Header hero */
  .hero-title {
      font-size: 2.6rem;
      font-weight: 700;
      background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.2;
      margin-bottom: 6px;
  }

  .hero-subtitle {
      color: #94a3b8;
      font-size: 1rem;
      font-weight: 400;
      margin-bottom: 0;
  }

  /* Badge de etapa */
  .stage-badge {
      display: inline-block;
      background: linear-gradient(90deg, #7c3aed, #3b82f6);
      color: white;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 20px;
      margin-bottom: 10px;
  }

  /* Métricas de resultado */
  .metric-row {
      display: flex;
      gap: 16px;
      margin: 16px 0;
  }
  .metric-box {
      flex: 1;
      background: rgba(124, 58, 237, 0.15);
      border: 1px solid rgba(124, 58, 237, 0.4);
      border-radius: 12px;
      padding: 16px;
      text-align: center;
  }
  .metric-value {
      font-size: 2rem;
      font-weight: 700;
      color: #a78bfa;
  }
  .metric-label {
      font-size: 0.78rem;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.06em;
  }

  /* Botones */
  .stButton > button {
      background: linear-gradient(90deg, #7c3aed, #3b82f6) !important;
      color: white !important;
      border: none !important;
      border-radius: 10px !important;
      font-weight: 600 !important;
      font-size: 0.95rem !important;
      padding: 0.6rem 1.8rem !important;
      transition: all 0.25s ease !important;
      letter-spacing: 0.02em;
  }
  .stButton > button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 8px 24px rgba(124, 58, 237, 0.45) !important;
  }

  /* Download button */
  .stDownloadButton > button {
      background: linear-gradient(90deg, #059669, #10b981) !important;
      color: white !important;
      border: none !important;
      border-radius: 10px !important;
      font-weight: 600 !important;
      font-size: 0.95rem !important;
      width: 100%;
      padding: 0.65rem 1.8rem !important;
      transition: all 0.25s ease !important;
  }
  .stDownloadButton > button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 8px 24px rgba(16, 185, 129, 0.45) !important;
  }

  /* Inputs */
  .stTextInput input, .stSelectbox select {
      background: rgba(255,255,255,0.07) !important;
      border: 1px solid rgba(255,255,255,0.15) !important;
      border-radius: 8px !important;
      color: #e2e8f0 !important;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.5); border-radius: 3px; }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.1) !important; }

  /* Dataframe */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* Alert boxes */
  .stAlert > div {
      border-radius: 10px !important;
  }
</style>
""", unsafe_allow_html=True)

# ==============================================================
# 🎯 SECCIÓN 1: HEADER
# ==============================================================
st.markdown("""
<div class="glass-card" style="text-align:center; padding: 36px 28px;">
  <div style="font-size:2.8rem; margin-bottom:8px;">⚡</div>
  <div class="hero-title">SplitCast</div>
  <div class="hero-subtitle">De la señal a la disponibilidad · Ordo · Lumen · Nexus · Ratio</div>
  <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 15px;">
    Sube cualquier reporte general en Excel y el sistema lo segmentará automáticamente en archivos .txt individuales por cada tienda/sucursal. Todo el procesamiento se realiza en memoria sin dejar rastros locales.
  </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================
# 📥 SECCIÓN 2: UPLOAD & PARÁMETROS
# ==============================================================
st.markdown('<div class="stage-badge">📂 Paso 1 · Subir Archivo</div>', unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("#### Sube tu archivo Excel de inventario")
st.info(
    "💡 **Requisito:** Asegúrate de que la pestaña seleccionada contenga al menos las columnas 'Tienda', 'SKU' y 'Cantidad'.",
    icon="ℹ️"
)

uploaded_file = st.file_uploader(
    "Arrastra o haz clic para seleccionar (XLS/XLSX)",
    type=["xlsx", "xls"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================
# ⚙️ PARÁMETROS DINÁMICOS (solo si hay archivo)
# ==============================================================
if uploaded_file:
    st.markdown('<div class="stage-badge">⚙️ Paso 2 · Configuración de Extracción</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        nombre_pestana = st.text_input(
            "🗂️ Nombre de la pestaña (hoja)",
            value="Formato",
            help="El nombre exacto de la hoja dentro del Excel"
        )
    with col2:
        col_tienda = st.text_input(
            "🏪 Columna de agrupación (Tienda)",
            value="Tienda",
            help="Nombre de la columna que identifica cada tienda"
        )

    col3, col4 = st.columns(2)
    with col3:
        col_sku = st.text_input(
            "🔖 Columna SKU",
            value="SKU",
            help="Nombre de la columna con el código del producto"
        )
    with col4:
        col_cantidad = st.text_input(
            "📦 Columna Cantidad",
            value="Cantidad",
            help="Nombre de la columna con la cantidad en inventario"
        )

    separador = st.radio(
        "🔗 Separador en el archivo de salida",
        options=[",", ";", "|", "\\t (tabulación)"],
        horizontal=True,
        help="Cómo se separarán el SKU y la Cantidad en cada línea del TXT"
    )
    sep_real = "\t" if separador == "\\t (tabulación)" else separador

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # PREVISUALIZACIÓN
    # ----------------------------------------------------------
    try:
        df = pd.read_excel(uploaded_file, sheet_name=nombre_pestana, engine='openpyxl')
        uploaded_file.seek(0)  # Resetear el buffer tras la lectura
        
        with st.expander("👁️ Ver muestra de los datos cargados"):
            st.dataframe(df.head(), use_container_width=True)

        # Validar columnas requeridas
        cols_req = [col_tienda, col_sku, col_cantidad]
        cols_faltantes = [c for c in cols_req if c not in df.columns]

        if cols_faltantes:
            st.warning(f"⚠️ **Atención:** No se encontraron las columnas: `{'`, `'.join(cols_faltantes)}`\n\nVerifica los nombres arriba antes de procesar.", icon="⚠️")
        else:
            st.success(f"✅ Columnas `{col_tienda}`, `{col_sku}` y `{col_cantidad}` encontradas correctamente.", icon="✅")

        # ==============================================================
        # 🧠 SECCIÓN 3: BOTÓN DE PROCESAMIENTO
        # ==============================================================
        st.markdown('<div class="stage-badge">🚀 Paso 3 · Procesar y Descargar</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if st.button("🚀 Procesar y Generar TXTs", use_container_width=True):

            with st.spinner("⚡ Segmentando datos por tienda..."):
                t_inicio = time.time()

                if cols_faltantes:
                    st.error(f"🚨 **Error de Columnas:** Faltan las columnas `{'`, `'.join(cols_faltantes)}` en el archivo. Verifica el formato.", icon="🚨")
                    st.stop()

                # Eliminar filas sin datos clave
                df_clean = df.dropna(subset=[col_tienda, col_sku, col_cantidad]).copy()
                total_filas = len(df_clean)
                tiendas_unicas = df_clean[col_tienda].nunique()

                # ==============================================================
                # 📦 SECCIÓN 4: CREACIÓN DEL ZIP EN MEMORIA (sin disco)
                # ==============================================================
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for tienda, grupo in df_clean.groupby(col_tienda):
                        # Limpieza robusta del nombre de la tienda
                        nombre_tienda_limpio = str(tienda).replace('/', '-').replace('\\', '-').strip()

                        # Formato estricto basado en la configuración
                        lineas = grupo.apply(
                            lambda row: f"{row[col_sku]}{sep_real}{int(row[col_cantidad]) if str(row[col_cantidad]).replace('.','',1).isdigit() else row[col_cantidad]}",
                            axis=1
                        )
                        contenido_txt = "\n".join(lineas.astype(str).tolist())

                        # Escribimos en el ZIP
                        zip_file.writestr(f"{nombre_tienda_limpio}.txt", contenido_txt.encode('utf-8'))

                zip_buffer.seek(0)
                t_fin = time.time()
                tiempo_ms = round((t_fin - t_inicio) * 1000)

                # ==============================================================
                # 📤 SECCIÓN 5: MÉTRICAS Y DESCARGA
                # ==============================================================
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="metric-value">{tiendas_unicas}</div>
                        <div class="metric-label">Archivos TXT</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{total_filas:,}</div>
                        <div class="metric-label">Líneas procesadas</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{tiempo_ms}ms</div>
                        <div class="metric-label">Tiempo total</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.success("✅ ¡Procesamiento completado con éxito!")
                st.divider()

                # Nombre dinámico para el ZIP basado en el archivo original
                nombre_original = uploaded_file.name.rsplit('.', 1)[0]
                nombre_zip = f"Export_{nombre_original}.zip"

                st.download_button(
                    label="📥 Descargar Paquete ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=nombre_zip,
                    mime="application/zip",
                    # type="primary" no is totally valid but custom styles will override it due to class .stDownloadButton > button
                    use_container_width=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)

    except ValueError:
        st.error(f"❌ Error: No se encontró una pestaña llamada '{nombre_pestana}' en el archivo.", icon="🚨")
    except KeyError as e:
        st.error(f"❌ Error de Columnas: Falta la columna {e} en el archivo. Verifica el formato.", icon="🚨")
    except Exception as e:
        st.error(f"❌ Error inesperado al procesar: {e}", icon="🚨")

else:
    # Estado vacío con instrucciones
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 40px; color: #64748b;">
        <div style="font-size: 3rem; margin-bottom: 12px;">📥</div>
        <div style="font-size: 1rem; color: #94a3b8;">Esperando archivo... Por favor, completa el Paso 1.</div>
        <div style="font-size: 0.85rem; margin-top: 8px; color: #64748b;">
            El procesamiento se realiza de forma local en el navegador
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================
# FOOTER
# ==============================================================
st.markdown("""
<div style="text-align:center; margin-top: 40px; color: #334155; font-size: 0.78rem;">
    ⚡ SplitCast · Ecosistema digital de planning retail<br>
    <span style="color:#7c3aed;">Powered by Streamlit + Pandas</span>
</div>
""", unsafe_allow_html=True)
