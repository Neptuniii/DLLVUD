import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

client = MongoClient("mongodb://localhost:27017/")
db = client['web_app']
collection = db['data_analysis']

def load_data():
    data = list(collection.find())
    return pd.DataFrame(data)

st.title("Phân tích dữ liệu với MongoDB và Streamlit")

df = load_data()

st.subheader("Dữ liệu từ MongoDB")
if not df.empty:
    st.dataframe(df)

     # 1. Đếm số bài viết theo userId
    st.subheader("1. Số bài viết theo userId")
    user_counts = df['userId'].value_counts()
    st.write(user_counts)

    # Biểu đồ
    fig1, ax1 = plt.subplots()
    user_counts.plot(kind='bar', ax=ax1)
    ax1.set_title("Số bài viết theo userId")
    ax1.set_xlabel("userId")
    ax1.set_ylabel("Số lượng bài viết")
    st.pyplot(fig1)

    # 2. Thống kê tổng quan
    st.subheader("2. Thống kê tổng quan")
    total_posts = len(df)
    avg_title_length = df['title'].apply(len).mean()
    avg_body_length = df['body'].apply(len).mean()
    st.write(f"- Tổng số bài viết: {total_posts}")
    st.write(f"- Độ dài trung bình của tiêu đề: {avg_title_length:.2f} ký tự")
    st.write(f"- Độ dài trung bình của nội dung: {avg_body_length:.2f} ký tự")

    # 3. Bài viết dài nhất và ngắn nhất
    st.subheader("3. Bài viết dài nhất và ngắn nhất")
    longest_post = df.iloc[df['body'].apply(len).idxmax()]
    shortest_post = df.iloc[df['body'].apply(len).idxmin()]
    st.write("**Bài viết dài nhất:**")
    st.write(longest_post[['userId', 'title', 'body']])
    st.write("**Bài viết ngắn nhất:**")
    st.write(shortest_post[['userId', 'title', 'body']])

    # 4. Tần suất từ khóa xuất hiện trong tiêu đề
    st.subheader("4. Tần suất từ khóa trong tiêu đề")
    keyword = st.text_input("Nhập từ khóa để phân tích", "dolor")
    keyword_count = df['title'].str.contains(keyword, case=False).sum()
    st.write(f"Từ khóa '{keyword}' xuất hiện trong {keyword_count} tiêu đề.")

else:
    st.warning("Không có dữ liệu để hiển thị!")

