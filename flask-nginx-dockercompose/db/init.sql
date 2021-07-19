CREATE DATABASE IF NOT EXISTS flasko;

CREATE TABLE users (
  id INT PRIMARY KEY,
  fullname VARCHAR(120),
  email VARCHAR(120),
  password VARCHAR(120),
  created_at DATE()
);