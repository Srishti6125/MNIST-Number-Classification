from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Load trained model
model = load_model("mnist_cnn.h5")


def preprocess_image_pil(image: Image.Image):
    """Convert PIL image to 28x28 grayscale tensor."""
    image = image.convert("L")           # grayscale
    image = image.resize((28, 28))       # resize

    img_array = np.array(image).astype("float32") / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    return img_array


def pil_to_base64(image: Image.Image):
    """Convert PIL image to base64 PNG for HTML img tag."""
    # Make a nicer preview size
    preview_img = image.convert("RGB")
    preview_img.thumbnail((160, 160))  # keep aspect ratio

    buf = BytesIO()
    preview_img.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probs = None
    error = None
    image_data = None
    image_name = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "No file uploaded."
            return render_template("index.html", error=error)

        file = request.files["file"]

        if file.filename == "":
            error = "Please select an image."
            return render_template("index.html", error=error)

        try:
            # Open once as PIL
            img = Image.open(file)
            image_name = file.filename

            # For preview in template
            image_data = pil_to_base64(img)

            # For model input
            processed = preprocess_image_pil(img)
            preds = model.predict(processed)
            predicted_label = int(np.argmax(preds, axis=1)[0])

            probs = [(i, float(preds[0][i])) for i in range(10)]
            prediction = predicted_label

        except Exception as e:
            error = f"Error processing image: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        probs=probs,
        error=error,
        image_data=image_data,
        image_name=image_name,
    )


if __name__ == "__main__":
    app.run(debug=True)
