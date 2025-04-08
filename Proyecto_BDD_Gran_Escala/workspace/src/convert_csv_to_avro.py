import csv
import fastavro
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from .convert import Convert

class ConvertCsvToAvro(Convert):
    def convert(self, input_filename, output_folder, compression):
        # Get output filename
        output_path = self.get_output_filename(input_filename, output_folder, "avro", compression)
        print(f"Converting {input_filename} to AVRO with compression {compression}")
        
        # Load avro schema
        parsed_schema = fastavro.schema.load_schema('resources/Earthquake schema.avsc')

        # Reading CSV and converting to AVRO
        # UTC_Date,Profundity,Magnitude,Date,Hour,Location,Latitude,Longitude
        records = []
        with open(input_filename, encoding='utf-8', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                record = {
                    "UTC_Date": int(datetime.strptime(row['UTC_Date'], "%Y-%m-%d %H:%M:%S").timestamp() * 1_000_000),
                    "Profundity": row["Profundity"],
                    "Magnitude": row["Magnitude"],
                    "Date": (datetime.strptime(row['Date'], "%Y-%m-%d").timestamp() if row['Date'] else None),
                    "Hour": (datetime.strptime(row['Hour'], "%H:%M:%S").timestamp() if row['Hour'] else None),
                    "Location": row["Location"],
                    "Latitude": Decimal(row["Latitude"]) if row["Latitude"] else None,
                    "Longitude": Decimal(row["Longitude"]) if row["Longitude"] else None
                }
                records.append(record)
        # Write records to AVRO file
        with open(output_path, 'wb') as out:
            fastavro.writer(out, parsed_schema, records, codec=compression)
        print(f"AVRO file created successfully at {output_path}")
        return output_path
            