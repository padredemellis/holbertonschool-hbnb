-- Script para insertar datos iniciales en la base de datos HBnB

-- El hash corresponde a "admin1234" usando bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$t6vfFdWioDfzJzBBfK6AeOu/gMmmD5VvFks8ZQhA5i8FVuStgi0m2', -- Hash de 'admin1234'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (id, name, description, created_at, updated_at)
VALUES (
    'f4b8d9a2-ef1c-4a0f-87b5-3e9c8d293a6d',
    'WiFi',
    'Conexión inalámbrica a Internet de alta velocidad',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (id, name, description, created_at, updated_at)
VALUES (
    '8d2e9a7b-6c5f-4e3d-b1a0-9c8f7e6d5a4b',
    'Swimming Pool',
    'Piscina al aire libre disponible para los huéspedes',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (id, name, description, created_at, updated_at)
VALUES (
    'c5b4a3d2-e1f0-4a9b-8c7d-6e5f4a3b2c1d',
    'Air Conditioning',
    'Sistema de climatización para control de temperatura',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
