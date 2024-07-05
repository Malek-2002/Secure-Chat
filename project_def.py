from Crypto.Cipher import AES
import time
from time import sleep
import pickle
import socket
import sys
import random
import math
import hashlib
from param import *


# =====================================================================================
# ==================================== Utils ==========================================
# =====================================================================================

def coprime(a, b):
    return math.gcd(a, b) == 1

def isPrime(x):
    if x <= 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    i = 5
    while i * i <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return False
        i += 6
    return True


def gen_invertable_num_mod_q(q):
    for k in range(q, 0, -1):
        if coprime(k, q-1):  # Check if k and q-1 are coprime
            return k

def get_lsb_n(num, n):
    mask = 1 << n
    return (num & mask) >> n

def is_primitive_root(a, q):
    return True
    # if math.gcd(a, q) != 1:
    #     return False

    phi_q = q - 1  # Since q is prime
    factors = set()
    m = phi_q
    for i in range(2, int(m**0.5) + 1):
        if m % i == 0:
            factors.add(i)
            while m % i == 0:
                m //= i
    if m > 1:
        factors.add(m)
    for p in factors:
        if binary_exponentiation(a, phi_q // p, q) == 1:
            return False
    return True

# =====================================================================================
# ======================================= Parameters ==================================
# =====================================================================================


def check_q(q):
    return True

def check_a(a, q):
    return (a > 1 and a < q) and is_primitive_root(a, q)

def check_parameters(a, q):
    return check_q(q) and check_a(a, q)

# =====================================================================================
# ======================================= Constants ===================================
# =====================================================================================

HEADER_SIZE = 10
IP = "127.0.0.1"
PORT = 1324


# =====================================================================================
# ======================================= AES =========================================
# =====================================================================================
def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('utf-8'))
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('utf-8')
    except:
        return False

# =====================================================================================
# ================================= Receive Data ======================================
# =====================================================================================

def receiveData_AES(client_socket, key):
    while True:
        obj = receiveData(client_socket)
        # print(f"Receiving: {obj['nonce']}, {obj['ciphertext']}, {obj['tag']}")
        plaintext = decrypt(obj['nonce'], obj['ciphertext'], obj['tag'], key)
        if not plaintext:
            print('[Error] Message is corrupted!')
        else:
            print(f"Received: {plaintext}")

def receiveData(client_socket):
    # Receive Data
    full_msg = b""
    new_msg = True
    while True:
        try:
            msg = client_socket.recv(16)  # buffer >= HEADER_SIZE
            if new_msg:
                msglen = int(msg[:HEADER_SIZE])
                new_msg = False
            full_msg += msg
        except:
            print("Sorry, other side is disconnected \nWill close in 5 seconds...")
            time.sleep(1)
            print("Will close in 4 seconds...")
            time.sleep(1)
            print("Will close in 3 seconds...")
            time.sleep(1)
            print("Will close in 2 seconds...")
            time.sleep(1)
            print("Will close in 1 second...")
            time.sleep(1)
            sys.exit()

        if len(full_msg) - HEADER_SIZE == msglen:
            d = pickle.loads(full_msg[HEADER_SIZE:])
            return d

# =====================================================================================
# ==================================== Send Data ======================================
# =====================================================================================


def sendData_AES(data, client_socket, key):
    # Encrypt
    nonce, ciphertext, tag = encrypt(data, key)
    # print(f"Sending: {nonce}, {ciphertext}, {tag}")
    encrypted_data = {"nonce":nonce, "ciphertext":ciphertext, "tag":tag}
    # Send
    sendData(encrypted_data, client_socket)

def sendData(data, client_socket):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg
    client_socket.send(msg)

# =====================================================================================
# ==================================== Connection =====================================
# =====================================================================================

def requestConnection(IP, port):
    try:
        # Connect to PORT
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, port))

        return client_socket
    except socket.error as e:
        print(f"Error: Unable to connect to {IP}:{port}. Error message: {e}")
        sys.exit(1)

def acceptConnection(my_socket):
    client_socket, address = my_socket.accept()
    print(f"[CONNECTED] Connection from {address} has been established!\n")

    return client_socket

