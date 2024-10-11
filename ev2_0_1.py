#Importaciones de librerias
import random
import datetime
import csv
import os
import re
import statistics
import pandas as pd


def limpiar_pantalla():
    # Verifica el sistema operativo
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Linux/MacOS
        os.system('clear')

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
    def __init__(self):
    
        self.df_unidad= pd.DataFrame(base_de_datos["unidad"]).T
        self.df_cliente= pd.DataFrame(base_de_datos["cliente"]).T
        self.df_prestamos= pd.DataFrame(base_de_datos["prestamo"]).T
        if not(len(base_de_datos["cliente"])==0):
            self.df_cliente.columns=["Apellido","Nombre","Telefono"] 
        if not(len(base_de_datos["prestamo"])==0):
            self.df_prestamos.columns=["ID_cliente","ID_unidad","Fecha","Dias C","Estado"] 
        if not(len(base_de_datos["unidad"])==0):
            self.df_unidad.columns=["Rodada","Color","Prestado"]



    def actualizar(self):
        self.df_unidad= pd.DataFrame(base_de_datos["unidad"]).T
        self.df_cliente= pd.DataFrame(base_de_datos["cliente"]).T
        self.df_prestamos= pd.DataFrame(base_de_datos["prestamo"]).T 
        if not(len(base_de_datos["cliente"])==0):
            self.df_cliente.columns=["Apellido","Nombre","Telefono"] 
        if not(len(base_de_datos["prestamo"])==0):
            self.df_prestamos.columns=["ID_cliente","ID_unidad","Fecha","Dias C","Estado"] 
        if not(len(base_de_datos["unidad"])==0):
            self.df_unidad.columns=["Rodada","Color","Prestado"]

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
    if vacio_prestamo() or vacio_cliente():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
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

def exportardf(df,nombre_exportacion):
    if len(df)==0:
        limpiar_pantalla()
        print("POR AHORA NO HAY NINGUN REGISTRO EN EL REPORTE CON LAS CONDICIONES QUE USTED PROPORCIONA MUCHAS GRACIAS QUE TENGA UN BUEN DIA!")
        return 0
    while True:
        #ESTE TRAMO DE CODIGO SOLO VALIDA LA VERACIDAD DE LA OPCION OSEA QUE SEA 1 O 2
        try:
            opcion=int(input("¿Quieres Exportar? \n1:Si \n2:No\n"))
            if opcion not in [1,2]:
                print("Esta opcion no esta disponible:",opcion)
                raise Exception
            break
        except Exception as e:
            print("La ocpion digitada no es valida")   

    if opcion==1:
        df.to_csv(nombre_exportacion,index=False)
        pass
    else:
        print("Perfecto que tenga un buen dia")

def reportes_clientes():
    print("\n--- Reporte de Clientes ---")
    if vacio_cliente():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    #RECORREMOS TODA LA BASE DE DATOS EN LA TABLA CLIENTES PARA MOSTRAR ABSOLUTAMENTE TODOS LOS CLIENTES 
    todos_clientes=df_db.df_cliente
    print(todos_clientes)
    exportardf(todos_clientes,"REPORTE_CLIENTES.csv")


def reportes_prestamos_retorno():
    print("\n--- Reporte de Préstamos por Retornar ---")
    if vacio_prestamo() or vacio_cliente() or vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
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
    #CONVERTIR LA COLUMNA FECHA A FECHAS
    df_db.df_prestamos["Fecha"] = df_db.df_prestamos['Fecha'].apply(lambda value: datetime.strptime(value, FORMAT_DATE))
    #FILTRAR LAS QUE ESTAN POR RETORNAR
    filtro = (fecha_inicio <= df_db.df_prestamos['Fecha']) & (fecha_fin >= df_db.df_prestamos['Fecha'])
    df_filtrado=df_db.df_prestamos[filtro] 
    #QUE ESTEN EN N/E
    df_xretornar=df_filtrado[df_filtrado["Estado"]=="N/E"]

    #HACEMOS LOS TPOS DE DATOS COMPATIBLES PARA EL MERGE
    df_xretornar["ID_unidad"] = df_xretornar["ID_unidad"].astype(int)
    df_xretornar["ID_cliente"] = df_xretornar["ID_cliente"].astype(int)
    #HACEMOS LOS INNER JOINS
    df_resultado = pd.merge(df_xretornar, df_db.df_unidad, left_on="ID_unidad", right_index=True)
    df_resultado = pd.merge(df_resultado, df_db.df_cliente, left_on="ID_cliente", right_index=True)

    # Seleccionar las columnas necesarias para el reporte
    df_reporte = df_resultado[["ID_unidad", "Rodada", "Fecha", "Nombre", "Apellido", "Telefono"]]
    print(df_reporte)
    exportardf(df_reporte,"REPORTE_X_RETORNAR.csv")


