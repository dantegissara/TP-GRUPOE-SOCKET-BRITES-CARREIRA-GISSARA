import socket
import random
import string

def validar_usuario(nombre_usuario):
    # Validar longitud
    if len(nombre_usuario) < 5 or len(nombre_usuario) > 20:
        return False
    # Validar solo letras (sin números ni caracteres especiales)
    if not nombre_usuario.isalpha():
        return False
    # Validar al menos una vocal y una consonante
    vocales = set('aeiouAEIOU')
    tiene_vocal = any(c in vocales for c in nombre_usuario)
    tiene_consonante = any(c.isalpha() and c not in vocales for c in nombre_usuario)
    return tiene_vocal and tiene_consonante

def generar_correo(nombre_usuario):
    # Generar correo con dominio válido aleatorio
    dominios_validos = ['gmail.com', 'hotmail.com']
    dominio = random.choice(dominios_validos)
    correo = f"{nombre_usuario.lower()}@{dominio}"
    return correo

def manejar_cliente(conn, addr, usuarios_creados, correos_creados):
    print(f"Cliente conectado desde {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode().strip()
            print(f"Recibido: {mensaje}")

            if mensaje.startswith("CREAR_USUARIO:"):
                nombre_usuario = mensaje[len("CREAR_USUARIO:"):].strip()
                if not validar_usuario(nombre_usuario):
                    conn.sendall("ERROR:Nombre de usuario inválido. Debe tener entre 5 y 20 letras, solo letras, con al menos una vocal y una consonante.\n".encode())
                elif nombre_usuario in usuarios_creados:
                    conn.sendall(f"ERROR:Usuario ya existe: {nombre_usuario}\n".encode())
                else:
                    usuarios_creados.add(nombre_usuario)
                    conn.sendall(f"OK:Usuario creado: {nombre_usuario}\n".encode())

            elif mensaje.startswith("CREAR_CORREO:"):
                nombre_usuario = mensaje[len("CREAR_CORREO:"):].strip()
                if nombre_usuario not in usuarios_creados:
                    conn.sendall("ERROR:Usuario no registrado.\n".encode())
                elif nombre_usuario in correos_creados:
                    correo = correos_creados[nombre_usuario]
                    conn.sendall(f"ERROR:Correo ya creado para este usuario: {correo}\n".encode())
                else:
                    correo = generar_correo(nombre_usuario)
                    correos_creados[nombre_usuario] = correo
                    conn.sendall(f"OK:{correo}\n".encode())

            elif mensaje == "SALIR":
                conn.sendall("OK:Conexión finalizada.\n".encode())
                break

            else:
                conn.sendall("ERROR:Comando no reconocido.\n".encode())

    print(f"Cliente {addr} desconectado.")

def main():
    HOST = '127.0.0.1'
    PUERTO = 5000
    usuarios_creados = set()
    correos_creados = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PUERTO))
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PUERTO}")

        while True:
            conn, addr = servidor.accept()
            manejar_cliente(conn, addr, usuarios_creados, correos_creados)

if __name__ == "__main__":
    main()
