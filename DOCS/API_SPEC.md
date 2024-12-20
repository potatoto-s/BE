# API 명세서

## 1. 인증 관련 API
## API 명세서

## 회원가입 (POST /api/users/signup/)

**Request Body**
```json
{
  "email": "string (필수)",
  "password": "string (필수)",
  "confirm_password": "string (필수)",
  "nickname": "string (필수, 2~10자)",
  "district": "string (필수)",
  "neighborhood": "string (필수)",
  "role": "string (필수, 'company' 또는 'workshop')",
  "company_name": "string (role이 'company'일 때 필수)",
  "workshop_name": "string (role이 'workshop'일 때 필수)"
}
```

**Response (201 Created)**
```json
{
  "message": "회원가입이 완료되었습니다. 이메일로 발송된 인증 코드를 입력해주세요.",
  "user_id": "integer"
}
```

## 이메일 인증 (POST /api/users/email-verification/)

**Request Body**
```json
{
  "user_id": "integer (필수)",
  "code": "string (필수, 6자리)"
}
```

**Response (200 OK)**
```json
{
  "message": "이메일이 성공적으로 인증되었습니다."
}
```

## 로그인 (POST /api/users/login/)

**Request Body**
```json
{
  "email": "string (필수)",
  "password": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "access": "string",
  "refresh": "string",
  "user": {
    "email": "string",
    "nickname": "string",
    "profilePhoto": "string",
    "district": "string",
    "neighborhood": "string",
    "bio": "string",
    "role": "string",
    "company_name": "string",
    "workshop_name": "string"
  }
}
```

## 로그아웃 (POST /api/users/logout/)

**Request Body**
```json
{
  "refresh_token": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "message": "로그아웃되었습니다."
}
```

## 사용자 정보 조회 (GET /api/users/user/)

**Response (200 OK)**
```json
{
  "email": "string",
  "nickname": "string",
  "profilePhoto": "string",
  "district": "string",
  "neighborhood": "string",
  "bio": "string",
  "role": "string",
  "company_name": "string",
  "workshop_name": "string"
}
```

## 사용자 정보 수정 (PATCH /api/users/user/)

**Request Body**
```json
{
  "nickname": "string (선택)",
  "profilePhoto": "file (선택)",
  "district": "string (선택)",
  "neighborhood": "string (선택)",
  "bio": "string (선택)",
  "company_name": "string (선택)",
  "workshop_name": "string (선택)"
}
```

**Response (200 OK)**
```json
{
  "email": "string",
  "nickname": "string",
  "profilePhoto": "string",
  "district": "string",
  "neighborhood": "string",
  "bio": "string",
  "role": "string",
  "company_name": "string",
  "workshop_name": "string"
}
```

## 회원 탈퇴 (DELETE /api/users/user/delete/)

**Response (204 No Content)**

## 비밀번호 변경 (POST /api/users/password-change/)

**Request Body**
```json
{
  "current_password": "string (필수)",
  "new_password": "string (필수)",
  "new_password_confirm": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "message": "비밀번호가 성공적으로 변경되었습니다."
}
```

## 비밀번호 재설정 (POST /api/users/password-reset/)

**Request Body**
```json
{
  "email": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "message": "임시 비밀번호가 이메일로 발송되었습니다."
}
```

## 이메일 중복 확인 (POST /api/users/email-check/)

**Request Body**
```json
{
  "email": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "available": "boolean"
}
```

## 닉네임 중복 확인 (POST /api/users/nickname-check/)

**Request Body**
```json
{
  "nickname": "string (필수)"
}
```

**Response (200 OK)**
```json
{
  "available": "boolean"
}
```

## 공통 에러 응답

**400 Bad Request**
```json
{
  "error": "string"
}
```

**401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
```json
{
  "error": "string"
}
```

## 2. 사용자 관련 API

### 2.1 프로필 조회
- **Endpoint**: `GET /api/users/profile`
- **Headers**: Authorization: Bearer {token}
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "email": "string",
        "nickname": "string",
        "name": "string",
        "phone": "string",
        "role": "string",
        "companyName": "string?",
        "workshopName": "string?"
    }
}
```

### 2.2 프로필 수정
- **Endpoint**: `PATCH /api/users/profile`
- **Headers**: Authorization: Bearer {token}
- **Request Body**:
```json
{
    "nickname": "string?",
    "name": "string?",
    "phone": "string?",
    "companyName": "string?",
    "workshopName": "string?"
}
```
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "nickname": "string",
        "name": "string",
        "phone": "string"
    }
}
```

## 3. 게시글 관련 API

## API 명세서

## 게시글 목록 조회 (GET /api/posts/)

