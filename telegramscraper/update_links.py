# update_links.py
import os
import re
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# --- CONFIGURATION ---
# https://t.me/abyssinialibrary--Your Telegram channel's username (e.g., '@abyssinialibrary')
CHANNEL_USERNAME = '@abyssinialibrary' 
# The path to your summaries
SUMMARIES_PATH = '../src/content/summaries/'
# ---------------------

print("--- Starting Link Updater Script ---")

# Load credentials from .env file
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')

if not all([api_id, api_hash, phone]):
    print("🛑 ERROR: API_ID, API_HASH, or PHONE_NUMBER not found in .env file. Exiting.")
    exit()

# We use a file to store the session, so you don't have to log in every time.
client = TelegramClient('telegram_session', int(api_id), api_hash)

async def main():
    print(f"Connecting to Telegram as {phone}...")
    await client.start(phone)
    print("✅ Connection successful.")

    # Get the channel entity
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
    except ValueError:
        print(f"🛑 ERROR: Channel '{CHANNEL_USERNAME}' not found. Make sure it's correct and you are a member.")
        return

    # 1. Scrape all PDF message links from the channel
    print(f"\nScanning '{CHANNEL_USERNAME}' for PDF files. This may take a moment...")
    book_links = {}
    message_count = 0
    async for message in client.iter_messages(channel):
        message_count += 1
        if message.media and isinstance(message.media, MessageMediaDocument) and message.media.document.mime_type == 'application/pdf':
            # Try to get the book title from the filename (e.g., "Atomic Habits.pdf")
            file_name = message.media.document.attributes[0].file_name
            # Clean up the title: remove .pdf, replace underscores/dashes with spaces
            book_title = os.path.splitext(file_name)[0].replace('_', ' ').replace('-', ' ').lower().strip()
            
            # Construct the public message link
            message_link = f"https://t.me/{channel.username}/{message.id}"
            
            book_links[book_title] = message_link
            print(f"  -> Found: '{book_title}' -> {message_link}")

    print(f"\n✅ Scan complete. Found {len(book_links)} PDF links in {message_count} messages.")

    # 2. Update the local Markdown files
    print("\nUpdating local .md files...")
    updated_files = 0
    for filename in os.listdir(SUMMARIES_PATH):
        if filename.endswith('.md'):
            filepath = os.path.join(SUMMARIES_PATH, filename)
            
            with open(filepath, 'r+', encoding='utf-8') as f:
                content = f.read()
                
                # Find the title from the frontmatter
                title_match = re.search(r'title:\s*"(.*?)"', content)
                if not title_match:
                    continue
                
                md_title = title_match.group(1).lower().strip()
                
                # Check if we found a matching PDF link for this title
                if md_title in book_links:
                    new_link = book_links[md_title]
                    
                    # Use regex to replace the old pdfUrl line
                    new_content, count = re.subn(r'pdfUrl:\s*".*?"', f'pdfUrl: "{new_link}"', content)
                    
                    if count > 0:
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        print(f"  -> Updated: {filename}")
                        updated_files += 1

    print(f"\n✅ Update complete. {updated_files} files were modified.")
    print("\n--- Script Finished ---")

# Run the main asynchronous function
with client:
    client.loop.run_until_complete(main())