import streamlit as st
import pandas as pd
from db import init_data, add_record, get_all_records
from datetime import datetime

# 初始化資料
init_data()

st.title("👥 員工推薦紀錄系統（進階版）")

# ====== 側邊欄：設定每月目標 ======
st.sidebar.header("🎯 每月目標設定")
month_target = st.sidebar.number_input("請輸入本月目標（件數）", min_value=10, value=150, step=10)

# ====== 表單：輸入推薦紀錄 ======
st.header("📥 輸入推薦資料")
with st.form("recommend_form"):
    employee = st.selectbox("員工姓名", ["山田", "佐藤", "鈴木"])
    method = st.selectbox("推薦方式", ["APP下載", "LINE登入", "LINE會員下載APP"])
    count = st.number_input("推薦次數", min_value=1, max_value=50, value=1, step=1)
    selected_date = st.date_input("推薦日期", value=datetime.today())

    submitted = st.form_submit_button("送出紀錄")
    if submitted:
        add_record(employee, method, count, selected_date.strftime('%Y-%m-%d'))
        st.success(f"✅ 已新增 {count} 筆推薦：{employee} → {method}（日期：{selected_date.strftime('%Y-%m-%d')}）")
        st.rerun()


# ====== 讀取所有紀錄 ======
df = get_all_records()

if not df.empty:
    # 確保 date 是 datetime 格式
    df['date'] = pd.to_datetime(df['date'])

    # ====== 每日統計 ======
    st.divider()
    st.header("📊 每日推薦統計")
    daily_summary = df.groupby(['date', 'method']).size().unstack(fill_value=0)
    st.dataframe(daily_summary)

    # ====== 每月累計與達成率 ======
    st.divider()
    st.header("🎯 每月進度追蹤")

    this_month = datetime.today().strftime('%Y-%m')
    df_this_month = df[df['date'].dt.strftime('%Y-%m') == this_month]
    month_total = len(df_this_month)  # 本月總數
    progress = min(int((month_total / month_target) * 100), 100)

    st.metric("本月累計推薦", f"{month_total} 件")
    st.metric("目標", f"{month_target} 件")
    st.progress(progress / 100)
    st.write(f"目前達成率：**{progress}%**")

else:
    st.info("尚無紀錄")
