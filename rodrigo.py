def mostrar_titulo():
     print(r"""
            ____ __  __ _   ___  ___  _   _ ___ 
            / ___|  \/  | | | \ \/ / | | | |_ _|
            | |   | |\/| | | | |\  /| | | | || | 
            | |___| |  | | |_| |/  \| |_| | || | 
            \____|_|  |_|\___//_/\_\\___/|___|  
                                                
            ════════════════════════════════════════
            SISTEMA DE GESTIÓN DE PASAJES      
            ════════════════════════════════════════
            """)

def pantalla_cliente():
                           print(r"""
        ✈  Elije una opcion

        [1] Ver cliente            [4] Eliminar cliente
        [2] Agregar cliente        [5] Volver al menu principal
        [3] Modificar cliente

        ════════════════════════════════════════
                                """)
def pantalla_venta():
         print(r"""
    ✈  Gestión de Destinos

    [1] Ver destinos           [3] Modificar destino
    [2] Agregar destino        [4] Eliminar destino
    [5] Volver al menú principal

    ════════════════════════════════════════
    """)



def inicio(): #inicio del programa
    
    mostrar_titulo() # Muestra el titulo de inicio        
    menu_inicio()  # Muestra el menu inicial

# FUNCIONES Y VARIABLES DE GESTION CLIENTES    
clientes_almacenado=[]

def gestion_cliente(): # Sub menu de gestion de clientes
        mostrar_titulo()
        pantalla_cliente()
        opcion_cliente= int(input("Seleccione una opción ►  "))
        while opcion_cliente not in (1,2,3,4,5):
                        print("Opcion Incorrecta seleccione una opcion valida")
                        opcion_cliente= int(input("Seleccione una opción ►  "))
        match opcion_cliente:
                            case 1:
                                    ver_cliente()
                            case 2:
                                    agregar_cliente()
                            case 3 : 
                                    modificar_cliente()
                            case 4 : 
                                    eliminar_cliente()
                            case 5 :
                                    menu_inicio()
    
def agregar_cliente(): # Funcion que muestra el sub menu de agregar clientes
    mostrar_titulo()

    print(r"""Elejiste la opcion agregar cliente
          ════════════════════════════════════════""")
    
    id=0
    while True:
        id+=1
        nombre=input("Escriba el nombre ►  ")
        apellido=input("Escriba el apellido ►  ")
        edad=int(input("Escriba la edad del cliente ►  "))
        sexo=input("Escriba el sexo del cliente ►  ")
        CLIENTE={"id":id,"nombre":nombre,"apellido":apellido,"edad":edad,"sexo":sexo}

        clientes_almacenado.append(CLIENTE)
        print(r"""
        se guardo el cliente con los siguente datos :
        ═══════════════════════════════════════════ 
    """)

        print(f"Nombre: {CLIENTE['nombre']}")
        print(f"Apellido: {CLIENTE['apellido']}")
        print(f"Edad: {CLIENTE['edad']}")
        print(f"Sexo: {CLIENTE['sexo']}")    
            
        respuesta_agregar_cliente=input("Desas agregar otro cliente SI/NO ? ► ").upper()
        while respuesta_agregar_cliente not in ("SI", "NO"):
            print("¡Error! Debes escribir SI o NO.")
            respuesta_agregar_cliente = input("¿Deseas agregar otro cliente SI/NO? ► ").upper()
        if respuesta_agregar_cliente == "NO":
            break
    gestion_cliente()


def ver_cliente():
    
                for cliente in clientes_almacenado:
                                    print("Los clientes son :")
                                    print(f"ID: {cliente['id']}")
                                    print(f"Nombre: {cliente['nombre']}")
                                    print(f"Apellido: {cliente['apellido']}")
                                    print(f"Edad: {cliente['edad']}")
                                    print(f"Sexo: {cliente['sexo']}")
                                    print("════════════════════════════════════════")
                  

def eliminar_cliente():
                ver_cliente()
                id=int(input("Seleccione un cliente que desees borrar ►  "))
                
                for cliente in clientes_almacenado:
                        if cliente["id"] == id :
                                clientes_almacenado.pop(id-1)
                print("Cliente borrado sastifactoriamente !!!")
                gestion_cliente()
