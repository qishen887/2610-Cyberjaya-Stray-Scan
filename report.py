from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Absolute path — works regardless of where you run the script from
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

        saved_filename = None
        if file and file.filename != '':
            saved_filename = file.filename  # just the filename e.g. "rabbit.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(filepath)
            print(f"[DEBUG] Saved: {filepath}")

        animal_display = custom_animal if custom_animal else animal_type

        return jsonify({
            "status": "success",
            "message": "Report submitted successfully",
            "data": {
                "animal": animal_display,
                "location": address,
                "quantity": quantity,
                "health": health_status,
                "details": details,
                "image": saved_filename  # ONLY the filename, e.g. "rabbit.jpg"
            }
        })

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)