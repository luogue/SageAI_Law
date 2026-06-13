"""测试管理员登录"""
import requests

url = "http://localhost:8016/admin/login"

# 测试表单格式
print("测试表单格式...")
data = {
    "username": "admin",
    "password": "a.144iLil123"
}
response = requests.post(url, data=data)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")

# 测试JSON格式
print("\n测试JSON格式...")
import json
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=data, headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")