from machine import Pin
import network
import socket
import time

LED = Pin(2, Pin.OUT)        # LED sur la broche GPIO 2
BP = Pin(4, Pin.IN, Pin.PULL_UP)  # Bouton sur la broche GPIO 4 avec pull-up

def button_isr(pin):
  LED.value(not LED.value())

BP.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)

# Fonction pour générer la page HTML
def web_page():
    led_state = "Allumée" if LED.value() == 1 else "Éteinte"
    return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="0.5"> <!-- Rafraîchissement toutes les 0.5 secondes -->
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                p{{margin-left: 4em;}}
                h1{{color: blue; margin-left: 0.5em;}}
                h2{{color: purple; margin-top: 1em; margin-left: 2em; margin-right: 1em; margin-bottom: 1em; font-size: 1.2em;}}
            </style>
            <title>Serveur ESP32 - Théo-Félix</title>
        </head>
        <body>
            <h1>Serveur ESP32 de Théo-Félix</h1>
            <p>Bienvenue sur le serveur de Théo-Félix.</p>
            <br>
            <h2>Etat des composants</h2>
            <p>Etat de la LED : {led_state}</p>
            <input class="styled" type="button" value="LED" />
            <p> <a href="{button_isr}"> LED </a> </p>
        </body>
        </html>
    """

# Configurer le point d'accès Wi-Fi
my_ap = network.WLAN(network.AP_IF)
my_ap.active(True)
my_ap.config(essid='Théo-Félix', authmode=network.AUTH_WPA_WPA2_PSK, password='theofefelegoat')

# Configurer le socket HTTP
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('', 80))
my_socket.listen(5)

# Attente d'un client qui se connecte
print("Serveur en attente de connexion...")

while True:
    try:
        # Attendre une connexion du client
        conn, addr = my_socket.accept()
        print('Connexion reçue de %s' % str(addr))
        request = conn.recv(1024)
        print('Requête : %s' % str(request))

        # Envoi de la page HTML
        conn.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        conn.send(web_page())  # Envoie la page web avec l'état actuel de la LED
        conn.close()  # Fermer la connexion

        time.sleep(0.1)  # Petit délai pour éviter un sur-engorgement du CPU
    except Exception as e:
        print("Erreur lors de la gestion de la connexion:", e)
        conn.close()  # Assurez-vous de fermer la connexion en cas d'erreur