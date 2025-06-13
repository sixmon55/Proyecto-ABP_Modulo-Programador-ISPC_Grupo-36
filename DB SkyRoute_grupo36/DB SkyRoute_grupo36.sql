      ---------- sentencia para crear y utilizar la base creada -----------
CREATE DATABASE IF NOT EXISTS skyroute_grupo36;

USE skyroute_grupo36;

      ---------- fin sentencia para crear y utilizar la base creada -----------






      ---------- sentencia para crear las tablas -----------
-- Tabla PAIS
CREATE TABLE IF NOT EXISTS PAIS (
    id_pais INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) not null
);

-- Tabla CIUDAD
CREATE TABLE IF NOT EXISTS CIUDAD (
    id_ciudad INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) not null,
    id_pais INT not null,
    FOREIGN KEY (id_pais) REFERENCES PAIS(id_pais)
);

-- Tabla DESTINO
CREATE TABLE IF NOT EXISTS DESTINO (
    id_destino INT PRIMARY KEY AUTO_INCREMENT,
    id_ciudad INT not null,
    costo_base DECIMAL(10, 2),
    FOREIGN KEY (id_ciudad) REFERENCES CIUDAD(id_ciudad)
);

-- Tabla CLIENTE
CREATE TABLE IF NOT EXISTS CLIENTE (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    cuit CHAR(11) not null,
    razon_social VARCHAR(100) not null,
    email VARCHAR(50) UNIQUE
);

-- Tabla ESTADO_VENTA
CREATE TABLE IF NOT EXISTS ESTADO_VENTA (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) not null
);

-- Tabla VENTA
CREATE TABLE IF NOT EXISTS VENTA (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT not null,
    id_destino INT not null,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_destino) REFERENCES DESTINO(id_destino) ON DELETE CASCADE
);

-- Tabla HISTORIAL_ESTADOVENTA
CREATE TABLE IF NOT EXISTS HISTORIAL_ESTADOVENTA (
    id_historialestadoventa INT PRIMARY KEY AUTO_INCREMENT,
    id_venta INT not null,
    id_estado INT not null,
    fecha DATETIME not null,
    FOREIGN KEY (id_venta) REFERENCES VENTA(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_estado) REFERENCES ESTADO_VENTA(id_estado)
);

      ---------- fin sentencia para crear las tablas -----------






      ---------- sentencia para el trigger -----------
-- Inserta un registro con el estado inicial de la venta en la tabla historial.
DELIMITER //

CREATE TRIGGER trg_historialventa
AFTER INSERT ON VENTA
FOR EACH ROW
BEGIN

    INSERT INTO HISTORIAL_ESTADOVENTA (id_venta, id_estado, fecha)
    VALUES (NEW.id_venta, 1, NOW());
END //
DELIMITER ;

      ---------- fin sentencia para el trigger -----------






      ---------- sentencias de insert -----------
-- INSERT de ejemplos para jugar con la base de datos

-- insert PAIS
INSERT INTO PAIS (nombre) VALUES ('Argentina');
INSERT INTO PAIS (nombre) VALUES ('Brasil');
INSERT INTO PAIS (nombre) VALUES ('Chile');
INSERT INTO PAIS (nombre) VALUES ('Uruguay');

-- insert CLIENTE
INSERT INTO CLIENTE (cuit, razon_social, email) VALUES ('20123456789', 'Empresa A SRL', 'contacto@empresaa.com');
INSERT INTO CLIENTE (cuit, razon_social, email) VALUES ('30987654321', 'Cliente B SA', 'info@clienteb.com');
INSERT INTO CLIENTE (cuit, razon_social, email) VALUES ('27555666777', 'Juan Perez', 'juan.perez@example.com');

-- insert ESTADO_VENTA
INSERT INTO ESTADO_VENTA (nombre) VALUES ('PENDIENTE');
INSERT INTO ESTADO_VENTA (nombre) VALUES ('COMPLETADO');
INSERT INTO ESTADO_VENTA (nombre) VALUES ('ANULADO');

-- insert CIUDAD
INSERT INTO CIUDAD (nombre, id_pais) VALUES ('Buenos Aires', 1); -- Argentina
INSERT INTO CIUDAD (nombre, id_pais) VALUES ('Rio de Janeiro', 2); -- Brasil
INSERT INTO CIUDAD (nombre, id_pais) VALUES ('Santiago', 3); -- Chile
INSERT INTO CIUDAD (nombre, id_pais) VALUES ('Montevideo', 4); -- Uruguay
INSERT INTO CIUDAD (nombre, id_pais) VALUES ('Córdoba', 1); -- Argentina

