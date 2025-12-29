import streamlit as st

# --- 1. 視覺風格設定 (CSS Injection) ---
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

    /* 全局背景與字體 */
    .stApp {
        background-color: #F5F2E9;
        color: #2B2B2B;
        font-family: 'Lato', sans-serif;
    }
    
    /* 標題 - 復古襯線體 */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #2B2B2B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 自定義按鈕 - 硬陰影風格 */
    .stButton>button {
        background-color: #E3B505;
        color: #2B2B2B;
        border: 2px solid #2B2B2B;
        border-radius: 0px;
        box-shadow: 4px 4px 0px #2B2B2B;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #2B2B2B;
    }
    .stButton>button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #2B2B2B;
    }

    /* 資訊卡片風格 */
    .recipe-card {
        background-color: #FFFFFF;
        border: 2px solid #2B2B2B;
        padding: 20px;
        box-shadow: 6px 6px 0px #2B2B2B;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心邏輯演算法 ---
def generate_recipe(bean_origin, process, roast, target_vol, brewer):
    # 基礎參數預設
    ratio = 15.0
    temp = 90
    grind_rec = "中細研磨 (Medium-Fine)"
    
    # 根據豆子特性調整 (AI 模擬邏輯)
    # 淺焙 + 耶加雪菲 + 水洗 = 追求花香與酸質 -> 拉高水溫，拉開粉水比
    if "淺" in roast:
        temp += 3 # 淺焙需要高溫
        ratio = 16.0 # 拉開層次
        if "水洗" in process:
            temp += 1 # 水洗通常結構扎實，可再高溫一點
            grind_rec = "中細研磨 (約海鹽大小, 稍細)"
        elif "日曬" in process:
            grind_rec = "中等研磨 (避免過度萃取雜味)"

    # 計算粉量
    # 公式：目標液體量 / (Ratio - 吸收率) *粗略估算，這裡簡化為投入水重
    # 一般手沖：投入水重 = 粉重 * Ratio
    # 使用者輸入的是「目標沖煮量(飲用量)」還是「注入總水量」？
    # 假設使用者輸入的是「目標喝到的量」，粉吸水約 2倍粉重。
    # 這裡採用更通用的標準：以「注入總水量」為基準計算較精準。
    # 假設 input 是 Total Water Target (cc)
    
    coffee_dose = target_vol / ratio
    
    # 沖煮階段規劃 (4:6法變體或經典分段)
    steps = []
    
    # 1. 悶蒸 (Bloom)
    bloom_water = coffee_dose * 2.5
    steps.append({
        "phase": "悶蒸 (Bloom)",
        "time": "0:00 - 0:40",
        "action": f"注入 {bloom_water:.0f}cc 水",
        "desc": "由內向外快速繞圈，確保粉層完全濕潤。觀察表面氣泡釋放（排氣）。"
    })
    
    # 剩餘水量
    remaining_water = target_vol - bloom_water
    
    if brewer == "V60":
        # 兩段式注水 (保留酸質與甜感平衡)
        pour_1 = remaining_water * 0.6
        pour_2 = remaining_water * 0.4
        
        steps.append({
            "phase": "第一段注水 (酸質萃取)",
            "time": "0:40 - 1:30",
            "action": f"注入 {pour_1:.0f}cc (累計 {bloom_water + pour_1:.0f}cc)",
            "desc": "以大柔水繞圈，擾動粉層，帶出耶加雪菲明亮的花果香。"
        })
        steps.append({
            "phase": "第二段注水 (甜感維持)",
            "time": "1:30 - 2:15",
            "action": f"注入 {pour_2:.0f}cc (累計 {target_vol:.0f}cc)",
            "desc": "中心緩慢注水，減少擾動，避免後段雜味，增加口感厚度。"
        })
    else:
        # 蛋糕濾杯 (Kalita) 適合一刀流或三段
        steps.append({
            "phase": "中心注水",
            "time": "0:40 - 2:00",
            "action": f"緩慢注入剩餘 {remaining_water:.0f}cc",
            "desc": "保持水位高度一致，不要淹滿濾杯，利用蛋糕濾杯的浸泡特性增加甜度。"
        })

    return {
        "dose": coffee_dose,
        "ratio": ratio,
        "temp": temp,
        "grind": grind_rec,
        "steps": steps
    }

# --- 3. 介面佈局 ---
def main():
    st.set_page_config(page_title="L'Extract Coffee AI", page_icon="☕")
    local_css()

    st.title("L'EXTRACT")
    st.markdown("### PROFESSIONAL BREWING ASSISTANT")
    st.write("---")

    # 1. 使用者輸入區 (Sidebar 或 Top columns)
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.selectbox("Coffee Origin / 產區", ["衣索比亞 耶加雪菲", "肯亞 AA", "哥倫比亞", "巴拿馬 藝伎", "其他"])
        process = st.selectbox("Processing / 處理法", ["水洗 (Washed)", "日曬 (Natural)", "蜜處理 (Honey)", "特殊發酵"])
        roast = st.select_slider("Roast Level / 烘焙度", options=["極淺焙", "淺焙", "中淺焙", "中焙", "中深焙", "深焙"], value="淺焙")

    with col2:
        brewer = st.selectbox("Brewer / 濾杯", ["V60", "Kalita Wave (蛋糕濾杯)", "Origami (折紙濾杯)", "Chemex"])
        target_vol = st.number_input("Target Water (cc) / 目標注水量", min_value=150, max_value=1000, value=300, step=10)

    # 觸發按鈕
    if st.button("GENERATE RECIPE / 生成萃取方案"):
        # 計算
        result = generate_recipe(origin, process, roast, target_vol, brewer)
        
        # 顯示結果
        st.write("---")
        st.markdown("## BREWING PROFILE")
        
        # 數據概覽卡片
        st.markdown(f"""
        <div class="recipe-card">
            <div style="display: flex; justify-content: space-between; text-align: center;">
                <div>
                    <h3 style="margin:0;">{result['dose']:.1f}g</h3>
                    <small>COFFEE</small>
                </div>
                <div>
                    <h3 style="margin:0;">1:{result['ratio']:.0f}</h3>
                    <small>RATIO</small>
                </div>
                <div>
                    <h3 style="margin:0;">{result['temp']}°C</h3>
                    <small>TEMP</small>
                </div>
            </div>
            <hr style="border: 1px solid #ddd;">
            <p><strong>研磨度建議：</strong> {result['grind']}</p>
            <p><strong>風味目標：</strong> 針對 {origin} {process} 優化，強調明亮酸質與乾淨尾韻。</p>
        </div>
        """, unsafe_allow_html=True)

        # 步驟化流程
        st.markdown("### STEPS")
        for step in result['steps']:
            st.markdown(f"""
            <div style="border-left: 4px solid #E3B505; padding-left: 15px; margin-bottom: 20px;">
                <h4 style="margin: 0; font-family: 'Lato'; font-weight: 700;">{step['time']} | {step['phase']}</h4>
                <p style="font-size: 1.2em; font-weight: bold; margin: 5px 0;">{step['action']}</p>
                <p style="color: #666; font-style: italic;">{step['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
