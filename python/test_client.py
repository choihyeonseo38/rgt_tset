import requests

base_url = "http://localhost:8000"

# 1. 회원가입 데이터 및 요청
signup_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
}
response = requests.post(f"{base_url}/auth/signup", json=signup_data)

# 2. 로그인 및 토큰 획득
login_data = {"username": "john_doe", "password": "securepass123"}
auth_response = requests.post(f"{base_url}/auth/login", json=login_data)
token = auth_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. 도서 등록 데이터 (admin_headers는 headers와 동일하게 설정 가능)
book_data = {
    "title": "Python Programming",
    "author": "John Smith",
    "isbn": "978-0123456789",
    "category": "Programming",
    "total_copies": 5
}
# 이미지에는 admin_headers가 별도 정의되어 있지 않으므로 headers를 사용하거나 새로 정의해야 합니다.
admin_headers = headers 
requests.post(f"{base_url}/books", json=book_data, headers=admin_headers)

# 4. 도서 검색
search_response = requests.get(f"{base_url}/books?category=Programming&available=true")

# 5. 도서 대출
borrow_data = {"book_id": 1, "user_id": 1}
requests.post(f"{base_url}/loans", json=borrow_data, headers=headers)

# 6. 내 대출 현황 조회
loans_response = requests.get(f"{base_url}/users/me/loans", headers=headers)

# 결과 확인을 위한 프린트 추가 (선택 사항)
print("Signup Response:", response.status_code)
print("Login Response:", auth_response.json())
print("Loans:", loans_response.json())
