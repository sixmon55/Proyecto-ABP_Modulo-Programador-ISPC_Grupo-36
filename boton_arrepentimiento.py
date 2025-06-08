import boton_arrepentimiento
import gestion_destino
import gestion_ventas


def mostrar_titulo():
     print(r"""
            ____ __  __ _   ___  ___  _   _ ___ 
            / ___|  \/  | | | \ \/ / | | | |_ _|
            | |   | |\/| | | | |\  /| | | | || | 
            | |___| |  | | |_| |/  \| |_| | || | 22
            \____|_|  |_|\___//_/\_\\___/|___|  
                                                
            ════════════════════════════════════════
            SISTEMA DE GESTIÓN DE PASAJES      
            ════════════════════════════════════════
            """)
     
     
def menu_inicio():
        print(r"""
        ✈  Bienvenido al sistema de gestión de reservas aéreas

        [1] Gestion de Clientes            [3] Gestionar ventas
        [2] Gestionar Destinos             [4] Consultar Ventas
        [5] Boton de Arrepentimiento       [7] Ver Reporte General
        [6] Acerca del Sistema             [8] Salir  

        ════════════════════════════════════════
        """)

        while True: 
                    try:        
                        opcion=int(input("Seleccione una opción ►  "))
                        if opcion in (1,2,3,4,5,6,7,8):
                            break
                        print("❌ Error: Inserta un Valor Valido")
                    except ValueError:
                        print("❌ Error: Debes insertar numeros")  
                                                  
        match opcion:
                        case 1:
                            gestion_clientes()
                        case 2:
                            gestion_destino.gestion_destino(menu_inicio)
                        case 3:
                            gestion_ventas.menu_ventas(menu_inicio)
                        case 4:
                            consultar_ventas()
                        case 5:
                            boton_arrepentimiento.pantalla_arrepentimiento()
                        case 6: 
                            acerca_sistema()
                        case 7:
                            ver_reporte()
                        case 8:
                            salir()
                            
                            

if __name__ == "__main__":
    menu_inicio()

