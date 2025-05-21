# Selenium Chrome Automation in Docker

This project uses **Selenium with Chrome** in a **Dockerized environment** to automate browser tasks such as web scraping, testing, or interaction.

## 🐳 Dockerized Chrome + ChromeDriver + Python + Selenium

This setup ensures compatibility between Chrome and ChromeDriver inside a container, making it portable and reliable across different systems.

---

## 📦 Features

- ✅ Headless Chrome support
- ✅ ChromeDriver version matched to Chrome
- ✅ Lightweight Python base image
- ✅ Automatically installs dependencies
- ✅ Suitable for CI/CD, scraping, or browser automation

---

## 📁 Project Structure

```
.
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/selenium-docker-chrome.git
cd selenium-docker-chrome
```

### 2. Build the Docker Image

```bash
docker build -t selenium-chrome-app .
```

### 3. Run the Container

```bash
docker run --rm selenium-chrome-app
```

---

## 🐍 Python Script (main.py)

Use `main.py` to define your browser automation. Example:

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

---

## 🧾 requirements.txt

```txt
selenium
```

---

## 🔧 Dockerfile Overview

- Uses Python base image
- Installs Google Chrome v124
- Downloads and installs matching ChromeDriver
- Adds your app code
- Installs Python dependencies

---

## 🛠️ Troubleshooting

- ❗ If ChromeDriver fails to download: make sure you're using a valid Chrome version
- ❗ For SSL issues, ensure `ca-certificates` are installed in Docker
- 🔁 Use the latest Chrome + Selenium versions to avoid deprecation


---

## 👨‍💻 Author

**Shujaat Ali**