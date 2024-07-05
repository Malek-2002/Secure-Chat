from project_def import *
import hashlib
import threading

client_socket = requestConnection(IP, PORT)
print(f"[CONNECTED] Connection with ({IP}, {PORT}) has been established!\n")

if not check_parameters(a, q):
    print(f"[ERROR] Invalid Parameters.")
    print("[DISCONNECTED] Terminating connection...")
    time.sleep(2)
    exit(1)

# Getting Symmetric Key
print(f"[INITIALIZING] Creating symmetric key...")
time.sleep(2) # just to show the loading
key = handshake_client_side(client_socket)
if key == -1:
    print("[DISCONNECTED] Terminating connection...")
    time.sleep(2)
    exit(1)
print(f"[INITIALIZING] Symmetric key generated.\n")

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

# Create a thread for receiving messages from the server
receive_thread = threading.Thread(target=receiveData_AES, args=(client_socket, AES_key))
receive_thread.start()

# Main thread for sending messages to the server
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
