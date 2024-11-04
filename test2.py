import requests
from bs4 import BeautifulSoup
import os

# URL của trang web mà bạn muốn lấy nội dung
url = 'https://nettruyenviet.com/truyen-tranh/ban-hoc-cua-toi-la-linh-danh-thue/chuong-210'  # Thay thế bằng URL thực tế

try:
    # Gửi yêu cầu GET tới URL
    response = requests.get(url)
    response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không

    # Phân tích HTML với Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả phần tử có class "reading-detail box_doc"
    content = soup.find_all(class_='reading-detail box_doc')

    # Tạo file HTML mới
    with open('output.html', 'w', encoding='utf-8') as f:
        # Thêm phần đầu của tài liệu HTML
        f.write('<html>\n<head>\n')

        # Lấy tất cả các liên kết đến CSS và thêm chúng vào file
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                # Nếu đường dẫn là tương đối, thêm URL gốc
                if not href.startswith('http'):
                    href = os.path.join(url, href)
                f.write(f'<link rel="stylesheet" href="{href}">\n')

        # Lấy tất cả các tệp JavaScript và thêm chúng vào file
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                # Nếu đường dẫn là tương đối, thêm URL gốc
                if not src.startswith('http'):
                    src = os.path.join(url, src)
                f.write(f'<script src="{src}"></script>\n')

        f.write('</head>\n<body>\n')

        # Lưu nội dung vào file
        for item in content:
            f.write(str(item))  # Lưu từng phần tử vào file

        f.write('</body>\n</html>')  # Kết thúc tài liệu HTML

    print("Nội dung đã được lưu vào file output.html")
except requests.exceptions.RequestException as e:
    print(f"Có lỗi xảy ra: {e}")
