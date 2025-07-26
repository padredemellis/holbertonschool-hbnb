-- Script para probar operaciones CRUD en la base de datos HBnB

SELECT * FROM users WHERE email = 'admin@hbnb.io';

SELECT * FROM amenities;

INSERT INTO users (id, first_name, last_name, email, password, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-1234567890ab',
    'Juan',
    'Pérez',
    'juan@example.com',
    '$2b$12$vP5ndCO6Vz.sG4gmf/AcF.YDLuFgfIYVwvP4caA9y9B0fN0c3c1Dy', -- Hash de 'password123'
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'b2c3d4e5-f6a7-8901-bcde-23456789abcd',
    'Apartamento en el centro',
    'Bonito apartamento con vistas al mar',
    75.50,
    40.4168,
    -3.7038,
    'a1b2c3d4-e5f6-7890-abcd-1234567890ab',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'b2c3d4e5-f6a7-8901-bcde-23456789abcd',
    'f4b8d9a2-ef1c-4a0f-87b5-3e9c8d293a6d'
);

INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'c3d4e5f6-a7b8-9012-cdef-345678901234',
    'Excelente ubicación y muy limpio',
    5,
    'b2c3d4e5-f6a7-8901-bcde-23456789abcd',
    'a1b2c3d4-e5f6-7890-abcd-1234567890ab',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

UPDATE places
SET description = 'Apartamento renovado con vistas espectaculares al mar', updated_at = CURRENT_TIMESTAMP
WHERE id = 'b2c3d4e5-f6a7-8901-bcde-23456789abcd';

SELECT a.name, a.description
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'b2c3d4e5-f6a7-8901-bcde-23456789abcd';

SELECT p.title, p.price
FROM places p
WHERE p.owner_id = 'a1b2c3d4-e5f6-7890-abcd-1234567890ab';

SELECT r.text, r.rating, u.first_name, u.last_name
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = 'b2c3d4e5-f6a7-8901-bcde-23456789abcd';

DELETE FROM reviews WHERE id = 'c3d4e5f6-a7b8-9012-cdef-345678901234';

DELETE FROM places WHERE id = 'b2c3d4e5-f6a7-8901-bcde-23456789abcd';