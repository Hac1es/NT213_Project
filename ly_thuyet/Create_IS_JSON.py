import pandas as pd
import json
import re

def normalize_scope(scope):
    """Chuẩn hóa Impact Scope và trả về danh sách các Category (để handle việc tách)."""
    scope = scope.strip().lower().rstrip(':') # Xóa dấu cách và dấu hai chấm ở cuối
    if not scope: return []
    
    # Định nghĩa các nhóm mapping
    # Nếu scope nằm trong list variations, nó sẽ map về key tương ứng
    mapping = {
        'Confidentiality': ['confidentiality', 'confidentialy', 'cònidentiality'],
        'Integrity': ['integrity', 'intigrity', 'intergrity', 'intergrity.'],
        'Availability': ['availability', 'avalability', 'avaibility'],
        'Access Control': ['access control', 'access control ', 'acces control'],
        'Authentication': ['authentication', 'athentication', 'aunthenticaion', 'authencation'],
        'Accountability': ['accountability'],
        'Account Takeover': ['account takeover', 'acount takeover'],
        'Non-Repudiation': ['non-repudiation'],
        'Other': ['other']
    }

    # Xử lý trường hợp đặc biệt: Gộp cả 2
    if 'confidentiality & integrity' in scope:
        return ['Confidentiality', 'Integrity']

    # Kiểm tra các mapping thông thường
    for target_key, variations in mapping.items():
        if scope in variations:
            return [target_key]
            
    # Nếu không khớp cái nào ở trên thì trả về chính nó (viết hoa chữ cái đầu)
    return [scope.title()]

# 1. Đọc dữ liệu
try:
    # Đọc từ .xlsx
    df = pd.read_excel('Mapping_STRIDE.xlsx', engine='openpyxl',dtype=str)
except Exception as e:
    print(f"Lỗi: {e}")
    exit()

impact_mapping = {}

# 2. Xử lý từng dòng
for _, row in df.iterrows():
    asvs_id = str(row['ASVS ID']).strip()
    impact_scope_raw = row['Impact Scope']
    
    if pd.isna(impact_scope_raw): 
        continue
    
    # Tách các giá trị bằng dấu phẩy hoặc dấu chấm phẩy
    raw_scopes = re.split(r'[,;]', str(impact_scope_raw))
    
    for rs in raw_scopes:
        # normalized_list bây giờ là một danh sách (ví dụ: ['Confidentiality', 'Integrity'])
        normalized_list = normalize_scope(rs)
        
        for normalized in normalized_list:
            if normalized not in impact_mapping:
                impact_mapping[normalized] = []
            if asvs_id not in impact_mapping[normalized]:
                impact_mapping[normalized].append(asvs_id)

# 3. Sắp xếp lại cho đẹp và loại bỏ các key thừa nếu có
# (Lúc này "Confidentiality & Integrity" sẽ không còn tồn tại như một key riêng lẻ)
final_json = {k: sorted(list(set(v))) for k, v in sorted(impact_mapping.items())}

# 4. Xuất file JSON
output_path = '../src/assets/impact_scope_mapping.json'
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
    print(f"Đã tạo file {output_path} thành công!")
except FileNotFoundError:
    # Nếu không tìm thấy path assets thì lưu tạm ở thư mục hiện tại
    with open('impact_scope_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
    print("Đã tạo file impact_scope_mapping.json tại thư mục hiện tại!")