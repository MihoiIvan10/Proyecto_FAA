import re
import os
import folium

def formatear_coordenadas(coord):
    # Limpiar espacios en blanco
    coord = coord.replace(" ", "").strip().upper()

    # Extrae latitud y longitud -> N/S y E/W/O
    match = re.match(r"^([0-9.]+)([NS])([0-9.]+)([EWO])$", coord)
    if not match:
        raise ValueError("Coordenada no válida")

    lat_val, lat_hem, lon_val, lon_hem = match.groups()

    # Latitud
    lat_deg = float(lat_val[0:2])
    lat_min = float(lat_val[2:4])
    lat_sec = float(lat_val[4:]) if len(lat_val) > 4 else 0.0

    lat_formateada = f"{int(lat_deg)}°{int(lat_min)}'"
    if lat_sec > 0:
        lat_formateada += f"{lat_sec}\"".replace('.0\"', '\"')
    lat_formateada += lat_hem

    lat_decimal = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)
    if lat_hem == 'S':
        lat_decimal = -lat_decimal

    # Longitud
    if len(lon_val.split('.')[0]) >= 7:
        lon_deg = float(lon_val[0:3])
        lon_min = float(lon_val[3:5])
        lon_sec = float(lon_val[5:]) if len(lon_val) > 5 else 0.0
    else:
        lon_deg = float(lon_val[0:2])
        lon_min = float(lon_val[2:4])
        lon_sec = float(lon_val[4:]) if len(lon_val) > 4 else 0.0

    lon_formateada = f"{int(lon_deg)}°{int(lon_min)}'"
    if lon_sec > 0:
        lon_formateada += f"{lon_sec}\"".replace('.0\"', '\"')
    lon_formateada += lon_hem

    lon_decimal = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)
    if lon_hem in ['W', 'O']:
        lon_decimal = -lon_decimal

    gmaps_link = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"

    return {
        "texto_formateado": f"{lat_formateada} {lon_formateada}",
        "lat_decimal": lat_decimal,
        "lon_decimal": lon_decimal,
        "gmaps_link": gmaps_link
    }



def generar_mapa(lat, lon, texto_popup):
    mapa = folium.Map(
        location=[lat, lon],
        zoom_start=15,
        tiles="Esri.WorldImagery" 
    )

    folium.Marker(
        [lat, lon],
        popup=texto_popup,
        tooltip="¡Haz clic aquí!",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)

    return mapa



if __name__ == "__main__":
    coordenada_usuario = input("Ingresa la coordenada: ")

    try:
        resultado = formatear_coordenadas(coordenada_usuario)

        print(resultado["texto_formateado"])
        print(resultado["gmaps_link"])

        mapa_int = generar_mapa(
            resultado["lat_decimal"],
            resultado["lon_decimal"],
            resultado["texto_formateado"]
        )

        display(mapa_int)

    except Exception as e:
        print(f"Error: {e}")