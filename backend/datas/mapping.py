"""
Mapping các biến trạng thái,... lưu dưới dạng Dictionary
"""

# Bảng DangKyNCKH
MAP_DANG_KY_NCKH_TRANG_THAI = {
    0: "Bị Hủy",
    1: "Đang Chờ Duyệt",
    2: "Đã Được Duyệt"
}

MAP_DANG_KY_NCKH_MUC_UU_TIEN = {
    1: "Nguyện Vọng 1",
    2: "Nguyện Vọng 2"
}

# Bảng NhomNCKH
MAP_NHOM_NCKH_TRANG_THAI = {
    0: "Đã Bị Hủy",
    1: "Đang Chờ Duyệt",
    2: "Đã Được Duyệt"
}

# Bảng Đề tài NCKH Sinh Viên
MAP_DE_TAI_NCKHSV_TRANG_THAI = {
    0: "Đã Hủy Bỏ",
    1: "Đang Chờ Duyệt",
    2: "Đã Hoàn Thành"
}

MAP_DE_TAI_NCKHSV_TIEN_DO = {
    1: "Chưa nộp đề cương",
    2: "Đã nộp đề cương",
    3: "Chưa bổ sung đề cương chỉnh sửa",
    4: "Đã nộp đề cương bổ sung chỉnh sửa",
    5: "Chưa nộp báo cáo",
    6: "Đã nộp báo cáo",
    7: "Chưa bổ sung báo cáo chỉnh sửa",
    8: "Đã nộp báo cáo bổ sung chỉnh sửa"
}

# Bảng Tài liệu NCKH Sinh Viên
MAP_TAI_LIEU_NCKHSV_TRANG_THAI = {
    1: "Chưa nộp",
    2: "Đã nộp thành công",
    3: "Đã hoàn thiện",
    4: "Cần chỉnh sửa"
}

MAP_TAI_LIEU_NCKHSV_LOAI_TAI_LIEU = {
    1: "Đề cương",
    2: "Đề cương chỉnh sửa",
    3: "Báo cáo",
    4: "Báo cáo chỉnh sửa"
}

# Bảng Đề tài NCKH Giảng Viên
MAP_DE_TAI_NCKHGV_TRANG_THAI = {
    0: "Đã hủy",
    1: "Đang thực hiện",
    2: "Đã nghiệm thu"
}

MAP_DE_TAI_NCKHGV_TIEN_DO = {
    1: "Đã nộp đề xuất",
    2: "Cần chỉnh sửa đề xuất",
    3: "Đã hoàn thiện đề xuất",
    4: "Chưa nộp thuyết minh",
    5: "Đã nộp thuyết minh",
    6: "Cần chỉnh sửa TM và DTKP",
    7: "Đã hoàn thiện TM và DTKP",
    8: "Chưa nộp báo cáo tiến độ",
    9: "Đã nộp báo cáo tiến độ",
    10: "Chưa nộp hồ sơ nghiệm thu",
    11: "Đã nộp hồ sơ nghiệm thu",
    12: "Cần chỉnh sửa hồ sơ nghiệm thu",
    13: "Đã hoàn thành nghiệm thu"
}

#Bảng tài liệu NCKH giảng viên
MAP_TAI_LIEU_NCKHGV_LOAI_TAI_LIEU = {
    1: "Đề xuất",
    2: "Đề xuất chỉnh sửa",
    3: "Thuyết minh",
    4: "Thuyết minh chỉnh sửa",
    5: "Báo cáo tiến độ",
    6: "Đơn xin gia hạn",
    7: "Hồ sơ nghiệm thu",
    8: "Hồ sơ nghiệm thu chỉnh sửa"
}

MAP_TAI_LIEU_NCKHGV_TRANG_THAI = {
    1: "Chưa nộp",
    2: "Đã nộp thành công",
    3: "Đã hoàn thiện",
    4: "Cần chỉnh sửa"
}

#Bảng hội đồng khoa
MAP_HOI_DONG_KHOA_LOAI = {
    1: "Hội đồng duyệt đề cương",
    2: "Hội đồng bảo vệ đề tài NCKH"
}

MAP_HOI_DONG_KHOA_TRANG_THAI = {
    1: "Chưa hoàn thành",
    2: "Đã hoàn thành"
}

MAP_HOI_DONG_KHOA_TU_CACH_THAM_DU = {
    1: "Chủ nhiệm",
    2: "Thư ký",
    3: "Ủy viên"
}

#Bảng hội đồng trường
MAP_HOI_DONG_TRUONG_LOAI = {
    1: "Hội đồng xét duyệt thuyết minh",
    2: "Hội đồng xét duyệt dự trù kinh phí",
    3: "Hội đồng nghiệm thu đề tài",
    11: "Hội đồng bảo vệ đề tài NCKH sinh viên"
}

MAP_HOI_DONG_TRUONG_TRANG_THAI = {
    1: "Chưa hoàn thành",
    2: "Đã hoàn thành"
}

MAP_HOI_DONG_TRUONG_TU_CACH_THAM_DU = {
    1: "Chủ nhiệm",
    2: "Phản biện 1",
    3: "Phản biện 2",
    4: "Ủy viên",
    5: "Thư ký"
}

#Bảng khen thưởng
MAP_KHEN_THUONG_CAP_DO = {
    1: "Cấp trường",
    2: "Cấp khoa"
}

MAP_KHEN_THUONG_MUC_DO = {
    0: "Giải đặc biệt",
    1: "Giải nhất",
    2: "Giải nhì",
    3: "Giải ba",
    4: "Giải khuyến khích"
}

# Hàm tiện ích lấy giá trị từ dictionary
def get_label(mapping, status_code):
    return mapping.get(status_code, "Lỗi trạng thái")

# Ví dụ sử dụng
print(get_label(MAP_DE_TAI_NCKHSV_TIEN_DO, 2))  # Output: Đã nộp đề cương
print(get_label(MAP_DE_TAI_NCKHGV_TRANG_THAI, 5))  # Output: Lỗi trạng thái
