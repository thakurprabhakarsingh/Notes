import json
import os
import requests

BOT_TOKEN = "8915217266:AAEs_T4obO44HpWH0xCcDtczgvd3xL_UskA"
CHANNEL_ID = "-1003873333488"
CHANNEL_USER = "App_Docs_Hub"
DB_FILE = "notes.json"

def upload():
    print("\n==============================")
    print("   NotesHub PDF Uploader      ")
    print("==============================")

    fpath = input("PDF File Path (e.g., /sdcard/Download/test.pdf): ").strip()
    if not os.path.exists(fpath):
        print(f"Error: File '{fpath}' nahi mili!")
        return

    title = input("Note Title: ").strip()
    subject = input("Subject: ").strip()
    course = input("Course (B.Tech / BCA / Diploma): ").strip()
    branch = input("Branch (CSE / IT / ECE etc): ").strip()
    sem = input("Semester (1-8): ").strip()
    college = input("College / University: ").strip()

    file_bytes = os.path.getsize(fpath)
    file_size = f"{round(file_bytes / (1024 * 1024), 1)} MB"

    caption = (
        f"📚 {title}\n"
        f"📖 Subject: {subject}\n"
        f"🎓 {course} ({branch}) - Sem {sem}\n"
        f"🏫 College: {college}\n"
        f"📦 Size: {file_size}"
    )

    print("\nUploading to Telegram channel...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(fpath, "rb") as doc:
        res = requests.post(
            url,
            data={"chat_id": CHANNEL_ID, "caption": caption},
            files={"document": doc}
        )

    res_data = res.json()
    if not res_data.get("ok"):
        print("Upload failed:", res_data)
        return

    msg_id = res_data["result"]["message_id"]
    telegram_url = f"https://t.me/{CHANNEL_USER}/{msg_id}"
    print(f"Telegram Upload Done: {telegram_url}")

    # Update notes.json
    notes = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                notes = json.load(f)
        except Exception:
            notes = []

    new_id = len(notes) + 1
    new_entry = {
        "id": new_id,
        "title": title,
        "subject": subject,
        "course": course,
        "branch": branch,
        "semester": str(sem),
        "college": college,
        "rating": 5.0,
        "reviewsCount": 1,
        "searches": 1,
        "telegramUrl": telegram_url,
        "fileSize": file_size,
        "uploaderUid": "ADMIN-01"
    }

    notes.insert(0, new_entry)

    with open(DB_FILE, "w") as f:
        json.dump(notes, f, indent=2)

    print(f"Successfully added to {DB_FILE}!\n")

if __name__ == "__main__":
    upload()
