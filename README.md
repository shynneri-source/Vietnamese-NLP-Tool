# 🇻🇳 Vietnamese NLP Tool

| Mã số sinh viên | Tên |
|-----------------|-----|
| 123000218 | Phước |

Ứng dụng web Streamlit xử lý ngôn ngữ tiếng Việt với các tính năng:
- **Tokenize** (Tách từ)
- **POS Tagging** (Gán nhãn từ loại)
- **Highlight màu** theo từ loại
- **Export CSV**

## Yêu cầu hệ thống

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

## Cài đặt

```bash
# Cài đặt dependencies
uv sync
```

## Chạy ứng dụng

```bash
uv run streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

## Các tính năng

### 1. Tokenize (Tách từ)
Sử dụng thư viện `underthesea` để tách văn bản tiếng Việt thành các token.

### 2. POS Tagging (Gán nhãn từ loại)
Gán nhãn từ loại cho từng token:
- **N** - Danh từ
- **V** - Động từ
- **A** - Tính từ
- **P** - Đại từ
- **R** - Phó từ
- **E** - Giới từ
- **C** - Liên từ
- **M** - Số từ
- **Np** - Danh từ riêng

### 3. Highlight màu
Mỗi từ loại được hiển thị với màu sắc khác nhau giúp dễ dàng nhận biết.

### 4. Export CSV
Tải xuống kết quả xử lý dưới dạng file CSV.

## Công nghệ sử dụng

- [Streamlit](https://streamlit.io/) - Web framework
- [underthesea](https://github.com/undertheseanlp/underthesea) - Vietnamese NLP toolkit

## License

MIT
