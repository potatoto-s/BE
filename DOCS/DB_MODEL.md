# Database Schema

```sql
-- Users Table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('COMPANY', 'WORKSHOP', 'GUEST')), -- 기업/공방/비회원
    company_name VARCHAR(255),
    workshop_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'SUSPENDED', 'DELETED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts Table
CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT workshop_only_posts CHECK (
        user_id IN (SELECT id FROM users WHERE role = 'WORKSHOP')
    )
);

-- Post Images Table
CREATE TABLE post_image (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments Table
CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact Inquiries Table
CREATE TABLE contact_inquirie (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email EMAIL NOT NULL,
    phone VARCHAR(20) NOT NULL,
    organization_name VARCHAR(255) NOT NULL, -- company_name or workshop_name
    content TEXT NOT NULL,
    preferred_contact VARCHAR(20) NOT NULL CHECK (preferred_contact IN ('EMAIL', 'PHONE')),
    inquiry_type VARCHAR(20) NOT NULL CHECK (inquiry_type IN ('COMPANY', 'WORKSHOP')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Post Likes Table
CREATE TABLE post_likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(post_id, user_id)
);
```