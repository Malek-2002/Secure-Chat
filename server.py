from project_def import *
import hashlib
import threading


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
print(f"[LISTENING] Server is listening on {IP}")
client_socket = acceptConnection(server_socket)

if not check_parameters(a, q):
    client_socket.close()
    print(f"[ERROR] Invalid Parameters.")
    print("[DISCONNECTED] Terminating connection...")
    time.sleep(2)
    exit(1)

# Getting Symmetric Key
print(f"[INITIALIZING] Creating symmetric key...")
time.sleep(2) # just to show the loading
key = handshake_server_side(client_socket)
if key == -1:
    print("[DISCONNECTED] Terminating connection...")
    time.sleep(2)
    exit(1)
print(f"[INITIALIZING] Symmetric key generated.\n")
time.sleep(2) # just to show the loading

# Creating AES layer
print(f"[INITIALIZING] Creating encryption layer...")
time.sleep(2) # just to show the loading

k_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
AES_key = hashlib.sha256(k_bytes).digest()  # 256-bit key
print(f"[INITIALIZING] Encryption layer created.\n")


print("======================")
print("\tChat App\t")
print("======================\n\n")

# print(key)
# print(AES_key)

# Create a thread for receiving messages from the client
receive_thread = threading.Thread(target=receiveData_AES, args=(client_socket, AES_key))
receive_thread.start()

# Main thread for sending messages to the client
while True:
    try:
        message = input()
        sendData_AES(message, client_socket, AES_key)
    except KeyboardInterrupt:
        try:
            client_socket.close()
        except:
            pass
        break
    except ConnectionResetError:
        break

receive_thread.join()

