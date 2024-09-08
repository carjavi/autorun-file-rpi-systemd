
# permite elegir si graficar todas las columnas o una en espeficico. cuando imprime todas imprimen uno x uno


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

# Función para listar archivos .log en el directorio actual
def list_log_files():
    log_files = [f for f in os.listdir() if f.endswith('.log')]
    return log_files

# Función para leer datos de un archivo .log
def read_log_file(log_file):
    dates = []
    data_dict = {}

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split(',')
                date_str = data[0].strip('[]')
                date = datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S')
                
                for item in data[1:]:
                    name, value_with_unit = item.split(':')
                    value_str = ''.join([char for char in value_with_unit if char.isdigit() or char == '.'])
                    value = float(value_str)
                    unit = value_with_unit.replace(value_str, '').strip()

                    if name not in data_dict:
                        data_dict[name] = {'values': [], 'units': []}

                    data_dict[name]['values'].append(value)
                    data_dict[name]['units'].append(unit)
                    data_dict[name]['dates'] = data_dict[name].get('dates', []) + [date]

        df_dict = {}
        for name, info in data_dict.items():
            df_dict[name] = pd.DataFrame({
                'Date': info['dates'],
                f'{name} ({info["units"][0]})': info['values']
            }).set_index('Date')

        return df_dict
    except Exception as e:
        print(f"Error reading {log_file}: {e}")
        return {}

# Función para graficar una columna específica
def plot_by_type(df_dict, data_type, period='day', start_date=None, end_date=None, min_value=None, max_value=None):
    try:
        if data_type not in df_dict:
            print(f"No data available for type {data_type}")
            return

        df = df_dict[data_type]
        
        if period == 'day':
            if start_date:
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                df = df[df.index.date == start_date.date()]
        elif period == 'month':
            if start_date:
                month = datetime.strptime(start_date, '%m-%Y')
                df = df[(df.index.month == month.month) & (df.index.year == month.year)]
        elif period == 'range':
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
                df = df[(df.index >= start_date) & (df.index <= end_date)]
        elif period == 'value_range':
            if min_value is not None and max_value is not None:
                df = df[(df[df.columns[0]] >= min_value) & (df[df.columns[0]] <= max_value)]

        if df.empty:
            print(f"No data available for the specified criteria.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df[df.columns[0]], marker='o', linestyle='-', color='b')
        plt.title(f'{data_type} over time')
        plt.xlabel('Time')
        plt.ylabel(df.columns[0])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error plotting data for {data_type}: {e}")

# Función para graficar todas las columnas
def plot_all_columns(df_dict, period='day', start_date=None, end_date=None, min_value=None, max_value=None):
    try:
        for data_type, df in df_dict.items():
            print(f"Plotting data for {data_type}...")
            if period == 'day':
                if start_date:
                    start_date = datetime.strptime(start_date, '%d-%m-%Y')
                    df = df[df.index.date == start_date.date()]
            elif period == 'month':
                if start_date:
                    month = datetime.strptime(start_date, '%m-%Y')
                    df = df[(df.index.month == month.month) & (df.index.year == month.year)]
            elif period == 'range':
                if start_date and end_date:
                    start_date = datetime.strptime(start_date, '%d-%m-%Y')
                    end_date = datetime.strptime(end_date, '%d-%m-%Y')
                    df = df[(df.index >= start_date) & (df.index <= end_date)]
            elif period == 'value_range':
                if min_value is not None and max_value is not None:
                    df = df[(df[df.columns[0]] >= min_value) & (df[df.columns[0]] <= max_value)]

            if df.empty:
                print(f"No data available for {data_type} with the specified criteria.")
                continue

            plt.figure(figsize=(10, 5))
            plt.plot(df.index, df[df.columns[0]], marker='o', linestyle='-', color='b')
            plt.title(f'{data_type} over time')
            plt.xlabel('Time')
            plt.ylabel(df.columns[0])
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print(f"Error plotting all columns: {e}")

# Función principal
def main():
    log_files = list_log_files()

    if not log_files:
        print("No .log files found in the directory.")
        return

    print("Available log files:")
    for i, file in enumerate(log_files):
        print(f"{i + 1}. {file}")

    try:
        file_choice = int(input("Select the log file number to plot: ")) - 1
        log_file = log_files[file_choice]

        df_dict = read_log_file(log_file)

        if not df_dict:
            print("No data to display.")
            return

        # Presentamos la opción de elegir entre graficar una columna o todas
        print("Choose plot option:")
        print("1. Plot a specific column")
        print("2. Plot all columns")
        choice = int(input("Enter your choice: "))

        # Si elige graficar una columna específica, se muestran las columnas disponibles
        if choice == 1:
            print("Available data types:")
            for i, data_type in enumerate(df_dict.keys()):
                print(f"{i + 1}. {data_type}")

            data_choice = int(input("Select the data type number to plot: ")) - 1
            data_type = list(df_dict.keys())[data_choice]

            print("1. Plot by day")
            print("2. Plot by month")
            print("3. Plot by date range")
            print("4. Plot by value range")
            plot_choice = int(input("Choose an option: "))

            if plot_choice == 1:
                day = input("Enter the day (dd-mm-yyyy): ")
                plot_by_type(df_dict, data_type, period='day', start_date=day)
            elif plot_choice == 2:
                month = input("Enter the month (mm-yyyy): ")
                plot_by_type(df_dict, data_type, period='month', start_date=month)
            elif plot_choice == 3:
                start_date = input("Enter the start date (dd-mm-yyyy): ")
                end_date = input("Enter the end date (dd-mm-yyyy): ")
                plot_by_type(df_dict, data_type, period='range', start_date=start_date, end_date=end_date)
            elif plot_choice == 4:
                min_value = float(input("Enter the minimum value: "))
                max_value = float(input("Enter the maximum value: "))
                plot_by_type(df_dict, data_type, period='value_range', min_value=min_value, max_value=max_value)
            else:
                print("Invalid choice")
        elif choice == 2:
            # Graficar todas las columnas
            print("1. Plot by day")
            print("2. Plot by month")
            print("3. Plot by date range")
            print("4. Plot by value range")
            plot_choice = int(input("Choose an option: "))

            if plot_choice == 1:
                day = input("Enter the day (dd-mm-yyyy): ")
                plot_all_columns(df_dict, period='day', start_date=day)
            elif plot_choice == 2:
                month = input("Enter the month (mm-yyyy): ")
                plot_all_columns(df_dict, period='month', start_date=month)
            elif plot_choice == 3:
                start_date = input("Enter the start date (dd-mm-yyyy): ")
                end_date = input("Enter the end date (dd-mm-yyyy): ")
                plot_all_columns(df_dict, period='range', start_date=start_date, end_date=end_date)
            elif plot_choice == 4:
                min_value = float(input("Enter the minimum value: "))
                max_value = float(input("Enter the maximum value: "))
                plot_all_columns(df_dict, period='value_range', min_value=min_value, max_value=max_value)
            else:
                print("Invalid choice")
        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

