import pandas as pd
import json

# Cấu hình tên file
input_file = 'ASVS-5 TANG.xlsx' # Hoặc file .csv của bạn
output_file = '../src/assets/coreMapping.json'

# 1. Đọc dữ liệu (Hỗ trợ cả Excel và CSV)
if input_file.endswith('.xlsx'):
    df = pd.read_excel(input_file, engine='openpyxl')
else:
    df = pd.read_csv(input_file)

# 2. Xử lý các ô trống do "gộp dòng" (Merged Cells)
# Cột Aspect, Criterion, Element và Mechanism thường để trống ở các dòng sau dòng đầu tiên
cols_to_fill = ['1. ASPECT', '2. CRITERION', '3. ELEMENT', '4. MECHANISM']
df[cols_to_fill] = df[cols_to_fill].ffill()

# 3. Xây dựng cấu trúc phân cấp (Hierarchy)
hierarchy = []

# Duyệt qua từng Aspect (Structure, Environment, Process)
for aspect_name, aspect_group in df.groupby('1. ASPECT', sort=False):
    aspect_obj = {"aspect": aspect_name, "criteria": []}
    
    # Duyệt qua từng Criterion trong Aspect
    for criterion_name, criterion_group in aspect_group.groupby('2. CRITERION', sort=False):
        criterion_obj = {"criterion": criterion_name, "elements": []}
        
        # Duyệt qua từng Element trong Criterion
        for element_name, element_group in criterion_group.groupby('3. ELEMENT', sort=False):
            element_obj = {"element": element_name, "mechanisms": []}
            
            # Duyệt qua từng Mechanism trong Element
            for _, row in element_group.iterrows():
                mechanism_name = row['4. MECHANISM']
                req_ids_raw = str(row['5. ASVS Requirement IDs'])
                
                # Tách chuỗi ID (ví dụ: "V14.5.1, V14.5.2" -> ["V14.5.1", "V14.5.2"])
                req_ids = [r.strip() for r in req_ids_raw.split(',') if r.strip()]
                
                element_obj["mechanisms"].append({
                    "mechanism": mechanism_name,
                    "requirements": req_ids
                })
            
            criterion_obj["elements"].append(element_obj)
        aspect_obj["criteria"].append(criterion_obj)
    hierarchy.append(aspect_obj)

# 4. Xuất ra file JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(hierarchy, f, ensure_ascii=False, indent=2)

print(f"Đã tạo file {output_file} thành công!")