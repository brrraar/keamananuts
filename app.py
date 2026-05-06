from flask import Flask, render_template, request, jsonify, send_file
from crypto import encrypt_message, decrypt_message
from stegano import embed, extract
from metrics import evaluate
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# STEP 1 — Enkripsi pesan dulu, tampilkan ciphertext
@app.route('/encrypt', methods=['POST'])
def encrypt_step():
    message = request.form.get('message', '')
    key = request.form.get('key', '')
    if not message or not key:
        return jsonify({'success': False, 'error': 'Pesan dan kunci harus diisi.'})
    cipher = encrypt_message(message, key)
    return jsonify({'success': True, 'cipher': cipher})

# STEP 2 — Embed ciphertext ke gambar
@app.route('/embed', methods=['POST'])
def embed_step():
    cipher = request.form.get('cipher', '')
    key    = request.form.get('key', '')
    file   = request.files.get('image')
    if not cipher or not file or not key:
        return jsonify({'success': False, 'error': 'Semua field harus diisi.'})
    path = 'uploads/input.png'
    os.makedirs('uploads', exist_ok=True)
    file.save(path)
    embed(path, cipher)
    psnr, ssim = evaluate(path, 'uploads/stego.png')
    return jsonify({
        'success': True,
        'psnr': round(psnr, 2),
        'ssim': round(ssim, 4),
        'message': f'Embed berhasil! PSNR={psnr:.2f} dB | SSIM={ssim:.4f}'
    })

# Download stego image
@app.route('/download')
def download():
    return send_file('uploads/stego.png', as_attachment=True, download_name='stego.png')

# STEP — Decode: extract + decrypt
@app.route('/decode', methods=['POST'])
def decode_step():
    key  = request.form.get('key', '')
    file = request.files.get('image')
    if not file or not key:
        return jsonify({'success': False, 'error': 'Gambar dan kunci harus diisi.'})
    path = 'uploads/decode_input.png'
    os.makedirs('uploads', exist_ok=True)
    file.save(path)
    cipher = extract(path)
    if "FOTO TIDAK ORIGINAL" in cipher:
        return jsonify({'success': False, 'error': cipher})
    plain = decrypt_message(cipher, key)
    if plain in ("KODE SALAH!", None):
        return jsonify({'success': False, 'error': 'Kunci salah atau pesan rusak.'})
    return jsonify({'success': True, 'message': plain, 'cipher': cipher})

if __name__ == '__main__':
    app.run(debug=True)