CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    company VARCHAR(255),
    role VARCHAR(50) DEFAULT 'USER',
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE file_scans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255),
    file_hash VARCHAR(64) UNIQUE NOT NULL,
    verdict VARCHAR(50),
    analysis TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(255),
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE threat_indicators (
    id SERIAL PRIMARY KEY,
    indicator_type VARCHAR(50),
    indicator_value VARCHAR(255) UNIQUE NOT NULL,
    threat_level VARCHAR(50),
    description TEXT,
    source VARCHAR(255),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_file_hash ON file_scans(file_hash);
CREATE INDEX idx_user_id ON audit_logs(user_id);
CREATE INDEX idx_threat_value ON threat_indicators(indicator_value);
