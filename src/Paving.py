import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setări pentru aspectul graficelor
sns.set_theme(style="whitegrid")

# --- PASUL 1: Filtrare și Curățare ---
# Filtrăm doar categoria Paving
df_paving = df[df['category'] == 'Paving'].copy()

# Asigurăm conversia numerică pentru coverage (gestionăm erori sau string-uri goale)
df_paving['coverage_m2_per_unit'] = pd.to_numeric(df_paving['coverage_m2_per_unit'], errors='coerce')

# Eliminăm liniile unde coverage este NaN sau 0 (pentru a evita împărțirea la zero)
df_paving = df_paving[df_paving['coverage_m2_per_unit'] > 0]

# --- PASUL 2: Indicatori Cheie ---
# Calculăm Cost per m2
df_paving['cost_per_m2'] = df_paving['list_price_gbp'] / df_paving['coverage_m2_per_unit']

# Statistici cu NumPy pentru Cost per m2
cost_percentiles = np.percentile(df_paving['cost_per_m2'], [25, 50, 75])
print(f"Cost per m2 - 25th percentile: £{cost_percentiles[0]:.2f}")
print(f"Cost per m2 - Median (50th):   £{cost_percentiles[1]:.2f}")
print(f"Cost per m2 - 75th percentile: £{cost_percentiles[2]:.2f}")

# Statistici pentru Quality Rating
mean_rating = df_paving['quality_rating'].mean()
std_rating = df_paving['quality_rating'].std()
print(f"Quality Rating - Media: {mean_rating:.2f}, Deviația Std: {std_rating:.2f}")

# --- PASUL 3: Vizualizări ---

# A. Histogramă Cost per m2
plt.figure(figsize=(10, 6))
sns.histplot(data=df_paving, x='cost_per_m2', kde=True, color='skyblue')
plt.title('Distribuția Costului per m² (Paving)')
plt.xlabel('Cost (£/m²)')
plt.show()

# B. Boxplot pe Subcategorii
#

[Image of interpreting a box plot]

plt.figure(figsize=(12, 8))
sns.boxplot(data=df_paving, x='subcategory', y='cost_per_m2')
plt.xticks(rotation=45)
plt.title('Variația prețului per m² pe Subcategorii')
plt.show()

# C. Scatter Plot + Regresie (Cost vs Rating)
#

[Image of positive vs negative correlation scatter plot]

plt.figure(figsize=(10, 6))
sns.regplot(data=df_paving, x='cost_per_m2', y='quality_rating',
            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Corelația: Cost per m² vs Quality Rating')
plt.xlabel('Cost (£/m²)')
plt.ylabel('Rating (1-5)')
plt.show()

# --- PASUL 4: Segmentare pe Intervale de Rating ---
# Definim intervalele (bins)
bins = [0, 3.9, 4.4, 5.0]
labels = ['3.0-3.9 (Low/Mid)', '4.0-4.4 (Good)', '4.5-5.0 (Excellent)']

df_paving['rating_segment'] = pd.cut(df_paving['quality_rating'], bins=bins, labels=labels)

# Grupăm și agregăm
segment_analysis = df_paving.groupby('rating_segment', observed=False).agg({
    'cost_per_m2': 'mean',
    'sku_id': 'count' # presupunem că ai o coloană de ID unic, altfel folosește orice coloană
}).rename(columns={'sku_id': 'numar_produse'})

print("\nAnaliza pe Segmente de Rating:")
print(segment_analysis)

# Vizualizare Bar Chart pentru segmente
plt.figure(figsize=(8, 5))
sns.barplot(data=segment_analysis.reset_index(), x='rating_segment', y='cost_per_m2', palette='viridis')
plt.title('Cost Mediu per m² pe Segmente de Calitate')
plt.ylabel('Cost Mediu (£/m²)')
plt.show()