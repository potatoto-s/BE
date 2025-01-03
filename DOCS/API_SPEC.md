# API 명세서

사용자, 인증 관련 API 명세는 다음 문서들을 참고해주세요:

- Swagger UI: `/schema/swagger-ui/`
- ReDoc: `/schema/redoc/`

## 로컬 개발 환경
- Swagger UI: `http://localhost:8000/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/schema/redoc/`

## API 인증
- 대부분의 API는 JWT 토큰 인증이 필요합니다
- 토큰은 로그인 API를 통해 발급받을 수 있습니다
- 인증이 필요한 API 호출 시 헤더에 다음과 같이 토큰을 포함해야 합니다:
- Authorization: Bearer {access_token}

## User 관련 API (Swagger 참조 어려울 시)

### 회원가입
**URL**: `/signup/`
**Method**: `POST`
**Request**:
```json
{
  "email": "string",
  "password": "string",
  "password2": "string",
  "name": "string",
  "nickname": "string",
  "phone": "string (형식: 010-1234-5678)",
  "role": "COMPANY | WORKSHOP",
  "company_name": "string (role이 COMPANY인 경우 필수)",
  "workshop_name": "string (role이 WORKSHOP인 경우 필수)"
}
```

**Response (201)**:
```json
{
  "id": "number",
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

### 로그인
**URL**: `/login/`
**Method**: `POST`
**Request**:
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
    "id": "number",
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

### 토큰 갱신
**URL**: `/token/refresh/`
**Method**: `POST`
**Request**:
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
- 401: 유효하지 않은 토큰

## 사용자 관련 API

### 프로필 조회
**URL**: `/profile/`
**Method**: `GET`
**Auth Required**: Yes
**Response (200)**:
```json
{
  "id": "number",
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
- 401: 인증되지 않은 사용자
- 403: 권한 없음

### 프로필 수정
**URL**: `/profile/`
**Method**: `PATCH`
**Auth Required**: Yes
**Request**:
```json
{
  "name": "string (optional)",
  "nickname": "string (optional)",
  "phone": "string (optional, 형식: 010-1234-5678)",
  "company_name": "string (optional, COMPANY 회원만 가능)",
  "workshop_name": "string (optional, WORKSHOP 회원만 가능)"
}
```

**Response (200)**:
```json
{
  "id": "number",
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
- 400: 잘못된 요청
- 401: 인증되지 않은 사용자
- 403: 권한 없음

### 회원 탈퇴
**URL**: `/profile/`
**Method**: `DELETE`
**Auth Required**: Yes
**Response (204)**: No Content
**Error Responses**:
- 401: 인증되지 않은 사용자
- 403: 권한 없음

### 이메일 중복 확인
**URL**: `/check/email/`
**Method**: `POST`
**Request**:
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

### 닉네임 중복 확인
**URL**: `/check/nickname/`
**Method**: `POST`
**Request**:
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

### 비밀번호 변경
**URL**: `/password/change/`
**Method**: `POST`
**Auth Required**: Yes
**Request**:
```json
{
  "current_password": "string",
  "new_password": "string",
  "new_password2": "string"
}
```

**Response (200)**:
```json
{
  "message": "비밀번호가 성공적으로 변경되었습니다."
}
```

**Error Responses**:
- 400: 잘못된 요청 (현재 비밀번호 불일치 또는 새 비밀번호 검증 실패)
- 401: 인증되지 않은 사용자

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
