import socket
import socks  # PySocks
from Crypto.PublicKey import RSA
from Crypto.Cipher.PKCS1_OAEP import new
from stem import Signal
from stem.control import Controller

# Encrypt the message with the server's public key
def encrypt_with_public_key(message, public_key):
    key = RSA.import_key(public_key)
    cipher = new(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

# Function to get the Tor circuit info
def get_tor_circuit_info():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        
        # Request circuit information
        circuits = controller.get_circuits()
        for circuit in circuits:
            print(f"Circuit {circuit.id}:")
            for path in circuit.path:
                print(f"  - {path}")
            print("------")

# Client logic to continuously send messages to the server through Tor
def client_program():
    host = '24.80.189.0'  # The server's IP address or domain
    port = 25000  # The port the server is listening on

    # Set up the Tor SOCKS5 proxy
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)  # Default Tor SOCKS5 Proxy settings
    socket.socket = socks.socksocket  # Replaces the socket object to route through Tor

    # Now, create a socket and connect to the server (via Tor)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive the server's public key
    public_key = client_socket.recv(2048)

    # Log current Tor circuit info
    get_tor_circuit_info()

    while True: 
        # Prompt the user to enter a message
        message = input("Enter message to send (or 'exit' to quit): ")

        if message.lower() == 'exit':
            break

        # Encrypt the message using the server's public key
        encrypted_message = encrypt_with_public_key(message, public_key)

        # Send the encrypted message to the server
        client_socket.send(encrypted_message)

    client_socket.close()

if __name__ == "__main__":
    client_program()

