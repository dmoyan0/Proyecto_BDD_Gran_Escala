from src.convert_csv_to_avro import ConvertCsvToAvro
from src.convert_csv_to_parquet import ConvertCsvToParquet

import os
import json
import matplotlib.pyplot as plt

def graph(results):
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharey=True)
    
    # Title
    fig.suptitle('Tamaño de Empaquetado por Archivo (kB)', fontsize=16, y=0.97)

    # Subtitle
    fig.text(0.5, 0.935, 'Tamaños expresados en kB (1 kB = 1024 bytes)',
             ha='center', va='center', fontsize=10, color='gray')

    axs = axs.flatten()

    for i, (nombre_archivo, tamanos_kb) in enumerate(results.items()):
        metodos = list(tamanos_kb.keys())
        valores_kb = list(tamanos_kb.values())

        bars = axs[i].bar(metodos, valores_kb, color='skyblue')
        axs[i].set_title(nombre_archivo, fontsize=10)
        axs[i].tick_params(axis='x', rotation=90)
        axs[i].grid(True, axis='y', linestyle='--', alpha=0.6)

        for bar in bars:
            height = bar.get_height()
            axs[i].text(bar.get_x() + bar.get_width()/2, height + 1, 
                        f'{height:.2f}', ha='center', va='bottom', fontsize=6)

    axs[-1].axis('off')

    fig.text(0.06, 0.5, 'Tamaño (kB)', va='center', rotation='vertical', fontsize=12)

    plt.tight_layout(rect=[0.04, 0.04, 1, 0.90])
    fig.subplots_adjust(left=0.1)

    # Create dir image/ if not exist
    os.makedirs("image", exist_ok=True)

    # Save image
    fig.savefig("image/Figura1.png", dpi=300)
    print("Gráfico guardado en 'image/Figura1.png'")

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
        filename = file.split("/")[-1]
        results[filename] = {}

        # AVRO
        for codec in ["null", "deflate", "snappy"]:
            key = f"AVRO-{codec}"
            output_path = ConvertCsvToAvro().convert(file, "output", codec)
            size_bytes = os.path.getsize(output_path)
            size_kb = size_bytes / 1024  # bytes to kilobytes
            results[filename][key] = round(size_kb, 2)

        # PARQUET
        for codec in ["NONE", "SNAPPY", "GZIP", "LZ4"]:
            key = f"PARQUET-{codec}"
            output_path = ConvertCsvToParquet().convert(file, "output", codec)
            size_bytes = os.path.getsize(output_path)
            size_kb = size_bytes / 1024  # bytes to kilobytes
            results[filename][key] = round(size_kb, 2)

    # Save results in .json
    with open("empaquetado_size.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Tamaños de archivos guardados en 'empaquetado_size.json'")

    print("Generando gráfico con los datos obtenidos")
    graph(results)

if __name__ == "__main__": 
  main()