# -*- coding: utf-8 -*-

import os
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


@app.route("/")
def home():
    return "TrotWave API running"


@app.route("/lyrics", methods=["POST"])
def make_lyrics():

    try:
        data = request.get_json()

        theme = data.get("theme", "")
        genre = data.get("genre", "")
        vocal = data.get("vocal", "")
        length = data.get("length", "")
        style = data.get("style", "")

        if theme == "":
            return "주제를 입력해주세요."

        prompt = f"""
너는 한국 트롯, EDM트롯, CCM트롯 전문 작사가다.

아래 조건에 맞춰 노래 가사를 작성하라.

[입력 정보]
주제: {theme}
장르: {genre}
보컬: {vocal}
길이: {length}
스타일: {style}

[작성 규칙]

- 반드시 한국어 가사만 출력
- 설명 금지
- JSON 금지
- 코드블록 금지
- 가사 외 문장 금지

- 형식:
[Verse 1]
가사

[Chorus]
가사

[Verse 2]
가사

[Chorus]
가사

- 후렴은 중독성 있게 작성
- 트롯이면 자연스러운 꺾기 느낌 반영
- EDM트롯이면 신나는 리듬감 반영
- 너무 빠르게 몰아치는 가사 금지
- 3분~3분30초 분량
"""

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        lyrics = response.output_text

        return lyrics

    except Exception as e:
        return "오류 발생: " + str(e)


@app.route("/music", methods=["POST"])
def make_music():
    return "음악 생성 기능 준비중"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
