#!/usr/bin/python3
"""
Script para generar hash bcrypt de una contraseña
"""
import bcrypt

def generate_password_hash(password):
    """Genera un hash bcrypt para una contraseña"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

if __name__ == "__main__":
    password = "admin1234"
    hashed_password = generate_password_hash(password)
    print(f"Password: {password}")
    print(f"Hashed Password: {hashed_password}")
