-- Verifica si la base de datos 'prueba' ya existe
SELECT 'prueba' IN (SELECT datname FROM pg_database);

