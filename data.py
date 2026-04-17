import pandas as pd

# 1. Carga de datos
ipm_dpto = pd.read_excel(
    "data/anex-PMultidimensional-Departamental-2025.xlsx", 
    sheet_name="IPM_Departamentos", 
    header=None, 
    skiprows=13, 
    nrows=33
)

# 2. Definición de nombres de columnas
col_names = ["nombre_dpto"]
years = list(range(2018, 2026))
grupos = ["total", "cabecera", "resto"]

for year in years:
    for grupo in grupos:
        col_names.append(f"{grupo}_{year}")

ipm_dpto.columns = col_names

# 3. Códigos de departamento (Divipola)
cod_dpto = [
    '05','08','11','13','15','17','18','19','20','23','25','27','41','44','47', 
    '50','52','54','63','66','68','70','73','76','81','85','86','88','91','94',
    '95','97','99'
]

ipm_dpto.insert(0, "cod_dpto", cod_dpto)

# 4. Transformación de ancho a largo (Tidy Data)
ipm_long = ipm_dpto.melt(
    id_vars=["cod_dpto", "nombre_dpto"], 
    var_name="var", 
    value_name="ipm"
)

# Separar la variable y el año
ipm_long[["grupo_ipm", "year"]] = ipm_long["var"].str.split("_", expand=True)

# 5. Pivotar para tener columnas por grupo (total, cabecera, resto)
ipm_dpto_ajust = ipm_long.pivot_table(
    index=["cod_dpto", "nombre_dpto", "year"], 
    columns="grupo_ipm", 
    values="ipm"
).reset_index()

# 6. Exportar resultado
ipm_dpto_ajust.to_csv("data/ipm_dpto_ajust.csv", index=False)
print("Archivo 'data/ipm_dpto_ajust.csv' creado con éxito.")