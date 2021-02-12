from flask import Flask, render_template, redirect, request, jsonify, send_file
import os
import io
import pymongo
import exrex
import base64

MONGO_CLIENT = pymongo.MongoClient(os.environ.get(
    'MONGO_URI', 'mongodb://localhost:27017/'))
MONGO_DB = MONGO_CLIENT['screenshots_go_burrrr']
MONGO_COLLECTION = MONGO_DB['images']

print(pymongo.MongoClient(os.environ.get(
    'MONGO_URI', 'mongodb://localhost:27017/')))

app = Flask(__name__)


def generate_error(code, details):
    return jsonify({"error": {"code": code, "message": details}}), code


@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Screenshots go BURRRR</title>
        </head>
        <body>
            Screenshots go BURRRR HAHA EPIC BURRRR THE SCREENSHOTS SAY (inspect element for extra brrrrs) <br><br><br>   <!-- Haha get it burr goes here because burr haha funny -->
            The epyc client & source coded can be found <a href="https://github.com/CatDevz/ScreenshotsGoBURRRR/">here</a>. 
        </body>
    </html>
    """


@app.route('/get/<slug>')
def get(slug):
    try:  # Try to get the image and return it
        if MONGO_COLLECTION.count_documents({'_id': slug}) > 0:
            doc = MONGO_COLLECTION.find_one({'_id': slug})
            return send_file(
                io.BytesIO(doc['image']),
                attachment_filename='{}.png'.format(slug),
                mimetype='image/png')
    except Exception as e:
        return generate_error(500, "Internal Server Error")
    return generate_error(404, "The file requested was not found")


@app.route('/upload', methods=['POST'])
def upload():
    req = request.json

    # Making sure the request is in JSON
    if req == None:
        return generate_error(400, "Request body must contain valid JSON")

    # Making sure all required fields are in the body
    if not 'image' in req:
        return generate_error(400, "Request body must contain image field")

    # Getting the image in binary
    image = base64.b64decode(req['image'])

    # Validating the image
    if 20000 > len(image) or len(image) > 15000000:
        return generate_error(400, 'Image must be larger than 20 KB and smaller than 15 MB')

    # Generate a random slug & secret
    slug = exrex.getone('([a-z0-9]{8})')
    secret = exrex.getone('([a-zA-Z0-9]{24})')

    try:  # Try to insert the document into the collection
        MONGO_COLLECTION.insert_one({
            '_id': slug,
            'secret': secret,
            'image': image
        })

        return jsonify({'slug': slug, 'secret': secret}), 200
    except Exception as ignored:
        return generate_error(500, 'Internal Database Error')
    return generate_error(500, 'Internal Server Error')


if __name__ == "__main__":
    app.run()
