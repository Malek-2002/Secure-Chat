<div align = "center">
<h1>Secure Chat</h1>
  
![image](https://github.com/user-attachments/assets/2657a828-23fe-40a8-8f2e-74336c032787)

![Used lang](https://img.shields.io/badge/Language-Python-4584b6)

Welcome to Secure Chat, a highly secure chatting application that ensures your messages are encrypted and safe from eavesdropping. This application uses a combination of cryptographic techniques to establish a secure communication channel over sockets.
</div>


## ❕ Description

Chat apps bring people closer virtually even if they live far off from each other. It gives them the convenience to connect without the need to spend a fortune and time to meet people in-person. However, ensuring the security of messages is a huge challenge that is critical for the end users. Here is where things become interesting and cryptography kicks in.

Each encryption algorithm has its strengths and weaknesses. For instance, AES is a symmetric algorithm that is fast enough and efficient for large data, but the encryption key must be shared securely, so we tend to use Diffie-Hellman for key exchange. However, DH is prone to man-in-the-middle attacks. To make things secure, a digital signature is required for making sure that only the source is the one who sent this message.

## 🌟 Features

- **Diffie-Hellman Key Exchange**: Securely exchange session keys.
- **ElGamal Digital Signature**: Ensure the authenticity of messages.
- **AES Encryption**: Encrypt messages with a strong symmetric encryption algorithm.
- **Socket-based Communication**: Establish a reliable connection for chatting.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
     git clone https://github.com/Mohamed0x3/secure-chat.git
     cd secure-chat
    ```

2. **Install dependencies:**
    ```bash
    pip install pycryptodome
    ```

3. **Set `q` and `alpha`:**
    1. Open param.py
    2. Set q to a prime number.
    3. Set a such that (1 < a < q) and a is a primitive root to q.

## 🚀 Usage

1. Open two terminals in the project directory:
    - In the first terminal, start the server:
    ```bash
    python .\server.py
    ```
    - Wait until the server is *LISTENING*.
     
2. In the second terminal, start the client:
    ```bash
    python .\client.py
    ```


  Start chatting! 😃

## 👨‍💻 Establishing Connection
  ![0](https://github.com/user-attachments/assets/e9408516-3831-493f-b657-53c09be21b05)
- Deffie Hellman keys (q, α, Xa, Ya, Xb, Yb) are different from ElGamal keys (q, α, Xa2, Ya2, Xb2, Yb2).
- Elgamal keys should be long-living (generated once a year) while DH keys are ephemeral (generated per session).
- Both parties will read DH(q, α) and Elgamal (q, α) from a file simulating being publicly accessed.
- Both parties will generate two public/private-key pairs (one for DH and one for Elgamal).
- Alice and Bob will exchange Elgamal keys.
- Alice sends to Bob her DH public key after signing it using Elgamal digital signature.
- Bob verifies Alice’s identity and terminates the connection if the signature is not valid.
- Bob sends back his DH public key after signing it using Elgamal digital signature.
- Alice verifies Bob’s identity and terminates the connection if the signature is not valid.
- Both parties compute the DH shared secret.
- Generate an AES 256-bit key from the DH shared key using a key derivation function SHA256(shared secret).
- Use the generated key for the subsequent chat messages between the two parties for encryption and decryption.
