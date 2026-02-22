# VPS to RDP Wizard 🚀

This project allows you to convert any Linux VPS (Ubuntu/Debian) into a high-performance Remote Desktop (RDP) environment that can be accessed natively from Windows.

## 🌟 Features
- **Zero Download (Web Edition)**: Use `web_wizard.html` in your browser to generate commands.
- **Auto-Configurator**: The Python app (`app.py`) can automatically SSH into your VPS and set everything up for you.
- **Cross-Platform**: The Python code is built with Flet and can be compiled to:
    - **Windows (.exe)**
    - **Android (.apk)**
    - **Web**

## 🛠️ How to use (No Download Method)
1. Open `web_wizard.html` in your browser.
2. Enter your VPS IP and Username.
3. Copy the generated **One-Liner Command**.
4. Open **PowerShell** on your Windows machine.
5. Paste the command and hit Enter.
6. Once the script finishes, press `Win + R`, type `mstsc`, and connect to your VPS IP.

## 🚀 Running the App
If you have Python installed:
```bash
pip install -r requirements.txt
python app.py
```

## 📱 Building as APK
To convert this project into a literal Android APK:
1. Install [Flet CLI](https://flet.dev/docs/guides/python/deploying-apps/android).
2. Run: `flet build apk`

## 🔒 Security Note
This script installs `xrdp` and opens port `3389`. Ensure you use a strong password for your VPS user.
