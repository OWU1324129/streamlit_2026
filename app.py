import streamlit as st
import datetime

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="誕生日プレゼント記録帳",
    page_icon="🎂",
    layout="centered"
)

# =========================
# CSSデザイン
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #FFF8FC;
}

.main-title {
    text-align: center;
    color: #FF4F8B;
    font-size: 42px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: #666;
    margin-bottom: 20px;
}

.record-card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.metric-box {
    background: white;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# セッション初期化
# =========================
if "gift_history" not in st.session_state:
    st.session_state.gift_history = []

# =========================
# タイトル
# =========================
st.markdown(
    "<div class='main-title'>🎂 Birthday Memory Book 🎁</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>誕生日プレゼントの思い出を記録しよう</div>",
    unsafe_allow_html=True
)

# =========================
# 入力フォーム
# =========================
with st.expander("➕ 新しい記録を追加する", expanded=True):

    with st.form("gift_form", clear_on_submit=True):

        st.subheader("👤 基本情報")

        col1, col2 = st.columns(2)

        with col1:
            friend_name = st.text_input(
                "友達の名前"
            )

            birthday = st.date_input(
                "友達の誕生日",
                value=datetime.date(2005, 4, 1)
            )

        with col2:
            celebration_date = st.date_input(
                "お祝いした日",
                value=datetime.date.today()
            )

        st.subheader("🎁 プレゼント情報")

        col3, col4 = st.columns(2)

        with col3:

            gift_category = st.selectbox(
                "プレゼントカテゴリ",
                [
                    "アクセサリー",
                    "コスメ",
                    "バッグ",
                    "財布",
                    "雑貨",
                    "食べ物",
                    "その他"
                ]
            )

            gift_item = st.text_input(
                "プレゼント名"
            )

        with col4:
            gift_price = st.number_input(
                "プレゼント金額",
                min_value=0,
                step=100
            )

        st.subheader("🍽️ お祝いしたお店")

        col5, col6 = st.columns(2)

        with col5:
            restaurant_name = st.text_input(
                "店名"
            )

            plate_price = st.number_input(
                "プレート代",
                min_value=0,
                step=100
            )

        with col6:
            food_total_price = st.number_input(
                "食事代",
                min_value=0,
                step=100
            )

        st.subheader("📸 思い出の写真")

        uploaded_file = st.file_uploader(
            "誕生日プレート写真",
            type=["jpg", "jpeg", "png"]
        )

        submit_btn = st.form_submit_button(
            "記録を保存する",
            use_container_width=True
        )

        

        if submit_btn:

            if not friend_name:
                st.error(
                    "友達の名前を入力してください。"
                )

            else:

                img_data = (
                    uploaded_file.getvalue()
                    if uploaded_file
                    else None
                )

                total_cost = (
                    gift_price
                    + plate_price
                    + food_total_price
                )

                new_record = {
                    "name": friend_name,
                    "birthday": birthday,
                    "celebration_date": celebration_date,
                    "gift_category": gift_category,
                    "gift": gift_item,
                    "price": gift_price,
                    "restaurant": restaurant_name,
                    "plate_price": plate_price,
                    "food_total_price": food_total_price,
                    "total_cost": total_cost,
                    "image": img_data
                }

                st.session_state.gift_history.append(
                    new_record
                )

                st.success(
                    f"{friend_name}さんの記録を保存しました！"
                )
            

# =========================
# 検索
# =========================
st.markdown("---")

search_word = st.text_input(
    "🔍 名前で検索"
)

if search_word:

    display_records = [
        r for r in st.session_state.gift_history
        if search_word.lower()
        in r["name"].lower()
    ]

else:
    display_records = st.session_state.gift_history

# =========================
# 記録一覧
# =========================
st.subheader("📚 思い出アルバム")

if not display_records:

    st.info(
        "まだ記録がありません。"
    )

else:

    for record in reversed(display_records):

        with st.container(border=True):

            st.markdown(
                f"## 🎂 {record['name']} さん"
            )

            col_img, col_info = st.columns(
                [1, 2]
            )

            with col_img:

                if record["image"]:

                    st.image(
                        record["image"],
                        use_container_width=True
                    )

                    st.caption(
                        f"{record['celebration_date']} の思い出"
                    )

                else:
                    st.write("📸 写真なし")

            with col_info:

                st.write(
                    f"🎂 誕生日：{record['birthday']}"
                )

                st.write(
                    f"📅 お祝い日：{record['celebration_date']}"
                )

                st.write(
                    f"🏷️ カテゴリ：{record['gift_category']}"
                )

                st.write(
                    f"🎁 プレゼント：{record['gift']}"
                )

                st.write(
                    f"💰 プレゼント代：{record['price']:,}円"
                )

                if record["restaurant"]:

                    st.write(
                        f"🍽️ お店：{record['restaurant']}"
                    )

                    st.write(
                        f"🍰 プレート代：{record['plate_price']:,}円"
                    )

                    st.write(
                        f"🍴 食事代：{record['food_total_price']:,}円"
                    )

                st.metric(
                    "今回のお祝い総額",
                    f"{record['total_cost']:,}円"
                )
