import cv2
from time import sleep
from cryptography.fernet import Fernet

c = {}
d = {}


def keygen():
    key = Fernet.generate_key()
    with open('fernet.key', 'wb') as key_file:
        key_file.write(key)
        key_file.flush()

    key_file.close()

    print('Saved .key file')
    sleep(5)
    return key


def load_key(key_loc):
    key = open(key_loc, 'rb').read()
    return key


def enc_msg(key, msg):
    f_msg = Fernet(key).encrypt(msg.encode())
    return f_msg.decode('utf-8')


def dec_msg(key, f_msg):
    msg = Fernet(key).decrypt(f_msg)
    return msg.decode('utf-8')


def encrypt(msg, img):
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    m = 0
    n = 0
    z = 0

    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    cv2.imwrite("encImg.png", img)
    print("Saved encrypted image as 'encImg.png'")
    sleep(3)


def decrypt(passkey, msg, img):
    message = ""
    n = 0
    m = 0
    z = 0

    passcode = input("Enter passkey for Decryption: ")
    if passkey == passcode:
        for i in range(len(msg)):
            message = message + c[img[n, m, z]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
        return message.encode()
    else:
        print("Unauthorized Access")
        sleep(3)
        return b'###########################'


key = None
msg = None
f_msg = None
passkey = None

option = 9
img = cv2.imread("spidey.png")
while option != 0:
    print("\tImage Steganography Interface\n"
          "\tWhat would you like to do:\n"
          "\t\t1- Hide some Secret Text in an image (LSB Steganography)\n"
          "\t\t2- Hide secure Secret Text in an image (LSB Steganography using Fernet)\n"
          "\t\t0- Exit\n")
    option = input("Your choice: ")

    match option:
        case '1':
            while option != 0:
                print("\tWhat would you like to do:\n"
                      "\t\t1- Encrypt\n"
                      "\t\t2- Decrypt\n"
                      "\t\t0- Main Menu\n")
                option = input("Your choice: ")
                match option:
                    case '1':
                        msg = input("Enter secret message: ")
                        passkey = input("Enter a passkey: ")
                        encrypt(msg, img)
                    case '2':
                        d_msg = decrypt(passkey, msg, img)
                        print("Decrypted Message:", d_msg.decode('utf-8'))
                        sleep(5)
                    case '0':
                        break
                    case _:
                        print("Invalid Input")

        case '2':
            print("\t1- I have an existing key\n"
                  "\t2- Generate a new key for me\n")
            option = input("Your choice: ")
            match option:
                case '1':
                    key_loc = input("Enter key location: ")
                    key = load_key(key_loc)

                case '2':
                    key = keygen()
            while option != 0:
                print("\tWhat would you like to do:\n"
                      "\t\t1- Encrypt\n"
                      "\t\t2- Decrypt\n"
                      "\t\t0- Main Menu\n")
                option = input("Your choice: ")
                match option:
                    case '1':
                        msg = input("Enter secret message: ")
                        passkey = input("Enter a passkey: ")
                        f_msg = enc_msg(key, msg)
                        encrypt(f_msg, img)
                    case '2':
                        d_msg = decrypt(passkey, f_msg, img)
                        res = dec_msg(key, d_msg)
                        print(res)
                        sleep(5)
                    case '0':
                        break
                    case _:
                        print("Invalid Input")

        case '0':
            break

        case _:
            print("Invalid Input")
