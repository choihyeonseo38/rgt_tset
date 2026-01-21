# 📚 Online Library Management System API (Backend)

본 프로젝트는 **FastAPI**를 사용하여 구축된 도서관 관리 시스템의 백엔드 서버입니다. 
RESTful API 설계를 바탕으로 사용자 인증, 도서 리소스 관리, 대출 로직을 구현하였습니다.

---

##  주요 구현 내용 (Requirements)

### 1. API 엔드포인트 구현 (POST, GET, DELETE)
* **POST**: 회원가입(`/auth/signup`), 로그인(`/auth/login`), 도서 등록(`/books`), 대출 신청(`/loans`) 기능을 구현했습니다.
* **GET**: 전체/조건별 도서 검색(`/books`) 및 내 대출 현황 조회(`/users/me/loans`) 기능을 구현했습니다.
* **DELETE**: 관리자 권한을 이용한 도서 삭제(`/books/{book_id}`) 기능을 구현했습니다.

### 2. 데이터베이스 모델 (Database Model)
* **메모리 기반 저장소**: 별도의 외부 DB 설치 없이 Python 딕셔너리 구조(`db`)를 사용하여 데이터를 관리합니다.
* **데이터 구조**: `users`, `books`, `loans` 세 가지 테이블 구조를 모사하여 설계했습니다.

### 3. 인증 및 인가 시스템 (Authentication & Authorization)
* **인증(Auth)**: 로그인 시 사용자의 자격 증명을 확인하고 `Bearer` 타입의 액세스 토큰을 발급합니다.
* **인가(Permission)**: 도서 추가/삭제 및 대출과 같은 민감한 작업은 HTTP Header에 유효한 토큰이 포함되어야만 접근 가능하도록 제한했습니다.

### 4. 데이터 검증 (Data Validation)
* **Pydantic 활용**: `BaseModel`을 상속받은 `UserSignup`, `BookData` 클래스를 통해 입력 데이터의 유효성을 검사합니다.
* **무결성 보장**: 필수 필드 누락이나 잘못된 데이터 형식이 들어올 경우 서버에서 자동으로 에러(422)를 반환합니다.

### 5. 환경설정 및 실행 방법 (Setup)
* **환경**: Python 3.13+, FastAPI, Uvicorn
* **실행 명령어**:
  ```bash
  python -m uvicorn main:app --reload
