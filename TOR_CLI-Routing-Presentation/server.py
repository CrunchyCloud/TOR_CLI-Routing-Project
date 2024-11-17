import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher.PKCS1_OAEP import new

# Generate RSA keys for the server
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Decrypt the received encrypted message using the server's private key
def decrypt_with_private_key(encrypted_message, private_key):
    key = RSA.import_key(private_key)
    cipher = new(key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()

# Server logic to continuously listen for incoming messages
def server_program():
    host = '0.0.0.0'  # listen on all available interfaces
    port = 25000  # Port to listen on
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for connections
    print(f"Server listening on port {port}...")

    # Generate RSA keys for the server
    private_key, public_key = generate_rsa_keys()

    while True:
        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Send the server's public key to the client
        client_socket.send(public_key)

        while True:
            # Receive encrypted message from client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break  # If no message, the connection is closed

            # Decrypt the received message
            print(f"\033[1;33mEncrypted message: {encrypted_message}\033[0m")
            decrypted_message = decrypt_with_private_key(encrypted_message, private_key)
            print(f"\033[32mDecrypted message: {decrypted_message}\033[0m")

        client_socket.close()
        print(f"Connection with {client_address} closed.")

if __name__ == "__main__":
    server_program()

