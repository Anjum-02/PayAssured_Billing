-- MySQL schema for PayAssured assignment
CREATE TABLE clients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_name VARCHAR(255) NOT NULL,
  company_name VARCHAR(255),
  city VARCHAR(100),
  contact_person VARCHAR(255),
  phone VARCHAR(50),
  email VARCHAR(255)
);

CREATE TABLE cases (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  invoice_number VARCHAR(100) NOT NULL,
  invoice_amount DECIMAL(12,2) NOT NULL,
  invoice_date DATE NOT NULL,
  due_date DATE NOT NULL,
  status VARCHAR(50) DEFAULT 'New',
  last_follow_up_notes TEXT,
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
