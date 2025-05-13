from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests


def openProfile(profile_id, api, win_scale=None, addination_args=None, win_pos=None, win_size=None):
    # Kiểm tra API có hợp lệ không
    if not api:
        print("❌ API không hợp lệ")
        return None

    # Xây dựng URL với các tham số tùy chọn
    params = []

    if addination_args:
        params.append(f"addination_args={addination_args}")
    if win_scale:
        params.append(f"win_scale={win_scale}")
    if win_pos:
        params.append(f"win_pos={win_pos}")
    if win_size:
        params.append(f"win_size={win_size}")

    param_str = "&".join(params)
    start_url = f"{api}/api/v3/profiles/start/{profile_id}"
    if param_str:
        start_url += f"?{param_str}"
    print(f"\t\t start_url : {start_url}")

    # Gọi API để mở profile
    try:
        start_response = requests.get(start_url)
        start_response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = start_response.json().get("data")

        if not data:
            print("❌ Không có dữ liệu trả về từ API.")
            print("Phản hồi từ API:", start_response.text)
            return None

        remote_debugging_address = data.get("remote_debugging_address")
        driver_path = data.get("driver_path")

        if not remote_debugging_address or not driver_path:
            print("❌ Thiếu thông tin cần thiết từ API.")
            return None

        print(f"✅ Địa chỉ remote debugging: {remote_debugging_address}")
        print(f"✅ Đường dẫn driver: {driver_path}")

        # Kiểm tra nếu đường dẫn driver không hợp lệ
        if driver_path == 'f' or not driver_path:
            print("❌ Đường dẫn driver không hợp lệ.")
            return None

        # Cấu hình ChromeOptions
        options = Options()
        options.debugger_address = remote_debugging_address

        # Khởi tạo WebDriver với driver GPM
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        return driver
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gửi yêu cầu: {e}")
        return None


def closeProfile(profile_id, api):
    # Đảm bảo URL chính xác khi đóng profile
    url = f"{api}/api/v3/profiles/close/{profile_id}"

    # Gửi yêu cầu GET để đóng profile
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            print("✅ Đã đóng profile thành công.")
        else:
            print("⚠️ Không thể đóng profile:", data.get("message"))
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gửi yêu cầu đóng profile: {e}")


