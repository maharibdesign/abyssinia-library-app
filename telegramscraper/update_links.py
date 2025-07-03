# update_links.py
import os
import re
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument

# --- CONFIGURATION ---
SUMMARIES_PATH = '../src/content/summaries/'
CHANNEL_USERNAME = '@abyssinialibrary'  # <--- SET YOUR CHANNEL USERNAME
# --- REFINEMENT ---
MINIMUM_MATCH_SCORE = 2 # We now require at least 2 points to consider it a match
# --------------------

print("--- Starting FINAL Refined Link Updater Script ---")

def get_keywords(text):
    words = re.split(r'\s|\W+', text.lower())
    return {word for word in words if len(word) > 3} # Increased min word length to 4

async def main():
    load_dotenv()
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE_NUMBER')

    if not all([api_id, api_hash, phone]):
        print("🛑 ERROR: API_ID, API_HASH, or PHONE_NUMBER not found in .env file. Exiting.")
        return

    client = TelegramClient('telegram_session', int(api_id), api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))
    
    print("✅ Connection successful.")

    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
    except Exception as e:
        print(f"🛑 ERROR: Could not get channel '{CHANNEL_USERNAME}'. Error: {e}")
        return

    print(f"\nScanning '{CHANNEL_USERNAME}' for all PDF files...")
    scraped_pdfs = {}
    async for message in client.iter_messages(channel):
        if message.media and isinstance(message.media, MessageMediaDocument) and message.media.document.mime_type == 'application/pdf':
            file_name_attr = next((attr for attr in message.media.document.attributes if hasattr(attr, 'file_name')), None)
            if file_name_attr:
                file_name = file_name_attr.file_name.lower()
                message_link = f"https://t.me/{channel.username}/{message.id}"
                scraped_pdfs[file_name] = message_link
    
    print(f"✅ Scan complete. Found {len(scraped_pdfs)} PDFs.")

    print("\nUpdating local .md files with REFINED intelligent matching...")
    updated_count = 0
    not_found_count = 0
    
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
                
                # REFINED ALGORITHM: Get keywords and give title keywords more weight
                title_keywords = get_keywords(md_title)
                author_keywords = get_keywords(md_author)

                best_match_url = None
                highest_score = 0
                best_match_filename = ""

                for pdf_filename, pdf_url in scraped_pdfs.items():
                    pdf_keywords = get_keywords(pdf_filename)
                    
                    # Calculate score with weighting
                    title_score = len(title_keywords.intersection(pdf_keywords)) * 2 # Title matches are worth 2 points
                    author_score = len(author_keywords.intersection(pdf_keywords)) # Author matches are worth 1 point
                    score = title_score + author_score
                    
                    if score > highest_score:
                        highest_score = score
                        best_match_url = pdf_url
                        best_match_filename = pdf_filename

                # REFINED THRESHOLD: Check against the minimum required score
                if best_match_url and highest_score >= MINIMUM_MATCH_SCORE:
                    print(f"  -> Match found for '{md_title}':")
                    print(f"     Best matching PDF: '{best_match_filename}' (Score: {highest_score})")
                    
                    new_content, count = re.subn(r'pdfUrl:\s*".*?"', f'pdfUrl: "{best_match_url}"', content)
                    
                    if count > 0:
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        print(f"     ✅ Successfully updated {md_filename}")
                        updated_count += 1
                else:
                    print(f"  -> ⚠️ No reliable match found for '{md_title}' (Highest score: {highest_score})")
                    not_found_count += 1

    print(f"\n--- Script Finished ---")
    print(f"📊 Results: {updated_count} files updated, {not_found_count} files could not be matched.")

if __name__ == '__main__':
    asyncio.run(main())