# SKYRO Scanner – Web Application Security Scanner

## Black-Box & Grey-Box Web Security Scanner

SKYRO Scanner is a web vulnerability scanner designed for modern web application security testing. It supports black-box and grey-box scanning, automated crawling, authenticated testing, and customizable scan parameters to help developers, bug bounty hunters, and security researchers detect vulnerabilities efficiently.

> ⚠️ Disclaimer: This tool is intended for authorized security testing only. Do not scan systems without proper permission.

## 📦 Installation
* pip install setuptools
* python setup.py install
* pip install -e .

Followed Below:
### 1️⃣ Install Required Dependency

Before installing SKYRO, ensure setuptools is installed:

bash/cmd
* pip install setuptools

If pip is not working properly, use:

bash/cmd
* python -m pip install setuptools

### 2️⃣ Install SKYRO (Recommended Modern Method)

Instead of using the outdated setup.py install, use:

bash/cmd
* pip install -e .

This installs SKYRO in editable mode, which is cleaner and ideal for development.

> ⚠️ Avoid using:
>
> bash/cmd
> python setup.py install
> 
>
> This is considered legacy installation practice.

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
