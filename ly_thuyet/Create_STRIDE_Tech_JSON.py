import pandas as pd
import json
import re

def clean_string(s):
    """Dọn dẹp các ký tự thừa và chuẩn hóa chuỗi cơ bản."""
    if not s or pd.isna(s): return ""
    # Xóa dấu chấm, dấu phẩy ở cuối và khoảng trắng thừa
    return str(s).strip().rstrip('.,:').strip()

def normalize_stride(item):
    """Chỉ giữ lại 6 nhóm STRIDE chuẩn, còn lại là rác -> loại bỏ."""
    val = item.lower().strip()
    
    # Mapping chuẩn
    mapping = {
        'Spoofing': 'Spoofing',
        'Tampering': 'Tampering',
        'Repudiation': 'Repudiation',
        'Information Disclosure': 'Information Disclosure',
        'Denial of Service': 'Denial of Service',
        'Elevation of Privilege': 'Elevation of Privilege'
    }
    
    for key, target in mapping.items():
        if key.lower() in val or (target == 'Denial of Service' and 'dos' in val):
            return target
            
    return None # Nếu là "12", "Reputation" hay linh tinh -> trả về None để loại bỏ

def process_mapping(df, target_column, normalization_func=None):
    """Hàm tổng quát để xử lý mapping cho từng cột."""
    result_map = {}
    
    for _, row in df.iterrows():
        asvs_id = str(row['ASVS ID']).strip()
        raw_val = row[target_column]
        
        if pd.isna(raw_val) or str(raw_val).lower() == 'nan':
            continue
            
        # Tách bằng dấu phẩy hoặc chấm phẩy
        items = re.split(r'[,;]', str(raw_val))
        
        for i in items:
            cleaned = clean_string(i)
            if not cleaned: continue
            
            # Nếu có hàm chuẩn hóa riêng (như STRIDE) thì dùng, không thì Title Case
            if normalization_func:
                final_val = normalization_func(cleaned)
            else:
                final_val = cleaned.title()
                
            if final_val:
                if final_val not in result_map:
                    result_map[final_val] = []
                result_map[final_val].append(asvs_id)
                
    # Sắp xếp lại cho đẹp
    return {k: sorted(list(set(v))) for k, v in sorted(result_map.items())}

# --- MAIN PROCESS ---

try:
    # Đọc file excel của bro (vẫn giữ engine openpyxl)
    df = pd.read_excel('Mapping_STRIDE.xlsx', engine='openpyxl', dtype=str)
except Exception as e:
    print(f"Lỗi đọc file: {e}")
    exit()

# 1. Xử lý STRIDE
print("Đang xử lý STRIDE...")
stride_json = process_mapping(df, 'Threat (Stride)', normalize_stride)

# 2. Xử lý Technical Impact
print("Đang xử lý Technical Impact...")
tech_impact_json = process_mapping(df, 'Technical Impact')

# --- XUẤT FILE ---

output_dir = '../src/assets/'

def save_json(data, filename):
    full_path = output_dir + filename
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"-> Đã lưu: {full_path}")
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"-> Không thấy folder assets, đã lưu tại thư mục hiện tại: {filename}")

save_json(stride_json, 'stride_mapping.json')
save_json(tech_impact_json, 'technical_impact_mapping.json')

print("\nNgon lành! Mọi thứ đã sẵn sàng.")