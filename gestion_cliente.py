from conexion import get_connection 

def pantalla_cliente():
                           print(r"""
        ✈  Elije una opcion

        [1] Ver cliente            [4] Eliminar cliente
        [2] Agregar cliente        [5] Volver al menu principal
        [3] Modificar cliente

        ════════════════════════════════════════
                                """)
                           

def lista_cliente(clientes):
      
        # Mostrar tabla de clientes con formato mejorado
        print("\n📋 Lista de Clientes Registrados:")
        print("+-----+-------------+----------------------+-----------------------------+")
        print("| ID  | CUIT        | Razón Social         | Email                       |")
        print("+-----+-------------+----------------------+-----------------------------+")
        
        for cliente in clientes:
            email = cliente['email'] or "Sin email"
            # Ajustar email si es muy largo
            if len(email) > 25:
                email = email[:22] + "..."
            print(f"| {cliente['id_cliente']:3} | {cliente['cuit']:<11} | {cliente['razon_social']:<20} | {email:<25} |")
        
        print("+-----+-------------+----------------------+-----------------------------+")
                          



def main(menu_inicio):
        pantalla_cliente()
        while True:
                
                try:
                    opcion_cliente= int(input("Seleccione una opción ►  "))
  
                    if opcion_cliente  in (1,2,3,4,5):
                            break
                    print("❌ Opcion Incorrecta seleccione un numero valido")
                except ValueError:
                    print("❌ Debes seleccionar numeros no letra")


        match opcion_cliente:
                            case 1:
                                    ver_cliente(menu_inicio)
                            case 2:
                                    agregar_cliente(menu_inicio)
                            case 3 : 
                                    modificar_cliente()
                            case 4 : 
                                    eliminar_cliente()
                            case 5 :
                                    menu_inicio()

def ver_cliente(menu_inicio):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()

        lista_cliente(clientes)
        # Menú de opciones
        print("\nOpciones:")
        print("    1. Volver al menú principal")
        print("    2. Salir")
        
        # Validación de entrada
        while True:
            try:
                opcion = int(input("    Selecciona una opción ►  "))
                if opcion == 1:
                    
                    menu_inicio()
                    return
                elif opcion == 2:
                    print("👋 ¡Hasta luego!")
                    exit()
                else:
                    print("    ❌ Error: Debe ser 1 o 2")
            except ValueError:
                print('    ❌ Error: Debe ser un número, no texto')

    except Exception as e:
        print(f"❌ Error al mostrar clientes: {str(e)}")
    finally:
        if cursor: 
            cursor.close()
        if connection: 
            connection.close()

def agregar_cliente(menu_inicio):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        while True:
            try:
                # Solicitar datos
                cuit = input("\nIngrese el CUIT (11 dígitos sin guiones) ► ").strip()
                razon_social = input("Ingrese la Razón Social ► ").strip()
                email = input("Ingrese el Email  ► ").strip()

                # Validaciones básicas
                if not cuit.isdigit() or len(cuit) != 11:
                    print("❌ El CUIT debe tener 11 dígitos numéricos")
                    continue
                    
                if not razon_social:
                    print("❌ La Razón Social no puede estar vacía")
                    continue

                # Verificar si el CUIT ya existe
                cursor.execute("SELECT 1 FROM cliente WHERE cuit = %s", (cuit,))
                if cursor.fetchone():
                    print("❌ Ya existe un cliente con este CUIT")
                    continue

                # Insertar nuevo cliente
                cursor.execute(
                    "INSERT INTO cliente (cuit, razon_social, email) VALUES (%s, %s, %s)",
                    (cuit, razon_social, email)
                )
                connection.commit()
                
                print(f"\n✅ Cliente {razon_social} agregado correctamente con ID: {cursor.lastrowid}")
                
                # Preguntar si desea agregar otro
                otro = input("\n¿Desea agregar otro cliente? (s/n) ► ").lower()
                if otro != 's':
                    break

            except ValueError as ve:
                print(f"❌ Error de validación: {str(ve)}")
            except Exception as e:
                connection.rollback()
                print(f"❌ Error al agregar cliente: {str(e)}")

    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
    finally:
        if cursor: cursor.close()
        if connection: connection.close()


def modificar_cliente():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Listar todos los clientes
        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()
        lista_cliente(clientes)
        
        if not clientes:
            print("No hay clientes registrados.")
            return
        
        # Seleccionar cliente a modificar
        while True:
            try:
                opcion = int(input("\nSelecciona el número de id del cliente que deseas modificar: "))
                
                cliente_encontrado = None
                for cliente in clientes:
                    if cliente["id_cliente"] == opcion:
                        cliente_encontrado = cliente
                        break
                
                if cliente_encontrado:
                    break
                else:
                    print("❌ El id del cliente ingresado no es válido")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        # Obtener nuevos datos (mantener los actuales si no se ingresan)
        print(f"\nModificando cliente: {cliente_encontrado['razon_social']}")
        print("(Presiona Enter para mantener el valor actual)")
        
        cuit_nuevo = input(f"CUIT actual [{cliente_encontrado['cuit']}]: ") or cliente_encontrado["cuit"]
        razon_social = input(f"Razón social actual [{cliente_encontrado['razon_social']}]: ") or cliente_encontrado["razon_social"]
        email = input(f"Email actual [{cliente_encontrado['email']}]: ") or cliente_encontrado["email"]
        
        # Actualizar en la base de datos
        cursor.execute("""
            UPDATE cliente 
            SET cuit = %s, razon_social = %s, email = %s
            WHERE id_cliente = %s
        """, (cuit_nuevo, razon_social, email, opcion))
        
        connection.commit()
        print("✅ Cliente modificado correctamente")
        
    except Exception as e:
        print(f"❌ Error al modificar cliente: {str(e)}")
        if connection:
            connection.rollback()
    finally:
        if cursor: cursor.close()
        if connection: connection.close()



        
      
