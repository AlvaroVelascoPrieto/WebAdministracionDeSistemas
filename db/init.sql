CREATE DATABASE a;

CREATE USER IF NOT EXISTS
  'root'@'%' IDENTIFIED BY 'root';

GRANT ALL PRIVILEGES
  ON a.*
  TO 'root'@'%';
  

use a;



CREATE TABLE IF NOT EXISTS Usuarios (
    `Nombre` VARCHAR(19) CHARACTER SET utf8mb4,
    `Apellidos` VARCHAR(19) CHARACTER SET utf8mb4,
    `email` VARCHAR(40) CHARACTER SET utf8mb4,
    `Contrasena` VARCHAR(70) CHARACTER SET utf8mb4,
    PRIMARY KEY (`email`)
);
INSERT INTO Usuarios (Nombre, Apellidos, email, Contrasena) VALUES
    ('Alvaro','Velasco','avelasco034@ikasle.ehu.eus', 'azsxdcfvgb');

CREATE TABLE IF NOT EXISTS Gastos (
    `id` int AUTO_INCREMENT,
    `Gasto` VARCHAR(19) CHARACTER SET utf8mb4,
    `Tienda` VARCHAR(12) CHARACTER SET utf8mb4,
    `Descripcion` VARCHAR(40) CHARACTER SET utf8mb4,
    `Importe` INT,
    `Moneda` VARCHAR(3) CHARACTER SET utf8mb4,
    `Fecha` INT,
    `Usuario` VARCHAR(40) CHARACTER SET utf8mb4,

    PRIMARY KEY (`id`),
    
    FOREIGN KEY (Usuario)
        REFERENCES Usuarios(email)
        ON DELETE CASCADE
    
);

INSERT INTO Gastos (Gasto, Tienda, Descripcion, Importe, Moneda, Fecha, Usuario) VALUES
    ('Pantalones Vaqueros','Zara','Compras otoño',35,'EUR',2023, 'avelasco034@ikasle.ehu.eus'),
    ('Lasaña boloñesa','Eroski','Comida septiembre',20,'USD',2023, 'avelasco034@ikasle.ehu.eus');


