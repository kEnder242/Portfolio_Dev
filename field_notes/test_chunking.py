import re
import os

def parse_notes_into_chunks(text):
    # Regex for M/D/Y patterns at the start of a line
    # Supports 1/1/16, 12/12/2016, etc.
    date_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4})'
    
    chunks = []
    current_date = "Header/Unknown"
    current_content = []
    
    lines = text.splitlines()
    for line in lines:
        match = re.match(date_pattern, line.strip())
        if match:
            # Save previous chunk
            if current_content:
                chunks.append({"date": current_date, "content": "\n".join(current_content)})
            
            current_date = match.group(1)
            current_content = [line]
        else:
            current_content.append(line)
            
    # Add final chunk
    if current_content:
        chunks.append({"date": current_date, "content": "\n".join(current_content)})
        
    return chunks

if __name__ == "__main__":
    test_file = "raw_notes/notes_2016_MVE.txt"
    with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    chunks = parse_notes_into_chunks(text)
    print(f"Total chunks found: {len(chunks)}")
    for chunk in chunks[:5]:
        print(f"Date: {chunk['date']} | Content Length: {len(chunk['content'])}")
        # print(chunk['content'][:100])
        # print("-" * 20)

