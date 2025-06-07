from conexion import get_connection  # Asegúrate que este es el nombre correcto de tu archivo



def pantalla_venta():
         print(r"""
    ✈  Gestión de Destinos

    [1] Ver destinos           [3] Modificar destino
    [2] Agregar destino        [4] Eliminar destino
    [5] Volver al menú principal

    ════════════════════════════════════════
    """)
         


def gestion_destino(menu_inicio):
        pantalla_venta()
        while True:
                    try:
                        opcion=int(input("Seleccione una opción ► "))
                        if opcion in (1,2,3,4,5):
                                break
                        print("Inserte un valor valido")
                    except ValueError:
                            print("Debes insertar un valor numerico")
        
        match opcion:
                case 1:
                        ver_destino(menu_inicio)
                case 2:
                        agregar_destino(menu_inicio)
                case 3:
                        modificar_destino(menu_inicio)
                case 4:
                        eliminar_destino(menu_inicio)
                case 5:
                        menu_inicio()
                        return
                             
def ver_destino(menu_inicio):
    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)  

        cursor.execute("SELECT destino.costo_base,destino.id_destino AS id,ciudad.nombre AS nombre_ciudad,pais.nombre AS nombre_pais FROM destino INNER JOIN ciudad ON destino.id_ciudad = ciudad.id_ciudad INNER JOIN pais ON ciudad.id_pais = pais.id_pais ORDER BY destino.id_destino ASC;")

        destinos = cursor.fetchall()

        # Mostrar tabla de destinos
        print("+----+----------------+-----------+-------------+")
        print("| ID | Ciudad         | País      | Costo       |")
        print("+----+----------------+-----------+-------------+")
        
        for destino in destinos:
            print(f"| {destino['id']:2} | {destino['nombre_ciudad']:<14} | {destino['nombre_pais']:<9} | $ {destino['costo_base']} |")
        
        print("+----+----------------+-----------+-------------+")
    except ValueError:
          print("❌ Error en la conexion")    
    # Mostrar menú de opciones
    print("\n    [1] Volver atras")
    print("    [2] Salir")
    print("\n    ════════════════════════════════════════")
    
    # Validación de entrada
    while True:
        try:
            opcion = int(input("    Selecciona una opción ►  "))
            if opcion in (1, 2):
                break
            print("    ❌ Error: Debe ser un numero entre 1 o 2")
        except ValueError:
            print('    ❌ Error: Debe ser un número, no texto')
        finally:  
            if cursor is not None:  # Verifica si el cursor existe
                cursor.close()
            if connection is not None:  # Verifica si la conexión existe
                connection.close()
            
    # Redirección según opción
    if opcion == 1:
        gestion_destino(menu_inicio)
        return
    elif opcion == 2:
         print("Saliste de la aplicacion")
         return                                
 

def agregar_destino(menu_inicio):
        try:
            connection = get_connection()

            cursor = connection.cursor(dictionary=True)  

             
            while True:
                        try:
                                pais=input("Escribe un pais ► ").title().strip()
                                cursor.execute(
                                    "SELECT id_pais FROM pais WHERE nombre = %s",  # Consulta SQL
                                    (pais,)  # Parámetro (la coma lo convierte en tupla)
                                )
                                resultado = cursor.fetchone()
                                
                                if not resultado :
                                    cursor.execute("INSERT INTO pais (nombre) VALUES (%s)",(pais,))
                                    id_pais = cursor.lastrowid 
                                    connection.commit()     
                                    
                                    
                                else:
                                    id_pais = resultado["id_pais"]
                                print(f"✅ País '{pais}' agregado correctamente")
                                break
                                
                        except ValueError:
                              print("❌ Escribe un valor correcto")

            while True:
                  
                        try:
                                ciudad=input("Escribe una Ciudad ► ").title().strip()
                                cursor.execute(
                                    "SELECT id_ciudad FROM ciudad WHERE nombre = %s",  
                                    (ciudad,)  
                                )
                                resultado = cursor.fetchone()
                                
                                if not resultado :
                                    cursor.execute("INSERT INTO ciudad (nombre,id_pais) VALUES (%s,%s)",(ciudad,id_pais))
                                    id_ciudad = cursor.lastrowid
                                    connection.commit()
                                else:
                                    id_ciudad = resultado["id_ciudad"]
                                           
                                print(f"✅ Ciudad '{ciudad}' agregada correctamente")
                                break
                                
                        except ValueError:
                              print("❌ Escribe un valor correcto")
            
            while True:
                  
                  
                        try:
                                costo=float(input("Escribe el valor de costo ► "))
                                cursor.execute("INSERT INTO destino (costo_base,id_ciudad) VALUES (%s,%s)",(costo,id_ciudad))
                                connection.commit()     
                                print(f"✅ Costo '{costo}' agregado correctamente")
                                break
                                
                        except ValueError:
                              print("❌ Escribe un valor correcto")
                              
            
        except ValueError:
             print("Error en la conexion")
        finally:
                if cursor is not None:  # Verifica si el cursor existe
                    cursor.close()
                if connection is not None:  # Verifica si la conexión existe
                    connection.close()
        
                                        
            
def modificar_destino():
    ver_destino()
    while True:
        try:
            opcion = int(input("Selecciona el ID del destino que deseas cambiar: "))
            for destino in destinos:
                if destino['id'] == opcion:
                    destino['pais'] = input(f"País [{destino['pais']}] ► ") or destino["pais"]
                    destino['ciudad'] = input(f"Ciudad [{destino['ciudad']}] ► ") or destino["ciudad"]
                    print("✅ Destino modificado correctamente")
                    break
            else:  
                print("ID no encontrado. Intenta nuevamente.")
        except ValueError:
            print("Error: Ingresa un número (ID), no letras.")        
              



def eliminar_destino():
    ver_destino()  # Mostrar lista de destinos
    opcion = input("Seleccione un destino que desee eliminar ► ").capitalize()
    
    # Buscar el destino en la lista
    destino_a_eliminar = None
    for destino in destinos:
        if destino['Ciudad'] == opcion:
            destino_a_eliminar = destino
            break  # Salir del for al encontrar
    
    # Si no existe, pedir nuevamente
    while destino_a_eliminar is None:
        print("❌ Destino no encontrado. Intente de nuevo.")
        opcion = input("Seleccione un destino que desee eliminar ► ").capitalize()
        for destino in destinos:
            if destino['Ciudad'] == opcion:
                destino_a_eliminar = destino
                break
    
    # Eliminar el destino y volver al menú anterior
    destinos.remove(destino_a_eliminar)
    print(f"✅ Destino '{opcion}' eliminado correctamente.")
              