def modificar_cliente():
    mostrar_titulo()
    print("✏  MODIFICAR CLIENTE")
    ver_cliente()  # Mostramos la lista actual
    
    try:
        id_modificar = int(input("\nIngrese el ID del cliente a modificar ► "))
        
        # Buscar el cliente por ID
        cliente_encontrado = None
        for cliente in clientes_almacenado:
            if cliente["id"] == id_modificar:
                cliente_encontrado = cliente
                break
        
        if cliente_encontrado:
            print("\nDatos actuales del cliente:")
            print(f"ID: {cliente_encontrado['id']}")
            print(f"Nombre: {cliente_encontrado['nombre']}")
            print(f"Apellido: {cliente_encontrado['apellido']}")
            print(f"Edad: {cliente_encontrado['edad']}")
            print(f"Sexo: {cliente_encontrado['sexo']}")
            print("════════════════════════════════════════")
            
            # Solicitar nuevos datos
            print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
            nuevo_nombre = input(f"Nombre [{cliente_encontrado['nombre']}] ► ") or cliente_encontrado["nombre"]
            nuevo_apellido = input(f"Apellido [{cliente_encontrado['apellido']}] ► ") or cliente_encontrado["apellido"]
            nueva_edad = input(f"Edad [{cliente_encontrado['edad']}] ► ")
            nueva_edad = int(nueva_edad) if nueva_edad else cliente_encontrado["edad"]
            nuevo_sexo = input(f"Sexo [{cliente_encontrado['sexo']}] ► ") or cliente_encontrado["sexo"]
            
            # Actualizar el cliente
            cliente_encontrado.update({
                "nombre": nuevo_nombre,
                "apellido": nuevo_apellido,
                "edad": nueva_edad,
                "sexo": nuevo_sexo
            })
            
            print("\n✅ Cliente modificado correctamente.")
        else:
            print(f"\n❌ No se encontró un cliente con ID {id_modificar}.")
    
    except ValueError:
        print("¡Error! El ID debe ser un número.")
    
    input("\nPresione Enter para volver al menú...")
    gestion_cliente()
destinos = [
    {'Pais': 'Italia', 'Ciudad': 'Roma', 'Precio': '$ 500.000'},
    {'Pais': 'Japón', 'Ciudad': 'Kioto', 'Precio': '$ 600.000'},  
    {'Pais': 'China', 'Ciudad': 'Peking', 'Precio': '$ 800.000'}, 
    {'Pais': 'Australia', 'Ciudad': 'Sídney', 'Precio': '$ 500.000'}, 
    {'Pais': 'Perú', 'Ciudad': 'Cusco', 'Precio': '$ 600.000'}
]

def gestion_venta():
        pantalla_venta()
        opcion=int(input("Seleccione una opción ►  "))
        while opcion  not in  (1,2,3,4):
                     print("opcion incorrecta")         
                     opcion=int(input("Seleccione una opción ►  "))      
            
        match opcion:
                        case 1:
                            ver_destino()
                        case 2:
                                eliminar_destino()
                        case 3:
                            
                            gestion_cliente()
 
def ver_destino():
                print("+----------------+-----------+-------------+")
                print("| Ciudad         | País      | Costo       |")
                print("+----------------+-----------+-------------+")
                for destino in destinos:
                    print(f"| {destino['Ciudad']:<14} | {destino['Pais']:<9} | {destino['Precio']:>10} |")
                print(r"""
    
               
    [1] Volver al menu destino        
    [2] Volver al menú principal

    ════════════════════════════════════════
    """)
                
                
                while True:
                        try:
                            opcion=int(input("Selecciona una opcion ►  "))
                            if opcion not in(1,2):
                                        opcion=int(input("Selecciona una opcion correcta ►  "))
                            elif opcion == 1:
                                    gestion_venta()
                                    break

                            elif opcion == 2:
                                    menu_inicio()
                                    break
                        except ValueError:
                                print('Debes seleccionar un numero no palabras')   
                                


                while opcion not in (1,2):
                                opcion=int(input("Selecciona una opcion correcta ►  "))
                match opcion:
                        case 1:
                                gestion_venta()
                        case 2:
                                menu_inicio()
                                
                


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
    gestion_venta()                
    
def menu_inicio():
        print(r"""
        ✈  Bienvenido al sistema de gestión de reservas aéreas

        [1] Gestion de venta          [3] Gestionar clientes
        [2] Consultar pasaje          [4] Administración
        [0] Salir del sistema

        ════════════════════════════════════════
        """)
        opcion=int(input("Seleccione una opción ►  "))

        while opcion  not in  (1,2,3,4):
                     print("opcion incorrecta")         
                     opcion=int(input("Seleccione una opción ►  "))

       
        match opcion:
                        case 1:
                            gestion_venta()
                        case 2:
                                print("consultar pasajes")
                        case 3:
                            
                            gestion_cliente()
 

inicio()

        
    
    