-- insert DESTINO
INSERT INTO DESTINO (id_ciudad, costo_base) VALUES (1, 15000.00);
INSERT INTO DESTINO (id_ciudad, costo_base) VALUES (2, 25000.00);
INSERT INTO DESTINO (id_ciudad, costo_base) VALUES (3, 18000.00);
INSERT INTO DESTINO (id_ciudad, costo_base) VALUES (5, 10000.00);

-- insert VENTA
INSERT INTO VENTA (id_cliente, id_destino) VALUES (1, 2);
INSERT INTO VENTA (id_cliente, id_destino) VALUES (2, 1);
INSERT INTO VENTA (id_cliente, id_destino) VALUES (3, 3);
INSERT INTO VENTA (id_cliente, id_destino) VALUES (1, 4);

      ---------- fin sentencias de insert -----------






      ---------- query -----------

-- Listar todos los clientes.
SELECT * FROM CLIENTE;



-- Listar todas las ventas.
SELECT * FROM venta;


-- Mostrar las ventas realizadas a partir del 2025.
SELECT VENTA.id_venta, razon_social, CIUDAD.nombre AS ciudad, PAIS.nombre AS pais, fecha
FROM VENTA
INNER JOIN CLIENTE ON VENTA.id_cliente = CLIENTE.id_cliente
INNER JOIN DESTINO ON VENTA.id_destino = DESTINO.id_destino
INNER JOIN CIUDAD ON DESTINO.id_ciudad = CIUDAD.id_ciudad
INNER JOIN PAIS ON CIUDAD.id_pais = PAIS.id_pais
INNER JOIN HISTORIAL_ESTADOVENTA ON VENTA.id_venta = HISTORIAL_ESTADOVENTA.id_venta
WHERE HISTORIAL_ESTADOVENTA.fecha LIKE '2025%' AND HISTORIAL_ESTADOVENTA.id_estado = 1;



-- Obtener la última venta de cada cliente y su fecha.
SELECT c.razon_social, v.id_venta, hv.fecha as fecha_ultima_venta
FROM cliente c, venta v, historial_estadoventa hv,
    (   SELECT v2.id_cliente, MAX(hv2.fecha) as ultima_fecha
        FROM venta v2, historial_estadoventa hv2
        WHERE hv2.id_venta = v2.id_venta
        GROUP BY v2.id_cliente
    ) AS ultimas_fechas_cliente
WHERE c.id_cliente = v.id_cliente
AND hv.id_venta = v.id_venta
AND c.id_cliente = ultimas_fechas_cliente.id_cliente
AND hv.fecha = ultimas_fechas_cliente.ultima_fecha;



-- Listar todos los destinos que empiezan con “S”.
SELECT id_destino, CIUDAD.nombre AS ciudad, PAIS.nombre AS pais, costo_base
FROM DESTINO
INNER JOIN CIUDAD ON DESTINO.id_ciudad = CIUDAD.id_ciudad
INNER JOIN PAIS ON CIUDAD.id_pais = PAIS.id_pais	
WHERE ciudad.nombre LIKE 'S%';



-- Mostrar cuántas ventas se realizaron por país.
SELECT PAIS.nombre AS pais, COUNT(VENTA.id_venta) AS cantidad_ventas
FROM VENTA
INNER JOIN DESTINO ON VENTA.id_destino = DESTINO.id_destino
INNER JOIN CIUDAD ON DESTINO.id_ciudad = CIUDAD.id_ciudad
INNER JOIN PAIS ON CIUDAD.id_pais = PAIS.id_pais
GROUP BY PAIS.nombre
ORDER BY cantidad_ventas DESC;



-- Mostrar el detalle de la ventas ralizadas.
SELECT ct.razon_social, v.id_venta, c.nombre ciudad, p.nombre pais, hv.fecha, e.nombre estado 
FROM pais p, ciudad c, destino d, venta v, cliente ct, historial_estadoventa hv, estado_venta e 
WHERE p.id_pais = c.id_pais and c.id_ciudad = d.id_ciudad and d.id_destino = v.id_destino
and v.id_venta = hv.id_venta and hv.id_estado = e.id_estado and ct.id_cliente = v.id_cliente;


      ---------- fin query -----------