# 데이터베이스 스키마 설계 설명서

## 1. Users 테이블 (회원 관리)

### 요구사항 연관성
- 회원가입 시 필요한 모든 필수 정보를 저장
  - `email`: 이메일 (중복 확인 필요) - UNIQUE 제약조건 적용
  - `nickname`: 닉네임 (중복 확인 필요) - UNIQUE 제약조건 적용
  - `name`: 이름
  - `phone`: 전화번호
  - `password`: 비밀번호 (암호화 저장)
  - `role`: 회원 구분 ('COMPANY' / 'WORKSHOP')

### 역할별 추가 정보
- 기업 회원(`role`='COMPANY')
  - `company_name`: 기업명 저장
- 공방 사장님(`role`='WORKSHOP')
  - `workshop_name`: 공방명 저장

### 데이터 관리
- `created_at`: 가입일시 자동 기록
- `updated_at`: 정보 수정 시 자동 업데이트
- 회원정보 수정 기능을 위한 필드들 모두 수정 가능하도록 설계

## 2. Posts 테이블 (게시글 관리)

### 요구사항 연관성
- 공방 사장님만 작성 가능 → `user_id`로 작성자 정보 연결
- 게시글 기본 정보 저장
  - `title`: 게시글 제목
  - `content`: 본문 내용
  - `category`: 게시글 카테고리 (예: 사업개발)
  - `view_count`: 조회수 기록

### 데이터 관리
- `created_at`: 작성일시 기록
- `updated_at`: 수정일시 자동 업데이트
- 페이지네이션을 위한 `id` 기준 정렬 가능

## 3. Post_Images 테이블 (게시글 이미지)

### 요구사항 연관성
- 게시글당 여러 장의 이미지 첨부 가능 → 1:N 관계 설계
  - `post_id`: 연결된 게시글 ID (외래키)
  - `image_url`: 업로드된 이미지 경로

### 데이터 관리
- `created_at`: 이미지 업로드 시점 기록
- 게시글 삭제 시 관련 이미지도 자동 삭제되도록 CASCADE 설정 필요

## 4. Comments 테이블 (댓글 기능)

### 요구사항 연관성
- 회원(기업/공방)만 작성 가능 → `user_id`로 작성자 정보 연결
- 기업 회원의 경우 기업명 표시 → Users 테이블의 company_name 참조
- 댓글 정보 저장
  - `content`: 댓글 내용
  - `post_id`: 연결된 게시글 ID (외래키)

### 데이터 관리
- `created_at`: 작성일시 기록
- `updated_at`: 수정일시 자동 업데이트
- 게시글 삭제 시 관련 댓글도 자동 삭제되도록 CASCADE 설정 필요

## 5. Contact_Inquiries 테이블 (문의하기)

### 요구사항 연관성
- 두 가지 문의 경로 지원
  - `inquiry_type`: 'COMPANY' / 'WORKSHOP' 구분
- 문의 양식 정보 저장
  - `name`: 이름
  - `email`: 이메일
  - `phone`: 전화번호
  - `organization_name`: 기업명/공방명
  - `content`: 문의 내용
  - `preferred_contact`: 선호 연락 방법 ('EMAIL' / 'PHONE')

### 데이터 관리
- `created_at`: 문의 접수 시점 기록
- `user_id`: 로그인한 사용자의 문의 내역 관리를 위한 연결

## 테이블 간 관계도

1. Users(1) ↔ Posts(N)
   - 한 사용자가 여러 게시글 작성 가능
2. Posts(1) ↔ Post_Images(N)
   - 한 게시글에 여러 이미지 첨부 가능
3. Posts(1) ↔ Comments(N)
   - 한 게시글에 여러 댓글 작성 가능
4. Users(1) ↔ Comments(N)
   - 한 사용자가 여러 댓글 작성 가능
5. Users(1) ↔ Contact_Inquiries(N)
   - 한 사용자가 여러 문의 작성 가능

## 주요 제약조건

1. 사용자 식별자
   - `email`, `nickname` UNIQUE 제약조건
   - `role` CHECK 제약조건 ('COMPANY', 'WORKSHOP')

2. 필수 입력 필드
   - `NOT NULL` 제약조건 적용
   - 회원가입 필수 정보
   - 게시글 제목/내용
   - 댓글 내용
   - 문의하기 양식 필드

3. 외래키 관계
   - 데이터 정합성 보장
   - 연관 데이터 삭제 시 CASCADE 처리