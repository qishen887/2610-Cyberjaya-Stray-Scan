from flask import Flask, render_template, request, jsonify
import os
from flask import send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def home():
    return render_template('report_page.html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        animal_type = request.form.get('animalType')
        custom_animal = request.form.get('customAnimal')
        address = request.form.get('address')
        quantity = request.form.get('quantity')
        health_status = request.form.get('healthStatus')
        details = request.form.get('details')

        file = request.files.get('img')

        filepath = None
        if file and file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

        animal_display = custom_animal if custom_animal else animal_type

        print("=== New Report ===")
        print(animal_type, custom_animal, address, quantity, health_status, details)
        print("Image:", filepath)

        return jsonify({
            "status": "success",
            "message": "Report submitted successfully",
            "data": {
                "animal": animal_display,
                "location": address,
                "quantity": quantity,
                "health": health_status,
                "details": details,
                "image": filepath  
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)
