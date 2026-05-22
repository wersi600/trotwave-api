from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "TrotWave AI API running"

@app.route("/music", methods=["POST"])
def make_music():
    data = request.get_json()

    theme = data.get("theme", "")
    genre = data.get("genre", "")
    vocal = data.get("vocal", "")
    length = data.get("length", "")
    style = data.get("style", "")
    lyrics = data.get("lyrics", "")

    return jsonify({
        "status": "success",
        "message": "테스트 서버 응답 성공",
        "theme": theme,
        "genre": genre,
        "vocal": vocal,
        "length": length,
        "style": style,
        "lyrics": lyrics,
        "audio_url": "https://example.com/test.mp3"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)