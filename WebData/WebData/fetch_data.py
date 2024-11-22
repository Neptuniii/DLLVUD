import requests 
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['web_app']
collection = db['data_analysis']

# Hàm thu thập dữ liệu từ API
def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"  # API giả lập
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Không thể thu thập dữ liệu!")
        return None

# Lưu dữ liệu vào MongoDB
data = fetch_data()
if data:
    collection.insert_many(data)
    print("Dữ liệu đã được lưu vào MongoDB!")
else:
    print("Không có dữ liệu để lưu!")
