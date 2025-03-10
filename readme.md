# HoneyPie 🍯

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python-based honeypot security project designed to deceive, log, and analyze unauthorized attackers and bots attempting to compromise a system.

## 📋 Overview

HoneyPie mimics a vulnerable machine by providing fake SSH and HTTP services, allowing security researchers to monitor attacker behavior in a controlled environment. The project helps understand attack patterns, collect threat intelligence, and enhance security posture.

### Key Features

* **SSH Honeypot:** A fake SSH server that logs brute-force login attempts and executed commands
* **HTTP Honeypot:** A fake WordPress admin login page that captures attacker credentials and logs unauthorized access attempts
* **Logging & Analysis:** Stores attacker data, including IP addresses, credentials, and command execution history
* **Tarpit Mode:** Slows down attackers to waste their resources and discourage automated attacks
* **Web Dashboard (Optional):** A web-based UI for visualizing attack trends and analyzing collected data

## 🛠️ Technologies

HoneyPie is built using the following technologies and libraries:

| Component | Technology Used |
|-----------|----------------|
| **Programming Language** | Python (3.8+) |
| **SSH Honeypot** | Paramiko (SSH server emulation) |
| **HTTP Honeypot** | Flask (Fake WordPress Admin Panel) |
| **Logging & Storage** | JSON and log files |
| **Web Dashboard** | Flask + HTML/CSS (for data visualization) |
| **Security Analysis** | Attack logging, IP tracking |
| **Environment Management** | Virtual environment using `venv` |

## 🚀 Installation

To install and run HoneyPie, follow these steps:

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/rudrakadel/HoneyPie.git
cd HoneyPie
```

### 2️⃣ Set Up a Virtual Environment

```sh
python -m venv honeypot_env
source honeypot_env/bin/activate  # Linux/Mac
honeypot_env\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Generate SSH Keys (For SSH Honeypot)

```sh
ssh-keygen -t rsa -b 2048 -f static/server.key -N ""
```

### 5️⃣ Run the Honeypot

#### SSH Honeypot (Fake SSH Server)

```sh
python honeypy.py -a 127.0.0.1 -p 2222 -u admin -w password --ssh
```

#### HTTP Honeypot (Fake Admin Panel)

```sh
python honeypy.py -a 127.0.0.1 -p 5000 --http
```

#### Web Dashboard (Optional - Attack Logs Visualization)

```sh
python web_app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## ⚙️ Requirements

### System Requirements

- ✅ Python 3.8+
- ✅ Linux/macOS/Windows environment (preferably a VM or isolated system)

### Python Dependencies (installed via `requirements.txt`)

- `paramiko` (SSH server emulation)
- `flask` (Web honeypot & dashboard)
- `requests` (HTTP request handling)
- `json` (For logging attack data)

To install all dependencies, run:

```sh
pip install -r requirements.txt
```

## ⚠️ Usage Warnings

- **DO NOT** run HoneyPie on production systems or personal machines
- Always deploy in isolated environments (VM, container, etc.)
- Use at your own risk and responsibility
- Always follow local laws and regulations regarding honeypot deployment

## 👥 Contributing

### 🔧 Contribution Guidelines

Developers and security enthusiasts can contribute by:

- **Reporting Issues:** Submit bug reports and security flaws in GitHub Issues
- **Enhancing Features:** Improve logging, add new protocols, or integrate AI-based attack detection
- **Submitting Pull Requests (PRs):** Fork the repository, make changes, and create a PR with clear descriptions
- **Improving Documentation:** Help refine the README and add tutorial guides

### 💡 Steps to Contribute

1. **Fork the Repository**
   ```sh
   git clone https://github.com/rudrakadel/HoneyPie.git
   cd HoneyPie
   ```

2. **Create a New Branch**
   ```sh
   git checkout -b feature-branch
   ```

3. **Make Changes & Test**
   Modify code and ensure proper functionality.

4. **Commit & Push**
   ```sh
   git add .
   git commit -m "Added new feature"
   git push origin feature-branch
   ```

5. **Submit a Pull Request** on GitHub.

## 📜 License

HoneyPie is licensed under the **MIT License**, which allows:
- ✅ Free usage and distribution
- ✅ Modifications and commercial use
- ✅ Open-source contributions

Check the full license details in the **LICENSE** file.

## 📞 Contact

For questions, feedback, or collaboration, please open an issue on GitHub or contact the me through Linkedin(https://www.linkedin.com/in/rudra-kadel-1084b6249).

---

**Note:** This project is intended for educational and defensive security research purposes only.
