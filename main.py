from flask import Flask, jsonify
import requests
import xmltodict
import os

app = Flask(__name__)

# imood XML url
XML_URL = "https://xml.imood.org/query.cgi?email=rayarmahedgehog@hotmail.com"

@app.route("/data", methods=["GET"])
def serve_custom_json():
    try:
        response = requests.get(XML_URL)
        response.raise_for_status()
        xml_data = xmltodict.parse(response.text)

        mood_data = xml_data["imood"]["bundle"]["mood"]
        mood_base = mood_data["base"]
        mood_face = mood_data["face"]

        result = {
            "mood": mood_base,
            "emoji": mood_face
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
