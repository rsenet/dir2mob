import requests
import sys
import os
import time
import glob

MOBSF_URL = 'http://localhost:8000'
API_KEY = 'MOBSF_API_KEY'
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3


def upload_apk(file_path):
    url     = f"{MOBSF_URL}/api/v1/upload"
    headers = {"Authorization": API_KEY}

    with open(file_path, "rb") as fp:
        # on précise le bon Content-Type pour qu'MobSF reconnaisse l'APK
        files = {
            "file": (
                os.path.basename(file_path),
                fp,
                "application/vnd.android.package-archive"
            )
        }
        resp = requests.post(url, headers=headers, files=files)

    return resp.json()


def scan_apk(scan_hash, re_scan=0):
    url = f'{MOBSF_URL}/api/v1/scan'
    headers = {'Authorization': API_KEY}
    data = {'hash': scan_hash, 're_scan': re_scan}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, data=data, headers=headers, timeout=TIMEOUT_SECONDS)

            if response.status_code == 200:
                print("[+] Scan triggered successfully.")
                return response.json()
            else:
                print(f"[-] Scan failed: {response.text}")
                return None

        except requests.exceptions.Timeout:
            print(f"[!] Timeout on scan attempt {attempt}. Retrying...")

    print("[-] Failed to scan after retries.")
    return None


def download_report(scan_hash, apk_name, reports_dir):
    headers = {'Authorization': API_KEY}
    os.makedirs(reports_dir, exist_ok=True)

    # Download JSON Report
    url_json = f'{MOBSF_URL}/api/v1/report_json'
    response = requests.post(url_json, data={'hash': scan_hash}, headers=headers)

    if response.status_code == 200:
        json_path = os.path.join(reports_dir, f'{apk_name}_report.json')
        with open(json_path, 'w') as f:
            f.write(response.text)
        print(f"[+] JSON report saved: {json_path}")

    else:
        print(f"[-] Failed to download JSON report: {response.text}")

    # Download PDF Report
    url_pdf = f'{MOBSF_URL}/api/v1/download_pdf'
    response = requests.post(url_pdf, data={'hash': scan_hash}, headers=headers)

    if response.status_code == 200:
        pdf_path = os.path.join(reports_dir, f'{apk_name}_report.pdf')

        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f"[+] PDF report saved: {pdf_path}")

    else:
        print(f"[-] Failed to download PDF report: {response.text}")


def upload_directory(directory_path):
    apk_files = glob.glob(os.path.join(directory_path, '*.apk'))
    if not apk_files:
        print(f"[-] No APK files found in {directory_path}")
        return

    print(f"[+] Found {len(apk_files)} APKs to upload.")

    reports_dir = os.path.join(directory_path, 'reports')

    for apk in apk_files:
        print(f"[+] Uploading {apk} to MobSF...")
        upload_response = upload_apk(apk)

        if upload_response:
            scan_hash = upload_response.get('hash')
            print(f"[+] Starting scan for hash {scan_hash}...")
            scan_response = scan_apk(scan_hash)

            if scan_response:
                print(f"[+] Scan completed for {apk}.")
                apk_name = os.path.splitext(os.path.basename(apk))[0]
                download_report(scan_hash, apk_name, reports_dir)
            else:
                print(f"[-] Scan failed for {apk}.")

        else:
            print(f"[-] Upload failed for {apk}.")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_directory>")
        sys.exit(1)

    dir_path = sys.argv[1]

    if not os.path.isdir(dir_path):
        print(f"[-] {dir_path} is not a valid directory.")
        sys.exit(1)

    upload_directory(dir_path)
