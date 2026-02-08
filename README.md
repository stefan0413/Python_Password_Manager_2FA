# Password Manager (CLI, 2FA)

This project is a **console-based Password Manager** written in Python.  
It allows users to securely store, generate, and manage passwords for different services and accounts.

The application supports:
- User accounts with authentication
- Encrypted password storage (AES-based)
- Password generation
- Grouping of passwords (e.g. Work, Personal)
- Two-Factor Authentication (TOTP)
- Clipboard support for copying passwords
- Fully terminal-based interaction

The project is intended as an educational example of:
- Secure password handling
- Database-backed CLI applications
- Testable architecture with high unit test coverage

---

## Features

- **User authentication**
  - Registration and login
  - Password hashing
  - TOTP-based 2FA

- **Password management**
  - Add, update, delete, list passwords
  - Optional grouping
  - Encrypted storage

- **Password generation**
  - Configurable length and character sets

- **Security**
  - AES encryption
  - Clipboard auto-clearing support
  - Strict user scoping for all operations

---

## Project Structure

password_manager/\
├── auth/ -------------------- # Authentication logic (login, registration, 2FA)\
├── storage/ -------------------- # SQLite persistence layer (users, groups, passwords)\
├── vault/ -------------------- # CLI flows (passwords, groups, generator)\
├── utils/ -------------------- # Utility helpers (clipboard, misc)\
├── model/ -------------------- # Domain models (authentication session)\
│\
├── cli.py -------------------- # CLI orchestration and menu routing\
├── main.py -------------------- # Application entry point\
│\
tests/ -------------------- # Unit and integration tests\

