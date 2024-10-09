#Importaciones de librerias
import random
import datetime
import csv
import os
import re
import statistics
import pandas as pd

#Fecha en constante para poder realizar cambios en caso de ser requerido
FORMAT_DATE="%m/%d/%Y"

#Diccionario para almacenar los datos importados 
base_de_datos = {
    "cliente": {},
    "unidad": {},
    "prestamo": {}
}

# Importar la tabla "cliente"
try:
    if os.path.exists('cliente.csv'):
        with open('cliente.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Leer encabezado
            for row in reader:
                id = int(row[0])
                base_de_datos["cliente"][id] = row[1:]
    else:
        print("El archivo cliente.csv no existe.")
except Exception as e:
    print(f"Error al leer cliente.csv: {e}")

# Importar la tabla "unidad"
try:
    if os.path.exists('unidad.csv'):
        with open('unidad.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Leer encabezado
            for row in reader:
                id = int(row[0])
                rodada = int(row[1])
                color = row[2]
                prestado=row[3] == "True"
                print(prestado)
                base_de_datos["unidad"][id] = [rodada,color,prestado]
    else:
        print("El archivo unidad.csv no existe.")
except Exception as e:
    print(f"Error al leer unidad.csv: {e}")

# Importar la tabla "prestamo"
try:
    if os.path.exists('prestamo.csv'):
        with open('prestamo.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Leer encabezado
            for row in reader:
                id = int(row[0])
                base_de_datos["prestamo"][id] = row[1:]
    else:
        print("El archivo prestamo.csv no existe.")
except Exception as e:
    print(f"Error al leer prestamo.csv: {e}")


#CREAMOS UNA CLASE PARA MANEJAR NUESTROS DATAFRAMES
class Dataframes:
    df_unidad= pd.DataFrame(base_de_datos["unidad"]).T
    df_cliente= pd.DataFrame(base_de_datos["cliente"]).T
    df_prestamos= pd.DataFrame(base_de_datos["prestamo"]).T
    df_unidad.columns=["Rodada","Color","Prestado"] 
    df_cliente.columns=["Apellido","Nombre","Telefono"] 
    df_prestamos.columns=["ID_cliente","ID_unidad","Fecha","Dias C","Estado"] 


    def actualizar(self):
        self.df_unidad= pd.DataFrame(base_de_datos["unidad"]).T
        self.df_cliente= pd.DataFrame(base_de_datos["cliente"]).T
        self.df_prestamos= pd.DataFrame(base_de_datos["prestamo"]).T 
        self.df_unidad.columns=["Rodada","Color","Prestado"] 
        self.df_cliente.columns=["Apellido","Nombre","Telefono"] 
        self.df_prestamos.columns=["ID_cliente","ID_unidad","Fecha","Dias C","Estado"] 

#instanciamos la clase data frames para manejar la bd como un data frame

df_db=Dataframes()
from datetime import datetime



# Función para validar que el valor sea un entero positivo
def validate_positive_integer(value, field_name):
    try:
        value = int(value)
        if value <= 0:
            raise ValueError(f"{field_name} debe ser un número entero mayor a cero.")
        return value
    except ValueError as e:
        raise ValueError(f"{field_name} debe ser un número entero válido.") from e

# Función para validar el formato de fecha mm-dd-aaaa
def validate_date_format(date_str, field_name):
    try:
        datetime.strptime(date_str, FORMAT_DATE)
        return date_str
    except ValueError:
        raise ValueError(f"{field_name} debe tener el formato mm/dd/aaaa.")

# Solicitar y validar el folio
def prestamo():
   #REQUISITOS PARA QUE SE PUEDA ACCEDER AL MENU DE PRESTAMOS
    if len(df_db.df_cliente)==0:
        print("actualmente no existen clientes regresando a la ventana anterior que tenga buen dia!")
        return 0
   
    if len(df_db.df_unidad)==0:
        print("actualmente no hay unidades existentes regresando a la ventana anterior que tenga buen dia!")
        return 0
    
    if len(df_db.df_unidad[df_db.df_unidad["Prestado"]==False])==0:
        print("actualmente no hay unidades dispoibles regresando a la ventana anterior que tenga buen dia!")
        return 0
   
    # Solicitar y validar la clave de la unidad
    while True:
        try:
            clave_unidad = validate_positive_integer(input("Clave de la unidad (número entero mayor a cero): "), "Clave de la unidad")
            #VALIDAR SI ESTA CLAVE EXISTE EN NUESTRA TABLA DE UNIDADES
            if clave_unidad not in base_de_datos["unidad"].keys():
                raise ValueError("LA CLAVE DIGITADA NO PERTENECE A NINGUNA UNIDAD")
            
            if base_de_datos["unidad"][clave_unidad][2]==True:
                raise ValueError("LA CLAVE DE LA UNIDAD PERTENECE A UN CARRO PRESTADO")
            
            break
        except ValueError as e:
            print(e)

    # Solicitar y validar la clave del cliente
    while True:
        try:
            clave_cliente = validate_positive_integer(input("Clave del cliente (número entero mayor a cero): "), "Clave del cliente")
            #VALIDAR SI ESTA CLAVE EXISTE EN NUESTRA TABLA CLIENTES
            if clave_cliente not in base_de_datos["cliente"].keys():
                raise ValueError("LA CLAVE DIGITADA NO PERTENECE A NINGUN CLIENTE")
            break
        except ValueError as e:
            print(e)

    # Solicitar y validar la fecha del préstamo
    while True:
        try:
            default_op=input("Desea usar la fecha de ahora como la fecha de prestamo o desea un prestamo a futuro? 1\n1:Si \n2:No, deseo un plazo a futuro \n")
            #FECHA DEFAULT DEL SISTEMA
            if default_op=="1":
                fecha_prestamo=datetime.now()
                fecha_prestamo=fecha_prestamo.strftime(FORMAT_DATE)
                break
                
            #EL USUSARIO DIGITARA UNA FECHA POSTERIOR A LA ACTUAL
            elif default_op=="2":
                while True:
                    try:
                        fecha_prestamo = validate_date_format(input("Fecha del préstamo  recuerde que no puede ser menor a la fecha actual(mm/dd/aaaa): "), "Fecha del préstamo")
                        #HACER LA VLAIDACION QUE LA FECHA NO SEA MENOR A LA ACTUAL
                        date_obj = datetime.strptime(fecha_prestamo, FORMAT_DATE).date()
                        # Verificar que la fecha no sea menor a la fecha actual si lo es mandar un error con su respectivo mensaje
                        if date_obj < datetime.now().date():
                            raise ValueError("La fecha es menor a la del sistema")
                        break
                    except Exception as e:
                        print(e)
                break

                

            

        except Exception as e:
            print("Error el valor digitado no es valido")

    # Solicitar y validar la cantidad de días del préstamo
    while True:
        try:
            cantidad_dias = int(input("Cantidad de días del préstamo (número entero) menor o igual a 14 dias: "))
            if cantidad_dias>14 or 0>=cantidad_dias:
                #SI PASA DE 14 O ES MENOR A 0 GENERAMOS UNA EXCEPCION PARA QUE ENTRE AL BLOQUE DE EXCEPT
                raise Exception
            break
        except Exception as e:
            print("el valor numerico no coincide con lo solicitado")

    # Dejar la fecha de retorno vacía al principio
    fecha_retorno = "N/E"
    
    #EL FOLIO SE GENERA AUTOMATICAMENTE CON LA LONGITUD
    folio = len(base_de_datos["prestamo"])+1

    #ALMACENAMOS LOS DETALLES DEL PRESTAMO EN NUESTRA BASE DE DATOS
    base_de_datos["prestamo"][folio]=[clave_unidad,clave_cliente,fecha_prestamo,cantidad_dias,fecha_retorno]
    #ACTUALIZAR EL ESTADO DE LA UNIDAD
    base_de_datos["unidad"][clave_unidad][2]=True
    #MOSTRAMOS EN CONSOLA ESTOS DETALLES AL CLIENTE
    print("\nDatos del préstamo:")
    print(f"Folio: {folio}")
    print(f"Clave de la unidad: {clave_unidad}")
    print(f"Clave del cliente: {clave_cliente}")
    print(f"Fecha del préstamo: {fecha_prestamo}")
    print(f"Cantidad de días del préstamo: {cantidad_dias}")

# Generador de clave única
def generar_clave():
    return random.randint(1, 10000)

def validar_telefono(telefono):
    # Verifica si el teléfono tiene 10 dígitos y es numérico
    return telefono.isdigit() and len(telefono) == 10

#Logica de Registro de cliente
def registro_cliente():
    print("\n--- Registro de Cliente ---")

    #Generación de clave
    clave = len(base_de_datos["cliente"]) + 1
    print(f"Clave generada: {clave}")
    
    # Solicitar apellidos
    apellidos = ""
    while not apellidos or len(apellidos) > 40:
        apellidos = input("Ingresa los apellidos (máximo 40 caracteres): ")
        if len(apellidos) > 40:
            print("Los apellidos deben tener un máximo de 40 caracteres.")
    
    # Solicitar nombres
    nombres = ""
    while not nombres or len(nombres) > 40:
        nombres = input("Ingresa los nombres (máximo 40 caracteres): ")
        if len(nombres) > 40:
            print("Los nombres deben tener un máximo de 40 caracteres.")
    
    # Solicitar teléfono
    telefono = ""
    while not validar_telefono(telefono):
        telefono = input("Ingresa el teléfono (10 dígitos): ")
        if not validar_telefono(telefono):
            print("El teléfono debe ser numérico y tener 10 dígitos.")

    #Agregar a nuestra base de datos en memoria al cliente
    """
    EJEMPLO
    {
    1:["Avila Lopez", Christian, 8180230620]
    }
    """
    base_de_datos["cliente"][clave]=[apellidos,nombres,telefono]
    print(f"{nombres} {apellidos} \n {telefono} \n cliente registrado con Clave: {clave}")

#Logica de Registro de Unidad
def registro_unidad():
    print("\n--- Registro de Unidad ---")
    #Esto mide la logitud de nuestra base de datos en unidad y le suma 1 esto genera una clave unica e irrepetible
    clave = len(base_de_datos["unidad"]) + 1
    print(f"Clave generada: {clave}") 
    
    
    #Selección de rodada
    rodada = None
    while rodada not in [20, 26, 29]:
        try:
            rodada = int(input("Selecciona la rodada (20, 26, 29): "))
            if rodada not in [20, 26, 29]:
                print("Rodada no válida. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor ingresa un número.")
    #Una vez pasa el filtro de ser 20, 26 o 29 en nuestra base de datos en el diccionario unidad añadimos la clave con su valor 
    """
    EJEMPLO
    {
        1:26
        2:20
        3:29    
    }
    """
    #aqui se pedira el color (Texto, obligatorio, aceptando hasta un máximo de 15 caracteres)
    while True:
        try:
            color=input("Digite un color que no sobre pase 15 caracteres:")
            if not color:
                raise Exception("El campo de color es obligatorio.")
            
            # Verificar si el tamaño excede los 15 caracteres
            if len(color) > 15:
                raise Exception("El color no puede tener más de 15 caracteres.")
        
            break
        except Exception as e:
            print("El color que usted proporciono es invalido\n",e)
        pass
    
    base_de_datos["unidad"][clave]=[rodada,color,False]
    print(f"Unidad registrada con Clave: {clave} y Rodada: {rodada}")

# Lógica de préstamo extendida
def retorno():
    #Cargamos nuestros datos en un df para tener un mejor manejo de nuestros datos
    #Prestamos por retornar
    df_prestamos=df_db.df_prestamos
    pxretornar=df_prestamos[df_prestamos["Estado"]=="N/E"]

    if len(pxretornar)==0:
        print("actualmente no hay pretsamos pendientes regresando a la ventana anterior que tenga buen dia!")
        return 0
    
    #vamos a mostrarle al usuario cuales son los pedidos que estan por retornar y su detalle
    for folio,row in pxretornar.iterrows():
        print(f"El prestamo con folio {folio} aun no se ha regresado ")
    #Folio de prestamo 
    while True:
        try:
            folio_s = validate_positive_integer(input("Folio (número entero mayor a cero): "), "Folio")
            if folio_s not in pxretornar.index.tolist():
                raise Exception("El folio no pertenece a ningun pedido que este pendiente")
            break
        except Exception as e:
            print(e)

    #Fecha efectiva de retorno
    while True:
        try:
            fecha_e_retorno = input(f"Ingrese la fecha efectiva de retorno con el formato: ({FORMAT_DATE}): ")
            # Convertir las fechas a objetos datetime
            fecha_1 = datetime.strptime(fecha_e_retorno, FORMAT_DATE)
            if fecha_1.date() < datetime.now().date():
                raise Exception
            break
        except Exception as e:
            print("La fecha proporcionada no es valida recuerde que la fecha de retorno no puede ser menor que la del sistema\n",e)
    
    #SACAMOS LOS DETALLES PARA INDICARLE A NUESTRO CLIENTE CUAL FUE EL PRESTAMO QUE RETORNO
    c_unidad=base_de_datos["prestamo"][folio][0]
    c_cliente=base_de_datos["prestamo"][folio][1]
    #INDICAMOS LA FECHA ACTUAL EN FECHA DE RETORNO EN DETALLES DE PRESTAMO
    base_de_datos["prestamo"][folio][4]=fecha_e_retorno
    #VOLVEMOS A DEJAR DISPOIBLE EL VEHICULO QUE ESTABA BAJO PRESTAMO
    
    base_de_datos["unidad"][int(base_de_datos["prestamo"][folio][1])][2]=False
    print(f"EL CLIENTE CON CLAVE: {c_cliente}\n DEVOLVIO LA UNIDAD CON CLAVE: {c_unidad}\n")


def reportes_clientes():
    print("\n--- Reporte de Clientes ---")
    #RECORREMOS TODA LA BASE DE DATOS EN LA TABLA CLIENTES PARA MOSTRAR ABSOLUTAMENTE TODOS LOS CLIENTES 

    for cliente_id,cliente_datos in base_de_datos["cliente"].items():
        print(cliente_id,cliente_datos)
    while True:
        #ESTE TRAMO DE CODIGO SOLO VALIDA LA VERACIDAD DE LA OPCION OSEA QUE SEA 1 O 2
        try:
            opcion=int(input("¿Quieres Exportar? \n1:Si \n 2: No\n"))
            if opcion not in [1,2]:
                print("Esta opcion no esta disponible:",opcion)
                raise Exception
            break
        except Exception as e:
            print("La ocpion digitada no es valida")      
    if opcion==1:
        #INICIALISAMOS EL ARCHIVO CSV
        with open('reporte_clientes.csv', 'w', newline='') as file:
            #ESTE SERA EL ESCRTOR DEL ARCHIVO
            writer = csv.writer(file)
            #DEFINIMOS LOS ENCABEZADOS
            writer.writerow(["ID", "Apellido", "Nombre", "Teléfono"])  # Encabezado

            for id, data in base_de_datos["cliente"].items():
                #Y ESCRIBIMOS LAS COLUMNAS DEL REPORTE EN BASE A LO QUE TENEMOS EN CLIENTES EN NUESTRA BASE DE DATOS
                writer.writerow([id] + data)
            print("EL ARCHIVO SE EXPORTO CORRECTAMENTE")
        pass
    else:
        print("Perfecto que tenga un buen dia")

def reportes_prestamos_retorno():
    print("\n--- Reporte de Préstamos por Retornar ---")
    while True:
        #VERIFICAR QUE LAS FECHAS SON CORRECTAS
        try:
            fecha_1_str = input(f"Ingrese la primer fecha ({FORMAT_DATE}): ")
            fecha_2_str = input(f"Ingrese la segunda fecha ({FORMAT_DATE}): ")

            # Convertir las fechas a objetos datetime
            fecha_1 = datetime.strptime(fecha_1_str, FORMAT_DATE)
            fecha_2 = datetime.strptime(fecha_2_str, FORMAT_DATE)
            
            if fecha_1 > fecha_2:
                fecha_fin = fecha_1
                fecha_inicio = fecha_2
            else:
                fecha_fin = fecha_2
                fecha_inicio = fecha_1
            break
        except Exception as e:
            print("Las fecha proporcionada no coinciden con lo solicitado por favor digite la fecha MM/DD/YYYY")
        
        
        
    for key,value in base_de_datos["prestamo"].items():
       fecha_folio=datetime.strptime(value[2], FORMAT_DATE)
       if fecha_inicio <= fecha_folio and fecha_fin >= fecha_folio:
            if value[4] == "N/E":
                print(key,value)


    while True:
        try:
            opcion=int(input("¿Quieres Exportar? \n1:Si \n 2: No\n"))
            if opcion not in [1,2]:
                print("esta opcion no esta disponible")
                raise Exception
            break
        except Exception as e:
            print("La ocpion digitada no es valida")
    
    if opcion==1:
        with open('retornar_reporte.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Cliente_ID", "Unidad_ID", "Fecha", "Cantidad", "Observaciones"])  # Encabezado
            for id, data in base_de_datos["prestamo"].items():
                fecha_folio=datetime.strptime(data[2], FORMAT_DATE)
                if fecha_inicio <= fecha_folio and fecha_fin >= fecha_folio:
                    if data[4] == "N/E":
                        writer.writerow([id] + data)
        print("EL ARCHIVO SE EXPORTO CORRECTAMENTE")

    else:
        print("Perfecto que tenga un buen dia")

def reportes_prestamos_periodo():
    print("\n--- Reporte de Préstamos por Periodo ---")
    while True:
        #VERIFICAR QUE LAS FECHAS SON CORRECTAS 
        try:
            """
            ESTE TRAMO DE CODIGO RECIVE DOS FECHAS Y ASIGNA LA FECHA FIN COMO LA MAYOR Y LA INICIO 
            """
            fecha_1_str = input(f"Ingrese la primer fecha ({FORMAT_DATE}): ")
            fecha_2_str = input(f"Ingrese la segunda fecha ({FORMAT_DATE}): ")

            # Convertir las fechas a objetos datetime
            fecha_1 = datetime.strptime(fecha_1_str, FORMAT_DATE)
            fecha_2 = datetime.strptime(fecha_2_str, FORMAT_DATE)
            
            if fecha_1 > fecha_2:
                fecha_fin = fecha_1
                fecha_inicio = fecha_2
            else:
                fecha_fin = fecha_2
                fecha_inicio = fecha_1
            break
        except Exception as e:
            print("Las fecha proporcionada no coinciden con lo solicitado por favor digite la fecha MM/DD/YYYY")
        
    for key,value in base_de_datos["prestamo"].items():
       fecha_folio=datetime.strptime(value[2], FORMAT_DATE)
       if fecha_inicio <= fecha_folio and fecha_fin >= fecha_folio:
            print(key,value)

    while True:
        #ESTE TRAMO DE CODIGO SOLO VALIDA LA VERACIDAD DE LA OPCION OSEA QUE SEA 1 O 2
        try:
            opcion=int(input("¿Quieres Exportar? \n1:Si \n 2: No\n"))
            if opcion not in [1,2]:
                print("Esta opcion no esta disponible:",opcion)
                raise Exception
            break
        except Exception as e:
            print("La ocpion digitada no es valida")   
    if opcion==1:
        with open('retornar_periodo.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Cliente_ID", "Unidad_ID", "Fecha", "Cantidad", "Observaciones"])  # Encabezado
            for id, data in base_de_datos["prestamo"].items():
                fecha_folio=datetime.strptime(data[2], FORMAT_DATE)
                if fecha_inicio <= fecha_folio and fecha_fin >= fecha_folio:
                    writer.writerow([id] + data)
        print("EL ARCHIVO SE EXPORTO CORRECTAMENTE")
    else:
        print("Perfecto que tenga un buen dia")

    
def salir():
    print("\nSaliendo del sistema. ¡Hasta luego!")
    

# Menús
def main_menu():
    print("\n--- Menú Principal ---")
    print("1. Registro")
    print("2. Préstamo")
    print("3. Retorno")
    print("4. Informes")
    print("5. Salir")


def registro_menu():
    print("\n--- Registro ---")
    print("1. Unidad")
    print("2. Cliente")
    print("3. Volver al Menú Principal")

def reportes_menu():
    print("\n--- Reportes ---")
    print("1. Clientes")
    print("2. Préstamos por Retornar")
    print("3. Préstamos por Período")
    print("4. Volver al Menú Principal")
    print("5. Retrasos")
    print("6. Listado de unidades")

def retrasos():
    pass

def listado_unidades():
    pass


# Función principal
def menu():
    while True:
        main_menu()
        opcion = input("Selecciona una opción:")
        #ES IMPORTANTE CARGAR LOS DATA FRAMES AQUI YA QUE CUALQUIER ACTUALIZACION QUE HAGA EL USUARIO DURANTE LA EJECUCION SE VERA REFLEJADA EN LOS REPORTES Y ANALISIS GRACIAS A ESTAS LINEAS
        df_db.actualizar()
        #Menu de Registros

        if opcion == '1':
            while True:
                registro_menu()
                sub_opcion = input("Selecciona una opción: ")
                #Registro de unidad
                if sub_opcion == '1':
                    registro_unidad()
                #Registro de cliente
                elif sub_opcion == '2':
                    registro_cliente()
                #Volver al menu principal
                elif sub_opcion == '3':
                    break
                #Caso contrario indicar al usuario que la opcion es invalida
                else:
                    print("Opción no válida. Inténtalo de nuevo.")
        
        #MENU DE PRESTAMO
        elif opcion == '2':
            prestamo()
        #MENU DE RETORNO
        elif opcion == '3':
            retorno()

        #MENU INFORMES
        elif opcion == '4':
            while True:
                opcion=input("A QUE SUB MENU DESEA IR:\n1:Reportes\n2:Analisis\n3:Volver al menu principal")
                #MENU DE REPORTES
                if opcion =="1":
                    while True:
                        reportes_menu()
                        sub_opcion = input("Bienvendio al menu de reportes selecciona una opción: ")
                        if sub_opcion == '1':
                            reportes_clientes()
                        elif sub_opcion == '2':
                            reportes_prestamos_retorno()
                        elif sub_opcion == '3':
                            reportes_prestamos_periodo()
                        elif sub_opcion == '4':
                            break
                        #Retrasos
                        elif sub_opcion == '5':

                            break
                        #Listado de unidades
                        elif sub_opcion == '6':
                            break
                        else:
                            print("Opción no válida. Inténtalo de nuevo.")
                #MENU DE ANALISIS
                elif opcion=="2":
                    pass
                #ESCAPE DEL SUB MENU
                elif opcion=="3":
                    break
                else:
                    print("esa opcion no esta disponible")
       
        #ESCAPE DEL SISTEMA
        elif opcion == '5':
            salir()
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Llamada al menú principal
menu()

# Exportar la tabla "cliente" aqui es donde almacenaremos nuestros datos
with open('cliente.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Apellido", "Nombre", "Teléfono"])  # Encabezado
    for id, data in base_de_datos["cliente"].items():
        writer.writerow([id] + data)

# Exportar la tabla "unidad" aqui es donde almacenaremos nuestros datos
with open('unidad.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Rodada","Color","Prestado"])  # Encabezado
    for id, datos in base_de_datos["unidad"].items():
        
        rodada=datos[0]
        color=datos[1]
        prestado=datos[2]
        writer.writerow([id, rodada, color, prestado])

# Exportar la tabla "prestamo" aqui es donde almacenaremos nuestros datos
with open('prestamo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Cliente_ID", "Unidad_ID", "Fecha", "Dias Cantidad", "Fecha retorno"])  # Encabezado
    for id, data in base_de_datos["prestamo"].items():
        writer.writerow([id] + data)
