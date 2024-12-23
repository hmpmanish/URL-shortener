from flask import Flask, request, render_template, redirect, url_for
import random
import string
import qrcode
import os

app = Flask(__name__)

# Dictionary to store URL mappings
url_mapping = {}

def generate_short_url():
    """Generate a random 6-character short URL"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    qr_code_url = None
    if request.method == 'POST':
        original_url = request.form['original_url']
        if original_url in url_mapping:
            short_url = url_mapping[original_url]
        else:
            short_url = generate_short_url()
            url_mapping[original_url] = short_url
            url_mapping[short_url] = original_url
        
        # Generate QR code
        qr = qrcode.make(f"http://127.0.0.1:5000/{short_url}")
        qr_code_path = os.path.join('static', f"{short_url}.png")
        qr.save(qr_code_path)
        qr_code_url = qr_code_path

    return render_template('home.html', short_url=short_url, qr_code_url=qr_code_url)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = url_mapping.get(short_url)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
