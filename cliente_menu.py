import socket

def mostrar_menu():
    print("\nMENÚ")
    print("1. Crear nombre de usuario")
    print("2. Crear dirección de correo")
    print("3. Salir")
    return input("Ingrese una opción: ")

def main():
    HOST = '127.0.0.1'
    PUERTO = 5000

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PUERTO))
            print("Conectado al servidor.")

            while True:
                opcion = mostrar_menu()

                if opcion == '1':
                    nombre_usuario = input("Ingrese un nombre de usuario (5-20 letras, al menos una vocal y una consonante, sin números): ")
                    mensaje = f"CREAR_USUARIO:{nombre_usuario}\n"
                    s.sendall(mensaje.encode())
                elif opcion == '2':
                    nombre_usuario = input("Ingrese el nombre de usuario para crear el correo: ")
                    mensaje = f"CREAR_CORREO:{nombre_usuario}\n"
                    s.sendall(mensaje.encode())
                elif opcion == '3':
                    s.sendall("SALIR\n".encode())
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida.")
                    continue

                respuesta = s.recv(1024).decode().strip()
                print(f"Servidor dice: {respuesta}")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. ¿Está corriendo?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
