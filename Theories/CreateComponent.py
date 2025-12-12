import pandas as pd
import re

file_path = 'OWASP ASVS 4.0.3.xlsx'

# 1. Đọc file
try:
    df = pd.read_excel(file_path, engine='openpyxl', dtype=str)
except Exception as e:
    print(f"Lỗi đọc file: {e}")
    exit()

# 2. Dọn dẹp tên cột (xóa khoảng trắng thừa)
df.columns = df.columns.str.strip()
print("Đang xử lý các cột:", df.columns.tolist())

# --- CẤU HÌNH TÊN CỘT THEO FILE CỦA BẠN ---
col_id = 'requestID'      # Sửa từ 'ID' thành 'requestID'
col_desc = 'Description'  # Giữ nguyên
col_chapter = 'Chapter Name' # Giữ nguyên

# Kiểm tra lại lần nữa cho chắc
if col_id not in df.columns or col_desc not in df.columns or col_chapter not in df.columns:
    print(f"❌ Vẫn chưa khớp tên cột. Hãy kiểm tra kỹ lại file Excel.")
    exit()

# 3. LẤP ĐẦY DỮ LIỆU TRỐNG (Fix lỗi lặp Chapter)
# Copy tên Chapter từ dòng trên xuống dòng dưới nếu bị trống (do merged cells)
df[col_chapter] = df[col_chapter].ffill()

# Hàm làm sạch text
def clean_text(text):
    if pd.isna(text) or str(text).lower() == "nan": return ""
    text = str(text).strip()
    text = text.replace('"', '&quot;')
    text = text.replace("'", "&apos;")
    text = text.replace('\n', ' ')
    return text

current_chapter = ""
processed_ids = [] # Danh sách ID muốn bỏ qua nếu cần

print("\n\n")

for index, row in df.iterrows():
    chapter_name = clean_text(row.get(col_chapter))
    raw_id = clean_text(row.get(col_id))
    description = clean_text(row.get(col_desc))

    # Bỏ qua nếu không có ID hoặc Description là deleted
    if not raw_id:
        continue
    if "deleted" in description.lower():
        continue

    # Format ID: Đảm bảo luôn có chữ V ở đầu và dấu chấm ở cuối
    # Ví dụ: "1.1.1" -> "V1.1.1."
    display_id = raw_id
    if not display_id.startswith('V'):
        display_id = 'V' + display_id
    if not display_id.endswith('.'):
        display_id = display_id + '.'

    # XỬ LÝ IN HEADER CHAPTER
    if chapter_name != current_chapter:
        if current_chapter != "":
            print('  </div>\n') # Đóng div cũ
        
        # Tách số chapter. Logic: Lấy ký tự số từ ID (V1.1.1 -> Chapter 1)
        # Cách này an toàn hơn split dấu chấm
        chapter_num = display_id.split('.')[0].replace('V', '')
        
        print(f'  <div class="mb-10">')
        print(f'    <h1 class="text-2xl font-medium pb-3">')
        print(f'      Chapter V{chapter_num}: {chapter_name}')
        print(f'    </h1>')
        
        current_chapter = chapter_name

    # IN ITEM
    print(f'    <ClickCriteria')
    print(f'      heading="{display_id}"')
    print(f'      title="{description}"')
    print(f'    />')

print('\n  </div>')
print("\n")