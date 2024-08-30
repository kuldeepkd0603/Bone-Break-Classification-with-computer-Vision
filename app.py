from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load your model
model = load_model('bone_break_classify.h5')

class_names = [
    'Avulsion Fracture', 'Comminuted Fracture', 'Fracture Dislocation',
    'Greenstick Fracture', 'Hairline Fracture', 'Impacted Fracture',
    'Longitudinal Fracture', 'Oblique Fracture', 'Pathological Fracture',
    'Spiral Fracture'
]

# Detailed information about fractures
fracture_info = {
    'Avulsion Fracture': {
        'overview': "An avulsion fracture is where a small piece of bone attached to a tendon or ligament gets pulled away from the main part of the bone. This often happens when you suddenly change direction.",
        'symptoms': [
            'Sudden, severe pain',
            'Bruising',
            'Swelling',
            'Muscle pain',
            'Popping or cracking sound',
            'Difficulty moving the limb'
        ],
        'causes': [
            'Suddenly changing direction',
            'Sprinting',
            'Kicking',
            'Leaping',
            'Falling on an outstretched hand'
        ],
        'diagnosis': [
            'X-rays to look at bones and joints',
            'CT scan for a more precise view'
        ],
        'treatment': [
            'Immobilization in a cast or splint',
            'Anti-inflammatory medications',
            'Restriction of activity',
            'Icing the area',
            'Physical therapy'
        ],
        'prognosis': "Recovery typically takes about three to 12 weeks. You may need to follow up with an orthopaedist."
    },
    'Comminuted Fracture': {
        'overview': "A comminuted fracture is when the bone is shattered into three or more pieces, often due to high-impact trauma.",
        'symptoms': [
            'Severe pain',
            'Swelling',
            'Bruising',
            'Deformity at the fracture site'
        ],
        'causes': [
            'High-impact trauma',
            'Vehicle accidents',
            'Falls from a height'
        ],
        'diagnosis': [
            'X-rays to visualize the fracture',
            'CT scan for detailed images of bone fragments'
        ],
        'treatment': [
            'Surgical intervention to realign and stabilize the bone',
            'Immobilization with cast or brace',
            'Rehabilitation exercises'
        ],
        'prognosis': "Healing depends on the fracture severity and treatment. It may require surgery and extensive rehabilitation."
    },
    'Fracture Dislocation': {
        'overview': "A fracture dislocation occurs when a bone breaks and the fractured end is displaced from its normal position, often affecting a joint.",
        'symptoms': [
            'Intense pain',
            'Visible deformity',
            'Swelling',
            'Inability to move the affected joint'
        ],
        'causes': [
            'Trauma or accidents',
            'Sports injuries',
            'Falls'
        ],
        'diagnosis': [
            'X-rays to check bone alignment and joint position',
            'MRI for detailed imaging of soft tissue damage'
        ],
        'treatment': [
            'Reduction of the fracture and dislocated joint',
            'Immobilization with cast or splint',
            'Physical therapy to restore function'
        ],
        'prognosis': "Recovery varies based on the severity of the dislocation and fracture. Early treatment improves outcomes."
    },
    'Greenstick Fracture': {
        'overview': "A greenstick fracture is an incomplete fracture where the bone bends. It typically occurs in children whose bones are softer and more flexible.",
        'symptoms': [
            'Pain at the site of injury',
            'Swelling',
            'Deformity or bending of the limb'
        ],
        'causes': [
            'Falling on an outstretched arm',
            'Direct blow to the bone'
        ],
        'diagnosis': [
            'Physical examination',
            'X-rays to confirm the fracture'
        ],
        'treatment': [
            'Casting or splinting',
            'Follow-up X-rays to ensure proper healing'
        ],
        'prognosis': "Greenstick fractures usually heal well with immobilization in 4 to 6 weeks."
    },
    'Hairline Fracture': {
        'overview': "A hairline fracture is a small, thin crack in the bone that often doesn't completely break through. It can be caused by repetitive stress or trauma.",
        'symptoms': [
            'Localized pain',
            'Swelling',
            'Tenderness'
        ],
        'causes': [
            'Repetitive stress or overuse',
            'Minor trauma',
            'Weakening of the bone'
        ],
        'diagnosis': [
            'X-rays may not always detect hairline fractures',
            'MRI or bone scan for more accurate diagnosis'
        ],
        'treatment': [
            'Rest and avoidance of activities causing pain',
            'Protective bracing or splinting',
            'Gradual return to activity'
        ],
        'prognosis': "Hairline fractures often heal with conservative treatment over several weeks."
    },
    'Impacted Fracture': {
        'overview': "An impacted fracture occurs when the broken ends of the bone are driven into each other, often resulting from high-impact trauma.",
        'symptoms': [
            'Severe pain',
            'Swelling',
            'Inability to move the affected limb'
        ],
        'causes': [
            'High-impact trauma',
            'Falls',
            'Automobile accidents'
        ],
        'diagnosis': [
            'X-rays to evaluate bone alignment',
            'CT scan for detailed fracture assessment'
        ],
        'treatment': [
            'Immobilization with cast or splint',
            'Possible surgical intervention to realign bones',
            'Rehabilitation for strength and mobility'
        ],
        'prognosis': "Treatment success and recovery time depend on fracture severity and alignment."
    },
    'Longitudinal Fracture': {
        'overview': "A longitudinal fracture runs along the length of the bone. It is less common and usually caused by a significant impact or trauma.",
        'symptoms': [
            'Pain along the length of the bone',
            'Swelling',
            'Difficulty moving the limb'
        ],
        'causes': [
            'Direct trauma',
            'Falls',
            'High-impact activities'
        ],
        'diagnosis': [
            'X-rays to visualize the fracture',
            'CT scan for detailed bone imaging'
        ],
        'treatment': [
            'Casting or splinting',
            'Surgical intervention in severe cases',
            'Physical therapy to restore function'
        ],
        'prognosis': "Healing time varies based on fracture severity and treatment."
    },
    'Oblique Fracture': {
        'overview': "An oblique fracture occurs at an angle across the bone, usually due to a sharp, direct force.",
        'symptoms': [
            'Pain at the fracture site',
            'Swelling',
            'Bruising'
        ],
        'causes': [
            'Direct impact',
            'Falls',
            'Sports injuries'
        ],
        'diagnosis': [
            'X-rays to assess fracture angle and alignment',
            'CT scan if X-rays are inconclusive'
        ],
        'treatment': [
            'Immobilization with cast or splint',
            'Possible surgical realignment',
            'Rehabilitation exercises'
        ],
        'prognosis': "Oblique fractures generally heal well with appropriate treatment and rehabilitation."
    },
    'Pathological Fracture': {
        'overview': "A pathological fracture occurs in a bone weakened by disease, such as cancer or osteoporosis, rather than trauma.",
        'symptoms': [
            'Pain in the affected area',
            'Swelling',
            'Increased vulnerability to fractures'
        ],
        'causes': [
            'Underlying disease such as osteoporosis or cancer',
            'Minor trauma or stress'
        ],
        'diagnosis': [
            'X-rays to detect fractures',
            'MRI or CT scan to assess underlying disease'
        ],
        'treatment': [
            'Addressing the underlying disease',
            'Casting or splinting',
            'Surgery in severe cases'
        ],
        'prognosis': "Healing depends on the underlying condition and overall treatment approach."
    },
    'Spiral Fracture': {
        'overview': "A spiral fracture is caused by a twisting or rotational force on the bone, resulting in a fracture that spirals around the bone.",
        'symptoms': [
            'Pain at the fracture site',
            'Swelling',
            'Deformity or twisting of the limb'
        ],
        'causes': [
            'Twisting injuries',
            'Sports accidents',
            'Falls'
        ],
        'diagnosis': [
            'X-rays to confirm the spiral pattern',
            'CT scan for detailed imaging'
        ],
        'treatment': [
            'Immobilization with cast or splint',
            'Surgical intervention if needed',
            'Rehabilitation to restore function'
        ],
        'prognosis': "Spiral fractures typically heal with appropriate treatment, but recovery time varies."
    }
}

# Set up the upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Preprocess the input image
    img = request.files['file']
    if img:
        filename = secure_filename(img.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(filepath)

        img = Image.open(filepath)
        img = img.resize((256, 256))
        img_array = np.array(img).reshape(1, 256, 256, 3)
        img_array = img_array / 255.0

        # Make a prediction
        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_names[predicted_class_index]

        # Retrieve information based on the predicted class
        info = fracture_info.get(predicted_class, "No information available for this type of fracture.")

        return render_template('result.html', 
                               predicted_class=predicted_class, 
                               overview=info.get('overview', 'No overview available.'),
                               symptoms=info.get('symptoms', []),
                               causes=info.get('causes', []),
                               diagnosis=info.get('diagnosis', []),
                               treatment=info.get('treatment', []),
                               prognosis=info.get('prognosis', 'No prognosis available.'),
                               image_path=filepath)
    return "No file uploaded", 400

if __name__ == "__main__":
    app.run(debug=True)
