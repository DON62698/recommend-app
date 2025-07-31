import streamlit as st
import pandas as pd
from db import init_db, add_record, get_all_records
from datetime import datetime

# 初始化資料庫
init_db()

st.title("👥 員工推薦紀錄系統")

st.header("📥 輸入推薦資料")

# 輸入表單（員工、方式、次數）
with st.form("recommend_form"):
    employee = st.selectbox("員工姓名", ["山田", "佐藤", "鈴木"])
    method = st.selectbox("推薦方式", ["APP下載", "LINE登入", "LINE會員下載APP"])
    count = st.number_input("推薦次數", min_value=1, max_value=50, value=1, step=1)

    submitted = st.form_submit_button("送出紀錄")

    if submitted:
        for _ in range(count):
            add_record(employee, method)
        st.success(f"✅ 已新增 {count} 筆推薦：{employee} → {method}")
        st.rerun()  # 🔄 強制刷新畫面

st.divider()
st.header("📊 今日推薦統計")

# 顯示今日統計
df = get_all_records()
if df is not None and not df.empty:
    today = datetime.today().strftime('%Y-%m-%d')
    df_today = df[df['date'] == today]
    result = df_today.groupby(["employee", "method"]).size().unstack(fill_value=0)
    st.dataframe(result)
else:
    st.info("今天尚無紀錄")

st.divider()
st.header("📈 累積推薦統計")

if df is not None and not df.empty:
    count_df = df.groupby(["employee", "method"]).size().unstack(fill_value=0)
    st.bar_chart(count_df)
    st.caption("顯示所有時間累積推薦次數")

