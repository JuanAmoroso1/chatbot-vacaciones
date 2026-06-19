# Chatbot de Gestión de Vacaciones — UTN TUP

## Descripción
Simulador de chatbot administrativo para gestión de solicitudes de vacaciones.
Desarrollado como Trabajo Práctico Integrador de Organización Empresarial.

## Integrantes
- Juan Amoroso
- Hernan Avila

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
| 1 | IDENTIFICADO | Legajo validado, solicita fecha de inicio |
| 2 | SALDO_VERIFICADO | Fecha de inicio válida, solicita fecha de fin |
| 3 | FECHAS_CONFIRMADAS | Ambas fechas válidas, solicita confirmación |
| 4 | ENVIADO_SUPERVISOR | Solicitud enviada, aguarda decisión del supervisor |
| 5 | FINALIZADO_APROBADO | Supervisor aprobó, notifica y registra |
| 6 | FINALIZADO_RECHAZADO | Solicitud rechazada, notifica motivo |

## Casos de prueba
- **Legajo 1001** (Ana García, 15 días) — camino feliz
- **Legajo 1003** (María Fernández, 0 días) — rechazo automático por saldo insuficiente
- **Legajo 9999** — legajo inexistente, reintenta
- **Fecha retroactiva** — bot rechaza e indica que debe ser futura
- **Fecha fin anterior a inicio** — bot rechaza el rango