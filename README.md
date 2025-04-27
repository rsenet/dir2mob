<a id="readme-top"></a>

![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![MobSF](https://img.shields.io/badge/MobSF-v4.3.2-informational?style=for-the-badge&logo=mobSF&logoColor=white)

<br />
<div align="center">
  <h3 align="center">dir2mob</h3>

  <p align="center">
    Automate the bulk upload, scan and report download of APKs to a local MobSF instance
    <br />
    <a href="https://github.com/rsenet/dir2mob"><strong>Explore the code »</strong></a>
  </p>
</div>

---

## What is dir2mob?

**dir2mob** is a lightweight Python utility that streamlines static analysis with [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF). Point it at any directory containing APKs, and it will:

- Discover all `.apk` files in a folder  
- Upload each APK to your local MobSF API  
- Trigger a static scan  
- Download PDF reports into a `reports/` subfolder  

Ideal for pentesters or CI pipelines that need to batch-analyze multiple Android packages.

---

## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/rsenet/dir2mob.git
   cd dir2mob
   ```

2. (Optional) Create a virtual environment  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install requirements  
   ```bash
   pip install requests
   ```

---

## Configuration

Edit the top of `dir2mob.py` (or set environment variables):

```python
MOBSF_URL       = 'http://localhost:8000'
API_KEY         = 'your_mobsf_api_key_here'
TIMEOUT_SECONDS = 30
MAX_RETRIES     = 3
```

- **MOBSF_URL**: URL of your MobSF server  
- **API_KEY**: your MobSF API key  
- **TIMEOUT_SECONDS**: per-request timeout  
- **MAX_RETRIES**: retry count on failures  

---

## Usage

```bash
python3 dir2mob.py /path/to/apk_directory
```

### Example

```bash
$ python3 dir2mob.py ./apk_samples
[+] Found 3 APKs to upload.
[+] Uploading apk_samples/app1.apk...
[+] APK uploaded, hash=82ab8b21…
[+] Scan triggered successfully.
[+] Downloading reports for app1…
[+] PDF report saved:  apk_samples/reports/app1_report.pdf
…

$ tree
.
├── apk
│   ├── base.apk
│   └── reports
│       └── base_report.pdf
└── dir2mob.py
```

All reports will be under `./apk_samples/reports/`, named `<apk_basename>_report.pdf`.

---

## Contributing

Contributions and feedback are welcome!  

1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m "feat: add new feature"`)  
4. Push to the branch (`git push origin feature/my-feature`)  
5. Open a Pull Request  

---

## Author

**Régis SENET**  
[https://github.com/rsenet](https://github.com/rsenet)

---

## License

This project is licensed under the [GPLv3 License](https://www.gnu.org/licenses/quick-guide-gplv3.en.html).
