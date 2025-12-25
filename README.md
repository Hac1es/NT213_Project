# Quantitative ASVS Evaluation System

### Đồ án môn Bảo mật ứng dụng Web - NT213

Hiện thực hóa bài báo: [A quantitative security evaluation model based on OWASP ASVS for software development - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S016740482300442X?ref=pdf_download&fr=RR-2&rr=9b3704eecfc9f876)

## Giới thiệu

**Q-ASVS** là một ứng dụng web giúp đánh giá định lượng mức độ bảo mật của phần mềm dựa trên tiêu chuẩn **OWASP ASVS 4.0.3** (Application Security Verification Standard). Hệ thống tính toán điểm bảo mật SOI (Security Objective Index) thông qua mô hình đánh giá 5 tầng phân cấp.

```
┌─────────────────────────────────────────────┐
│           Tầng 5: SOI Score (0-10)          │
├─────────────────────────────────────────────┤
│   Tầng 4: Aspect (Structure/Environment/    │
│           Process) × Weight                 │
├─────────────────────────────────────────────┤
│         Tầng 3: Criterion Score             │
├─────────────────────────────────────────────┤
│          Tầng 2: Element Score              │
├─────────────────────────────────────────────┤
│         Tầng 1: Mechanism Score             │
├─────────────────────────────────────────────┤
│    Tầng 0: Requirement (ASVS Checklist)     │
└─────────────────────────────────────────────┘
```

## Công thức tính điểm

### SOI Score

```
SOI = Σ(Aspect_Score × Aspect_Weight) × 10
```

Trong đó:

- **Aspect_Score** = Trung bình cộng các Criterion_Score
- **Criterion_Score** = Trung bình cộng các Element_Score
- **Element_Score** = Trung bình cộng các Mechanism_Score
- **Mechanism_Score** = Trung bình cộng các Requirement_Score

### Thang đánh giá

| Điểm SOI   | Đánh giá           |
| ---------- | ------------------ |
| 9.0 - 10.0 | Excellent Security |
| 7.0 - 8.9  | Good Security      |
| 4.0 - 6.9  | Moderate Security  |
| 0.0 - 3.9  | Weak Security      |

### Tham khảo

- [OWASP ASVS 4.0.3](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Top 10 2025](https://owasp.org/Top10/)
- [STRIDE Threat Model](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
