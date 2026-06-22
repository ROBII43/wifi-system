CREATE DATABASE IF NOT EXISTS wifi_system;
USE wifi_system;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20),
    mac VARCHAR(100) UNIQUE,
    plan VARCHAR(50),
    expiry DATETIME,
    status VARCHAR(20)
);

-- PAYMENTS / TRANSACTIONS TABLE
CREATE TABLE transactions (
    id VARCHAR(100) PRIMARY KEY,
    phone VARCHAR(20),
    plan VARCHAR(50),
    amount DECIMAL(10,2),
    status VARCHAR(20),
    mac VARCHAR(100),
    mpesa_receipt VARCHAR(100),
    created_at DATETIME,
    paid_at DATETIME NULL,
    expiry DATETIME NULL,
    active TINYINT DEFAULT 0,
    mikrotik_username VARCHAR(100) NULL,
    mikrotik_password VARCHAR(100) NULL,
    mikrotik_status VARCHAR(50) NULL,
    mikrotik_message TEXT NULL
);

-- SESSIONS TABLE
CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mac VARCHAR(100),
    ip VARCHAR(50),
    active TINYINT DEFAULT 1,
    expiry DATETIME
);