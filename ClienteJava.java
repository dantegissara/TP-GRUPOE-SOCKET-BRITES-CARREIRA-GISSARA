
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class ClienteJava {
    public static void main(String[] args) {
        final String HOST = "127.0.0.1";
        final int PUERTO = 5000;

        try (Socket socket = new Socket(HOST, PUERTO);
             BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter salida = new PrintWriter(socket.getOutputStream(), true);
             Scanner scanner = new Scanner(System.in);) {

            System.out.println("Conectado al servidor.");

            while (true) {
                // Menú simple
                System.out.println("\nMENÚ");
                System.out.println("1. Crear nombre de usuario");
                System.out.println("2. Crear dirección de correo");
                System.out.println("3. Salir");
                System.out.print("Ingrese una opción: ");
                String opcion = scanner.nextLine();

                if (opcion.equals("1")) {
                    System.out.print("Ingrese un nombre de usuario (5-20 letras, al menos una vocal y una consonante, sin números): ");
                    String nombreUsuario = scanner.nextLine();
                    salida.println("CREAR_USUARIO:" + nombreUsuario);
                } else if (opcion.equals("2")) {
                    System.out.print("Ingrese su nombre de usuario para crear el correo: ");
                    String nombreUsuario = scanner.nextLine();
                    salida.println("CREAR_CORREO:" + nombreUsuario);
                } else if (opcion.equals("3")) {
                    salida.println("SALIR");
                    break;
                } else {
                    System.out.println("Opción inválida.");
                    continue;
                }

                // Leer respuesta del servidor
                String respuesta = entrada.readLine();
                System.out.println("Servidor dice: " + respuesta);
            }

            System.out.println("Desconectado del servidor.");

        } catch (IOException e) {
            System.err.println("Error de conexión: " + e.getMessage());
        }
    }
}