# =====================================================================================
# ==================================== Handshake ======================================
# =====================================================================================
# To get symmetric key

def get_m_value(M):
    # Calc sha1 of M
    M_sha1 = hashlib.sha1(str(M).encode('utf-8')).digest()
    # convert M_sha1 to int
    m_int = int.from_bytes(M_sha1, byteorder='big')

    for i in range(m_int.bit_length(), 0, -1):
        if  get_lsb_n(m_int, i) > 0 and get_lsb_n(m_int, i-1) < q-1:
            return get_lsb_n(m_int, i)


def binary_exponentiation(a, b, m):
    res = 1
    a = a % m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b = b // 2
    return res

def handshake_server_side(client_socket):
    # ========================= Diffe Helman
    # Generate Xa, Ya
    Xa = random.randint(1, q)
    # Caclulate Diff Helman public key
    Ya = binary_exponentiation(a, Xa, q)

    # ========================= El Gamal
    Xa2 = random.randint(1, q)
    Ya2 = binary_exponentiation(a, Xa2, q)
    # share public keys Ya2, Yb2
    sendData(Ya2, client_socket)
    Yb2 = int(receiveData(client_socket))

    M = Ya
    m = get_m_value(M)
    k = gen_invertable_num_mod_q(q)
    # binary_exponentiation(a, -1, m) calcuates the mod inverse of a mod m
    S1 = binary_exponentiation(a, k, q)
    S2 = (binary_exponentiation(k, -1, q - 1) * (m - Xa2 * S1)) % (q-1)

    # Send keys (El Gamal)
    sendData(Ya, client_socket)
    sendData(S1, client_socket)
    sendData(S2, client_socket)

    # Receive keys (El Gamal)
    Yb = int(receiveData(client_socket))
    S1 = int(receiveData(client_socket))
    S2 = int(receiveData(client_socket))

    # Verify signature
    M = Yb
    m = get_m_value(M)
    V1 = (binary_exponentiation(Yb2,S1,q) * binary_exponentiation(S1,S2,q)) % q
    V2 = binary_exponentiation(a,m,q)
    # print(f"V1 % q? {V1 % q}, V2 % q? {V2 % q}")
    # print(f"Valid? {V1 % q == V2 % q}")

    if V1 % q != V2 % q:
        print('[Error] Signature is not valid!')
        client_socket.close()
        return -1

    # ** Key **
    k = binary_exponentiation(Yb, Xa,q)

    return k

def handshake_client_side(client_socket):
    # ========================= Diffe Helman
    # Generate Xb, Yb
    Xb = random.randint(1, q)
    # Caclulate Diff Helman public key
    Yb = binary_exponentiation(a, Xb,q)

    # ========================= El Gamal
    Xb2 = random.randint(1, q)
    Yb2 = binary_exponentiation(a, Xb2, q)
    # share public keys Ya2, Yb2
    sendData(Yb2, client_socket)
    Ya2 = int(receiveData(client_socket))

    # Receive keys (El Gamal)
    Ya = int(receiveData(client_socket))
    S1 = int(receiveData(client_socket))
    S2 = int(receiveData(client_socket))

    # Verify signature
    M = Ya
    m = get_m_value(M)
    V1 = (binary_exponentiation(Ya2,S1, q) * binary_exponentiation(S1,S2, q))
    V2 = binary_exponentiation(a,m, q)
    # print(f"Valid? {V1 % q == V2 % q}")
    # print(f"V1 % q? {V1 % q}, V2 % q? {V2 % q}")


    if V1 % q != V2 % q:
        print('[Error] Signature is not valid!')
        client_socket.close()
        return -1


    M = Yb
    m = get_m_value(M)
    k = gen_invertable_num_mod_q(q)

    # binary_exponentiation(a, -1, m) calcuates the mod inverse of a mod m
    S1 = binary_exponentiation(a, k, q)
    S2 = (binary_exponentiation(k, -1, q-1) * (m - Xb2 * S1)) % (q-1)

    # Send keys (El Gamal)
    sendData(Yb, client_socket)
    sendData(S1, client_socket)
    sendData(S2, client_socket)

    # ** Key **
    k = binary_exponentiation(Ya, Xb, q)

    return k
