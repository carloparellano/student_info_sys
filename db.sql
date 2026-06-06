DROP DATABASE IF EXISTS student_info_sys;
CREATE DATABASE IF NOT EXISTS student_info_sys;
USE student_info_sys;

CREATE TABLE IF NOT EXISTS college (
    college_code VARCHAR(100) PRIMARY KEY,
    college_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
    course_code VARCHAR(200) PRIMARY KEY,
    course_name VARCHAR(200) NOT NULL,
    college_code VARCHAR(100) NOT NULL,
    FOREIGN KEY (college_code) 
        REFERENCES college(college_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS student (
    student_id CHAR(9) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(200) NOT NULL,
    year_level INT NOT NULL,
    gender VARCHAR(45) NOT NULL,
    student_url VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (course_code) 
        REFERENCES course(course_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
