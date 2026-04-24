from datetime import datetime

def check_for_alerts(telemetry_data: dict) -> list[dict]:
    """
    Evalúa los datos de telemetría contra los umbrales definidos
    y retorna una lista de alertas generadas.
    """
    alertas_generadas = []
    
    # Extraemos metadata y sensores
    metadata = telemetry_data.get("metadata", {})
    id_areariego = metadata.get("id_areariego")
    
    # Si no hay ID de área, no podemos asociar la alerta
    if not id_areariego:
        return []

    sensor_data = telemetry_data.get("sensor_data", {})
    soil = sensor_data.get("soil", {})
    environment = sensor_data.get("environment", {})
    plant = sensor_data.get("plant", {})

    # 1. Validación de Humedad de Suelo (Rango normal: 0.10 - 0.40)
    moisture = soil.get("moisture")
    if moisture is not None:
        if moisture < 0.15:
            alertas_generadas.append({
                "id_areariego": id_areariego,
                "tipo_de_alerta": "Estrés Hídrico",
                "mensaje_de_alerta": f"Humedad de suelo crítica ({moisture}). Posible estrés hídrico.",
            })
        elif moisture > 0.35:
            alertas_generadas.append({
                "id_areariego": id_areariego,
                "tipo_de_alerta": "Saturación",
                "mensaje_de_alerta": f"Humedad de suelo alta ({moisture}). Riesgo de saturación.",
            })

    # 2. Validación de Temperatura de Suelo (Rango normal: 10 - 35)
    soil_temp = soil.get("temp")
    if soil_temp is not None and soil_temp > 35:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Temperatura Suelo Alta",
            "mensaje_de_alerta": f"Temperatura de suelo en {soil_temp}°C. Puede afectar raíces.",
        })

    # 3. Validación de Conductividad Eléctrica (Rango normal: 0.2 - 4.0)
    ce = soil.get("conductivity")
    if ce is not None and ce > 4.0:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Salinidad Alta",
            "mensaje_de_alerta": f"Conductividad eléctrica en {ce} dS/m. Nivel de salinidad alto.",
        })

    # 4. Validación de Potencial Hídrico (Rango normal: -10 a -1500)
    water_potential = soil.get("water_potential")
    if water_potential is not None and water_potential < -500:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Estrés Hídrico Severo",
            "mensaje_de_alerta": f"Potencial hídrico en {water_potential} kPa. Estrés severo.",
        })

    # 5. Validación de Evapotranspiración (Rango normal: 2 - 8)
    et0 = environment.get("et0")
    if et0 is not None and et0 > 6:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Alta Demanda Hídrica",
            "mensaje_de_alerta": f"Evapotranspiración en {et0} mm/día. Requerimiento de agua elevado.",
        })

    # 6. Validación de Humedad Relativa (Rango normal: 20 - 90)
    humidity = environment.get("humidity")
    if humidity is not None and humidity < 30:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Humedad Ambiental Baja",
            "mensaje_de_alerta": f"Humedad relativa en {humidity}%. Aumenta tasa de evaporación.",
        })

    # 7. Validación de Velocidad de Viento (Rango normal: 0 - 10)
    wind_speed = environment.get("wind_speed")
    if wind_speed is not None and wind_speed > 5:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Viento Fuerte",
            "mensaje_de_alerta": f"Velocidad de viento en {wind_speed} m/s. Aumenta evapotranspiración.",
        })

    # 8. Validación de NDVI (Rango normal: 0.2 - 0.9)
    ndvi = plant.get("ndvi")
    if ndvi is not None and ndvi < 0.2:
        alertas_generadas.append({
            "id_areariego": id_areariego,
            "tipo_de_alerta": "Bajo Vigor Vegetal",
            "mensaje_de_alerta": f"Índice NDVI crítico ({ndvi}). Indica vegetación pobre o enferma.",
        })

    return alertas_generadas