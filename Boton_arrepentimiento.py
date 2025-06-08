# pantalla_arrepentimiento.py
from conexion import get_connection  # Conexión a la base de datos
from datetime import datetime        # Para manejo de fechas y horas

def pantalla_arrepentimiento():
    print(r"""
🛑  BOTÓN DE ARREPENTIMIENTO
────────────────────────────
""")

    email = input("Ingrese el email del cliente para consultar sus ventas: ").strip()

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # 1. Obtener ventas asociadas al cliente por su email
        query = """
        SELECT VENTA.id_venta, DESTINO.id_ciudad, VENTA.id_cliente, HISTORIAL_ESTADOVENTA.fecha, ESTADO_VENTA.nombre
        FROM VENTA
        JOIN CLIENTE ON VENTA.id_cliente = CLIENTE.id_cliente
        JOIN HISTORIAL_ESTADOVENTA ON VENTA.id_venta = HISTORIAL_ESTADOVENTA.id_venta
        JOIN ESTADO_VENTA ON HISTORIAL_ESTADOVENTA.id_estado = ESTADO_VENTA.id_estado
        JOIN DESTINO ON VENTA.id_destino = DESTINO.id_destino
        WHERE CLIENTE.email = %s
        ORDER BY HISTORIAL_ESTADOVENTA.fecha DESC
        """
        cursor.execute(query, (email,))
        ventas = cursor.fetchall()

        if not ventas:
            print("❌ No se encontraron ventas asociadas a este cliente.")
            return

        # 2. Mostrar ventas
        print("\n📋 Ventas registradas:")
        for idx, venta in enumerate(ventas, start=1):
            print(f"{idx}. ID Venta: {venta[0]}, Ciudad ID: {venta[1]}, Fecha: {venta[3]}, Estado: {venta[4]}")

        # 3. Seleccionar venta
        seleccion = int(input("\nSeleccione el número de la venta que desea revisar: "))
        venta_seleccionada = ventas[seleccion - 1]
        id_venta = venta_seleccionada[0]
        fecha_venta = venta_seleccionada[3]
        estado_actual = venta_seleccionada[4]

        # 4. Verificar diferencia de tiempo
        ahora = datetime.now()
        diferencia = ahora - fecha_venta

        if estado_actual.lower() != "pendiente":
            print("\n⚠️ Esta venta excedió el tiempo para solicitud de arrepentimiento. No puede cancelarse.")
            return

        if diferencia.total_seconds() <= 300:  # 5 minutos = 300 segundos
            print("\n🛑 ¿Está usted seguro? Si continúa, su venta será cancelada.")
            print("1 - Continuar con la cancelación")
            print("2 - Cancelar y volver")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Cambiar estado a "Anulada" (ID = 3, se asume)
                insert_estado = """
                INSERT INTO HISTORIAL_ESTADOVENTA (id_venta, id_estado, fecha)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_estado, (id_venta, 3, ahora))
                connection.commit()
                print("\n✅ La venta ha sido cancelada exitosamente.")
            else:
                print("\n⏪ Operación cancelada por el usuario.")
        else:
            print("""
⏰ Usted ha sobrepasado el tiempo estipulado para cancelación/arrepentimiento.
Por favor, comuníquese con la compañía para gestionar un cambio.
📞 0800-000000 | Atención al cliente de SkyRoute
🕘 Lunes a Viernes de 09 a 18 hs.
""")
            print("1 - Volver al menú principal")
            print("2 - Salir del sistema")

            opcion = input("Seleccione una opción: ")
            if opcion == "2":
                print("👋 Gracias por utilizar SkyRoute. ¡Hasta luego!")
                exit()

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
