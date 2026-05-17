CREATE DATABASE IF NOT EXISTS library_db;

USE library_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    roll_number VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    password VARCHAR(100),
    contact_no VARCHAR(20),
    course VARCHAR(100),
    year VARCHAR(20)
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(50) UNIQUE,
    title VARCHAR(255),
    authors VARCHAR(255),
    genre VARCHAR(100),
    total_copies INT,
    shelf_number VARCHAR(50),
    publisher VARCHAR(255),
    branch VARCHAR(100),
    year VARCHAR(20)
);

CREATE TABLE issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(50),
    roll_number VARCHAR(50),
    issue_date DATE,
    due_date DATE,
    return_date DATE NULL,
    status VARCHAR(50)
);

CREATE TABLE return_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(50),
    roll_number VARCHAR(50),
    return_date DATE
);

CREATE TABLE reserve_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(50),
    roll_number VARCHAR(50),
    reserve_date DATE
);