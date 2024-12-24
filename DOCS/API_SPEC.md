# API 명세서

## 1. 인증 관련 API

### 1.1 회원가입
**Endpoint**: `POST /api/signup/`

**Request Body**:
```json
{
    "email": "string",
    "password": "string",
    "password2": "string",
    "name": "string",
    "nickname": "string",
    "phone": "string",
    "role": "COMPANY | WORKSHOP",
    "company_name": "string (optional)",
    "workshop_name": "string (optional)"
}
```

**Response (201)**:
```json
{
    "email": "string",
    "name": "string",
    "nickname": "string",
    "phone": "string",
    "role": "string",
    "company_name": "string",
    "workshop_name": "string"
}
```

**Error Responses**:
- 400: 잘못된 요청 (유효성 검증 실패)

### 1.2 로그인
**Endpoint**: `POST /api/login/`

**Request Body**:
```json
{
    "email": "string",
    "password": "string"
}
```

**Response (200)**:
```json
{
    "access": "string",
    "refresh": "string",
    "user": {
        "email": "string",
        "name": "string",
        "nickname": "string",
        "phone": "string",
        "role": "string",
        "company_name": "string",
        "workshop_name": "string"
    }
}
```

**Error Responses**:
- 401: 인증 실패

### 1.3 토큰 재발급
**Endpoint**: `POST /api/token/refresh/`

**Request Body**:
```json
{
    "refresh": "string"
}
```

**Response (200)**:
```json
{
    "access": "string"
}
```

**Error Responses**:
- 401: 유효하지 않은 리프레시 토큰

## 2. 사용자 관련 API

### 2.1 프로필 조회
**Endpoint**: `GET /api/profile/`

**Headers**: 
```
Authorization: Bearer {access_token}
```

**Response (200)**:
```json
{
    "email": "string",
    "name": "string",
    "nickname": "string",
    "phone": "string",
    "role": "string",
    "company_name": "string",
    "workshop_name": "string"
}
```

**Error Responses**:
- 401: 인증되지 않은 요청

### 2.2 프로필 수정
**Endpoint**: `PATCH /api/profile/`

**Headers**: 
```
Authorization: Bearer {access_token}
```

**Request Body**:
```json
{
    "name": "string (optional)",
    "nickname": "string (optional)",
    "phone": "string (optional)",
    "company_name": "string (optional)",
    "workshop_name": "string (optional)"
}
```

**Response (200)**:
```json
{
    "email": "string",
    "name": "string",
    "nickname": "string",
    "phone": "string",
    "role": "string",
    "company_name": "string",
    "workshop_name": "string"
}
```

**Error Responses**:
- 400: 잘못된 요청 (유효성 검증 실패)
- 401: 인증되지 않은 요청

### 2.3 중복 확인 API

#### 2.3.1 이메일 중복 확인
**Endpoint**: `POST /api/check/email/`

**Request Body**:
```json
{
    "email": "string"
}
```

**Response (200)**:
```json
{
    "message": "사용 가능한 이메일입니다."
}
```

**Error Responses**:
- 400: 중복된 이메일

#### 2.3.2 닉네임 중복 확인
**Endpoint**: `POST /api/check/nickname/`

**Request Body**:
```json
{
    "nickname": "string"
}
```

**Response (200)**:
```json
{
    "message": "사용 가능한 닉네임입니다."
}
```

**Error Responses**:
- 400: 중복된 닉네임

### 2.4 회원 탈퇴
**Endpoint**: `DELETE /api/profile/`

**Headers**: 
```
Authorization: Bearer {access_token}
```

**Response (204)**:
No content

**Error Responses**:
- 401: 인증되지 않은 요청

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