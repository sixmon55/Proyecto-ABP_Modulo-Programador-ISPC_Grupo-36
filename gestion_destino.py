from conexion import get_connection 



def pantalla_destinos():
         print(r"""
    ✈  Gestión de Destinos

    [1] Ver destinos           [3] Modificar destino
    [2] Agregar destino        [4] Eliminar destino
    [5] Volver al menú principal

    ════════════════════════════════════════
    """)
         


def gestion_destino(menu_inicio):
        pantalla_destinos()
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
        
                                        
            
def modificar_destino(menu_inicio):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
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

        while True:
            try:
                id_destino = int(input("Selecciona el ID del destino que deseas cambiar: "))
                # Verificar si el destino existe
                cursor.execute("SELECT id_destino FROM destino WHERE id_destino = %s", (id_destino,))
                if not cursor.fetchone():
                    print("ID no encontrado. Intenta nuevamente.")
                    continue
                
                # Obtener datos actuales
                cursor.execute("""
                    SELECT d.id_destino, d.costo_base, 
                           c.id_ciudad, c.nombre AS ciudad, 
                           p.id_pais, p.nombre AS pais
                    FROM destino d
                    JOIN ciudad c ON d.id_ciudad = c.id_ciudad
                    JOIN pais p ON c.id_pais = p.id_pais
                    WHERE d.id_destino = %s
                """, (id_destino,))
                destino_actual = cursor.fetchone()

                # Solicitar nuevos datos
                nuevo_pais = input(f"País actual ({destino_actual['pais']}) ► ") or destino_actual['pais']
                nueva_ciudad = input(f"Ciudad actual ({destino_actual['ciudad']}) ► ") or destino_actual['ciudad']
                
                while True:
                    try:
                        nuevo_costo = input(f"Costo actual ({destino_actual['costo_base']}) ► ")
                        nuevo_costo = float(nuevo_costo) if nuevo_costo else destino_actual['costo_base']
                        break
                    except ValueError:
                        print("❌ El costo debe ser un número")

                # Actualizar país (si cambió)
                if nuevo_pais != destino_actual['pais']:
                    cursor.execute("""
                        INSERT INTO pais (nombre) VALUES (%s)
                        ON DUPLICATE KEY UPDATE id_pais = LAST_INSERT_ID(id_pais)
                    """, (nuevo_pais,))
                    id_pais = cursor.lastrowid
                else:
                    id_pais = destino_actual['id_pais']

                # Actualizar ciudad (si cambió)
                if nueva_ciudad != destino_actual['ciudad']:
                    cursor.execute("""
                        INSERT INTO ciudad (nombre, id_pais) VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE id_ciudad = LAST_INSERT_ID(id_ciudad)
                    """, (nueva_ciudad, id_pais))
                    id_ciudad = cursor.lastrowid
                else:
                    id_ciudad = destino_actual['id_ciudad']

                # Actualizar destino
                cursor.execute("""
                    UPDATE destino 
                    SET costo_base = %s, id_ciudad = %s
                    WHERE id_destino = %s
                """, (nuevo_costo, id_ciudad, id_destino))

                connection.commit()
                print("✅ Destino modificado correctamente (país, ciudad y costo actualizados)")
                break

            except ValueError:
                print("Error: Ingresa un número válido")
            except Exception as e:
                print(f"Error al modificar: {e}")
                if connection: connection.rollback()

    except Exception as e:
        print(f"Error en la conexión: {e}")
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def eliminar_destino(menu_inicio):
    connection = None
    cursor = None
    try:
        # 1. Establecer conexión y mostrar destinos
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Mostrar tabla de destinos
        cursor.execute("""
            SELECT d.id_destino, d.costo_base, 
                   c.nombre AS ciudad, p.nombre AS pais,
                   c.id_ciudad, p.id_pais
            FROM destino d
            JOIN ciudad c ON d.id_ciudad = c.id_ciudad
            JOIN pais p ON c.id_pais = p.id_pais
            ORDER BY d.id_destino
        """)
        destinos = cursor.fetchall()

        print("\n📋 Lista de Destinos Disponibles:")
        print("+-----+-----------------+------------+--------------+")
        print("| ID  | Ciudad          | País       | Costo        |")
        print("+-----+-----------------+------------+--------------+")
        for destino in destinos:
            print(f"| {destino['id_destino']:3} | {destino['ciudad']:<15} | {destino['pais']:<10} | $ {destino['costo_base']:9.2f} |")
        print("+-----+-----------------+------------+--------------+")

        # 2. Proceso de eliminación
        while True:
            try:
                id_destino = int(input("\nIngrese el ID del destino a eliminar (0 para cancelar) ► "))
                
                if id_destino == 0:
                    print("🚫 Operación cancelada")
                    menu_inicio()
                    return
                
                # Verificar existencia del destino
                cursor.execute("""
                    SELECT d.id_destino, c.nombre AS ciudad, p.nombre AS pais,
                           c.id_ciudad, p.id_pais
                    FROM destino d
                    JOIN ciudad c ON d.id_ciudad = c.id_ciudad
                    JOIN pais p ON c.id_pais = p.id_pais
                    WHERE d.id_destino = %s
                """, (id_destino,))
                destino = cursor.fetchone()
                
                if not destino:
                    print("❌ Error: No existe un destino con ese ID")
                    continue
                    
                # Confirmación de eliminación
                confirmar = input(f"¿Está seguro de eliminar {destino['ciudad']} ({destino['pais']})? [s/n] ► ").lower()
                if confirmar != 's':
                    print("🚫 Eliminación cancelada")
                    continue
                
                try:
                    # Primero eliminar el destino
                    cursor.execute("DELETE FROM destino WHERE id_destino = %s", (id_destino,))
                    
                    cursor.execute("SELECT COUNT(*) FROM destino WHERE id_ciudad = %s", (destino['id_ciudad'],))
                    if cursor.fetchone()['COUNT(*)'] == 0:
                        cursor.execute("DELETE FROM ciudad WHERE id_ciudad = %s", (destino['id_ciudad'],))
                        print(f"⚠️ Se eliminó la ciudad {destino['ciudad']}")
                    
                    cursor.execute("SELECT COUNT(*) FROM ciudad WHERE id_pais = %s", (destino['id_pais'],))
                    if cursor.fetchone()['COUNT(*)'] == 0:
                        cursor.execute("DELETE FROM pais WHERE id_pais = %s", (destino['id_pais'],))
                        print(f"⚠️ Se eliminó el país {destino['pais']}")
                    
                    connection.commit()
                    print(f"✅ Destino ID {id_destino} eliminado exitosamente")
                    
                    # Preguntar si desea eliminar otro destino
                    otro = input("¿Desea eliminar otro destino? [s/n] ► ").lower()
                    if otro == 's':
                        eliminar_destino(menu_inicio)
                    else:
                        menu_inicio()
                    return
                    
                except Exception as e:
                    connection.rollback()
                    print(f"❌ Error al eliminar: {str(e)}")
                
            except ValueError:
                print("❌ Error: Debe ingresar un número válido")

    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        if connection: connection.rollback()
    finally:
        if cursor: cursor.close()
        if connection: connection.close()