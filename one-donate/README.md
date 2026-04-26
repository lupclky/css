# One Donate - Hệ thống gộp donate 3 nền tảng

Gộp donate từ **Zypage**, **Wescan**, **YouTube** vào 1 overlay hiển thị trên stream, với **queue** để tránh 3 nền tảng dồn dập cùng lúc.

## Cách hoạt động

1. **Server** nhận webhook từ 3 nền tảng qua các endpoint riêng
2. Mỗi donate được đưa vào **queue** (hàng đợi FIFO)
3. **Overlay** hiển thị **1 donate tại 1 thời điểm**, sau X giây chuyển sang donate tiếp theo

## Cài đặt & Chạy

```bash
cd one-donate
node server.js
```

Server chạy tại `http://localhost:3847`

## Cấu hình OBS

1. Thêm **Browser Source** trong OBS
2. URL: `http://localhost:3847/overlay`
   - Hoặc mở file `donate-overlay.html` trực tiếp (cần chạy server trước)
3. Kích thước: 500x300 (hoặc tùy layout stream)
4. Tham số URL (tùy chọn):
   - `?duration=8000` – thời gian hiển thị mỗi donate (ms), mặc định 8000
   - `?server=http://IP:3847` – nếu overlay chạy trên máy khác

## Webhook Endpoints

| Nền tảng | Endpoint | Cách cấu hình |
|----------|----------|---------------|
| Zypage   | `POST /webhook/zypage` | Trong Zypage: cài webhook, URL = `http://IP_MÁY_BẠN:3847/webhook/zypage` |
| Wescan   | `POST /webhook/wescan` | Trong Wescan: cài webhook, URL = `http://IP_MÁY_BẠN:3847/webhook/wescan` |
| YouTube  | `POST /webhook/youtube` | Dùng tool/bridge (VD: Chatbot, StreamElements) gửi Super Chat tới endpoint này |

**Lưu ý:** Nếu stream từ máy ở mạng local, dùng `localhost`. Nếu webhook từ internet (Zypage/Wescan gửi tới), cần:
- Mở port 3847 trên router
- Hoặc dùng **ngrok**: `ngrok http 3847` → lấy URL public làm webhook

## Định dạng webhook (chuẩn hóa)

Server chấp nhận nhiều format, sẽ chuẩn hóa về:

```json
{
  "donorName": "Tên người donate",
  "amount": 50000,
  "message": "Nội dung tin nhắn",
  "currency": "₫",
  "platform": "zypage|wescan|youtube"
}
```

Nếu Zypage/Wescan dùng format khác, chỉnh hàm `parseZypage` / `parseWescan` trong `server.js` cho đúng field của API họ.

## API thủ công (test / tích hợp custom)

```bash
curl -X POST http://localhost:3847/donate \
  -H "Content-Type: application/json" \
  -d '{"donorName":"Test User","amount":100000,"message":"Hello!","platform":"youtube"}'
```

## YouTube Super Chat

YouTube không có webhook trực tiếp. Có thể:
1. Dùng **StreamElements** / **StreamLabs** – nếu họ hỗ trợ gửi webhook khi có Super Chat
2. Dùng **browser extension** đọc chat YouTube và POST tới `/webhook/youtube`
3. Dùng **Chatbot** (VD: Nightbot, StreamElements chatbot) có tích hợp YouTube

## Cấu trúc thư mục

```
one-donate/
├── server.js          # Server nhận webhook + SSE
├── donate-overlay.html # Overlay hiển thị (OBS Browser Source)
├── package.json
└── README.md
```
