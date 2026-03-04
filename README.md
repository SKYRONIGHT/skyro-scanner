# SKYRO Scanner – Web Application Security Scanner

## Black-Box & Grey-Box Web Security Scanner

SKYRO Scanner is a web vulnerability scanner designed for modern web application security testing. It supports black-box and grey-box scanning, automated crawling, authenticated testing, and customizable scan parameters to help developers, bug bounty hunters, and security researchers detect vulnerabilities efficiently.

> ⚠️ Disclaimer: This tool is intended for authorized security testing only. Do not scan systems without proper permission.

## 📦 Installation

SKYRO Scanner supports **Linux (Kali/Ubuntu)** and **Windows**. Follow the instructions based on your operating system.

---

# 🐧 Kali Linux / Linux Installation (Recommended)

Due to Python security restrictions on Kali (PEP 668), the recommended way to install SKYRO is using **pipx**.

### 1️⃣ Install pipx

```bash
sudo apt install pipx
pipx ensurepath
```

Restart your terminal after installation.

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/SKYRONIGHT/skyro-scanner
cd skyro-scanner
```


### 3️⃣ Install SKYRO

```bash
pipx install .
```


### 4️⃣ Run the Scanner

```bash
skyro -h
```

Example scan:

```bash
skyro https://example.com
```


# 🪟 Windows Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SKYRONIGHT/skyro-scanner
cd skyro-scanner
```

Or download and extract the ZIP file.

---

### 2️⃣ Install Required Dependency

```bash
pip install setuptools
```

If pip does not work:

```bash
python -m pip install setuptools
```


### 3️⃣ Install SKYRO

```bash
pip install -e .
```

### 4️⃣ Run the Scanner

```bash
skyro -h
```

Example:

```bash
skyro https://example.com
```

# ⚡ Quick Run (Without Installation)

You can also run SKYRO directly without installing it:

```bash
git clone https://github.com/SKYRONIGHT/skyro-scanner
cd skyro-scanner
python3 skyro.py https://example.com

# 🔧 Requirements

* Python **3.8+**
* requests
* beautifulsoup4
* lxml
* urllib3

Dependencies are automatically installed during setup.

## 🚀 Usage Guide

SKYRO supports two scanning modes:

* Black-Box (no authentication required)
* Grey-Box (authenticated scanning)

### 🔍 1. Black-Box Scan (Default Mode)

No credentials required:

bash/cmd

skyro http://example.com

### 🔐 2. Grey-Box Scan (With Credentials)

Scan authenticated areas of a web application:

bash/cmd

skyro http://example.com -m grey-box -u admin -p password123

### ⚙️ 3. Advanced Grey-Box Scan

#### 🔎 Deep Scan (More Threads & Depth)

bash/cmd

skyro http://example.com -m grey-box -u admin -p password123 -d 5 -t 15


* -d → Crawl depth
* -t → Number of threads

#### 🛡️ Low-Impact / Safe Scan

bash/cmd

skyro http://example.com -m grey-box -u admin -p password123 -d 1 -t 2


Use this mode when testing production systems with minimal impact.

## 🧠 Features

* ✅ Black-Box scanning
* 🔐 Grey-Box authenticated scanning
* ⚡ Multi-threaded crawling
* 🎯 Adjustable depth control
* 🛡️ Designed for safe and responsible security testing

## 📌 Version

SKYRO Scanner v1.0+
Now with full Grey-Box Support.

## 🤝 Contributing

Pull requests and feature suggestions are welcome.
Please ensure all contributions follow responsible security practices.

## 🔒 Developed with Security in Mind

SKYRO is built to empower ethical hackers and security professionals to identify vulnerabilities responsibly and improve web security.

@Developed by Vikash Kumar Ray