def reportes_prestamos_periodo():
    print("\n--- Reporte de Préstamos por Periodo ---")

    if vacio_prestamo() or vacio_cliente() or vacio_unidad():
            print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
            return 0
    
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
    #CONVERTIR LA COLUMNA FECHA A FECHAS
    df_db.df_prestamos["Fecha"] = df_db.df_prestamos['Fecha'].apply(lambda value: datetime.strptime(value, FORMAT_DATE))
    #FILTRAR LAS QUE ESTAN POR RETORNAR
    filtro = (fecha_inicio <= df_db.df_prestamos['Fecha']) & (fecha_fin >= df_db.df_prestamos['Fecha'])


    df_filtrado=df_db.df_prestamos[filtro] 
    df_filtrado["ID_unidad"] = df_filtrado["ID_unidad"].astype(int)
    df_filtrado["ID_cliente"] = df_filtrado["ID_cliente"].astype(int)
    #HACEMOS LOS INNER JOINS
    df_resultado = pd.merge(df_filtrado, df_db.df_unidad, left_on="ID_unidad", right_index=True)
    df_resultado = pd.merge(df_resultado, df_db.df_cliente, left_on="ID_cliente", right_index=True)
    df_reporte = df_resultado[["ID_unidad", "Rodada", "Fecha", "Nombre", "Apellido", "Telefono"]]
    print(df_reporte)
    exportardf(df_reporte,"REPORTE_X_PERIODO.csv")    

    
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

def vacio_cliente():
    if not(len(base_de_datos["cliente"])==0):
        return False
    return True
def vacio_prestamo():
    if not(len(base_de_datos["prestamo"])==0):
        return False
    return True
def vacio_unidad():
    if not(len(base_de_datos["unidad"])==0):
        return False
    return True


def listado_unidades_completo():
    print("\n--- Listado de Unidades Completo ---")
    if vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    # Mostrar todas las unidades con sus atributos
    df_reporte = df_db.df_unidad
    print(df_reporte)
    
    # Exportar el reporte
    exportardf(df_reporte, "LISTADO_UNIDADES_COMPLETO.csv")


def listado_unidades_por_rodada():
    print("\n--- Listado de Unidades por Rodada ---")
    if vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    while True:
        try:
            # Solicitar la rodada al usuario
            rodada = int(input("Ingrese la rodada deseada: "))
            break
        except Exception as e:
            print("Rodada no válida, intente nuevamente.")


    # Filtrar unidades por rodada
    df_filtrado = df_db.df_unidad[df_db.df_unidad["Rodada"] == rodada]

    # Mostrar solo la clave y el color
    df_reporte = df_filtrado[["Rodada", "Color"]]
    print(df_reporte)

    # Exportar el reporte
    exportardf(df_reporte, f"LISTADO_UNIDADES_RODADA_{rodada}.csv")


def listado_unidades_por_color():
    print("\n--- Listado de Unidades por Color ---")
    if vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    while True:
        try:
            # Solicitar el color al usuario
            color = input("Ingrese el color deseado: ")
            break
        except Exception as e:
            print("Color no válido, intente nuevamente.")


    # Filtrar unidades por color
    df_filtrado = df_db.df_unidad[df_db.df_unidad["Color"] == color]

    # Mostrar solo la clave y la rodada
    df_reporte = df_filtrado[["Rodada", "Color"]]
    print(df_reporte)

    # Exportar el reporte
    exportardf(df_reporte, f"LISTADO_UNIDADES_COLOR_{color}.csv")


