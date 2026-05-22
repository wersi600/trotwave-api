# -*- coding: utf-8 -*-

import os
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/")
def home():
    return "TrotWave AI API running"


@app.route("/lyrics", methods=["POST"])
def make_lyrics():
    data = request.get_json() or {}

    theme = data.get("theme", "").strip()
    genre = data.get("genre", "").strip()
    vocal = data.get("vocal", "").strip()
    length = data.get("length", "").strip()
    style = data.get("style", "").strip()

    if not theme:
        return "노래 주제를 입력해주세요."

    prompt = f"""
너는 한국 대중가요, 트롯, EDM트롯, CCM트롯 가사를 전문으로 만드는 작사가다.

아래 조건에 맞춰 노래 가사를 만들어라.

[사용자 입력]
주제: {theme}
장르: {genre}
보컬: {vocal}
곡 길이: {length}
스타일: {style}

[가사 작성 규칙]
- 한국어 가사만 출력
- 설명, 해설, JSON, 코드블록 금지
- [Verse 1], [Chorus], [Verse 2], [Chorus] 형식 사용
- 가사가 너무 빽빽하지 않게 작성
- 3분~3분30초 노래에 어울리는 분량
- 후렴은 기억하기 쉽게
- 트롯 선택 시 자연스러운 꺾기와 중년 감성 반영
- EDM트롯 선택 시 신나는 리듬감과 반복 후렴 반영
- 종교적 주제가 아니면 종교 용어 사용 금지
"""

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )
        return response.output_text.strip()

    except Exception as e:
        return "가사 생성 오류: " + str(e)


@app.route("/music", methods=["POST"])
def make_music():
    return "음악 생성 기능은 다음 단계에서 연결합니다."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
