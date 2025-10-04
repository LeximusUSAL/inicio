#!/usr/bin/env python3
import json

# Load the JSON file
with open('/Users/maria/revista_musical_bilbao_transcriptions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Generate JavaScript object entries for pages 8-30
print("// Add these entries to your staticTranscriptions object:")
print()

for page_num in range(8, 31):
    page_key = str(page_num)
    if page_key in data:
        transcription = data[page_key]['transcription']
        # Escape quotes and backslashes for JavaScript
        escaped_transcription = transcription.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        print(f'    {page_num}: "{escaped_transcription}",')
        print()
    else:
        print(f'    // Page {page_num}: Not found in JSON data')
        print()