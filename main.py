import speedtest
import time
import datetime
import os


DOWNLOAD_THRESHOLD = 50  # minimum download speed
UPLOAD_THRESHOLD = 10    # minimumn upload speed

TIME_INTERVAL = 1800  # 30 minutes

LOG_FILE = "internet_speed_log.txt"

def ensure_log_file_exists():
    """Ensure the log file exists and create it if not."""
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, 'w') as log:
            log.write("Timestamp - Download (Mbps), Upload (Mbps)\n")

def log_message(message):
    """Log a message with a timestamp to the log file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log:
        log.write(f"{timestamp} - {message}\n")

def test_internet_speed():
    """Perform an internet speed test and return the download and upload speeds."""
    speed = speedtest.Speedtest()
    speed.get_best_server()
    download_speed = speed.download() / 1_000_000
    upload_speed = speed.upload() / 1_000_000
    return download_speed, upload_speed

def monitor_internet_speed():
    """Monitor the internet speed every 30 minutes and log the results."""
    ensure_log_file_exists()

    while True:
        try:
            download_speed, upload_speed = test_internet_speed()
            print(f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")

            if download_speed < DOWNLOAD_THRESHOLD or upload_speed < UPLOAD_THRESHOLD:
                log_message(f"ALERT: Low speed! Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")                

                print(f"\033[91mALERT: Low speed! Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps\033[0m")
            else:
                log_message(f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")

        except Exception as e:
            print(f"Error while testing speed: {e}")

        time.sleep(TIME_INTERVAL)

if __name__ == "__main__":
    print(f"Starting internet speed monitor. Logging every 30 minutes.")
    monitor_internet_speed()