def reporte_retrasos():
    print("\n--- Reporte de Retrasos ---")
    if vacio_prestamo() or vacio_cliente() or vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    # Actualizar el DataFrame
    df_prestamos=df_db.df_prestamos

    # Obtener la fecha actual
    fecha_actual = pd.to_datetime("today").date()

    try:
        df_prestamos["Fecha"] = pd.to_datetime(df_prestamos["Fecha"], format=FORMAT_DATE, errors='coerce')
    except Exception as e:
        print(f"Error al convertir la columna Fecha a datetime: {e}")
    #convertir los dias a enteros
    df_prestamos["Dias C"] = df_prestamos["Dias C"].astype(int)
    # Calcular la fecha en que se debió retornar la unidad
    df_prestamos["Fecha Retorno"] = df_prestamos["Fecha"] + pd.to_timedelta(df_prestamos["Dias C"], unit='D')

    # Filtrar préstamos que están retrasados y aún pendientes
    fecha_actual = pd.to_datetime(fecha_actual)
    df_retrasos = df_prestamos[(df_prestamos["Fecha Retorno"] < fecha_actual) & (df_prestamos["Estado"] == "N/E")]

    # Calcular los días de retraso
    df_retrasos["Días de Retraso"] = (fecha_actual - df_retrasos["Fecha Retorno"]).dt.days

    # Unir la información del cliente y la unidad pero primero convertir las llaves a valores compatibles
    df_retrasos=df_retrasos.astype({
        "ID_unidad":int,
        "ID_cliente":int
    })

    df_resultado = pd.merge(df_retrasos, df_db.df_unidad, left_on="ID_unidad", right_index=True)
    df_resultado = pd.merge(df_resultado, df_db.df_cliente, left_on="ID_cliente", right_index=True)

    # Seleccionar las columnas necesarias
    df_reporte = df_resultado[["Días de Retraso", "Fecha Retorno", "ID_unidad", "Rodada", "Color", "Nombre", "Apellido", "Telefono"]]

    # Crear una columna con el nombre completo del cliente
    df_reporte["Nombre Completo"] = df_reporte["Nombre"] + " " + df_reporte["Apellido"]

    # Ordenar por días de retraso de mayor a menor
    df_reporte = df_reporte.sort_values(by="Días de Retraso", ascending=False)

    # Mostrar el reporte
    print(df_reporte)

    # Exportar el reporte
    exportardf(df_reporte, "REPORTE_RETRASOS.csv")




def reporte_duracion_prestamos():
    print("\n--- Reporte de Duración de Préstamos ---")
    # Verifica que los días registrados sean de tipo numérico
    if vacio_prestamo():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    df_prestamos = df_db.df_prestamos
    df_prestamos["Dias C"] = pd.to_numeric(df_prestamos["Dias C"], errors='coerce')
    
    # Calcula las estadísticas descriptivas
    estadisticas = df_prestamos["Dias C"].describe(percentiles=[0.25, 0.5, 0.75])
    
    # Añade la moda manualmente, ya que describe() no la incluye
    moda = df_prestamos["Dias C"].mode()[0]
    
    # Prepara el reporte con las estadísticas en un DataFrame
    df_reporte = pd.DataFrame({
        "Estadística": ["Media", "Mediana", "Moda", "Mínimo", "Máximo", "Desviación estándar", "Primer cuartil", "Tercer cuartil"],
        "Valor": [
            estadisticas['mean'],
            estadisticas['50%'],
            moda,
            estadisticas['min'],
            estadisticas['max'],
            estadisticas['std'],
            estadisticas['25%'],
            estadisticas['75%']
        ]
    })
    
    # Muestra los resultados
    print(df_reporte)

    # Exporta el reporte a un archivo CSV
    exportardf(df_reporte, "REPORTE_DURACION_PRESTAMOS.csv")



def ranking_clientes():
    print("\n--- Ranking de Clientes ---")
    if vacio_prestamo() or vacio_cliente():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    # Agrupar por ID de cliente y contar los préstamos
    ranking = df_db.df_prestamos.groupby("ID_cliente").size().reset_index(name="Cantidad de Préstamos")
    
    # Convertir el ID de cliente a entero para el merge
    ranking["ID_cliente"] = ranking["ID_cliente"].astype(int)
    
    # Realizar el merge con la tabla de clientes
    ranking_completo = pd.merge(ranking, df_db.df_cliente, left_on="ID_cliente", right_index=True)
    
    # Seleccionar las columnas necesarias
    ranking_completo = ranking_completo[["ID_cliente", "Nombre", "Apellido", "Telefono", "Cantidad de Préstamos"]]
    
    # Ordenar de manera descendente por la cantidad de préstamos
    ranking_completo = ranking_completo.sort_values(by="Cantidad de Préstamos", ascending=False)
    
    print(ranking_completo)
    exportardf(ranking_completo, "RANKING_CLIENTES.csv")


