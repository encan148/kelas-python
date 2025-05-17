import dbf
import csv

def dbf_to_csv(dbf_file, csv_file):
    """
    Converts a DBF file to a CSV file.

    Args:
        dbf_file (str): Path to the input DBF file.
        csv_file (str): Path to the output CSV file.
    """
    try:
        table = dbf.Table(dbf_file)
        table.open()

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            writer.writerow(table.field_names)

            # Write data rows
            for record in table:
                writer.writerow(list(record))

        table.close()
        print(f"Successfully converted '{dbf_file}' to '{csv_file}'")

    except dbf.errors.DBFError as e:
        print(f"Error reading DBF file '{dbf_file}': {e}")
    except IOError as e:
        print(f"Error opening or writing file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_dbf_file = "AN251298.dbf"  # Replace with your DBF file path
    output_csv_file = "AN251298.csv" # Replace with your desired CSV file path

    dbf_to_csv(input_dbf_file, output_csv_file)
    