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
    data = request.get_json(force=True, silent=True) or {}

    # 1. 코듈라에서 보낸 title 데이터를 가져옵니다.
    title = data.get("title", "").strip()
    theme = data.get("theme", "").strip()
    genre = data.get("genre", "").strip()
    vocal = data.get("vocal", "").strip()
    length = data.get("length", "").strip()
    style = data.get("style", "").strip()

    # 주제가 없다면 기존처럼 방어막 작동
    if not theme:
        return "노래 주제를 입력해주세요."

    # 2. AI에게 전달할 프롬프트에 제목(title) 정보를 추가하고, 규칙을 보완합니다.
    prompt = f"""
너는 한국 대중가요, 트롯, EDM트롯, CCM트롯 가사를 전문으로 만드는 작사가다.

아래 조건에 맞춰 노래 가사를 만들어라.

[사용자 입력]
제목(선호하는 방향): {title if title else "자유롭게 정해줘"}
주제: {theme}
장르: {genre}
보컬: {vocal}
곡 길이: {length}
스타일: {style}

[가사 작성 규칙]
- 한국어 가사만 출력
- 설명, 해설, JSON, 코드블록 금지
- 출력 결과물 맨 첫 줄에는 노래 제목을 🎵 제목: [노래제목] 형태로 출력하고 한 줄 띄운 뒤 가사를 시작하라.
- [Verse 1], [Chorus], [Verse 2], [Chorus] 형식 사용
- 가사가 너무 빽빽하지 않게 작성
- 3분~3분30초 노래에 어울리는 분량
- 후렴은 기억하기 쉽게
- 트롯 선택 시 자연스러운 꺾기와 중년 감성 반영
- EDM트롯 선택 시 신나는 리듬감과 반복 후렴 반영
- 종교적 주제가 아니면 종교 용어 사용 금지
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return "가사 생성 오류: " + str(e)


@app.route("/music", methods=["POST"])
def make_music():
    return "음악 생성 기능은 다음 단계에서 연결합니다."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
