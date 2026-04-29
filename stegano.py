import cv2

END = '11111110'

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


def embed(img_path, message):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 100, 200)

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

                # STOP lebih cepat kalau marker ditemukan
                if len(binary) >= 8:
                    if binary[-8:] == END:
                        return bin_to_text(binary)

    return bin_to_text(binary)