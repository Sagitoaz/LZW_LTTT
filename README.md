FITSP25PRJB23DCCN861-README.txt

1. Thông tin nhóm:
- Nguyen Thanh Trung - B23DCCN861 - group 12
- Dang Phi Long - B23DCCN497 - group 12
- Tran Trung Kien - B23DCCN469 - group 12
- Pham Anh Tu - B23DCCN875 - group 12

2. Yêu cầu của dự án:
Xây dựng công cụ nén và giải nén file sử dụng thuật toán LZW. Ứng dụng có giao diện đồ họa hỗ trợ:
- Nén 1 file hoặc nhiều file (batch compress)
- Bảo vệ file nén bằng mật khẩu (tùy chọn)
- Giải nén file và khôi phục định dạng gốc
- Vẽ biểu đồ tỷ lệ nén
- Xuất báo cáo CSV quá trình nén

3. Cấu trúc thư mục:
- `dist/LZW_tool.exe`  : File thực thi đã build bằng PyInstaller
- `gui_app.py`         : Giao diện chính của chương trình
- `lzw.py`             : Thuật toán nén và giải nén
- `file_handler.py`    : Xử lý file nhị phân và định dạng lưu trữ
- `ShowDict.py`        : Script hiển thị từ điển nén LZW từ file `.lzw`
- `ReadLZW.py`         : Script đọc file `.lzw` và in mã sau khi nén
- `Example1.txt`       : File mẫu để test
- `Example2.txt`       : File mẫu để test

4. Thiết lập môi trường (nếu chạy bằng mã nguồn):
- Yêu cầu: Python 3.8+  
- Cài đặt thư viện bổ sung:
    pip install matplotlib

5. Hướng dẫn sử dụng:

**Chạy ứng dụng (2 cách)**:

*Cách 1: Dùng file đã build (khuyên dùng)*  
    - Mở file: `dist/LZW_tool.exe`  
    - Giao diện sẽ hiện ra tương tự như chạy bằng mã nguồn

*Cách 2: Dùng mã nguồn Python*  
    - Chạy bằng lệnh trong cmd: `python gui_app.py`

**Nén file**:
    - Nhấn "📦 Compress File", chọn file
    - (Tùy chọn) nhập mật khẩu
    - File nén có đuôi `.lzw` sẽ được tạo

**Giải nén**:
    - Nhấn "📂 Decompress File", chọn `.lzw`
    - Nhập mật khẩu nếu có
    - File gốc được phục hồi

**Batch Compress**:
    - Nhấn "📚 Batch Compress" để chọn nhiều file
    - Nhấn "📊 Show Chart" để xem biểu đồ
    - Xuất báo cáo bằng "📄 Export CSV"

**Script phụ trợ**:
    - Đọc `.lzw`: chỉnh đường dẫn trong `ReadLZW.py` rồi chạy
    - Hiển thị dictionary đã tạo bằng cách chạy lệnh sau: 
```py
python ShowDict.py <file.lzw>
```

6. Ghi chú:
- Nếu file nén lớn hơn file gốc → hệ thống sẽ cảnh báo và tự động xóa file `.lzw`.
- Ứng dụng sẽ chạy tốt nhất nếu sử dụng file txt có nhiều kí tự lặp lại, có thể sử dụng 2 file example có sẵn trong dự án để kiểm tra
- Cấu trúc file `.lzw` gồm: loại mã (`B`, `H`, `I`), đuôi gốc, mã hóa mật khẩu (SHA-256), mã nén.