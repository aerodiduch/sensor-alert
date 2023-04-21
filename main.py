import psutil
import smtplib


def get_cpu_temps():
    sensors = psutil.sensors_temperatures()["coretemp"]
    max_temperature = 0
    temps = 0
    for sensor in sensors:
        temps += sensor.current
        if sensor.current > max_temperature:
            max_temperature = sensor.current
            hottest_core = sensor.label
    average_temperature = round((temps / len(sensors)), 1)

    return {
        "hottest_core": hottest_core,
        "max_temperature": max_temperature,
        "average_temp": average_temperature,
    }


def send_email(data):
    subject = f"🚨 ALERTA DE TEMPERATURA 🚨 {data.get('max_temperature')} °C"
    body = f"""Temperatura promedio del sistema: {data.get("average_temperature")} 
Núcleo más caliente: {data.get("hottest_core")}

Llamen a los bomberos que me estoy quemando!
"""

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("mi_email@proveedor.com", "application_password")
        server.sendmail("sender_email", "receiver_email", message.encode("utf-8"))


if __name__ == "__main__":
    data = get_cpu_temps()
    if data.get("max_temperature") >= 70:
        send_email(data)
