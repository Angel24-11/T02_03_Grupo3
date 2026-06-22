\# Sistema de Gestión de Reservas de Hotel - UPS 🏨



\*\*Tarea T02.03 - Construcción de aplicación de software\*\*

\*\*Carrera de Computación | Ingeniería de Software\*\*

\---



\## 👥 Asignación de Tareas por Integrante (Grupo 3)

\* \*\*Chancay Rodriguez Oscar Emilio\*\* $\\rightarrow$ Desarrollo del Módulo de Usuarios y Clientes \[RF01 - RF03].

\* \*\*López Ortiz Karen Koraima\*\* $\\rightarrow$ Desarrollo del Módulo de Habitaciones y Disponibilidad \[RF04 - RF05].

\* \*\*Zambrano Infante Ángel Alejandro\*\* $\\rightarrow$ Desarrollo del Módulo de Reservas y Check-in/out \[RF06 - RF09].



\---



\## 📋 Requerimientos Funcionales (SRS - Tarea 02.01)

\* \*\*RF01:\*\* Crear, editar y deshabilitar usuarios con perfil de acceso.

\* \*\*RF02:\*\* Registrar información general de huéspedes.

\* \*\*RF03:\*\* Mostrar historial de reservas por cliente.

\* \*\*RF04:\*\* Registrar habitaciones con sus características (tipo, precio y estado).

\* \*\*RF05:\*\* Consultar disponibilidad en tiempo real.

\* \*\*RF06:\*\* Crear reservas de habitaciones.

\* \*\*RF07:\*\* Modificar o cancelar reservas.

\* \*\*RF08:\*\* Gestionar Check-in pasando la habitación a estado "Ocupada".

\* \*\*RF09:\*\* Gestionar Check-out y emitir factura.



\---



\## 🏛️ Esquema de Arquitectura (DDS - Tarea 02.02)

El proyecto implementa el patrón \*\*Modelo -> Repositorio -> Servicio -> Controlador\*\* similar al definido en la Figura 1 de la práctica:

\* `models/`: Entidades de la base de datos SQLite.

\* `repositories/`: Capa de acceso a persistencia y consultas SQL.

\* `services/`: Lógica de negocio e intermediación.

\* `controllers/`: Endpoints REST y APIRouter.



\---



\## 🚀 Tecnologías y Ejecución

\* \*\*Framework Backend:\*\* FastAPI (Python).

\* \*\*Documentación de Servicios:\*\* Interfaz Swagger UI generada automáticamente en la ruta `/docs`.

