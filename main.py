from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="온라인 도서관 관리 시스템 API")

# 1. 데이터베이스 모델 
# 데이터 구조 정의
db = {
    "users": [],
    "books": [],
    "loans": []
}

# 2. 데이터 검증
# 유효성 검사 로직
class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class BookData(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int

# (POST, GET, DELETE)

# [POST] 회원가입
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def signup(data: UserSignup):
    db["users"].append(data.dict())
    return {"message": "User created successfully"}

# [POST] 로그인 및 인증 
@app.post("/auth/login", tags=["Auth"])
def login(login_info: dict):
    # 입력 파일의 오타 'usemame' 대응
    username = login_info.get("username") or login_info.get("usemame")
    password = login_info.get("password")
    
    for user in db["users"]:
        if user["username"] == username and user["password"] == password:
            # 간단한 Bearer 토큰 반환
            return {"access_token": f"secret-token-{username}", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# [POST] 도서 등록 
@app.post("/books", tags=["Books"])
def create_book(book: BookData, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_book = book.dict()
    new_book["id"] = len(db["books"]) + 1
    new_book["available"] = True
    db["books"].append(new_book)
    return new_book

# [GET] 도서 검색
@app.get("/books", tags=["Books"])
def search_books(category: Optional[str] = None, available: Optional[bool] = None):
    results = db["books"]
    if category:
        results = [b for b in results if b["category"] == category]
    if available is not None:
        results = [b for b in results if b["available"] == available]
    return results

# [DELETE] 도서 삭제 
@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    global db
    initial_count = len(db["books"])
    db["books"] = [b for b in db["books"] if b["id"] != book_id]
    
    if len(db["books"]) == initial_count:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} deleted successfully"}

# [POST] 도서 대출 처리
@app.post("/loans", tags=["Loans"])
def borrow_book(loan_data: dict, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 도서 상태를 대출 중
    for b in db["books"]:
        if b["id"] == loan_data.get("book_id"):
            b["available"] = False
            db["loans"].append(loan_data)
            return {"message": "Loan successful"}
    raise HTTPException(status_code=404, detail="Book not found")

# [GET] 내 대출 현황 조회
@app.get("/users/me/loans", tags=["Loans"])
def get_my_loans(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db["loans"]