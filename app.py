from flask import Flask, render_template, request
from crypto import encrypt_message, decrypt_message
from stegano import embed, extract
from metrics import evaluate

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():

    result = ''

    if request.method == 'POST':

        mode = request.form['mode']
        key = request.form['key']

        file = request.files['image']
        path = 'uploads/input.png' 
        file.save(path)

        if mode == 'encode':

            msg = request.form['message']

            # Encrypt 
            cipher = encrypt_message(msg, key)

            # Embed ke gambar
            embed(path, cipher)

            # Evaluasi 
            psnr, ssim = evaluate(path, 'uploads/stego.png')

            result = f'Encode Success | PSNR={psnr:.2f} | SSIM={ssim:.4f}'

        else:

            # Extract dari gambar
            cipher = extract(path)

            # Kalau gambar tidak valid
            if "FOTO TIDAK ORIGINAL" in cipher:
                result = cipher

            else:
                # Decrypt
                plain = decrypt_message(cipher, key)
                result = f'Hidden Message : {plain}'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)