**Query Parameters**
- `page`: (선택) 페이지 번호 (기본값: 1)
- `limit`: (선택) 페이지당 항목 수 (기본값: 10, 최대: 50)
- `category`: (선택) 게시글 카테고리 필터링
- `search`: (선택) 검색어

**Response (200 OK)**
```json
{
  "data": [
    {
      "id": "integer",
      "title": "string",
      "category": "string",
      "view_count": "integer",
      "like_count": "integer",
      "comment_count": "integer",
      "author": {
        "id": "integer",
        "nickname": "string",
        "workshop_name": "string"
      },
      "created_at": "datetime",
      "is_deleted": "boolean"
    }
  ],
  "pagination": {
    "total_pages": "integer",
    "current_page": "integer",
    "total_count": "integer",
    "has_next": "boolean",
    "has_previous": "boolean",
    "limit": "integer"
  }
}
```

## 게시글 생성 (POST /api/posts/create/)

**Request Body**
```json
{
  "title": "string (필수)",
  "content": "string (필수, 최소 10자)",
  "category": "string (필수)",
  "images": "file[] (선택)"
}
```

**Response (201 Created)**
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "category": "string",
  "view_count": "integer",
  "like_count": "integer",
  "comment_count": "integer",
  "author": {
    "id": "integer",
    "nickname": "string",
    "workshop_name": "string"
  },
  "images": [
    {
      "id": "integer",
      "image_url": "string",
      "created_at": "datetime"
    }
  ],
  "is_liked": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 게시글 상세 조회 (GET /api/posts/{post_id}/)

**Response (200 OK)**
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "category": "string",
  "view_count": "integer",
  "like_count": "integer",
  "comment_count": "integer",
  "author": {
    "id": "integer",
    "nickname": "string",
    "workshop_name": "string"
  },
  "images": [
    {
      "id": "integer",
      "image_url": "string",
      "created_at": "datetime"
    }
  ],
  "is_liked": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 게시글 수정 (PATCH /api/posts/{post_id}/update/)

**Request Body**
```json
{
  "title": "string (선택)",
  "content": "string (선택)",
  "category": "string (선택)",
  "add_images": "file[] (선택)",
  "remove_image_ids": "integer[] (선택)"
}
```

**Response (200 OK)**
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "category": "string",
  "view_count": "integer",
  "like_count": "integer",
  "comment_count": "integer",
  "author": {
    "id": "integer",
    "nickname": "string",
    "workshop_name": "string"
  },
  "images": [
    {
      "id": "integer",
      "image_url": "string",
      "created_at": "datetime"
    }
  ],
  "is_liked": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 게시글 삭제 (DELETE /api/posts/{post_id}/delete/)

**Response (204 No Content)**

## 게시글 좋아요 토글 (POST /api/posts/{post_id}/like/)

**Response (200 OK)**
```json
{
  "is_liked": "boolean"
}
```

## 공통 에러 응답

**400 Bad Request**
```json
{
  "detail": "string"
}
```

**401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**
```json
{
  "detail": "Not found."
}
```


## 4.문의하기 관련 API

## API 명세서

## 문의하기 (POST /api/contact/)

**Request Body**
```json
{
  "name": "string (필수)",
  "email": "string (필수, 이메일 형식)",
  "phone": "string (필수, 최대 20자)",
  "message": "string (필수)",
  "company_name": "string (선택, 최대 100자)",
  "prefered_reply": "string (필수, 'email' 또는 'phone')"
}
```

**Response (201 Created)**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string",
  "company_name": "string",
  "prefered_reply": "string",
  "created_at": "datetime"
}
```

## 문의 내역 조회 (GET /api/contact/{inquiry_id}/)

**Response (200 OK)**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string",
  "company_name": "string",
  "prefered_reply": "string",
  "created_at": "datetime"
}
```

## 문의 내역 수정 (PATCH /api/contact/{inquiry_id}/)

**Request Body**
```json
{
  "name": "string (선택)",
  "email": "string (선택)",
  "phone": "string (선택)",
  "message": "string (선택)",
  "company_name": "string (선택)",
  "prefered_reply": "string (선택)"
}
```

**Response (200 OK)**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string",
  "company_name": "string",
  "prefered_reply": "string",
  "created_at": "datetime"
}
```

## 공통 에러 응답

**400 Bad Request**
```json
{
  "error": {
    "name": ["이 필드는 필수 항목입니다."],
    "email": ["유효한 이메일 주소를 입력하세요."],
    "prefered_reply": ["선호하는 답변 방식은 'email' 또는 'phone'이어야 합니다."]
  }
}
```

**404 Not Found**
```json
{
  "detail": "Not found."
}
```

**500 Internal Server Error**
```json
{
  "detail": "이메일 전송에 실패했습니다."
}
```