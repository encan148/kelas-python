import dbf
import pandas as pd

def dbf_to_xlsx(dbf_file, xlsx_file):
    """
    Converts a DBF file to an XLSX (Excel) file using pandas.

    Args:
        dbf_file (str): Path to the input DBF file.
        xlsx_file (str): Path to the output XLSX file.
    """
    try:
        table = dbf.Table(dbf_file)
        table.open()

        # Read the DBF table into a pandas DataFrame
        df = pd.DataFrame(iter(table))

        # Write the DataFrame to an Excel file
        df.to_excel(xlsx_file, index=False, engine='openpyxl')

        table.close()
        print(f"Successfully converted '{dbf_file}' to '{xlsx_file}'")

    except ImportError:
        print("Error: pandas and openpyxl libraries are required. Please install them using 'pip install pandas openpyxl'")
    except dbf.errors.DBFError as e:
        print(f"Error reading DBF file '{dbf_file}': {e}")
    except IOError as e:
        print(f"Error opening or writing file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_dbf_file = "input.dbf"      # Replace with your DBF file path
    output_xlsx_file = "output.xlsx"    # Replace with your desired XLSX file path

    dbf_to_xlsx(input_dbf_file, output_xlsx_file)
