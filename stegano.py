import cv2
import hashlib

END = '11111110'
HEADER = "STEGO:"

def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text) + END


def bin_to_text(binary):
    text = ''

    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]

        if len(byte) < 8:
            break

        if byte == END:
            break

        text += chr(int(byte, 2))

    return text


# 🔐 Tambahkan header + hash
def prepare_message(message):
    hash_val = hashlib.sha256(message.encode()).hexdigest()[:8]
    return HEADER + hash_val + ":" + message


def verify_message(text):
    if not text.startswith(HEADER):
        return None  # bukan gambar original

    try:
        content = text[len(HEADER):]
        hash_val, message = content.split(":", 1)

        check_hash = hashlib.sha256(message.encode()).hexdigest()[:8]

        if hash_val != check_hash:
            return None  # data rusak / sudah diedit

        return message

    except:
        return None


def embed(img_path, message):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 100, 200)

    # 🔐 prepare message
    message = prepare_message(message)

    binary = text_to_bin(message)
    idx = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if edge[i, j] > 0:
                if idx < len(binary):
                    img[i, j, 0] = (img[i, j, 0] & 254) | int(binary[idx])
                    idx += 1
                else:
                    break
        if idx >= len(binary):
            break

    cv2.imwrite("uploads/stego.png", img)


def extract(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 100, 200)

    binary = ''

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if edge[i, j] > 0:
                binary += str(img[i, j, 0] & 1)

                if len(binary) >= 8:
                    if binary[-8:] == END:
                        raw_text = bin_to_text(binary)

                        # 🔐 VALIDASI
                        valid = verify_message(raw_text)

                        if valid is None:
                            return "FOTO TIDAK ORIGINAL / DATA RUSAK"

                        return valid

    return "FOTO TIDAK ORIGINAL / DATA RUSAK"