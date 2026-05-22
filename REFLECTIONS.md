# REFLECTIONS

## What did you learn?

Em đã học được rằng API tagging của AWS không đồng nhất giữa các dịch vụ.
EC2 và EBS sử dụng `create_tags`, trong khi RDS và S3 cần các API khác nhau để quản lý tag.

Em cũng học được cách sử dụng thư viện `moto` để mock các dịch vụ AWS phục vụ cho unit testing mà không cần sử dụng tài khoản AWS thật.

## What was difficult?

Khó khăn lớn nhất là phải khớp chính xác output mà pytest mong đợi.
Chỉ cần khác một chút về nội dung hoặc format cũng khiến test bị fail.

Em cũng học được cách tổ chức một ứng dụng CLI bằng `argparse` và mô hình dispatch function để xử lý nhiều command khác nhau.