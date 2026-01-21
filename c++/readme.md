# Smart Pointer 기반 로그 파일 관리 프로그램

C++ 스마트 포인터를 활용하여 다중 로그 파일을 관리하는 LogFileManager 구현 프로젝트입니다.

## 설치 환경 및 빌드 정보 
Windows 11환경에서 Visual Studio Code를 사용하여 개발 및 테스트되었습니다.

- **OS**: Windows 11 (64-bit)
- **IDE**: Visual Studio Code (VS Code)
  - 필수 확장: `C/C++ Extension Pack` (Microsoft)
- **Compiler**: MinGW-w64 (g++ 15.2.0)
  - C++ 표준: C++17
- **Terminal**: Windows PowerShell (VS Code 내장 터미널)
- **Build Tool**: g++ (GNU Compiler Collection)

### 1. 개요
각기 다른 목적(에러, 디버그, 정보 등)의 로그 파일을 효율적으로 관리하고, 타임스탬프를 포함한 로그 기록 및 읽기 기능을 제공합니다. 리소스 관리의 안전성을 위해 `std::unique_ptr`를 사용한 것이 핵심입니다.

### 2. 주요 설계 및 구현 내용
- **스마트 포인터 활용**: `std::unique_ptr<std::ofstream>`을 사용하여 파일 핸들을 관리합니다. 이를 통해 수동으로 메모리를 해제할 필요 없이 자원 누수를 방지했습니다.
- **소유권 및 복사 제한**: 파일 리소스의 유일성을 보장하기 위해 복사 생성자와 복사 대입 연산자를 `delete` 처리했습니다.
- **데이터 구조**: `std::map`을 사용하여 파일 이름을 키값으로 관리하며, 여러 개의 로그 파일 핸들을 동시에 유지하고 빠르게 접근할 수 있도록 구성했습니다.
- **시간 정보 자동화**: `std::strftime`을 사용하여 로그 기록 시 `[YYYY-MM-DD HH:MM:SS]` 포맷의 타임스탬프가 자동으로 삽입되도록 구현했습니다.

### 3. 핵심 함수 구성
- `openLogFile`: 파일명을 확인하여 맵에 등록하고 `append` 모드로 파일을 오픈합니다.
- `writeLog`: 해당 파일 핸들을 찾아 메시지를 타임스탬프와 함께 기록합니다.
- `readLogs`: 파일의 전체 내용을 `std::vector<std::string>` 형태로 반환하여 로그 분석을 용이하게 합니다.
- `closeLogFile`: 명시적으로 파일을 닫고 관리 목록에서 삭제하여 자원을 반환합니다.

### 4. 실행 (Output)
```text
// error.log 파일 내용
[2025-09-04 14:30:15] Database connection failed

// debug.log 파일 내용
[2025-09-04 14:30:16] User login attempt

// info.log 파일 내용
[2025-09-04 14:30:17] Server started successfully

// readLogs 반환값
errorLogs[0] = "[2025-09-04 14:30:15] Database connection failed"




