# Guardamos los archivos para el proyecto
import zipfile
import os

app_code = """import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="NutriGanado Paraguay - Villeta",
    page_icon="🐄",
    layout="wide"
)

if 'inventario_alimentos' not in st.session_state:
    st.session_state.inventario_alimentos = pd.DataFrame([
        {"Nombre": "Maíz Molido (Grano)", "MS (%)": 88.0, "PB (%)": 8.5, "NDT (%)": 88.0, "Fibra (%)": 2.2, "Ca (%)": 0.02, "P (%)": 0.28, "Costo/kg (₲)": 1800, "Tipo": "Energético"},
        {"Nombre": "Caña de Azúcar / Cogollo", "MS (%)": 28.0, "PB (%)": 3.5, "NDT (%)": 56.0, "Fibra (%)": 30.0, "Ca (%)": 0.20, "P (%)": 0.12, "Costo/kg (₲)": 250, "Tipo": "Forraje Voluminoso"},
        {"Nombre": "Afrecho de Trigo", "MS (%)": 87.0, "PB (%)": 15.5, "NDT (%)": 70.0, "Fibra (%)": 10.0, "Ca (%)": 0.14, "P (%)": 0.95, "Costo/kg (₲)": 1450, "Tipo": "Subproducto"},
        {"Nombre": "Expeller de Soja", "MS (%)": 90.0, "PB (%)": 44.0, "NDT (%)": 78.0, "Fibra (%)": 6.5, "Ca (%)": 0.30, "P (%)": 0.65, "Costo/kg (₲)": 3800, "Tipo": "Proteico"},
        {"Nombre": "Expeller de Algodón", "MS (%)": 91.0, "PB (%)": 32.0, "NDT (%)": 68.0, "Fibra (%)": 14.0, "Ca (%)": 0.25, "P (%)": 0.80, "Costo/kg (₲)": 2900, "Tipo": "Proteico"},
        {"Nombre": "Cáscara de Soja", "MS (%)": 89.0, "PB (%)": 12.0, "NDT (%)": 74.0, "Fibra (%)": 35.0, "Ca (%)": 0.50, "P (%)": 0.15, "Costo/kg (₲)": 1600, "Tipo": "Fibra Digestible"},
        {"Nombre": "Pasto Camerún / Pastoreo", "MS (%)": 20.0, "PB (%)": 9.0, "NDT (%)": 55.0, "Fibra (%)": 32.0, "Ca (%)": 0.35, "P (%)": 0.20, "Costo/kg (₲)": 150, "Tipo": "Forraje Verde"},
        {"Nombre": "Sal Mineral Ganadera (P 8%)", "MS (%)": 98.0, "PB (%)": 0.0, "NDT (%)": 0.0, "Fibra (%)": 0.0, "Ca (%)": 16.0, "P (%)": 8.0, "Costo/kg (₲)": 8000, "Tipo": "Mineral"},
        {"Nombre": "Sustituto Lácteo (Guachos)", "MS (%)": 95.0, "PB (%)": 22.0, "NDT (%)": 90.0, "Fibra (%)": 0.5, "Ca (%)": 1.10, "P (%)": 0.80, "Costo/kg (₲)": 18700, "Tipo": "Lácteo Comercial"}
    ])

st.title("🇵🇾 NutriGanado - Tacuatí / Villeta")
st.caption("Prototipo v3.0 — Formulación Local, Requerimientos por Categoría y Sistema de Alertas")

opcion = st.sidebar.radio(
    "Selecciona una función:",
    ["1. Formular Dieta y Alertas", "2. Escanear / Analizar Etiqueta", "3. Catálogo de Insumos"]
)

if opcion == "1. Formular Dieta y Alertas":
    st.header("📋 Formulación de Ración y Alertas Nutricionales")
    col_req, col_mix = st.columns([1, 2])
    
    with col_req:
        st.subheader("1. Categoría Animal")
        categoria = st.selectbox(
            "Selecciona la categoría productiva:",
            [
                "Ternero Guacho (0-3 meses)",
                "Desmante / Crecimiento (3-12 meses)",
                "Novillo Engorde / Confina (350-450 kg)",
                "Vaca Lechera (Doble Propósito)",
                "Vaca Lechera Alta Producción (>20 L)",
                "Cerda Gestante / Parición",
                "Cerda Lactante",
                "Cerdos Crecimiento / Engorde",
                "Gallinas Ponedoras",
                "Patos / Aves de Corral"
            ]
        )
        peso_vivo = st.number_input("Peso Vivo Promedio (kg)", min_value=1.0, max_value=1000.0, value=350.0 if "Novillo" in categoria else (50.0 if "Ternero" in categoria else 450.0), step=5.0)
        
        if "Ternero Guacho" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.025, 20.0, 5.0
        elif "Novillo Engorde" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.028, 13.0, 15.0
        elif "Lechera Alta" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.038, 17.0, 17.0
        elif "Lechera (Doble" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.030, 14.5, 19.0
        elif "Cerda Gestante" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.020, 14.0, 7.0
        elif "Cerda Lactante" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.040, 17.5, 5.0
        elif "Cerdos Crecimiento" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.045, 16.0, 4.0
        elif "Gallinas" in categoria:
            req_ms_pct, req_pb, req_fibra_min = 0.08, 17.0, 3.0
        else:
            req_ms_pct, req_pb, req_fibra_min = 0.030, 15.0, 10.0

        req_ms = peso_vivo * req_ms_pct
        st.info(f"**Objetivos:**\\n* Consumo MS: ~{req_ms:.2f} kg/día\\n* PB: {req_pb}%\\n* Fibra Mín: {req_fibra_min}%")

    with col_mix:
        st.subheader("2. Mezcla de Insumos")
        df_alimentos = st.session_state.inventario_alimentos
        alimentos_sel = st.multiselect("Ingredientes:", df_alimentos["Nombre"].tolist(), default=["Maíz Molido (Grano)", "Caña de Azúcar / Cogollo", "Expeller de Soja"])
        
        cantidades = {}
        if alimentos_sel:
            for ing in alimentos_sel:
                cantidades[ing] = st.number_input(f"Cantidad de **{ing}** (kg/día):", min_value=0.0, value=1.5, step=0.2)
            
            tot_fresco = sum(cantidades.values())
            tot_ms, tot_pb_kg, tot_fibra_kg, tot_costo = 0.0, 0.0, 0.0, 0.0
            
            for ing, cant in cantidades.items():
                row = df_alimentos[df_alimentos["Nombre"] == ing].iloc[0]
                ms_k = cant * (row["MS (%)"] / 100.0)
                tot_ms += ms_k
                tot_pb_kg += ms_k * (row["PB (%)"] / 100.0)
                tot_fibra_kg += ms_k * (row["Fibra (%)"] / 100.0)
                tot_costo += cant * row["Costo/kg (₲)"]
            
            pb_pct = (tot_pb_kg / tot_ms * 100.0) if tot_ms > 0 else 0
            fibra_pct = (tot_fibra_kg / tot_ms * 100.0) if tot_ms > 0 else 0
            costo_kg_ms = (tot_costo / tot_ms) if tot_ms > 0 else 0

            st.markdown("---")
            st.subheader("📊 Indicadores")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Kilos Frescos", f"{tot_fresco:.2f} kg")
            c2.metric("Materia Seca", f"{tot_ms:.2f} kg", delta=f"{tot_ms - req_ms:.2f} kg vs Obj")
            c3.metric("Proteína Bruta", f"{pb_pct:.2f}%", delta=f"{pb_pct - req_pb:.1f}% vs Obj")
            c4.metric("Fibra Bruta", f"{fibra_pct:.2f}%")

            c5, c6 = st.columns(2)
            c5.metric("Costo Diario por Animal", f"₲ {tot_costo:,.0f}")
            c6.metric("Costo por kg de MS", f"₲ {costo_kg_ms:,.0f}")

            st.markdown("### 🚨 Panel de Alertas")
            if ("Novillo" in categoria or "Lechera" in categoria) and fibra_pct < req_fibra_min:
                st.error(f"⚠️ **ALERTA DE ACIDOSIS RUMINAL:** Fibra baja ({fibra_pct:.1f}% vs mín {req_fibra_min}%). Aumenta la Caña o Forraje.")
            if pb_pct < req_pb - 1.0:
                st.warning(f"⚠️ **DÉFICIT PROTEICO:** {pb_pct:.1f}% PB vs objetivo de {req_pb}%. Ajusta con Expeller de Soja o Algodón.")
            elif pb_pct > req_pb + 3.0:
                st.info(f"💡 **EXCESO PROTEICO:** {pb_pct:.1f}% PB. Se puede reducir para optimizar costos.")

            resumen_txt = f"REPORTE DE RACION\\nCategoria: {categoria}\\nPeso Vivo: {peso_vivo} kg\\n"
            for ing, cant in cantidades.items():
                resumen_txt += f"- {ing}: {cant} kg\\n"
            resumen_txt += f"Materia Seca: {tot_ms:.2f} kg | PB: {pb_pct:.2f}% | Costo: ₲ {tot_costo:,.0f}\\n"
            
            st.download_button("📥 Descargar Hoja de Mezcla (.txt)", data=resumen_txt, file_name="racion.txt", mime="text/plain")

elif opcion == "2. Escanear / Analizar Etiqueta":
    st.header("📷 Análisis de Etiquetas Comerciales")
    uploaded_file = st.file_uploader("Subir foto de etiqueta (JPG, PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col_img, col_data = st.columns([1, 1])
        with col_img:
            st.image(image, caption="Etiqueta Inspeccionada", use_container_width=True)
        with col_data:
            st.subheader("🔍 Corrección y Verificación")
            with st.form("form_etiqueta"):
                nombre_prod = st.text_input("Nombre / Marca Comercial", "Balanceado Iniciador")
                tipo_prod = st.selectbox("Categoría", ["Balanceado Completo", "Concentrado / Núcleo", "Sustituto Lácteo", "Suplemento Mineral"])
                ms_val = st.number_input("Materia Seca (%)", value=88.0)
                pb_val = st.number_input("Proteína Bruta (%)", value=18.0)
                costo_prod = st.number_input("Costo por kg (₲)", value=3200, step=100)
                guardar = st.form_submit_button("💾 Incorporar al Catálogo")
                if guardar:
                    nuevo_insumo = pd.DataFrame([{"Nombre": nombre_prod, "MS (%)": ms_val, "PB (%)": pb_val, "NDT (%)": 75.0, "Fibra (%)": 8.0, "Ca (%)": 1.0, "P (%)": 0.6, "Costo/kg (₲)": costo_prod, "Tipo": tipo_prod}])
                    st.session_state.inventario_alimentos = pd.concat([st.session_state.inventario_alimentos, nuevo_insumo], ignore_index=True)
                    st.success(f"¡Agregado **{nombre_prod}** exitosamente!")

elif opcion == "3. Catálogo de Insumos":
    st.header("🗂️ Catálogo General de Insumos Locales")
    st.dataframe(st.session_state.inventario_alimentos, use_container_width=True)
"""

req_code = """streamlit>=1.28.0
pandas>=2.0.0
Pillow>=9.5.0
"""
