# 브랜치 규칙

## 브랜치 명명 규칙
`<type>/<description>`

## 브랜치 유형
- feature: 새로운 기능
- bugfix: 버그 수정
- hotfix: 긴급 수정
- refactor: 리팩토링
- docs: 문서 작업
- style: 코드 포맷팅
- test: 테스트 코드

## 브랜치 이름 예시
```text
feature/유저 인증 구현
bugfix/데이터베이스 연결 픽스
hotfix/보안 취약점
refactor/쿼리 최적화
docs/API문서 업데이트
style/새 린트규칙 적용
test/유저 서비스 테스트
```

# 코딩 규칙

## 개발 환경
- Python: 3.8 이상
- 패키지 관리: Poetry

## Lint 설정

### pyproject.toml
[tool.poetry]
name = "your-project-name"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]
black = "^24.1.1"
isort = "^5.13.2"
mypy = "^1.8.0"
pre-commit = "^3.6.0"

[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310"]
include = "\.pyi?$"
extend-exclude = '''
/(
    \.eggs
  | \.git
  | \.mypy_cache
  | \.venv
  | venv
  | env
  | _build
  | build
  | dist
  | migrations
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip = [".gitignore", ".dockerignore"]
skip_glob = ["*/migrations/*"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
default_section = "THIRDPARTY"

[tool.mypy]
python_version = "3.8"
disallow_untyped_defs = true
ignore_missing_imports = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
exclude = [
    'migrations/',
    'tests/',
    'env/',
    'venv/',
]

### .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        name: isort (python)

### 개발 환경 설정

```bash
# 1. 개발 의존성 설치
poetry add -D black isort mypy pre-commit

# 2. pre-commit 설치
poetry run pre-commit install

# 3. 린터 실행
poetry run pre-commit run --all-files

# 개별 도구 실행
poetry run black .
poetry run isort .
poetry run mypy .

### pre-commit으로 모든 검사 실행
poetry run pre-commit run --all-files
```

# 커밋 규칙

## 커밋 메시지 형식
`유형(<scope>): <subject>`

## 커밋 유형
- ✨ feat: 새로운 기능 추가
- 🐛 fix: 기능 수정, 버그 수정
- 💡 chore: 오타 수정, 코드 변경 (주석 추가/수정 포함)
- 📝 docs: 문서 수정
- 🚚 build: 빌드 관련 파일 수정/삭제
- ✅ test: 테스트 코드 추가
- ♻️ refactor: 코드 리팩터링

## 커밋 메시지 예시
- ✨ feat(인증): JWT 인증 구현
- 🐛 fix(DB): 연결 타임아웃 문제 해결
- ♻️ refactor(API): 쿼리 성능 최적화

# Pull Request 규칙

## Pull Request 템플릿
```markdown
## 변경 사항
[구체적인 변경 내용 설명]


## 체크리스트
- [ ] 단위 테스트 추가/수정
- [ ] 테스트 커버리지 70% 이상
- [ ] API 문서 업데이트
- [ ] 코드 린트 통과
- [ ] 충분한 코멘트 작성

## 기타 참고사항
[추가 정보 또는 스크린샷]
```

# 코드 리뷰 규칙

## 기본 원칙
- 최소 1명 이상의 승인 필요
- 24시간 이내 리뷰 진행
- 코드 품질, 테스트 커버리지 확인
- 버그/보안 취약점 검토

## 배포 프로세스
1. 테스트 통과 확인
2. 코드 리뷰 완료
3. CI/CD 파이프라인 통과
4. production 배포

## 환경 구분
- development: 개발/테스트 환경
- main: 운영/배포 환경
