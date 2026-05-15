import pandas as pd
import matplotlib.pyplot as plt
# Seaborn se importa para mejorar la estética global automáticamente
import seaborn as sns 


# Configuración estética global de Seaborn
sns.set_theme(style="whitegrid")


# # --- INSUMOS SINTÉTICOS (Dataset Analítico) ---
# # 1. Datos Temporales
# df_meses = pd.DataFrame({'mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May'], 'ventas': [10, 15, 13, 22, 30]})
# # 2. Datos Categóricos
# df_asesores = pd.DataFrame({'asesor': ['Ana Gomez', 'Carlos Ruiz', 'Marta Perez'], 'ventas_totales': [5000, 3200, 4100]})
# # 3. Datos Numéricos (Dispersión)
# df_clientes = pd.DataFrame({'edad': [25, 34, 45, 52, 23, 60], 'gasto_usd': [150, 400, 800, 750, 100, 1200]})
df_grafico = pd.read_csv("data/processed/02_estudiantes_por_programa.csv")

# print("--- GRÁFICO 1: RANKING CATEGORICO ---")
# plt.figure(figsize=(8, 4))
# # marker='o' pone un punto en cada mes
# plt.barh(df_grafico['nombre'], df_grafico['cantidad_estudiantes'], color='#2ca02c', marker='o', linewidth=2)
# plt.title("Estudiante por programa", fontsize=14, fontweight='bold')
# plt.xlabel("Cantidad de estudiantes")
# plt.ylabel("Programa")
# plt.show() # Cierra y renderiza el primer gráfico
colores = sns.color_palette("coolwarm", len(df_grafico))

print("\n--- GRÁFICO 2: RANKING CATEGÓRICO (Barras Horizontales) ---")
# Obligatorio: Ordenar los datos antes de graficar barras para que formen una escalera
# df_asesores_ordenado = df_asesores.sort_values(by='ventas_totales', ascending=True)

plt.figure(figsize=(8, 4))
# plt.barh es ideal para nombres largos en el eje Y
plt.barh(df_grafico['nombre'], df_grafico['cantidad_estudiantes'], color=colores)
plt.title("Estudiantes por programas")
plt.xlabel("Cantidad de estudiantes")
# plt.tight_layout() ajusta los márgenes automáticamente para que no se corten los nombres
plt.tight_layout() 
plt.show()


# print("\n--- GRÁFICO 3: RELACIÓN ESTADÍSTICA (Dispersión con Seaborn) ---")
# plt.figure(figsize=(8, 5))
# # Seaborn (sns) hace el scatter plot más limpio
# sns.scatterplot(data=df_clientes, x='edad', y='gasto_usd', s=100, color='purple')
# plt.title("Comportamiento de Gasto por Edad")
# plt.xlabel("Edad del Cliente")
# plt.ylabel("Gasto Histórico (USD)")
# plt.show()
