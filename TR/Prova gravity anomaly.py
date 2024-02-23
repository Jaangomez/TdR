import pandas as pd
import numpy as np
df = pd.read_csv("landgrav_csv.csv")

print(df.columns)

y = df.LATITUDE
x = df.LONGITUDE
z = df.STATION_ELEV
col = df.BOUGUER_AN
import matplotlib.pyplot as plt
plt.figure(figsize = (12, 10))
plt.subplot(1,2,1)
plt.scatter(x, y, c = z, cmap = "viridis", s=1)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar()
plt.title("Elevation Map")
plt.subplot(1,2,2)
plt.scatter(x, y, c = col, cmap = "jet", s=1)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar()
plt.title("Bouguer Anomaly Map")
plt.show()


               
