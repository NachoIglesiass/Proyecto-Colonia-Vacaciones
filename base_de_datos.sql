CREATE DATABASE IF NOT EXISTS colonia_vacaciones
use colonia_vacaciones;

CREATE TABLE participantes (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100),               
    apellido VARCHAR(100),             
    dni VARCHAR(20),                   
    edad INT,                          
    fecha_nacimiento DATE,             
    nombre_padre_tutor VARCHAR(100),   
    numero_telefono VARCHAR(20),       
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    CONSTRAINT uq_dni UNIQUE(dni)
)

