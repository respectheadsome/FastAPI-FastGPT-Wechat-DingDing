import streamlit as st
import requests
from datetime import datetime

# 设置 API URL
api_url = "YOUR_API URL"

# 页面标题
st.title("会话数据管理")

# 日期选择器
query_type = st.radio("请选择操作类型", ("查询", "删除"))
date_format = st.selectbox("请选择日期格式", ("YYYY-MM-DD", "YYYY-MM", "MM-DD", "YYYY", "MM", "DD"))

if date_format == "YYYY-MM-DD":
    date_input = st.date_input("选择日期", datetime.now()).strftime("%Y-%m-%d")
elif date_format == "YYYY-MM":
    year = st.number_input("请输入年份", min_value=2000, max_value=datetime.now().year, value=datetime.now().year)
    month = st.number_input("请输入月份", min_value=1, max_value=12, value=datetime.now().month)
    date_input = f"{year}-{month:02d}"
elif date_format == "MM-DD":
    month = st.number_input("请输入月份", min_value=1, max_value=12, value=datetime.now().month)
    day = st.number_input("请输入日期", min_value=1, max_value=31, value=datetime.now().day)
    date_input = f"{month:02d}-{day:02d}"
elif date_format == "YYYY":
    year = st.number_input("请输入年份", min_value=2000, max_value=datetime.now().year, value=datetime.now().year)
    date_input = f"{year}"
elif date_format == "MM":
    month = st.number_input("请输入月份", min_value=1, max_value=12, value=datetime.now().month)
    date_input = f"{month:02d}"
elif date_format == "DD":
    day = st.number_input("请输入日期", min_value=1, max_value=31, value=datetime.now().day)
    date_input = f"{day:02d}"

# 操作按钮
if query_type == "查询":
    if st.button("查询"):
        query_url = f"{api_url}/?date={date_input}"
        try:
            response = requests.get(query_url)
            if response.status_code == 200:
                conversations = response.json()
                if conversations:
                    st.write(f"查询结果：共找到 {len(conversations)} 条会话数据")
                    for convo in conversations:
                        st.write(f"日期: {convo['year']}-{convo['month']}-{convo['day']}")
                        st.write(f"消息: {convo['message']}")
                        st.write("---")
                else:
                    st.write("没有找到符合条件的会话数据。")
            else:
                st.write(f"查询失败，状态码: {response.status_code}")
                st.write(f"错误信息: {response.text}")
        except requests.exceptions.RequestException as e:
            st.write("请求出错，请检查网络连接或联系管理员。")

elif query_type == "删除":
    if st.button("删除"):
        delete_url = f"{api_url}/?date={date_input}"
        try:
            response = requests.delete(delete_url)
            if response.status_code == 200:
                st.write(f"成功删除了日期为 {date_input} 的会话数据。")
            elif response.status_code == 404:
                st.write("未找到符合条件的会话数据，无法删除。")
            else:
                st.write(f"删除失败，状态码: {response.status_code}")
                st.write(f"错误信息: {response.text}")
        except requests.exceptions.RequestException as e:
            st.write("请求出错，请检查网络连接或联系管理员。")

# 手动页面刷新
if st.button("刷新页面"):
    st.experimental_set_query_params()  # 触发页面重新加载
