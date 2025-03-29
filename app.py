import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import requests
import os


# URL del archivo en GitHub (RAW)
file_url = "https://raw.githubusercontent.com/Juan-Madera/Lugares-De-Estudio/main/DataspruebacondatosDe.xlsx"

# Descargar el archivo
response = requests.get(file_url)
file_path = os.path.join(os.getcwd(), "DataspruebacondatosDe.xlsx")


with open(file_path, "wb") as file:
    file.write(response.content)

# Cargar el archivo con pandas
df = pd.read_excel(file_path)
print(df.head())  # Verificar que se cargó correctamente

# CSS para centrar contenido
st.markdown(
    """
    <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .box {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            width: 60%;
            margin: 10px auto;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .title {
            font-size: 28px;
            font-weight: bold;
            margin-top: 20px;
        }
        .subtitle {
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    df = pd.read_excel(file_path)
    df["Lugar"] = df["Lugar"].fillna('').astype(str).str.strip().str.capitalize()
    
    frecuencia_lugares = df["Lugar"].value_counts()
    total_registros = df["Lugar"].count()
    
    df["Lugar_numeric"] = df["Lugar"].map(frecuencia_lugares)
    
    media_valor = df["Lugar_numeric"].mean()
    mediana_valor = df["Lugar_numeric"].median()
    desviacion_std = df["Lugar_numeric"].std()
    moda = df["Lugar"].mode()[0]

    mediana_lugar = frecuencia_lugares[frecuencia_lugares == mediana_valor].index[0] if (frecuencia_lugares == mediana_valor).any() else "N/A"
    media_lugar = frecuencia_lugares.iloc[(frecuencia_lugares - media_valor).abs().argsort()[0]]

    Q1, Q3 = df["Lugar_numeric"].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    limite_inferior = max(0, Q1 - 1.5 * IQR)
    limite_superior = Q3 + 1.5 * IQR
    valores_atipicos = df["Lugar"][(df["Lugar_numeric"] < limite_inferior) | (df["Lugar_numeric"] > limite_superior)]

    # Mostrar resultados centrados
    st.markdown('<p class="title centered">📊 Análisis de Preferencias de Lugares</p>', unsafe_allow_html=True)
    st.markdown('<div class="box centered">', unsafe_allow_html=True)
    st.markdown(f"**▶ Lugar más frecuente:** {moda}")
    st.markdown(f"**▶ Total de registros en 'Lugar':** {total_registros}")
    st.markdown(f"**▶ Media de frecuencia de lugares:** {media_valor:.2f} - {media_lugar}")
    st.markdown(f"**▶ Mediana de frecuencia de lugares:** {mediana_valor:.2f} - {mediana_lugar}")
    st.markdown(f"**▶ Desviación estándar:** {desviacion_std:.2f}")
    st.markdown(f"**▶ Q1 (Primer cuartil):** {Q1:.2f}")
    st.markdown(f"**▶ Q3 (Tercer cuartil):** {Q3:.2f}")
    st.markdown(f"**▶ IQR (Rango Intercuartil):** {IQR:.2f}")
    st.markdown(f"**▶ Límite Inferior:** {limite_inferior:.2f}")
    st.markdown(f"**▶ Límite Superior:** {limite_superior:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Valores atípicos
    st.markdown('<p class="subtitle centered">📌 Valores Atípicos</p>', unsafe_allow_html=True)
    if valores_atipicos.empty:
        st.markdown('<div class="box centered">No se encontraron valores atípicos.</div>', unsafe_allow_html=True)
    else:
        st.code(valores_atipicos.to_string(index=False))

    # Distribución de Frecuencias
    st.markdown('<p class="subtitle centered">📈 Distribución de Frecuencias</p>', unsafe_allow_html=True)
    st.code(frecuencia_lugares.to_string())

    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 5))
    frecuencia_lugares.plot(kind='bar', color='skyblue', ax=ax)
    ax.axhline(media_valor, color='red', linestyle='dashed', label=f'Media: {media_valor:.2f}')
    ax.axhline(mediana_valor, color='green', linestyle='dashed', label=f'Mediana: {mediana_valor:.2f}')
    ax.set_title("Distribución de preferencias de lugares")
    ax.set_xlabel("Lugares")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    # Gráfico de pastel
    fig2, ax2 = plt.subplots(figsize=(7, 7))
    ax2.pie(frecuencia_lugares, labels=frecuencia_lugares.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax2.set_title("Distribución de Lugares (Gráfico de Pastel)")
    st.pyplot(fig2)

    # Gráfico de caja
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    ax3.boxplot(df["Lugar_numeric"], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    ax3.axvline(limite_inferior, color="red", linestyle="dashed", label=f"Límite Inferior: {limite_inferior:.2f}")
    ax3.axvline(limite_superior, color="red", linestyle="dashed", label=f"Límite Superior: {limite_superior:.2f}")
    ax3.legend()
    ax3.set_title("Valores Atípicos")
    ax3.set_xlabel("Frecuencia de Lugares")
    st.pyplot(fig3)

    # Gráfico de Dispersión
    st.markdown('<p class="subtitle centered">📌 Diagrama de Dispersión</p>', unsafe_allow_html=True)
    fig4, ax4 = plt.subplots(figsize=(9, 6))
    ax4.scatter(df.index, df["Lugar_numeric"], color='purple', alpha=0.6, edgecolors='black')
    ax4.set_title("Diagrama de Dispersión de Frecuencia de Lugares")
    ax4.set_xlabel("Índice")
    ax4.set_ylabel("Frecuencia de Lugares")
    ax4.grid(True, linestyle="--", alpha=0.5)
    
    # Mostrar diagrama de dispersión
    st.pyplot(fig4)

    # Mostrar resultados en Streamlit
    st.title("Análisis de Preferencias de Lugares")
    st.write(f"**Lugar más frecuente:** {frecuencia_lugares.idxmax()}")
    st.write(f"**Total de registros en 'Lugar':** {df['Lugar'].count()}")
    
    # Diagrama de frecuencia (gráfico de línea)
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    frecuencia_lugares.sort_index().plot(kind='line', marker='o', color='blue', linestyle='-', linewidth=2, markersize=6, ax=ax5)
    ax5.set_title("Diagrama de Frecuencia de Lugares", fontsize=14, fontweight='bold')
    ax5.set_xlabel("Lugares", fontsize=12)
    ax5.set_ylabel("Frecuencia de Visitas", fontsize=12)
    ax5.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Mostrar en Streamlit
    st.pyplot(fig5)

except FileNotFoundError:
    st.error(f"❌ Error: No se encontró el archivo en la ruta: {file_path}")

except Exception as e:
    st.error(f"⚠️ Error inesperado: {str(e)}")
