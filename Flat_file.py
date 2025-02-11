import pymssql
import csv
import datetime

def input_date(prompt):
    while True:
        try:
            date_str = input(prompt)
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj
        except ValueError:
            print("Fecha no válida. Por favor, ingresa la fecha en formato YYYY-MM-DD.")

def main():
    #Informacion para la conexión base de datos
    userdata = input("Usuario de conexión")
    passworddata = input ("Clave de conexión")
    hostddata = input ("ip de de conexión ")
    nameddatabase = input ("nombre de la base de datos")

    #Valores ingresados para  la generacion del archivo
    fecha_inicial = input_date("Ingresa la fecha inicial (YYYY-MM-DD): ")
    fecha_final = input_date("Ingresa la fecha final (YYYY-MM-DD): ")

    #Conexión a la base de datos
    config = {
        'user': userdata,
        'password': passworddata,
        'host': hostddata,
        'database': nameddatabase,
    }

    try:
        connection = pymssql.connect(**config)
        cursor = connection.cursor()

        query = """ Consulta realizada a Base de datos para crear el archivo plano"""
        cursor.execute(query, (fecha_inicial.strftime('%Y-%m-%d'), fecha_final.strftime('%Y-%m-%d')))

        column_names = [i[0] for i in cursor.description]

        with open('resultado.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(column_names)
            
            for row in cursor:
                writer.writerow(row)

        print("Consulta ejecutada y archivo generado exitosamente.")

    except pymssql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()