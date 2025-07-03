# update_links.py
import os
import re
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# --- CONFIGURATION ---
SUMMARIES_PATH = '../src/content/summaries/'
CHANNEL_USERNAME = '@abyssinialibrary'  # <--- IMPORTANT: SET YOUR CHANNEL USERNAME HERE
# ---------------------

print("--- Starting Intelligent Link Updater Script ---")

# Load credentials from .env file in the current directory
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')

# This function cleans and tokenizes a string into a set of keywords
def get_keywords(text):
    # Convert to lowercase and split by any non-alphanumeric character
    words = re.split(r'\s|\W+', text.lower())
    # Return a set of words that are longer than 2 characters to avoid common small words
    return {word for word in words if len(word) > 2}

async def main():
    if not all([api_id, api_hash, phone]):
        print("🛑 ERROR: API_ID, API_HASH, or PHONE_NUMBER not found in .env file. Exiting.")
        return

    # Use a session file so you don't have to log in every single time
    client = TelegramClient('telegram_session', int(api_id), api_hash)
    
    print("Connecting to Telegram...")
    await client.connect()
    if not await client.is_user_authorized():
        print("  -> First time login, sending code...")
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('  -> Please enter the code you received: '))
        except Exception as e:
            print(f"🛑 ERROR during sign-in: {e}")
            return
    print("✅ Connection successful.")

    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
    except Exception as e:
        print(f"🛑 ERROR: Could not find channel '{CHANNEL_USERNAME}'. Please check the name. Error: {e}")
        return

    print(f"\nScanning '{CHANNEL_USERNAME}' for all PDF files. This may take a moment...")
    scraped_pdfs = {}
    async for message in client.iter_messages(channel):
        if message.media and isinstance(message.media, MessageMediaDocument) and message.media.document.mime_type == 'application/pdf':
            file_name_attr = next((attr for attr in message.media.document.attributes if hasattr(attr, 'file_name')), None)
            if file_name_attr:
                # Store the lowercase filename and its direct message link
                file_name = file_name_attr.file_name.lower()
                message_link = f"https://t.me/{channel.username}/{message.id}"
                scraped_pdfs[file_name] = message_link
    
    print(f"✅ Scan complete. Found {len(scraped_pdfs)} PDFs in the channel.")

    print("\nUpdating local .md files with intelligent matching...")
    updated_count = 0
    not_found_count = 0
    
    # Ensure the summaries directory exists
    if not os.path.isdir(SUMMARIES_PATH):
        print(f"🛑 ERROR: Summaries directory not found at '{SUMMARIES_PATH}'.")
        return

    for md_filename in os.listdir(SUMMARIES_PATH):
        if md_filename.endswith('.md'):
            filepath = os.path.join(SUMMARIES_PATH, md_filename)
            with open(filepath, 'r+', encoding='utf-8') as f:
                content = f.read()
                title_match = re.search(r'title:\s*"(.*?)"', content)
                author_match = re.search(r'author:\s*"(.*?)"', content)

                if not title_match or not author_match:
                    continue
                
                md_title = title_match.group(1)
                md_author = author_match.group(1)
                
                # Create a set of keywords from the title and author in the .md file
                md_keywords = get_keywords(f"{md_title} {md_author}")

                best_match_url = None
                highest_score = 0
                best_match_filename = ""

                # Iterate through all scraped PDFs to find the best match
                for pdf_filename, pdf_url in scraped_pdfs.items():
                    pdf_keywords = get_keywords(pdf_filename)
                    # The score is the number of common keywords
                    score = len(md_keywords.intersection(pdf_keywords))
                    
                    if score > highest_score:
                        highest_score = score
                        best_match_url = pdf_url
                        best_match_filename = pdf_filename

                # Update the file if we found a reasonably good match (score > 1)
                if best_match_url and highest_score > 1:
                    print(f"  -> Match found for '{md_title}':")
                    print(f"     Best matching PDF: '{best_match_filename}' (Score: {highest_score})")
                    
                    # Use regex to replace only the pdfUrl line
                    new_content, count = re.subn(r'pdfUrl:\s*".*?"', f'pdfUrl: "{best_match_url}"', content)
                    
                    if count > 0:
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        print(f"     ✅ Successfully updated {md_filename}")
                        updated_count += 1
                else:
                    print(f"  -> ⚠️ No reliable match found for '{md_title}'")
                    not_found_count += 1

    print(f"\n--- Script Finished ---")
    print(f"📊 Results: {updated_count} files updated, {not_found_count} files could not be matched.")

# This ensures the script can be run directly
if __name__ == '__main__':
    asyncio.run(main())