#!/bin/bash
# Script para probar los endpoints de la API HBnB

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URL base de la API
BASE_URL="http://localhost:5000/api/v1"

# Función para mostrar resultados
show_result() {
    echo -e "${YELLOW}==== $1 ====${NC}"
    echo -e "${YELLOW}Comando:${NC} $2"
    echo -e "${YELLOW}Resultado:${NC}"
    eval "$2"
    echo ""
}

echo -e "${GREEN}Iniciando pruebas de API HBnB...${NC}"
echo ""

# ========= PRUEBAS DE USUARIO =========
echo -e "${GREEN}=== PRUEBAS DE USUARIO ===${NC}"

# Prueba 1: Crear usuario (caso exitoso)
show_result "Crear usuario (caso exitoso)" "curl -s -X POST \"$BASE_URL/users/\" -H \"Content-Type: application/json\" -d '{
    \"first_name\": \"John\",
    \"last_name\": \"Doe\",
    \"email\": \"john.doe@example.com\"
}' | json_pp"

# Guardamos el ID del usuario para pruebas posteriores
USER_ID=$(curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe2@example.com"
}' | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)

echo -e "${YELLOW}ID del usuario creado: $USER_ID${NC}"
echo ""

# Prueba 2: Crear usuario con email inválido
show_result "Crear usuario con email inválido" "curl -s -X POST \"$BASE_URL/users/\" -H \"Content-Type: application/json\" -d '{
    \"first_name\": \"Invalid\",
    \"last_name\": \"User\",
    \"email\": \"invalid-email\"
}' | json_pp"

# Prueba 3: Obtener usuario por ID
show_result "Obtener usuario por ID" "curl -s -X GET \"$BASE_URL/users/$USER_ID\" | json_pp"

# Prueba 4: Obtener usuario con ID inexistente
show_result "Obtener usuario con ID inexistente" "curl -s -X GET \"$BASE_URL/users/nonexistent-id\" | json_pp"

# Prueba 5: Actualizar usuario
show_result "Actualizar usuario" "curl -s -X PUT \"$BASE_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -d '{
    \"first_name\": \"John Updated\",
    \"last_name\": \"Doe Updated\"
}' | json_pp"

# ========= PRUEBAS DE AMENIDADES =========
echo -e "${GREEN}=== PRUEBAS DE AMENIDADES ===${NC}"

# Prueba 6: Crear amenidad (caso exitoso)
show_result "Crear amenidad (caso exitoso)" "curl -s -X POST \"$BASE_URL/amenities/\" -H \"Content-Type: application/json\" -d '{
    \"name\": \"WiFi\"
}' | json_pp"

# Guardamos el ID de la amenidad para pruebas posteriores
AMENITY_ID=$(curl -s -X POST "$BASE_URL/amenities/" -H "Content-Type: application/json" -d '{
    "name": "Pool"
}' | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)

echo -e "${YELLOW}ID de la amenidad creada: $AMENITY_ID${NC}"
echo ""

# Prueba 7: Crear amenidad con nombre vacío
show_result "Crear amenidad con nombre vacío" "curl -s -X POST \"$BASE_URL/amenities/\" -H \"Content-Type: application/json\" -d '{
    \"name\": \"\"
}' | json_pp"

# Prueba 8: Obtener amenidad por ID
show_result "Obtener amenidad por ID" "curl -s -X GET \"$BASE_URL/amenities/$AMENITY_ID\" | json_pp"

# Prueba 9: Actualizar amenidad
show_result "Actualizar amenidad" "curl -s -X PUT \"$BASE_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\" -d '{
    \"name\": \"Heated Pool\"
}' | json_pp"

# ========= PRUEBAS DE LUGARES =========
echo -e "${GREEN}=== PRUEBAS DE LUGARES ===${NC}"

# Prueba 10: Crear lugar (caso exitoso)
show_result "Crear lugar (caso exitoso)" "curl -s -X POST \"$BASE_URL/places/\" -H \"Content-Type: application/json\" -d '{
    \"title\": \"Beach House\",
    \"description\": \"Beautiful house near the beach\",
    \"price\": 150.0,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
}' | json_pp"

# Guardamos el ID del lugar para pruebas posteriores
PLACE_ID=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" -d "{
    \"title\": \"Mountain Cabin\",
    \"description\": \"Cozy cabin in the mountains\",
    \"price\": 120.0,
    \"latitude\": 39.7392,
    \"longitude\": -104.9903,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
}" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)

echo -e "${YELLOW}ID del lugar creado: $PLACE_ID${NC}"
echo ""

# Prueba 11: Crear lugar con latitud inválida
show_result "Crear lugar con latitud inválida" "curl -s -X POST \"$BASE_URL/places/\" -H \"Content-Type: application/json\" -d '{
    \"title\": \"Invalid Place\",
    \"description\": \"Place with invalid latitude\",
    \"price\": 100.0,
    \"latitude\": 100.0,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\"
}' | json_pp"

# Prueba 12: Obtener lugar por ID
show_result "Obtener lugar por ID" "curl -s -X GET \"$BASE_URL/places/$PLACE_ID\" | json_pp"

# Prueba 13: Actualizar lugar
show_result "Actualizar lugar" "curl -s -X PUT \"$BASE_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -d '{
    \"title\": \"Updated Mountain Cabin\",
    \"price\": 130.0
}' | json_pp"

# ========= PRUEBAS DE REVIEWS =========
echo -e "${GREEN}=== PRUEBAS DE REVIEWS ===${NC}"

# Prueba 14: Crear review (caso exitoso)
show_result "Crear review (caso exitoso)" "curl -s -X POST \"$BASE_URL/reviews/\" -H \"Content-Type: application/json\" -d '{
    \"text\": \"Great place to stay!\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}' | json_pp"

# Guardamos el ID de la review para pruebas posteriores
REVIEW_ID=$(curl -s -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" -d "{
    \"text\": \"Amazing view and amenities\",
    \"rating\": 4,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}" | grep -o '"id": *"[^"]*"' | cut -d'"' -f4)

echo -e "${YELLOW}ID de la review creada: $REVIEW_ID${NC}"
echo ""

# Prueba 15: Crear review con rating inválido
show_result "Crear review con rating inválido" "curl -s -X POST \"$BASE_URL/reviews/\" -H \"Content-Type: application/json\" -d '{
    \"text\": \"Invalid rating\",
    \"rating\": 6,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}' | json_pp"

# Prueba 16: Obtener review por ID
show_result "Obtener review por ID" "curl -s -X GET \"$BASE_URL/reviews/$REVIEW_ID\" | json_pp"

# Prueba 17: Obtener reviews por lugar
show_result "Obtener reviews por lugar" "curl -s -X GET \"$BASE_URL/reviews/places/$PLACE_ID/reviews\" | json_pp"

# Prueba 18: Actualizar review
show_result "Actualizar review" "curl -s -X PUT \"$BASE_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\" -d '{
    \"text\": \"Updated review: Fantastic place!\",
    \"rating\": 5
}' | json_pp"

# Prueba 19: Eliminar review (única operación DELETE en la API)
show_result "Eliminar review" "curl -s -X DELETE \"$BASE_URL/reviews/$REVIEW_ID\" | json_pp"

# Prueba 20: Verificar que la review se eliminó
show_result "Verificar que la review se eliminó" "curl -s -X GET \"$BASE_URL/reviews/$REVIEW_ID\" | json_pp"

echo -e "${GREEN}Pruebas completadas!${NC}"