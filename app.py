import streamlit as st
import sys
from main import leer_datos
import pandas as pd

st.title("Dashboard Financiero")
st.write("Mi primer Dashboard")

sys.path.append('.')

empresa = st.selectbox("Selecciona una empresa", ["AAPL", "GOOGL", "MSFT"])
datos = leer_datos(empresa)
df = pd.DataFrame(datos, columns=["id", "empresa", "fecha", "cierre"])
st.dataframe(df)