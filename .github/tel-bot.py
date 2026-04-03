import asyncio
import sys
import requests
import os

# --- Environment Variables ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
APK_PATH = os.environ.get("APK_PATH")
COMMIT_MESSAGE = os.environ.get("COMMIT_MESSAGE")


async def send_telegram_files():
    if not BOT_TOKEN or not CHAT_ID:
        print("[-] BOT_TOKEN and CHAT_ID environment variables must be set.")
        return
    if not APK_PATH:
        print("[-] No files to send.")
        return
    """
    Connects to Telegram and sends the specified files as a group message.
    """
    url = "https://api.telegram.org/bot{0}/sendDocument".format(BOT_TOKEN)
    # Send the files together as an album/group
    files = [
        (
            "document",
            (
                APK_PATH.split("/")[-1],
                open(APK_PATH, "rb"),
                "application/octet-stream",
            ),
        )
    ]
    payload = {"chat_id": CHAT_ID, "caption": COMMIT_MESSAGE}

    requests.request("POST", url, data=payload, files=files)
    print("[+] Files sent successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get all file paths from command-line arguments
        message = sys.argv[1]
        apk_files = sys.argv[2:]
        print(f"[+] Found files to upload: {APK_PATH}")
        try:
            # Run the asynchronous function
            asyncio.run(send_telegram_files())
        except Exception as e:
            print(f"[-] An error occurred: {e}")
    else:
        print("[-] No file paths provided as arguments.")
