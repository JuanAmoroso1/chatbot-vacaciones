import csv
from datetime import datetime

# ── BASE DE DATOS ──────────────────────────────────────────
def cargar_empleados():
    empleados = {}
    with open('empleados.csv', newline='', encoding='utf-8') as f:
        for fila in csv.DictReader(f):
            empleados[fila['legajo']] = {
                'nombre': fila['nombre'],
                'dias_disponibles': int(fila['dias_disponibles'])
            }
    return empleados

def guardar_solicitud(legajo, nombre, fecha_inicio, dias_solicitados, estado):
    with open('solicitudes.csv', 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([legajo, nombre, fecha_inicio, dias_solicitados, estado])

# ── MÁQUINA DE ESTADOS ─────────────────────────────────────
def chatbot():
    print("=" * 45)
    print("  BOT DE GESTIÓN DE VACACIONES - UTN TUP")
    print("=" * 45)

    empleados = cargar_empleados()
    estado = 0
    empleado_actual = None
    fecha_inicio = None
    dias_solicitados = None

    while True:

        # ESTADO 0 — Pedir legajo
        if estado == 0:
            legajo = input("\nBot: Hola, ingresá tu número de legajo: ").strip()
            if legajo in empleados:
                empleado_actual = empleados[legajo]
                empleado_actual['legajo'] = legajo
                print(f"Bot: Bienvenido, {empleado_actual['nombre']}. "
                      f"Tenés {empleado_actual['dias_disponibles']} días disponibles.")
                estado = 1
            else:
                print("Bot: Legajo no encontrado. Intentá de nuevo.")
                # estado se mantiene en 0

        # ESTADO 1 — Pedir fechas
        elif estado == 1:
            fecha_inicio = input("\nBot: ¿Desde qué fecha querés tomar vacaciones? (DD/MM/AAAA): ").strip()
            try:
                datetime.strptime(fecha_inicio, "%d/%m/%Y")
                dias_str = input("Bot: ¿Cuántos días solicitás?: ").strip()
                dias_solicitados = int(dias_str)
                if dias_solicitados <= 0:
                    print("Bot: La cantidad de días debe ser mayor a cero.")
                else:
                    estado = 2
            except ValueError:
                print("Bot: Fecha u cantidad inválida. Intentá de nuevo.")

        # ESTADO 2 — Verificar saldo (automático)
        elif estado == 2:
            print("\nBot: Verificando saldo de días...")
            if dias_solicitados <= empleado_actual['dias_disponibles']:
                print(f"Bot: Saldo suficiente. Enviando solicitud al supervisor...")
                estado = 3
            else:
                print(f"Bot: Saldo insuficiente. Tenés {empleado_actual['dias_disponibles']} días "
                      f"y solicitás {dias_solicitados}. Solicitud rechazada automáticamente.")
                guardar_solicitud(empleado_actual['legajo'], empleado_actual['nombre'],
                                  fecha_inicio, dias_solicitados, 'RECHAZADA')
                estado = 4

        # ESTADO 3 — Decisión del supervisor
        elif estado == 3:
            decision = input("\nSupervisor: ¿Aprobás la solicitud? (si/no): ").strip().lower()
            if decision == 'si':
                print(f"Bot: ✔ Solicitud APROBADA. ¡Que disfrutes tus vacaciones, {empleado_actual['nombre']}!")
                guardar_solicitud(empleado_actual['legajo'], empleado_actual['nombre'],
                                  fecha_inicio, dias_solicitados, 'APROBADA')
            elif decision == 'no':
                print(f"Bot: ✘ Solicitud RECHAZADA por el supervisor.")
                guardar_solicitud(empleado_actual['legajo'], empleado_actual['nombre'],
                                  fecha_inicio, dias_solicitados, 'RECHAZADA')
            else:
                print("Supervisor: Respuesta inválida. Ingresá 'si' o 'no'.")
                continue
            estado = 4

        # ESTADO 4 — Finalizado
        elif estado == 4:
            print("\nBot: Proceso finalizado. ¡Hasta luego!")
            print("=" * 45)
            break

chatbot()