def preferencias_rentas_por_rodada():
    print("\n--- Preferencias de Rentas por Rodada ---")
    # Agrupar por rodada y contar la cantidad de préstamos
    if vacio_prestamo():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    df_prestamos=df_db.df_prestamos
    df_unidad=df_db.df_unidad
    df_prestamos["ID_unidad"] = df_prestamos["ID_unidad"].astype(int)
    df_unido = pd.merge(df_prestamos, df_unidad, left_on="ID_unidad", right_index=True)
    preferencias_rodada = df_unido.groupby("Rodada").size().reset_index(name="Cantidad de Préstamos")
    
    # Ordenar de manera descendente por la cantidad de préstamos
    preferencias_rodada = preferencias_rodada.sort_values(by="Cantidad de Préstamos", ascending=False)
    
    print(preferencias_rodada)
    exportardf(preferencias_rodada, "PREFERENCIAS_RENTAS_RODADA.csv")


def preferencias_rentas_por_color():
    print("\n--- Preferencias de Rentas por Color ---")
    # Agrupar por color y contar la cantidad de préstamos
    if vacio_prestamo() or vacio_unidad():
        print("ACTUALMENTE NO HAY SUFICIENTES DATOS PARA REALIZAR ESTA ACCION")
        return 0
    df_prestamos=df_db.df_prestamos
    df_unidad=df_db.df_unidad
    df_prestamos["ID_unidad"] = df_prestamos["ID_unidad"].astype(int)
    

    df_unido = pd.merge(df_prestamos, df_unidad, left_on="ID_unidad", right_index=True)
    preferencias_color = df_unido.groupby("Color").size().reset_index(name="Cantidad de Préstamos")
    
    # Ordenar de manera descendente por la cantidad de préstamos
    preferencias_color = preferencias_color.sort_values(by="Cantidad de Préstamos", ascending=False)
    
    print(preferencias_color)
    exportardf(preferencias_color, "PREFERENCIAS_RENTAS_COLOR.csv")








# Función principal
def menu():
    while True:
        main_menu()
        opcion = input("Selecciona una opción:")
        """
        ES IMPORTANTE CARGAR LOS DATA FRAMES AQUI YA QUE CUALQUIER ACTUALIZACION QUE HAGA EL USUARIO DURANTE LA EJECUCION SE VERA REFLEJADA EN LOS REPORTES Y ANALISIS GRACIAS A ESTAS LINEAS
        """
        df_db.actualizar()
        #MENU DE REGISTROS
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
                opcion=input("A QUE SUB MENU DESEA IR:\n1:Reportes\n2:Analisis\n3:Volver al menu principal\n")
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
                            reporte_retrasos()                         
                        #Listado de unidades
                        elif sub_opcion == '6':
                            while True:
                                listado_opcion=input("Bienvenido al menu de  Reportes Listados a que submenu desea ir?\n1. Listado completo \n2. Listado por rodada \n3. Listado por color\n4. Salir\n")
                                if listado_opcion=="1":
                                    listado_unidades_completo()
                                elif listado_opcion=="2":
                                    listado_unidades_por_rodada()
                                elif listado_opcion=="3":
                                    listado_unidades_por_color()
                                elif listado_opcion=="4":
                                    break
                                else:
                                    print("Opcion no valida")
                        else:
                            print("Opción no válida. Inténtalo de nuevo.")
                #MENU DE ANALISIS
                elif opcion=="2":
                    while True:
                        opcion=input("A que area de analisis desea ir?:\n1:Duracion de prestamos\n2:Ranking de clientes\n3:Preferencias de rentas\n4.Volver al menu principal\n")
                        #MENU DE REPORTES
                        if opcion =="1":
                            reporte_duracion_prestamos()
                            
                        elif opcion=="2":
                            ranking_clientes()
                            
                        elif opcion=="3":
                            while True:
                                opcion_preferncias=input("En base a que preferencias quiere el reporte?\n1.Color\n2.Rodada\n3Volver al menu de analisis")
                                if opcion_preferncias=="1":
                                    preferencias_rentas_por_color()
                                elif opcion_preferncias=="2":
                                    preferencias_rentas_por_rodada()
                                elif opcion_preferncias=="3":
                                    break
                                else:
                                    print("Opcion no valida intente de nuevo")
                            
                        elif opcion=="4":
                            break
                        else:
                            print("Opción no válida. Inténtalo de nuevo.")                    
                            
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
