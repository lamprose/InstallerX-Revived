import asyncio
import sys
import requests
import os

# --- Environment Variables ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def send_telegram_files(files, message):
    """
    Connects to Telegram and sends the specified files as a group message.
    """
    url = "https://api.telegram.org/bot{0}/sendDocument".format(BOT_TOKEN)
    # Send the files together as an album/group
    files = map(
        lambda f: (
            "document",
            (
                f.split("/")[-1],  # Use the file name from the path
                open(f, "rb"),
                "application/octet-stream",
            ),
        ),
        files,
    )
    payload = {"chat_id": CHAT_ID, "caption": message}

    requests.request("POST", url, data=payload, files=files)
    print("[+] Files sent successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get all file paths from command-line arguments
        message = sys.argv[1]
        apk_files = sys.argv[2:]
        print(f"[+] Found files to upload: {apk_files}")
        try:
            # Run the asynchronous function
            asyncio.run(send_telegram_files(apk_files, message))
        except Exception as e:
            print(f"[-] An error occurred: {e}")
    else:
        print("[-] No file paths provided as arguments.")
