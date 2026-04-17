# Dashboard de Brechas de Pobreza en Colombia (IPM)

Este proyecto es una aplicación web interactiva desarrollada en **Python** utilizando **Dash** y **Plotly**. Su objetivo es visualizar y analizar el Índice de Pobreza Multidimensional (IPM) en los departamentos de Colombia, permitiendo identificar las disparidades críticas entre las zonas urbanas y rurales.

## 📊 Sobre los Datos

El dashboard utiliza datos oficiales del **DANE**:
- **Cabecera (Urbano):** Pobreza en los cascos urbanos/alcaldías.
- **Resto (Rural):** Pobreza en veredas, corregimientos y zonas rurales dispersas.
- **Total:** El promedio ponderado departamental.
- **Brecha:** Una métrica calculada (`Resto - Cabecera`) que mide la desigualdad social en el territorio.

## 🛠️ Tecnologías Utilizadas

- **Dash & Dash Bootstrap Components:** Para la estructura de la interfaz web y el diseño responsivo.
- **Plotly Express:** Para la generación del mapa coroplético y las gráficas dinámicas.
- **Pandas:** Para la manipulación y limpieza de los datos del CSV.
- **GeoPandas:** Para el procesamiento de archivos espaciales (Shapefiles) y conversión a GeoJSON.

## 📁 Estructura del Proyecto

Para que el código funcione correctamente, la estructura de carpetas debe ser:
```text
PROYECTO/
├── data/
│   ├── MGN2024_DPTO_POLITICO.zip  # Archivos geográficos del DANE
│   └── ipm_dpto_ajust.csv        # Datos de pobreza exportados
├── app.py                         # Código principal de la aplicación
└── README.md                      # Documentación
```

## Ejecucion

1. Sincronizar e Instalar Dependencias
Desde la terminal en la carpeta del proyecto, ejecuta el siguiente comando para preparar el entorno virtual e instalar las librerías EN LA TERMINAL: uv sync

2. Ejecutar la Aplicación. Para lanzar el dashboard sin necesidad de activar manualmente el entorno, usar EN LA TERMINAL: uv run app.py

3. Abrir el "http://127.0.0.1:8050/" o algo parecido que aparezca EN LA TERMINAL
