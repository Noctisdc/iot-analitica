import streamlit as st
import pandas as pd

st.title("Analítica IoT: Temperatura y Humedad")

f_temp = st.sidebar.file_uploader("CSV de temperatura", type="csv")
f_hum = st.sidebar.file_uploader("CSV de humedad", type="csv")

tab1, tab2 = st.tabs(["Datos", "Análisis"])

if f_temp and f_hum:
    t = pd.read_csv(f_temp).iloc[:, :2]
    h = pd.read_csv(f_hum).iloc[:, :2]
    t.columns = ["tiempo", "temperatura"]
    h.columns = ["tiempo", "humedad"]
    df = t.merge(h, on="tiempo")

    for c in ["temperatura", "humedad"]:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(r"[^0-9.\-]", "", regex=True))

    with tab1:
        st.dataframe(df)

    with tab2:
        st.write(df[["temperatura", "humedad"]].describe())
        st.write(df[["temperatura", "humedad"]].corr())
        st.line_chart(df.set_index("tiempo")[["temperatura", "humedad"]])
        st.scatter_chart(df, x="temperatura", y="humedad")
else:
    st.info("Sube los dos CSV en el panel de la izquierda")
