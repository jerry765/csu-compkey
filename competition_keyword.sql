-- 创建数据库
CREATE DATABASE IF NOT EXISTS competition_keyword_db;

-- 切换到新创建的数据库
USE competition_keyword_db;

-- 创建用户表
CREATE TABLE IF NOT EXISTS User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建种子关键词表
CREATE TABLE IF NOT EXISTS SeedKeyword (
    SeedKeywordID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Keyword VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- 创建竞争性关键词表
CREATE TABLE IF NOT EXISTS CompetitiveKeyword (
    CompetitiveKeywordID INT AUTO_INCREMENT PRIMARY KEY,
    SeedKeywordID INT,
    Keyword VARCHAR(255),
    CompetitiveScore FLOAT,
    FOREIGN KEY (SeedKeywordID) REFERENCES SeedKeyword(SeedKeywordID)
);

-- 创建用户搜索历史表
CREATE TABLE IF NOT EXISTS UserSearchHistory (
    SearchHistoryID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    SeedKeywordID INT,
    SearchTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (SeedKeywordID) REFERENCES SeedKeyword(SeedKeywordID)
);

-- 创建数据源信息表
CREATE TABLE IF NOT EXISTS DataSourceInfo (
    DataSourceID INT AUTO_INCREMENT PRIMARY KEY,
    FilePath VARCHAR(255),
    Encoding VARCHAR(50),
    ImportTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
