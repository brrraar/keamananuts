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

            cipher = encrypt_message(msg,key)

            embed(path,cipher)

            psnr, ssim = evaluate(path,'uploads/stego.png')

            result = f'Encode Success | PSNR={psnr:.2f} | SSIM={ssim:.4f}'

        else:

            cipher = extract(path)
            plain = decrypt_message(cipher,key)

            result = f'Hidden Message : {plain}'

    return render_template('index.html',result=result)

app.run(debug=True)