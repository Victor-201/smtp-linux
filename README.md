# TRIỂN KHAI HỆ THỐNG GỬI EMAIL QUA SMTP TRÊN LINUX

*(Chuyên ngành Công nghệ Thông tin – Môn Hệ điều hành Linux)*

---

## I. GIỚI THIỆU DỰ ÁN

Email là một dịch vụ mạng cốt lõi trên hệ điều hành Linux, hoạt động dựa trên giao thức SMTP (Simple Mail Transfer Protocol). Trong thực tế, các Mail Server như Postfix, Sendmail hay Exim đều được triển khai và vận hành trực tiếp trên Linux.

Dự án này yêu cầu **tự xây dựng một hệ thống SMTP thu gọn**, nhằm hiểu rõ cách Linux xử lý **tiến trình, I/O, socket mạng, xác thực và quản lý file**, thông qua việc lập trình **Bash Script thuần**.

---

## II. MỤC TIÊU DỰ ÁN

### Mục tiêu học tập

Sau khi hoàn thành dự án, sinh viên có khả năng:

* Hiểu nguyên lý hoạt động của giao thức SMTP
* Thực hành lập trình Shell Script trên Linux
* Làm việc với socket TCP thông qua Terminal
* Quản lý tiến trình, stdin/stdout, file và thư mục
* Hiểu vai trò của xác thực người dùng trong dịch vụ mạng

### Yêu cầu bắt buộc

* **Thực hành trực tiếp trên hệ điều hành Ubuntu**
* **Sử dụng 100% Terminal Linux** để triển khai và demo
* Không sử dụng giao diện đồ họa (GUI)

---

## III. CHỨC NĂNG HỆ THỐNG

### Chức năng chính

1. Xây dựng **Client SMTP** gửi email đến Server
2. Xây dựng **Server SMTP** tiếp nhận và xử lý email
3. Hỗ trợ xác thực người dùng bằng lệnh `AUTH LOGIN`
4. Lưu trữ email theo từng người dùng
5. Ghi log toàn bộ phiên làm việc SMTP

### Các lệnh SMTP phải hỗ trợ

* `HELO <domain>`
* `AUTH LOGIN`
* `MAIL FROM:<email>`
* `RCPT TO:<email>`
* `DATA`
* `QUIT`

### Mã phản hồi SMTP

* `220` – Service ready
* `250` – OK
* `354` – Start mail input
* `235` – Authentication successful
* `535` – Authentication failed
* `221` – Service closing

---

## IV. YÊU CẦU KỸ THUẬT

* **Hệ điều hành:** Ubuntu Linux
* **Ngôn ngữ:** Bash Script (.sh)
* **Môi trường:** Terminal
* **Không sử dụng:** Python, C/C++, Java, thư viện SMTP có sẵn

### Công cụ được phép sử dụng

* `netcat (nc)` hoặc `socat`
* `base64`
* Các lệnh Linux cơ bản: `echo`, `read`, `printf`, `grep`, `cut`, `awk`, `date`, `mkdir`, `cat`

---

## V. CẤU TRÚC THƯ MỤC DỰ ÁN

```bash
smtp-linux/
├── bin/
│   ├── start_server.sh
│   └── start_client.sh
│
├── server/
│   ├── server_main.sh
│   ├── socket_listener.sh
│   ├── smtp_parser.sh
│   ├── auth_handler.sh
│   ├── mail_handler.sh
│   └── log_handler.sh
│
├── client/
│   ├── client_main.sh
│   ├── socket_client.sh
│   ├── auth_client.sh
│   └── mail_sender.sh
│
├── config/
│   ├── server.conf
│   └── users.txt
│
├── data/
│   └── mailbox/
│
├── logs/
│   └── smtp_server.log
│
└── README.md
```

---

## VI. PHÂN CHIA CÔNG VIỆC SONG SONG

### PHẦN SERVER

| File                 | Người thực hiện   | Chức năng             | Interface                                                    |
| -------------------- | ----------------- | --------------------- | ------------------------------------------------------------------ |
| `server_main.sh`     | Nguyễn Văn Thắng  | Điều phối server      | Gọi `socket_listener.sh`, chuyển stdin/stdout cho `smtp_parser.sh` |
| `socket_listener.sh` | Nguyễn Ngọc Trung | Mở cổng TCP SMTP      | Truyền stdin/stdout của kết nối TCP                                |
| `smtp_parser.sh`     | Phan Đình Trọng   | Phân tích lệnh SMTP   | Gọi `auth_handler.sh`, `mail_handler.sh`, `log_handler.sh`         |
| `auth_handler.sh`    | Hiến Thanh Sang   | Xác thực `AUTH LOGIN` | Nhận base64 user/pass → trả `235` hoặc `535`                       |
| `mail_handler.sh`    | Nguyễn Văn Lượm   | Lưu email             | Nhận FROM, TO, DATA                                                |
| `log_handler.sh`     | Nguyễn Văn Lượm   | Ghi log hệ thống      | Hàm `log_event "TIME IP FROM TO STATUS"`                           |

### PHẦN CLIENT

| File               | Người thực hiện   | Chức năng        | Interface chuẩn                |
| ------------------ | ----------------- | ---------------- | ------------------------------ |
| `client_main.sh`   | Đinh Thành Đạt    | Điều phối client | Gọi các module client          |
| `socket_client.sh` | Đinh Thành Đạt    | Kết nối server   | Truyền stdin/stdout            |
| `auth_client.sh`   | Nguyễn Tấn Đạt    | Xác thực         | Gửi base64 user/pass           |
| `mail_sender.sh`   | Huỳnh Phạm Tố Như | Gửi email        | MAIL FROM, RCPT TO, DATA, QUIT |

---

## VII. CÁCH CHẠY CHƯƠNG TRÌNH

### Bước 1: Cấp quyền thực thi

```bash
chmod +x bin/*.sh server/*.sh client/*.sh
```

### Bước 2: Chạy Server

```bash
sh bin/start_server.sh
```

### Bước 3: Chạy Client

```bash
sh bin/start_client.sh
```

---

## VIII. YÊU CẦU ĐẦU RA

* Client gửi email thành công
* Server xác thực người dùng chính xác
* Email lưu tại:

```
data/mailbox/<user>/timestamp.eml
```

* Log ghi đầy đủ:

```
[TIME] [IP] [FROM] [TO] [AUTH_STATUS]
```
