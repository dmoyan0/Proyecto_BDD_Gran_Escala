from src.convert_csv_to_avro import ConvertCsvToAvro
from src.convert_csv_to_parquet import ConvertCsvToParquet

import time
import json
import matplotlib.pyplot as plt

def graph(results):
  fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharey=True)
  fig.suptitle('Tiempos de Empaquetado por Archivo (segundos)', fontsize=16)

  axs = axs.flatten()

  for i, (nombre_archivo, tiempos) in enumerate(results.items()):
      metodos = list(tiempos.keys())
      valores = list(tiempos.values())
      
      bars = axs[i].bar(metodos, valores, color='skyblue')
      axs[i].set_title(nombre_archivo, fontsize=10)
      axs[i].tick_params(axis='x', rotation=90)
      axs[i].grid(True, axis='y', linestyle='--', alpha=0.6)

      for bar in bars:
          height = bar.get_height()
          axs[i].text(bar.get_x() + bar.get_width()/2, height + 0.02, 
                      f'{height}', ha='center', va='bottom', fontsize=6)

  axs[-1].axis('off')

  fig.text(0.06, 0.5, 'Tiempo (s)', va='center', rotation='vertical', fontsize=12)

  plt.tight_layout(rect=[0.04, 0.04, 1, 0.95])
  fig.subplots_adjust(left=0.1)
  plt.show()

    
def main():
    print("Running")
    files = [
        "data/EarthquakesChile_2000-2024_1pct.csv",
        "data/EarthquakesChile_2000-2024_10pct.csv",
        "data/EarthquakesChile_2000-2024_25pct.csv",
        "data/EarthquakesChile_2000-2024_50pct.csv",
        "data/EarthquakesChile_2000-2024.csv"
    ]

    results = {}

    for file in files:
        # Find name of file
        filename = file.split("/")[-1]
        results[filename] = {}

        # AVRO
        for codec in ["null", "deflate", "snappy"]:
            key = f"AVRO-{codec}"
            start = time.time()
            ConvertCsvToAvro().convert(file, "output", codec)
            end = time.time()
            results[filename][key] = round(end - start, 5)

        # PARQUET
        for codec in ["NONE", "SNAPPY", "GZIP", "LZ4"]:
            key = f"PARQUET-{codec}"
            start = time.time()
            ConvertCsvToParquet().convert(file, "output", codec)
            end = time.time()
            results[filename][key] = round(end - start, 5)

    # Save results as JSON
    with open("empaquetado_tiempos.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Tiempos de conversión guardados en 'empaquetado_tiempos.json'")

    print("Generando gráficos con los datos obtenidos")
    graph(results)



if __name__ == "__main__": 
  main()