#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <cstdlib>

// Manejador personalizado para capturar señales asíncronas
void manejador_senal(int numero_senal) {
    std::cout << "\n[HIJO] ¡Señal " << numero_senal << " recibida con éxito! Ejecutando limpieza preventiva..." << std::endl;
    std::cout << "[HIJO] Proceso finalizado de forma controlada." << std::endl;
    exit(0); // Terminación exitosa
}

int main() {
    // Registrar el manejador para la señal SIGUSR1 utilizando signal()
    signal(SIGUSR1, manejador_senal);

    std::cout << "[PADRE] Iniciando demostración de ciclo de vida de procesos." << std::endl;
    std::cout << "[PADRE] Mi PID actual es: " << getpid() << std::endl;

    // 1. Demostración de fork()
    pid_t pid_resultado = fork();

    if (pid_resultado < 0) {
        std::cerr << "[ERROR] Falló la bifurcación del sistema mediante fork()." << std::endl;
        return 1;
    }
    
    if (pid_resultado == 0) {
        // --- Bloque de ejecución del PROCESO HIJO ---
        std::cout << "[HIJO] Proceso clonado correctamente." << std::endl;
        std::cout << "[HIJO] Mi PID es: " << getpid() << " | El PID de mi padre (PPID) es: " << getppid() << std::endl;
        
        std::cout << "[HIJO] Entrando en bucle infinito de espera pasiva..." << std::endl;
        while (true) {
            pause(); // Suspende el hilo del hijo hasta que arribe cualquier señal
        }
    } else {
        // --- Bloque de ejecución del PROCESO PADRE ---
        std::cout << "[PADRE] He creado un hijo con éxito. El PID asignado a mi hijo es: " << pid_resultado << std::endl;
        
        // Pausa breve para garantizar que el hijo imprima sus mensajes en la terminal
        sleep(2);
        
        // 2. Demostración de la comunicación mediante signal() y kill()
        std::cout << "\n[PADRE] Enviando señal personalizada SIGUSR1 al proceso hijo mediante kill()..." << std::endl;
        kill(pid_resultado, SIGUSR1);
        
        // Esperar formalmente a que el hijo termine para evitar procesos zombi
        int estado_hijo;
        waitpid(pid_resultado, &estado_hijo, 0);
        
        std::cout << "\n[PADRE] El proceso hijo ha sido recolectado. Estado de salida capturado." << std::endl;
        std::cout << "[PADRE] Demostración finalizada sin errores. Saliendo..." << std::endl;
    }

    return 0;
}