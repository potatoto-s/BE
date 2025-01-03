# API 명세서

## 1. 인증 관련 API

### 1.1 회원가입
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
```json
{
    "email": "string",
    "password": "string",
    "passwordConfirm": "string",
    "nickname": "string",
    "name": "string",
    "phone": "string",
    "role": "COMPANY | WORKSHOP",
    "companyName": "string (optional)",
    "workshopName": "string (optional)"
}
```
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "email": "string",
        "nickname": "string",
        "name": "string",
        "role": "string"
    }
}
```
- **Error Responses**:
  - 400: 잘못된 요청 (유효성 검증 실패)
  - 409: 이메일 또는 닉네임 중복

### 1.2 로그인
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
```json
{
    "email": "string",
    "password": "string"
}
```
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "accessToken": "string",
        "user": {
            "id": "number",
            "email": "string",
            "nickname": "string",
            "role": "string"
        }
    }
}
```
- **Error Responses**:
  - 401: 인증 실패

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

### 3.1 게시글 작성
- **Endpoint**: `POST /api/posts`
- **Headers**: Authorization: Bearer {token}
- **Request Body** (multipart/form-data):
```json
{
    "title": "string",
    "content": "string",
    "category": "string",
    "images": "File[]"
}
```
- **Response (201)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "title": "string",
        "content": "string",
        "category": "string",
        "imageUrls": "string[]",
        "createdAt": "datetime"
    }
}
```
- **Error Responses**:
  - 401: 권한 없음 (비로그인 또는 공방 회원이 아닌 경우)

### 3.2 게시글 목록 조회
- **Endpoint**: `GET /api/posts`
- **Query Parameters**:
  - page: number (default: 1)
  - limit: number (default: 10)
  - category: string (optional)
  - search: string (optional)
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "posts": [{
            "id": "number",
            "title": "string",
            "content": "string",
            "category": "string",
            "viewCount": "number",
            "imageUrls": "string[]",
            "createdAt": "datetime",
            "author": {
                "id": "number",
                "nickname": "string",
                "role": "string"
            }
        }],
        "totalPages": "number",
        "currentPage": "number"
    }
}
```

### 3.3 게시글 상세 조회
- **Endpoint**: `GET /api/posts/{postId}`
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "title": "string",
        "content": "string",
        "category": "string",
        "viewCount": "number",
        "imageUrls": "string[]",
        "createdAt": "datetime",
        "author": {
            "id": "number",
            "nickname": "string",
            "role": "string"
        },
        "comments": [{
            "id": "number",
            "content": "string",
            "createdAt": "datetime",
            "author": {
                "id": "number",
                "nickname": "string",
                "role": "string",
                "companyName": "string?"
            }
        }]
    }
}
```

### 3.4 게시글 수정
- **Endpoint**: `PATCH /api/posts/{postId}`
- **Headers**: Authorization: Bearer {token}
- **Request Body**:
```json
{
    "title": "string?",
    "content": "string?",
    "category": "string?",
    "addImages": "File[]?",
    "removeImageIds": "number[]?"
}
```
- **Response (200)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "title": "string",
        "content": "string",
        "category": "string",
        "imageUrls": "string[]"
    }
}
```

### 3.5 게시글 삭제
- **Endpoint**: `DELETE /api/posts/{postId}`
- **Headers**: Authorization: Bearer {token}
- **Response (204)**

## 4. 댓글 관련 API

### 4.1 댓글 작성
- **Endpoint**: `POST /api/posts/{postId}/comments`
- **Headers**: Authorization: Bearer {token}
- **Request Body**:
```json
{
    "content": "string"
}
```
- **Response (201)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "content": "string",
        "createdAt": "datetime",
        "author": {
            "id": "number",
            "nickname": "string",
            "role": "string",
            "companyName": "string?"
        }
    }
}
```

### 4.2 댓글 삭제
- **Endpoint**: `DELETE /api/comments/{commentId}`
- **Headers**: Authorization: Bearer {token}
- **Response (204)**

## 5. 문의하기 API

### 5.1 문의하기
- **Endpoint**: `POST /api/contact`
- **Headers**: Authorization: Bearer {token}
- **Request Body**:
```json
{
    "name": "string",
    "email": "string",
    "phone": "string",
    "organizationName": "string",
    "content": "string",
    "preferredContact": "EMAIL | PHONE",
    "inquiryType": "COMPANY | WORKSHOP"
}
```
- **Response (201)**:
```json
{
    "status": "success",
    "data": {
        "id": "number",
        "message": "문의가 성공적으로 접수되었습니다."
    }
}
```
- **Error Responses**:
  - 400: 잘못된 요청 (유효성 검증 실패)
  - 500: 이메일 발송 실패