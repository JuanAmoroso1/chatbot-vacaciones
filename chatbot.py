import csv
from datetime import datetime, date

# ── BASE DE DATOS ──────────────────────────────────────────
def cargar_empleados():
    empleados = {}

    with open('empleados.csv', newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for fila in lector:
            empleados[fila['legajo']] = {
                'nombre': fila['nombre'],
                'dias_disponibles': int(fila['dias_disponibles'])
            }

    return empleados


def guardar_solicitud(legajo, nombre, fecha_inicio, fecha_fin, dias_solicitados, estado, motivo=''):

    with open('solicitudes.csv', 'a', newline='', encoding='utf-8') as f:

        escritor = csv.writer(f)

        escritor.writerow([
            legajo,
            nombre,
            fecha_inicio.strftime("%d/%m/%Y"),
            fecha_fin.strftime("%d/%m/%Y"),
            dias_solicitados,
            estado,
            motivo,
            datetime.now().strftime("%d/%m/%Y %H:%M")
        ])


def calcular_dias_habiles(fecha_inicio, fecha_fin):

    dias = 0
    diferencia = fecha_fin - fecha_inicio

    for i in range(diferencia.days + 1):

        dia_actual = date.fromordinal(fecha_inicio.toordinal() + i)

        if dia_actual.weekday() < 5:
            dias += 1

    return dias


def verificar_solicitud_pendiente(legajo):

    try:
        with open('solicitudes.csv', newline='', encoding='utf-8') as f:

            lector = csv.DictReader(f)

            for fila in lector:

                if fila['legajo'] == legajo and fila['estado'] == 'PENDIENTE':
                    return True

    except:
        return False

    return False


# ── CHATBOT ────────────────────────────────────────────────
def chatbot():

    print("=" * 50)
    print(" BOT DE GESTIÓN DE VACACIONES - UTN TUP ")
    print("=" * 50)

    empleados = cargar_empleados()

    estado = 0

    while True:

        # ESTADO 0: pedir legajo
        if estado == 0:

            legajo = input("\nBot: Ingresá tu legajo: ")

            if not legajo.isdigit():
                print("Bot: El legajo debe ser numérico.")
                continue

            if legajo not in empleados:
                print("Bot: Legajo no encontrado.")
                continue

            if verificar_solicitud_pendiente(legajo):
                print("Bot: Ya tenés una solicitud pendiente.")
                continue

            empleado = empleados[legajo]

            print(f"Bot: Bienvenido {empleado['nombre']}")
            print(f"Bot: Tenés {empleado['dias_disponibles']} días disponibles.")

            estado = 1

        # ESTADO 1: fecha inicio
        elif estado == 1:

            entrada = input("Bot: Fecha de inicio (DD/MM/AAAA): ")

            try:
                fecha_inicio = datetime.strptime(entrada, "%d/%m/%Y").date()

                if fecha_inicio < date.today():
                    print("Bot: La fecha debe ser futura.")
                    continue

                estado = 2

            except:
                print("Bot: Fecha inválida.")

        # ESTADO 2: fecha fin
        elif estado == 2:

            entrada = input("Bot: Fecha de fin (DD/MM/AAAA): ")

            try:
                fecha_fin = datetime.strptime(entrada, "%d/%m/%Y").date()

                if fecha_fin <= fecha_inicio:
                    print("Bot: La fecha final debe ser posterior.")
                    continue

                dias_solicitados = calcular_dias_habiles(
                    fecha_inicio, fecha_fin)

                print(f"Bot: Solicitás {dias_solicitados} días hábiles.")

                estado = 3

            except:
                print("Bot: Fecha inválida.")

        # ESTADO 3: confirmación
        elif estado == 3:

            respuesta = input("Bot: ¿Confirmás la solicitud? (si/no): ")

            if respuesta.lower() == "no":
                print("Bot: Solicitud cancelada.")
                break

            elif respuesta.lower() == "si":

                if dias_solicitados > empleado['dias_disponibles']:

                    guardar_solicitud(
                        legajo,
                        empleado['nombre'],
                        fecha_inicio,
                        fecha_fin,
                        dias_solicitados,
                        "RECHAZADA",
                        "Saldo insuficiente"
                    )

                    estado = 6

                else:
                    print("Bot: Solicitud enviada al supervisor.")
                    estado = 4

            else:
                print("Bot: Ingresá si o no.")

        # ESTADO 4: supervisor
        elif estado == 4:

            decision = input(
                "Supervisor: ¿Aprobás la solicitud? (si/no): ")

            if decision.lower() == "si":

                guardar_solicitud(
                    legajo,
                    empleado['nombre'],
                    fecha_inicio,
                    fecha_fin,
                    dias_solicitados,
                    "APROBADA"
                )

                estado = 5

            elif decision.lower() == "no":

                motivo = input("Supervisor: Motivo del rechazo: ")

                guardar_solicitud(
                    legajo,
                    empleado['nombre'],
                    fecha_inicio,
                    fecha_fin,
                    dias_solicitados,
                    "RECHAZADA",
                    motivo
                )

                estado = 6

            else:
                print("Supervisor: Ingresá si o no.")

        # ESTADO 5: aprobado
        elif estado == 5:

            saldo_restante = empleado['dias_disponibles'] - dias_solicitados

            print("\nBot: Solicitud APROBADA.")
            print(f"Bot: Te quedan {saldo_restante} días.")

            break

        # ESTADO 6: rechazado
        elif estado == 6:

            print("\nBot: Solicitud RECHAZADA.")

            break


chatbot()