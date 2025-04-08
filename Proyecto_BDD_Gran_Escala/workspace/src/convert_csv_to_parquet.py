import csv
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from decimal import Decimal
from .convert import Convert

class ConvertCsvToParquet(Convert):

    def convert(self, input_filename, output_folder, compression):
        # Get output filename
        output_path = self.get_output_filename(input_filename, output_folder, "parquet", compression)
        print(f"Converting {input_filename} to Parquet with compression {compression}")

        # Create schema
        parquet_schema = pa.schema([
            pa.field("UTC_Date", pa.timestamp("ms")),
            pa.field("Profundity", pa.string()),
            pa.field("Magnitude", pa.string()),       
            pa.field("Date", pa.date32()),
            pa.field("Hour", pa.time32('ms')),       
            pa.field("Location", pa.string()),       
            pa.field("Latitude", pa.decimal128(5, 3)), 
            pa.field("Longitude", pa.decimal128(6, 3))
        ])

        # Reading CSV and converting to Parquet
        records = []
        with open(input_filename, encoding='utf-8', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                record = {
                    "UTC_Date": datetime.strptime(row["UTC_Date"], "%Y-%m-%d %H:%M:%S"),
                    "Profundity": row["Profundity"],
                    "Magnitude": row["Magnitude"],
                    "Date": datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                    "Hour": datetime.strptime(row["Hour"], "%H:%M:%S").time(),
                    "Location": row["Location"],
                    "Latitude": Decimal(row["Latitude"]),
                    "Longitude": Decimal(row["Longitude"])
                }
                records.append(record)
        # Create DataFrame
        table = pa.Table.from_pylist(records, schema=parquet_schema)

        pq.write_table(
            table,
            output_path,
            compression=compression,
        )
        print(f"Parquet file created successfully at {output_path}")
        return output_path
