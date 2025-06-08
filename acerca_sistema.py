import sys
def info_programa(menu_inicio):
    print("""
    --- INFORMACIÓN DEL PROGRAMA ---
    
    SkyRoute es una plataforma de gestión de ventas de pasajes aéreos.
    Este sistema permite realizar un seguimiento detallado del estado de cada venta,
    ofreciendo funciones para consulta, cancelación y modificación dentro de los plazos estipulados. Además, genera informes
    básicos y permite eliminar algunos registros.
          
    Desarrollado por el grupo 36 del módulo programador del ISPC, de la carrera Ciencia de Datos e IA. Cohorte 2025.

    """)

    print("\n1 - Volver al menú principal")
    print("2 - Cerrar programa")
    opcion = input("Ingrese una opción: ")
    
    if opcion == "1":
        menu_inicio()
    elif opcion == "2":
        sys.exit()
    else:
        print("Opción inválida. Volviendo al menú.")
        menu_inicio()

if __name__ == "__main__":
    info_programa()