import csv
import dbf

def csv_to_dbf(csv_file, dbf_file, field_names=None, field_types=None):
    """
    Converts a CSV file to a DBF file.

    Args:
        csv_file (str): Path to the input CSV file.
        dbf_file (str): Path to the output DBF file.
        field_names (list, optional): List of field names for the DBF table.
                                     If None, the first row of the CSV is used.
                                     Defaults to None.
        field_types (list, optional): List of field types for the DBF table.
                                     Must correspond to field_names.
                                     Supported types (case-insensitive):
                                     'C' (Character), 'N' (Numeric), 'F' (Float),
                                     'L' (Logical), 'D' (Date), 'M' (Memo),
                                     'B' (Binary/Blob), 'I' (Integer), 'T' (DateTime).
                                     Defaults to creating all fields as 'C' (Character).
    """
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header row

            if field_names is None:
                field_names = header
            elif len(field_names) != len(header):
                raise ValueError("Number of field names must match the number of columns in the CSV.")

            if field_types is None:
                field_types = ['C'] * len(field_names)
            elif len(field_types) != len(field_names):
                raise ValueError("Number of field types must match the number of field names.")
            else:
                field_types = [ftype.upper() for ftype in field_types]  # Convert to uppercase

            # Create the DBF table structure
            dbf_structure = []
            for name, ftype in zip(field_names, field_types):
                dbf_structure.append((name, ftype))

            # Create the DBF table
            table = dbf.Table(dbf_file, dbf_structure, dbf_type='dbase III+')
            table.open(mode=dbf.WRITE)

            # Add records from the CSV
            for row in reader:
                if len(row) == len(field_names):
                    # Basic type conversion (you might need more sophisticated handling)
                    converted_row = []
                    for value, ftype in zip(row, field_types):
                        if ftype == 'N' or ftype == 'F' or ftype == 'I':
                            try:
                                converted_row.append(float(value) if '.' in value or ftype == 'F' else int(value))
                            except ValueError:
                                converted_row.append(None)  # Or handle error differently
                        elif ftype == 'L':
                            converted_row.append(value.lower() in ['true', 't', 'yes', 'y', '1'])
                        elif ftype == 'D':
                            # Attempt to parse date in common formats (adjust as needed)
                            from datetime import datetime
                            for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d-%b-%Y'):
                                try:
                                    converted_row.append(datetime.strptime(value, fmt).date())
                                    break
                                except ValueError:
                                    pass
                            else:
                                converted_row.append(None)
                        elif ftype == 'T':
                            # Attempt to parse datetime (adjust as needed)
                            from datetime import datetime
                            for fmt in ('%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S'):
                                try:
                                    converted_row.append(datetime.strptime(value, fmt))
                                    break
                                except ValueError:
                                    pass
                            else:
                                converted_row.append(None)
                        else:
                            converted_row.append(value)
                    table.append(converted_row)
                else:
                    print(f"Warning: Skipping row with incorrect number of columns: {row}")

            table.close()
            print(f"Successfully converted '{csv_file}' to '{dbf_file}'")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except dbf.errors.DBFError as e:
        print(f"Error writing DBF file '{dbf_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_csv_file = "input.csv"      # Replace with your CSV file path
    output_dbf_file = "output.dbf"    # Replace with your desired DBF file path

    # Option 1: Infer field names from the CSV header, all fields as Character
    # csv_to_dbf(input_csv_file, output_dbf_file)

    # Option 2: Specify field names and types
    field_names_example = ["ID", "Name", "Price", "Active", "OrderDate"]
    field_types_example = ["N", "C", "F", "L", "D"]
    csv_to_dbf(input_csv_file, output_dbf_file, field_names=field_names_example, field_types=field_types_example)
    