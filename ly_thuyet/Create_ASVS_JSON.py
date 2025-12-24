import pandas as pd
import re
import json

file_path = 'OWASP ASVS 4.0.3.xlsx'

try:
    df = pd.read_excel(file_path, engine='openpyxl', dtype=str)
except Exception as e:
    print(f"Lỗi: {e}")
    exit()

df.columns = df.columns.str.strip()
col_id = 'requestID'
col_desc = 'Description'
col_chapter = 'Chapter Name'

df[col_chapter] = df[col_chapter].ffill()

def process_content(text):
    if pd.isna(text): return "", "", ""
    text = str(text).replace('\n', ' ').strip()
    
    # Regex tìm pattern ([Label](URL))
    # Nhóm 1: Label (C1, C2...), Nhóm 2: URL
    link_pattern = r'\(\[(.*?)\]\((.*?)\)\)'
    match = re.search(link_pattern, text)
    
    label = ""
    url = ""
    clean_title = text
    
    if match:
        label = match.group(1) # Ví dụ: "C1"
        url = match.group(2)   # Ví dụ: "https://owasp.org/..."
        # Xóa đoạn ([C1](...)) khỏi title
        clean_title = re.sub(link_pattern, '', text).strip()
        
    return clean_title, label, url

def detect_level_array(row):
    # Trả về mảng level theo logic tích lũy
    if pd.notna(row.get('level1')): return [1, 2, 3]
    if pd.notna(row.get('level2')): return [2, 3]
    if pd.notna(row.get('level3')): return [3]
    return [1, 2, 3] # Mặc định

chapters_json = []
current_chapter = None

for _, row in df.iterrows():
    raw_desc = row.get(col_desc)
    raw_id = row.get(col_id)
    
    if not raw_id or "deleted" in str(raw_desc).lower():
        continue

    title, ref_label, ref_url = process_content(raw_desc)
    lvl_array = detect_level_array(row)
    chapter_name = row.get(col_chapter)
    
    if not current_chapter or current_chapter['chapterName'] != chapter_name:
        current_chapter = {"chapterName": chapter_name, "requirements": []}
        chapters_json.append(current_chapter)

    current_chapter['requirements'].append({
        "id": raw_id if raw_id.startswith('V') else f"V{raw_id}",
        "text": title,
        "refLabel": ref_label, # Lưu nhãn C1, C2 vào đây
        "refUrl": ref_url,     # Lưu link gốc vào đây
        "level": lvl_array     # Giờ là mảng [1, 2, 3]
    })

# Xuất file JSON cho Frontend dùng
with open('../src/assets/asvsData.json', 'w', encoding='utf-8') as f:
    json.dump(chapters_json, f, ensure_ascii=False, indent=2)

print("Đã tách link thành công và xuất file asvsData.json!")