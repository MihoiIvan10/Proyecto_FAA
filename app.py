import streamlit as st
from streamlit_folium import st_folium
from converter import formatear_coordenadas, generar_mapa

st.set_page_config(
    page_title="GeoNOTAM",
    page_icon="🌍",
    layout="wide"
)

st.title("GeoNOTAM")
st.subheader("Conversor de coordenadas aeronáuticas")

st.write(
    "Ingresa una coordenada NOTAM para convertirla "
    "y visualizar su ubicación en el mapa."
)

if "resultado" not in st.session_state:
    st.session_state.resultado = None

coordenada = st.text_input(
    "Coordenadas aeronáuticas",
    placeholder="Ejemplo: 190000N0990000W"
)

if st.button("Convertir coordenada", type="primary"):
    try:
        st.session_state.resultado = formatear_coordenadas(coordenada)
    except Exception as e:
        st.session_state.resultado = None
        st.error(f"Error en la coordenada: {e}")

if st.session_state.resultado is not None:
    resultado = st.session_state.resultado
    st.success("Coordenada convertida correctamente")

    columna1, columna2 = st.columns([1, 2])

    with columna1:
        st.subheader("Resultados")
        st.write("Coordenada formateada:")
        st.info(resultado["texto_formateado"])
        st.write("Latitud decimal:")
        st.code(str(resultado["lat_decimal"]))
        st.write("Longitud decimal:")
        st.code(str(resultado["lon_decimal"]))
        st.link_button(
            "Abrir en Google Maps",
            resultado["gmaps_link"]
        )

    with columna2:
        st.subheader("Ubicación geográfica")
        mapa = generar_mapa(
            resultado["lat_decimal"],
            resultado["lon_decimal"],
            resultado["texto_formateado"]
        )
        st_folium(
            mapa,
            height=500,
            use_container_width=True,
            returned_objects=[]
        )