import numpy as np

# Ejemplo de datos
data = np.array([1, 2, 3, 4, 5, 1000])

# Calcular el primer y tercer cuartil
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)

# Calcular el rango intercuartílico (IQR)
IQR = Q3 - Q1

# Definir los límites para identificar los valores atípicos
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrar los valores atípicos
filtered_data = data[(data >= lower_bound) & (data <= upper_bound)]
print (filtered_data)