# Chatbot de Gestión de Vacaciones — UTN TUP

## Descripción
Simulador de chatbot administrativo para gestión de solicitudes de vacaciones.
Desarrollado como Trabajo Práctico Integrador de Organización Empresarial.

## Integrantes
- Juan Amoroso
- Celina Medina

## Tecnologías
- Python 3
- CSV como base de datos simulada

## Archivos
- `chatbot.py` — lógica del bot y máquina de estados
- `empleados.csv` — base de datos de empleados
- `solicitudes.csv` — registro de solicitudes generadas

## Cómo ejecutar
1. Clonar el repositorio
2. Abrir una terminal en la carpeta
3. Ejecutar: `python chatbot.py`

## Máquina de estados
| Estado | Nombre | Descripción |
|--------|--------|-------------|
| 0 | INICIO | Solicita legajo del empleado |
| 1 | ESPERANDO_FECHAS | Solicita fecha y días |
| 2 | VERIFICANDO_SALDO | Verifica días disponibles (automático) |
| 3 | ESPERANDO_SUPERVISOR | Aguarda decisión del supervisor |
| 4 | FINALIZADO | Muestra resultado y cierra |

## Casos de prueba
- **Legajo 1001** (Ana García, 15 días) — camino feliz
- **Legajo 1003** (María Fernández, 0 días) — rechazo automático
- **Legajo 9999** — legajo inexistente