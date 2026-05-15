import streamlit as st
import base64
import os
import json

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"total": 0, "types": {}}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="SIUFC Football Persona Test", page_icon="⚽️", layout="centered")

# --- UI 숨기기 CSS 주입 ---
hide_streamlit_style = """
            <style>
            /* 상단 헤더 전체 숨기기 (Deploy 및 ... 메뉴 포함) */
            [data-testid="stHeader"] {d
                visibility: hidden;
            }

            /* 상단 기본 패딩 제거 */
            [data-testid="stAppViewContainer"] > section:first-child {
                padding-top: 10px !important;
            }
            .block-container {
                padding-top: 10px !important;
            }

            /* 혹시 모를 툴바 강제 숨김 */
            [data-testid="stToolbar"] {
                visibility: hidden !important;
            }

            /* 하단의 'Made with Streamlit' 워터마크 숨기기 */
            footer {
                visibility: hidden;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 2. 로컬 배경 이미지 적용 (Base64 변환) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    if os.path.exists(png_file):
        bin_str = get_base64(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        '''
    else:
        # 파일이 없을 경우 기본 배경색
        page_bg_img = '<style>.stApp { background-color: #f0f2f6; }</style>'

    st.markdown(page_bg_img, unsafe_allow_html=True)


# 모바일 최적화 스타일
st.markdown("""
    <style>
    /* 모바일 반응형 설정 */
    @media (max-width: 768px) {
        .stApp { padding: 10px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        p, div { font-size: 15px !important; line-height: 1.6 !important; }
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        padding: 14px 10px;
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
        color: white;
        font-size: 14px;
        font-weight: 600;
        margin: 8px 0;
        border: none;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
        text-align: center;
        line-height: 1.4;
        word-wrap: break-word;
        white-space: normal;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
    }
    
    /* 다시 테스트 버튼 */
    button[kind="secondary"][data-testid="baseButton-secondary"]:first-of-type,
    .stButton:has(button[key="retry"]) > button {
        background: linear-gradient(135deg, #a8a8a8 0%, #6c6c6c 100%) !important;
        box-shadow: 0 4px 15px rgba(108, 108, 108, 0.4) !important;
    }
    
    /* 질문 박스 */
    .question-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.2);
        animation: fadeIn 0.5s ease-in;
    }
    
    /* 결과 카드 */
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin: 15px 0;
        border-left: 5px solid #667eea;
        animation: slideUp 0.6s ease-out;
    }
    
    /* 프로그레스 바 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 컬럼 내부 텍스트 강제 검은색 */
    .stColumn p, .stColumn div, .stColumn span, .stColumn strong, .stColumn b {
        color: #1a1a1a !important;
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* 로딩 애니메이션 */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 뒤로가기 버튼 */
    .back-button {
        background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%) !important;
        margin-top: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 배경화면 실행 (파일명이 univ_bg.jpg 인지 확인해주세요!)
set_background("univ_bg.png")

# --- 3. 데이터 세팅 ---

questions = [
    # --- [E vs I] 필드 위에서의 존재감 (Energy/Presence) ---
    {"q": "Q1. 경기 시작 전 라커룸(Locker Room)! 킥오프를 기다리는 나의 모습은?", 
     "options": [
         "\"Let's go guys!!🔥\" 노래를 크게 틀고 박수를 치며 팀원들의 텐션을 미친듯이 끌어올린다.", 
         "조용히 이어폰을 꽂고 이미지 트레이닝을 하며 나의 역할에만 무섭게 집중한다."
     ], "type": "EI"},
    
    {"q": "Q2. 우리 팀이 공격 중이다! 패스를 받고 싶을 때 나의 스타일은?", 
     "options": [
         "\"Hey! Here! Pass me!!🙋‍♂️\" 손을 번쩍 들고 큰 소리로 패스를 요구하며 시선을 끈다.", 
         "소리 없이 빈 공간으로 파고든 뒤, 패서(Passer)와 눈빛을 교환하여 공을 받는다."
     ], "type": "EI"},

    {"q": "Q3. 마침내 극장골을 넣었다! 나의 세리머니(Celebration)는?", 
     "options": [
         "코너 플래그로 전력 질주 후 무릎 슬라이딩! 관중들의 환호를 온몸으로 즐긴다 (SIU!!).", 
         "가볍게 주먹을 불끈 쥐고, 어시스트를 해준 동료를 손가락으로 가리키며 하이파이브 한다."
     ], "type": "EI"},

    # --- [S vs N] 플레이 스타일 (Playstyle/Skill) ---
    {"q": "Q4. 측면에서 수비수와 1:1로 맞붙었다! 나의 돌파 방법은?", 
     "options": [
         "치달(Kick and Rush)! 공을 길게 차놓고 나의 압도적인 스피드와 피지컬로 찍어 누른다.", 
         "알까기(Nutmeg) 아니면 플립플랩! 수비수의 템포를 빼앗는 화려하고 창의적인 개인기를 쓴다."
     ], "type": "SN"},
    
    {"q": "Q5. 동료가 뛰기 시작했다. 지금 나에게 필요한 패스는?", 
     "options": [
         "가장 안전하고 정확하게 동료의 발밑에 배달되는 인사이드 땅볼 패스.", 
         "\"이게 길이 있다고?\" 수비수 3명 사이를 가르는 예술적인 아웃프런트(Trivela) 킬패스."
     ], "type": "SN"},

    {"q": "Q6. 개인 훈련을 할 때, 내가 더 공들여서 연습하는 것은?", 
     "options": [
         "축구는 체력과 기본기! 코어 트레이닝, 스프린트, 정확한 슈팅 연습에 매진한다.", 
         "축구는 예술! 유튜브에서 본 새로운 개인기나 묘기 같은 발리슛을 시도해 본다."
     ], "type": "SN"},

    # --- [T vs F] 멘탈과 의사결정 (Mentality/Decision) ---
    {"q": "Q7. 앗! 우리 팀 에이스가 상대의 거친 태클에 쓰러졌다! 나의 반응은?", 
     "options": [
         "즉시 심판에게 다가가 논리적으로 파울 상황을 어필하고 카드(Yellow Card)를 요구한다.", 
         "\"What are you doing?!🤬\" 이성을 잃고 태클한 상대 선수에게 달려가 가슴을 밀친다."
     ], "type": "TF"},
    
    {"q": "Q8. 전반전 종료, 스코어는 0:3. 최악의 분위기 속에서 내가 할 말은?", 
     "options": [
         "\"수비 라인이 너무 높아. 4-4-2로 바꾸고 미드필드 간격을 더 좁혀야 해!\" (전술적 피드백)", 
         "\"포기하지 마! 우리 자존심이 있잖아! 유니폼에 흙 묻을 때까지 뛰어!!\" (감정적 독려)"
     ], "type": "TF"},

    {"q": "Q9. 완벽한 1:1 찬스에서 슛이 골대를 빗나갔다. 이 순간 나의 머릿속은?", 
     "options": [
         "'디딤발이 너무 멀었고 상체가 들렸네. 다음엔 반대 포스트를 노려야지.' (원인 분석)", 
         "'아 미쳤다 진짜... 팀원들한테 너무 미안해ㅠㅠ' 무릎을 꿇고 머리를 감싸 쥔다. (멘탈 붕괴)"
     ], "type": "TF"},

    # --- [J vs P] 전술과 경기 운영 (Tactics/Pacing) ---
    {"q": "Q10. 내가 감독이라면 만들고 싶은 '가장 완벽한 팀'의 축구는?", 
     "options": [
         "점유율 70%! 끝없는 패스 워크와 체계적인 포메이션으로 상대를 숨 막히게 하는 축구.", 
         "10초면 충분하다! 라인을 내리고 버티다 벼락같은 스피드로 뒷공간을 박살 내는 역습 축구."
     ], "type": "JP"},
    
    {"q": "Q11. 후반 85분, 1:0으로 우리가 이기고 있다. 남은 5분 동안 우리는?", 
     "options": [
         "공을 돌리며 점유율을 유지하고, 코너 플래그로 가 시간을 영리하게 소비한다(Time wasting).", 
         "상대가 급해서 라인을 올렸다! 이 빈틈을 노려 확실하게 쐐기골(2nd Goal)을 박으러 간다."
     ], "type": "JP"},

    {"q": "Q12. 경기 중, 감독님이 지시한 전술이 전혀 먹히지 않고 있다!", 
     "options": [
         "그래도 훈련한 시스템(System)을 믿는다. 우리의 포메이션과 계획을 흔들림 없이 유지한다.", 
         "계획은 버려! 그라운드 위에서의 본능(Instinct)과 변수 창출을 믿고 자유롭게 스위칭한다."
     ], "type": "JP"}
]
questions_en = [
    # --- [E vs I] Energy/Presence ---
    {"q": "Q1. In the locker room before kickoff! What's your pre-game routine?", 
     "options": [
         "\"Let's go guys!!🔥\" Blasting music, clapping, and hyping up the squad to the max.", 
         "Quietly putting on headphones, visualizing the game, and locking in on my role."
     ], "type": "EI"},
    
    {"q": "Q2. We're on the attack! When you want the ball, what's your style?", 
     "options": [
         "\"Hey! Here! Pass me!!🙋\u200d♂️\" Waving my hands and shouting to grab the passer's attention.", 
         "Silently slipping into the open space and making eye contact to receive the ball."
     ], "type": "EI"},

    {"q": "Q3. You just scored a last-minute winner! What's your celebration?", 
     "options": [
         "Sprinting to the corner flag for a knee slide! Soaking in the crowd's roar (SIU!!).", 
         "A subtle fist pump, pointing at the teammate who assisted me, and going for a high-five."
     ], "type": "EI"},

    # --- [S vs N] Playstyle/Skill ---
    {"q": "Q4. You're facing a defender 1-on-1 on the wing! How do you beat them?", 
     "options": [
         "Kick and Rush! Knocking the ball past them and dominating with raw pace and physicality.", 
         "A nutmeg or a flip-flap! Using flashy and creative skills to destroy the defender's ankles."
     ], "type": "SN"},
    
    {"q": "Q5. A teammate makes a run. The pass you're looking to make is:", 
     "options": [
         "The safest, most clinical inside-foot ground pass right to their feet.", 
         "\"How did that get through?\" An artistic trivela (outside-of-the-boot) slicing through 3 defenders."
     ], "type": "SN"},

    {"q": "Q6. When training individually, what do you focus on the most?", 
     "options": [
         "Football is about stamina and basics! Focusing on core training, sprints, and shooting drills.", 
         "Football is art! Trying out new skill moves or acrobatic volleys I saw on YouTube."
     ], "type": "SN"},

    # --- [T vs F] Mentality/Decision ---
    {"q": "Q7. Oh no! Your team's ace is down after a reckless tackle! Your reaction?", 
     "options": [
         "Immediately approaching the ref, logically explaining the foul, and demanding a yellow card.", 
         "\"What are you doing?!🤬\" Losing my temper, running up to the opponent, and shoving them."
     ], "type": "TF"},
    
    {"q": "Q8. Halftime, and you're down 0-3. In this terrible atmosphere, what do you say?", 
     "options": [
         "\"Our defensive line is too high. Let's switch to a 4-4-2 and stay compact!\" (Tactical focus)", 
         "\"Don't give up! Show some pride! Run until your jersey is covered in dirt!!\" (Emotional focus)"
     ], "type": "TF"},

    {"q": "Q9. You just missed a perfect 1-on-1 sitter. What's going through your mind?", 
     "options": [
         "'My plant foot was too far and I leaned back. I'll aim for the far post next time.' (Analytical)", 
         "'Ah, this is crazy... I feel terrible for the team ㅠㅠ' Dropping to my knees in despair. (Emotional)"
     ], "type": "TF"},

    # --- [J vs P] Tactics/Pacing ---
    {"q": "Q10. If you were the manager, what would your 'perfect team' play like?", 
     "options": [
         "70% Possession! Suffocating the opponent with endless passing networks and a rigid formation.", 
         "10 seconds is enough! Sitting deep and destroying their backline with lightning-fast counter-attacks."
     ], "type": "JP"},
    
    {"q": "Q11. 85th minute, you are winning 1-0. For the last 5 minutes, your team should:", 
     "options": [
         "Keep possession, pass it around safely, and cleverly waste time near the corner flag.", 
         "They pushed their line up! Exploit the gap and go for the absolute kill (2nd goal)."
     ], "type": "JP"},

    {"q": "Q12. During the match, the manager's tactics aren't working at all!", 
     "options": [
         "Trust the system. Maintain our formation and strictly stick to the original game plan.", 
         "Ditch the plan! Trust our instincts on the pitch and play freely to create chaos."
     ], "type": "JP"}
]

results_map = {
    "ESTP": {
        "name": "킬리안 음바페 - 뒷공간의 파괴자 (The Speed Demon)",
        "traits": "에너지방출+피지컬+냉철효율+역습변수",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "필드 위에서 적극적으로 찬스를 요구하며(E), 압도적인 스피드(S)와 차갑고 치명적인 골 결정력(T)을 자랑합니다. 상대 라인이 조금이라도 올라온 틈을 타 치명적인 역습(P)을 꽂아 넣는 현대 축구 최고의 카운터 어택 스페셜리스트입니다."
    },
    "ESFP": {
        "name": "손흥민 - 폭발하는 양발의 스프린터 (The Passionate Sprinter)",
        "traits": "에너지방출+피지컬+열정투지+역습변수",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "동료들과 적극적으로 소통하고 분위기를 띄우며(E), 빠른 발과 양발 슈팅이라는 확실한 무기(S)를 가졌습니다. 팀을 향한 헌신과 열정(F)으로 뛰며, 측면에서 중앙으로 파고드는 다이내믹한 돌파(P)가 일품입니다."
    },
    "ISTP": {
        "name": "엘링 홀란드 - 침묵의 득점 사이보그 (The Cyborg)",
        "traits": "공간스캐너+피지컬+냉철효율+역습변수",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "경기 내내 조용히 고립된 척(I) 상대 수비수들 사이에 숨어 있습니다. 그러다 완벽한 피지컬(S)과 기계처럼 차가운 결정력(T)으로 순식간에 나타나 원터치로 골망을 찢어버립니다(P). 최소 터치, 최대 효율의 끝판왕입니다."
    },
    "ISFP": {
        "name": "은골로 캉테 - 지치지 않는 언성 히어로 (The Relentless Engine)",
        "traits": "공간스캐너+피지컬+열정투지+역습변수",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "경기장 밖에서는 세상 조용하지만(I), 필드 위에선 15km를 뛰는 체력과 태클(S)로 상대를 숨 막히게 합니다. 팀을 위해 헌신하는 심장을 가졌으며(F), 공을 탈취하자마자 매끄럽게 역습으로 전환하는(P) 최고의 박스 투 박스입니다."
    },
    "ENTJ": {
        "name": "케빈 데 브라위너 - 그라운드의 절대 사령관 (The Mastermind)",
        "traits": "에너지방출+창의성+냉철효율+점유통제",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "동료들의 움직임을 적극적으로 지시하고(E), 대지를 가르는 완벽한 궤적의 킬패스로 경기를 지배합니다(N). 철저한 계산과 넓은 시야로(T) 팀의 공격 템포와 점유율을 완벽하게 통제하는(J) 4-2-3-1 포메이션의 완벽한 10번(CAM)입니다."
    },
    "ESTJ": {
        "name": "크리스티아누 호날두 - 승부욕의 득점 기계 (The Ultimate Competitor)",
        "traits": "에너지방출+피지컬+냉철효율+점유통제",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "강력한 카리스마로 팀의 전방을 이끌고(E), 엄청난 훈련으로 다져진 피지컬과 점프력(S)을 자랑합니다. 오직 골을 향한 냉철한 효율성(T)을 추구하며, 그라운드 위에서 자신만의 확고한 루틴과 템포(J)를 주도합니다."
    },
    "INTJ": {
        "name": "토니 크로스 - 냉철한 템포 스나이퍼 (The German Sniper)",
        "traits": "공간스캐너+창의성+냉철효율+점유통제",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "불필요한 움직임 없이 조용히 공간을 확보하고(I), 창의적인 패스 길(N)을 봅니다. 어떤 압박 속에서도 감정 기복 없이 패스 성공률 99%를 유지하며(T), 후방에서부터 팀의 볼 점유와 경기 흐름을 완전히 지배합니다(J)."
    },
    "ISTJ": {
        "name": "버질 반 다이크 - 흔들리지 않는 통곡의 벽 (The Iron Wall)",
        "traits": "공간스캐너+피지컬+냉철효율+점유통제",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "절대 흥분하거나 큰 소리를 내지 않고 침착하게 수비 라인을 리드합니다(I). 완벽한 피지컬과 대인 방어 능력(S)을 바탕으로 차가운 머리로 태클 타이밍을 재며(T), 수비 진영에서부터 안정적인 빌드업(J)을 통제하는 최후의 보루입니다."
    },
    "INTP": {
        "name": "리오넬 메시 - 외계에서 온 축구의 신 (The Alien Genius)",
        "traits": "공간스캐너+창의성+냉철효율+역습변수",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "경기 중 대부분의 시간을 조용히 걸어 다니며 필드의 공간을 스캔합니다(I). 그러다 공을 잡는 순간, 중력의 법칙을 무시하는 드리블과 시야(N)로 기적을 만듭니다. 불필요한 움직임이 전혀 없는 극강의 전술적 효율(T)을 발휘하며 프리롤로 수비진을 파괴합니다(P)."
    },
    "ENFP": {
        "name": "호나우지뉴 - 그라운드의 마법사 (The Joy of Football)",
        "traits": "에너지방출+창의성+열정투지+역습변수",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "항상 치아를 드러내고 웃으며 관중들의 호응을 즐깁니다(E). 상상도 할 수 없는 노룩 패스와 플립플랩(N)으로 수비를 농락하며, 진정으로 축구를 사랑하는 마음(F)으로 경기장에 마법 같은 변수와 재미(P)를 불어넣습니다."
    },
    "ENTP": {
        "name": "네이마르 - 수비수를 농락하는 크랙 (The Trickster)",
        "traits": "에너지방출+창의성+냉철효율+역습변수",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "T": "감정에 휘둘리지 않고 극도의 효율과 기계적인 정확도로 플레이하는 전술적 톱니바퀴.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "화려한 쇼맨십으로 상대의 시선을 한 몸에 받으며(E), 정해진 전술보다는 예측 불가능한 개인기(N)로 승부합니다. 상대의 도발에 지능적으로 대처하고 도발하며(T), 끊임없이 그라운드에 변수를 창출하는(P) 악동 크랙입니다."
    },
    "INFP": {
        "name": "안드레스 이니에스타 - 팬텀 드리블의 창시자 (The Illusionist)",
        "traits": "공간스캐너+창의성+열정투지+역습변수",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "P": "라인을 내리고 웅크리다 상대의 빈틈이 보이면 치명적인 속도로 뒷공간을 파괴하는 카운터 어택."
        },
        "desc": "수줍음이 많고 과묵한 성격이지만(I), 좁은 공간에서 수비수들 사이를 유령처럼 빠져나가는 천재적인 탈압박(N) 능력을 지녔습니다. 거친 몸싸움 대신 부드럽고 섬세한 플레이(F)로 동료들에게 찬스를 물 흐르듯(P) 연결해 줍니다."
    },
    "ENFJ": {
        "name": "주드 벨링엄 - 차세대 리더, 골든 보이 (The Golden Boy)",
        "traits": "에너지방출+창의성+열정투지+점유통제",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "어린 나이에도 관중의 호응을 유도하는 압도적인 스타성과 리더십(E)을 갖췄습니다. 박스 투 박스로 전역을 누비는 창의적 센스(N)와 헌신적인 투지(F)로 무장하여, 팀을 체계적으로 승리로 이끄는(J) 완벽한 육각형 미드필더입니다."
    },
    "ESFJ": {
        "name": "토마스 뮐러 - 공간을 지배하는 연주자 (Raumdeuter)",
        "traits": "에너지방출+피지컬+열정투지+점유통제",
        "traits_desc": {
            "E": "끊임없이 공을 쫓아 활발히 움직이고, 동료를 콜하며, 관중의 환호와 필드의 중심에서 에너지를 뿜어내는 인싸형 플레이어.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "경기 내내 쉬지 않고 동료들에게 지시를 내리고 소통합니다(E). 화려한 발재간보다는 축구 지능과 기본기(S)에 충실하며, 팀을 위해 헌신하는 마음(F)으로 체계적인 전술(J) 속에서 기가 막히게 빈 공간을 찾아냅니다."
    },
    "INFJ": {
        "name": "지네딘 지단 - 우아한 마에스트로 (The Artistic Commander)",
        "traits": "공간스캐너+창의성+열정투지+점유통제",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "N": "번뜩이는 직감, 화려한 발재간, 남들이 보지 못하는 패스 길을 뚫어내는 그라운드의 아티스트.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "조용한 카리스마로 팀 전체의 무게를 잡아주는(I) 중원의 사령관입니다. 마르세유 턴 등 누구도 흉내 낼 수 없는 우아하고 창의적인 볼 터치(N)를 보여주며, 뜨거운 심장(F)으로 경기 흐름 전체를 지배하고 장악합니다(J)."
    },
    "ISFJ": {
        "name": "카를레스 푸욜 - 피 흘리는 심장, 위대한 캡틴 (The Braveheart)",
        "traits": "공간스캐너+피지컬+열정투지+점유통제",
        "traits_desc": {
            "I": "체력 소모 없이 조용히 필드를 걷고 관찰하며, 자신에게 공이 왔을 때 가장 확실하고 치명적인 플레이를 보여주는 침묵의 암살자.",
            "S": "압도적인 스피드, 체력, 탄탄한 기본기로 감독의 전술을 오차 없이 수행하는 클래식 플레이어.",
            "F": "뱃지에 대한 충성심, 팀을 위해 유니폼이 더러워지는 것을 두려워하지 않는 뜨거운 심장.",
            "J": "안정적인 볼 소유와 체계적인 빌드업으로 상대의 숨통을 서서히 조이는 지배자."
        },
        "desc": "말보다는 행동과 헌신으로(I) 팀원들의 귀감이 됩니다. 기교보다는 묵묵히 몸을 날리는 정석적인 수비와 피지컬(S)을 보여주며, 팀과 로고를 향한 무한한 애정(F)으로 단단한 수비 라인(J)을 사수하는 정신적 지주입니다."
    }
}

results_map_en = {
    "ESTP": {
        "name": "Kylian Mbappé - The Speed Demon",
        "traits": "Explosive Energy + Physicality + Cold Efficiency + Counter-Attack",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Actively demands the ball on the pitch (E), boasting overwhelming pace (S) and a cold-blooded, clinical finish (T). The ultimate counter-attacking specialist in modern football, ready to exploit the slightest high line with a devastating sprint (P)."
    },
    "ESFP": {
        "name": "HeunEeg-min Son - The Passionate Sprinter",
        "traits": "Explosive Energy + Physicality + Passion & Grit + Counter-Attack",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Constantly communicates and hypes up the squad (E), armed with explosive pace and a deadly two-footed strike (S). Plays with immense dedication and passion for the team (F), specializing in dynamic, game-changing runs cutting inside from the wing (P)."
    },
    "ISTP": {
        "name": "Erling Haaland - The Cyborg",
        "traits": "Space Scanner + Physicality + Cold Efficiency + Counter-Attack",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Quietly isolates himself among the defenders like a ghost throughout the game (I). Then, with perfect physicality (S) and cyborg-like clinical finishing (T), he suddenly appears to rip the net with a single touch (P). The absolute boss of minimal touches and maximum efficiency."
    },
    "ISFP": {
        "name": "N'Golo Kanté - The Relentless Engine",
        "traits": "Space Scanner + Physicality + Passion & Grit + Counter-Attack",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "The quietest guy off the pitch (I), but on the field, he suffocates opponents by covering 15km with relentless stamina and tackles (S). Possesses a heart dedicated entirely to the team (F), acting as the ultimate box-to-box engine who smoothly turns a steal into a lightning-fast counter (P)."
    },
    "ENTJ": {
        "name": "Kevin De Bruyne - The Mastermind",
        "traits": "Explosive Energy + Creative Flair + Cold Efficiency + Possession & Control",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Actively directs teammates' movements (E) and dominates the game with pitch-perfect killer passes (N). With absolute calculation and wide vision (T), he completely controls the team's attacking tempo and possession (J). The ultimate number 10 (CAM) in a 4-2-3-1 system."
    },
    "ESTJ": {
        "name": "Cristiano Ronaldo - The Ultimate Competitor",
        "traits": "Explosive Energy + Physicality + Cold Efficiency + Possession & Control",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Leads the frontline with powerful charisma (E) and boasts an unbelievable physique and leaping ability built through relentless training (S). Driven purely by a cold, clinical hunger for goals (T), he dictates his own firm routines and the game's tempo on the pitch (J)."
    },
    "INTJ": {
        "name": "Toni Kroos - The German Sniper",
        "traits": "Space Scanner + Creative Flair + Cold Efficiency + Possession & Control",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Secures space quietly without unnecessary movements (I) and sees creative passing lanes (N). Unfazed by any pressing, he maintains a 99% pass accuracy without emotional fluctuation (T), completely dictating the team's possession and the flow of the game from deep (J)."
    },
    "ISTJ": {
        "name": "Virgil van Dijk - The Iron Wall",
        "traits": "Space Scanner + Physicality + Cold Efficiency + Possession & Control",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Leads the defensive line with absolute composure, never raising his voice or losing his cool (I). Relying on flawless physicality and 1-on-1 defending (S), he times his tackles with a cold, calculating mind (T) and acts as the ultimate anchor controlling stable build-up from the back (J)."
    },
    "INTP": {
        "name": "Lionel Messi - The Alien Genius",
        "traits": "Space Scanner + Creative Flair + Cold Efficiency + Counter-Attack",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Spends most of the game quietly walking and scanning the spatial dynamics of the pitch (I). But the moment he touches the ball, he creates miracles with gravity-defying dribbles and vision (N). Demonstrating extreme tactical efficiency with zero wasted movements (T), he destroys defenses as the ultimate free-roaming playmaker (P)."
    },
    "ENFP": {
        "name": "Ronaldinho - The Joy of Football",
        "traits": "Explosive Energy + Creative Flair + Passion & Grit + Counter-Attack",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Always flashing a massive smile and feeding off the crowd's energy (E). He humiliates defenders with unimaginable no-look passes and flip-flaps (N), injecting magical unpredictability and pure fun (P) into the game with a heart that genuinely loves football (F)."
    },
    "ENTP": {
        "name": "Neymar Jr. - The Trickster",
        "traits": "Explosive Energy + Creative Flair + Cold Efficiency + Counter-Attack",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "T": "A tactical cog who plays with cold efficiency and mechanical precision, never swayed by emotions.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Thrives on the spotlight with flashy showmanship (E), relying on unpredictable, creative flair rather than rigid tactics (N). Intelligently handles and even invites opponent provocations (T), constantly creating chaos and magical variables on the pitch (P)."
    },
    "INFP": {
        "name": "Andrés Iniesta - The Illusionist",
        "traits": "Space Scanner + Creative Flair + Passion & Grit + Counter-Attack",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "P": "Sits deep, waits for the opponent's gap, and destroys the backline with lethal speed on the counter-attack."
        },
        "desc": "Shy and quiet by nature (I), but possesses the genius ability to glide through a sea of defenders like a ghost in tight spaces (N). Instead of rough physicality, he uses soft, delicate play (F) to link up chances for his teammates seamlessly like flowing water (P)."
    },
    "ENFJ": {
        "name": "Jude Bellingham - The Golden Boy",
        "traits": "Explosive Energy + Creative Flair + Passion & Grit + Possession & Control",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Boasts overwhelming star power and leadership that gets the crowd roaring, despite his young age (E). A perfect all-around midfielder armed with creative box-to-box vision (N) and relentless dedication (F), systematically driving the team toward victory (J)."
    },
    "ESFJ": {
        "name": "Thomas Müller - Raumdeuter (The Space Investigator)",
        "traits": "Explosive Energy + Physicality + Passion & Grit + Possession & Control",
        "traits_desc": {
            "E": "Constantly chasing the ball, calling out to teammates, and feeding off the crowd's energy as the center of attention.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Constantly shouting instructions and communicating with teammates non-stop (E). Rather than flashy skills, he relies on supreme football IQ and fundamentals (S). With a dedicated heart for the team (F), he brilliantly finds and exploits empty spaces within a systematic tactical setup (J)."
    },
    "INFJ": {
        "name": "Zinedine Zidane - The Artistic Commander",
        "traits": "Space Scanner + Creative Flair + Passion & Grit + Possession & Control",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "N": "A pitch artist with brilliant intuition, flashy footwork, and the ability to thread passes through impossible lanes.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "The midfield maestro who anchors the team with a quiet, undeniable charisma (I). Displays elegant, unparalleled touches like the Marseille roulette (N), and dominates the entire flow of the game (J) with a burning, passionate heart (F)."
    },
    "ISFJ": {
        "name": "Carles Puyol - The Braveheart",
        "traits": "Space Scanner + Physicality + Passion & Grit + Possession & Control",
        "traits_desc": {
            "I": "A silent assassin who quietly walks and scans the pitch to save energy, delivering the most lethal and decisive play when the ball arrives.",
            "S": "A classic player who executes the manager's tactics flawlessly with overwhelming speed, stamina, and solid fundamentals.",
            "F": "Absolute loyalty to the badge, a burning heart that isn't afraid to get the jersey dirty for the team.",
            "J": "A dictator of the game, slowly suffocating the opponent with stable possession and systematic build-up."
        },
        "desc": "Leads by example and sacrifice rather than words, becoming the ultimate role model for the squad (I). Showcases textbook defending and pure physicality over fancy tricks (S), guarding the defensive line like a fortress (J) with boundless love and passion for the badge (F)."
    }
}

# --- 4. 세션 상태 초기화 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    st.session_state.answer_history = []
    st.session_state.loading = False
    st.session_state.lang = None

# --- 5. 화면 렌더링 ---
# (1) 인트로 화면
if st.session_state.step == 0:
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    if os.path.exists("univ_bg.png"):
        st.image("univ_bg.png", use_container_width=True)
    
    st.markdown(
        """
        <div class='question-box'>
            <h1 style='color: #005088; margin-bottom: 10px;'>⚽ SIUFC Football Persona Test</h1>
            <p style='font-size: 17px; line-height: 1.6; color: #333;'>
                <b>"나는 화려한 그라운드의 마법사일까, 피도 눈물도 없는 득점 기계일까?"</b><br>
                <b>"Am I a magical playmaker, or a cold-blooded goal machine?"</b><br><br>
                단 12개의 질문으로 나의 플레이 스타일, 전술적 성향, 멘탈을 분석하여<br>내 안에 숨겨진 '월드클래스 축구선수 DNA'를 찾아드립니다. 🧬<br>
                <span style='font-size: 15px; color: #555;'>Through 12 quick questions analyzing your playstyle, tactical mindset, and mentality, we'll uncover your hidden 'World-Class Player DNA'.</span><br><br>
                16명의 레전드 플레이어 중 나와 완벽하게 똑같은 선수는 누구일까요?<br>
                지금 바로 그라운드에 입장하세요! 👀✨<br>
                <span style='font-size: 15px; color: #555;'>Which of the 16 legendary players matches you perfectly? Step onto the pitch and find out now!</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_ko, col_en = st.columns(2)
    with col_ko:
        if st.button("🚀 테스트 시작하기 (한국어)", key="start_btn_ko", use_container_width=True):
            st.session_state.lang = "ko"
            st.session_state.step = 1
            st.rerun()
    with col_en:
        if st.button("🚀 Start Test (English)", key="start_btn_en", use_container_width=True):
            st.session_state.lang = "en"
            st.session_state.step = 1
            st.rerun()
    
    st.markdown(
        "<p style='text-align: center; color: #aaa; font-size: 13px; margin-top: 10px;'>made by SIU FC woody </p>",
        unsafe_allow_html=True
    )

# (2) 질문 진행 화면
elif 1 <= st.session_state.step <= 12:
    q_idx = st.session_state.step - 1
    questions = questions_en if st.session_state.get("lang") == "en" else questions
    current_q = questions[q_idx]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.progress(st.session_state.step / 12)
    st.markdown(f"<p style='text-align: center; color: #667eea; font-weight: 600; font-size: 16px; margin: 15px 0;'>질문 {st.session_state.step} / 12</p>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='question-box'>
            <h3 style='color: #333; font-size: 17px; line-height: 1.6; margin: 0; font-weight: 600;'>{current_q['q']}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

    if st.button(f"A. {current_q['options'][0]}", key=f"opt1_{q_idx}"):
        st.session_state.scores[current_q['type'][0]] += 1
        st.session_state.answer_history.append((q_idx, 0, current_q['type'][0]))
        if st.session_state.step == 12:
            st.session_state.loading = True
        st.session_state.step += 1
        st.rerun()

    if st.button(f"B. {current_q['options'][1]}", key=f"opt2_{q_idx}"):
        st.session_state.scores[current_q['type'][1]] += 1
        st.session_state.answer_history.append((q_idx, 1, current_q['type'][1]))
        if st.session_state.step == 12:
            st.session_state.loading = True
        st.session_state.step += 1
        st.rerun()
    
    # 뒤로가기 버튼
    if st.session_state.step > 1:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⬅️ 이전 질문으로", key="back_btn"):
                # 마지막 답변 취소
                if st.session_state.answer_history:
                    last_answer = st.session_state.answer_history.pop()
                    st.session_state.scores[last_answer[2]] -= 1
                st.session_state.step -= 1
                st.rerun()

# (3) 로딩 화면
elif st.session_state.step == 13 and st.session_state.loading:
    # 통계 업데이트
    mbti_temp = ""
    mbti_temp += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    mbti_temp += "S" if st.session_state.scores["S"] >= st.session_state.scores["N"] else "N"
    mbti_temp += "T" if st.session_state.scores["T"] >= st.session_state.scores["F"] else "F"
    mbti_temp += "J" if st.session_state.scores["J"] >= st.session_state.scores["P"] else "P"
    stats = load_stats()
    stats["total"] += 1
    stats["types"][mbti_temp] = stats["types"].get(mbti_temp, 0) + 1
    save_stats(stats)
    count = stats["total"]
    st.markdown(
        f"""
        <div class='loading-container'>
            <div class='spinner'></div>
            <h2 style='color: #667eea; margin-top: 30px; font-size: 22px;'>🧬 {count}번째 DNA 분석 중...</h2>
            <p style='color: #666; margin-top: 10px; font-size: 16px;'>잠시만 기다려주세요</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    import time
    time.sleep(2)
    st.session_state.loading = False
    st.rerun()

# (4) 결과 화면
else:
    mbti = ""
    mbti += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    mbti += "S" if st.session_state.scores["S"] >= st.session_state.scores["N"] else "N"
    mbti += "T" if st.session_state.scores["T"] >= st.session_state.scores["F"] else "F"
    mbti += "J" if st.session_state.scores["J"] >= st.session_state.scores["P"] else "P"

    result = results_map[mbti]
    st.balloons()

    # 통계 로드
    stats = load_stats()
    total = stats["total"] if stats["total"] > 0 else 1
    my_count = stats["types"].get(mbti, 0)
    my_pct = round(my_count / total * 100, 1)

    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='question-box' style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <h2 style='margin: 0; font-size: 20px; font-weight: 700;'>🎉 당신의 유형은</h2>
            <h1 style='margin: 15px 0; font-size: 24px; font-weight: 800;'>{result['name']}</h1>
            <p style='font-size: 48px; font-weight: 800; margin: 10px 0; letter-spacing: 5px;'>{mbti}</p>
            <p style='font-size: 16px; margin: 8px 0; opacity: 0.95;'>전체 응시자 중 <b>{my_pct}%</b>가 같은 유형이에요!</p>
            <p style='font-size: 13px; margin: 4px 0; opacity: 0.75;'>지금까지 총 {total}명이 테스트했어요 🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    img_path = f"images/{mbti}.png"
    if os.path.exists(img_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img_path, use_container_width=True)

    st.markdown(
        f"""
        <div class='result-card'>
            <p style='font-size: 16px; line-height: 1.8; color: #333; margin: 0;'>💡 {result['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 성향 조합 해석
    if 'traits_desc' in result:
        icons = {"E": "📢", "I": "📡", "S": "💪", "N": "🪄", "T": "🧊", "F": "❤️‍🔥", "J": "♟️", "P": "🚀"}
        labels = {"E": "E (에너지 방출 / Energy)", 
    "I": "I (공간 스캐너 / Scanner)", 
    "S": "S (피지컬·기본기 / Physical)", 
    "N": "N (창의성·센스 / Flair)",
    "T": "T (냉철·효율 / Cold&Clinical)", 
    "F": "F (열정·투지 / Passion)", 
    "J": "J (점유·통제 / Control)", 
    "P": "P (역습·변수 / Counter)"}
        items_html = "".join([
            f"<div style='margin: 12px 0; padding: 12px 15px; background: #f8f9ff; border-radius: 12px; border-left: 4px solid #667eea;'>"
            f"<b style='color: #667eea; font-size: 15px;'>{icons.get(k, '')} {labels.get(k, k)}</b>"
            f"<p style='color: #333; font-size: 14px; margin: 6px 0 0 0; line-height: 1.6;'>{v}</p></div>"
            for k, v in result['traits_desc'].items()
        ])
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #764ba2;'>
                <h3 style='color: #764ba2; font-size: 18px; margin-bottom: 10px;'>🧬 나의 성향 조합 해석</h3>
                {items_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 인스타 버튼 (중앙)
    col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
    with col_i2:
        st.markdown(
            "<a href='https://www.instagram.com/siu__fc?igsh=MWt3cW80OWpzMGVlaw==' target='_blank'>"
            "<button style='width:100%; border-radius:25px; padding:18px 20px; "
            "background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); "
            "color:white; font-size:16px; font-weight:600; border:none; cursor:pointer;'>"
            "📸 SIU FC INS</button></a>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 다시 테스트 + 링크 복사
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 다시 테스트", key="retry"):
            st.session_state.step = 0
            st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            st.session_state.answer_history = []
            st.session_state.loading = False
            st.session_state.lang = None
            st.rerun()
    with col_b:
        share_url = "https://your-app-url.com"  # 실제 배포 URL로 변경
        if st.button("🔗 테스트 링크 복사"):
            st.code(share_url, language=None)
            st.success("링크를 복사해서 친구들과 공유하세요! 📤")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)