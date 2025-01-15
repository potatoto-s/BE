# Hands-with BE

핸즈윗은 단순히 공방 사장님들을 위한 커뮤니티를 넘어, 공방의 성장을 이끌고 공예 문화를 발전시키는 데 기여하는 플랫폼

---
<h3 align="center"> Stack </h3>
<div align="center">
<a href="https://www.djangoproject.com/">
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
</a>
<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</a>
<a href="https://www.postgresql.org/">
  <img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
</a>
<a href="https://gunicorn.org/">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=Gunicorn&logoColor=white">
</a>
<a href="https://www.nginx.com/">
  <img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white">
</a>
<a href="https://ncloud.com/">
  <img src="https://img.shields.io/badge/NCloud-0070F3?style=for-the-badge&logo=NCloud&logoColor=white">
</a>
</div>


<h3 align="center"> Management Tool </h3>
<div align="center">
<a href="https://www.notion.so/">
  <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white">
</a>
  <a href="https://github.com/">
    <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  </a>
  <a href="https://discord.com/">
    <img src="https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  </a>
</div>

---

## 프로젝트 구조

```
BE
├── config
│   ├── settings.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── wsgi.py
│   ├── urls.py
│   └── asgi.py
│
├── users       # 사용자
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── posts       # 게시글
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── comments    # 댓글
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── contexts    # 문의하기
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
└── manage.py
```
![alt text](image.png)