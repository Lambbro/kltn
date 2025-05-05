"""
Mapping các biến trạng thái,... lưu dưới dạng Dictionary
"""
# Bảng DangKyNCKH
MAP_DANG_KY_TRANG_THAI = {
    0: "Bị Hủy",
    1: "Đang Chờ Duyệt",
    2: "Đã Được Duyệt"
}
MAP_NGUYEN_VONG_TRANG_THAI = {
    0: "Bị Hủy",
    1: "Đang Chờ Duyệt",
    2: "Đã Được Duyệt"
}

MAP_NGUYEN_VONG_MUC_UU_TIEN = {
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
    3: "Báo cáo cấp khoa",
    4: "Báo cáo cấp khoa chỉnh sửa",
    5: "Báo cáo cấp trường",
    6: "Báo cáo cấp trường cần chỉnh sửa"
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

MAP_HOC_VI = {#hoc_vi - HocVi, bac_dao_tao - TrinhDoHocVan
    1: "Đại Học",
    2: "Thạc Sĩ",
    3: "Tiến Sĩ",
    4: "Tiến Sĩ Khoa Học"
}

MAP_KY_NANG_NGOAI_NGU = {
    1: "Xuất sắc",
    2: "Tốt",
    3: "Khá",
    4: "Trung bình",
    5: "Yếu"
}

MAP_TAC_GIA = {
    True: "Tác giả",
    False: "Đồng tác giả"
}

MAP_SACH_BAO = {
    1: "Sách chuyên khảo",
    2: "Giáo trình",
    3: "Sách tham khảo",
    4: "Sách hướng dẫn",
    5: "Bài báo khoa học trong nước",
    6: "Bài báo khoa học ngoài nước "
}

MAP_LOAI_DE_TAI_KHCN = {
    1: "Đề tài, Nhiệm vụ",
    2: "Đề án - Dự án",
    3: "Chương trình",
    4: "Dự án hợp tác quốc tế",
    5: "Đề tài với tư cách thành viên"
}

MAP_VAI_TRO_HD_CAO_HOC = {
    0: "Hướng dẫn một mình",
    1: "Hướng dẫn một",
    2: "Hướng dẫn hai"
}

MAP_HOC_VI_DAO_TAO = {
    1: "Nghiên cứu sinh đã bảo vệ thành công và được cấp bằng tiến sĩ",
    2: "Nghiên cứu sinh đang thực hiện luận án",
    3: "Thạc sĩ đã bảo vệ thành công và được cấp bằng thạc sĩ",
    4: "Thạc sĩ đang thực hiện luận văn"
}

MAP_CAP_DO_GIANG_DAY = {
    1: "Đại học",
    2: "Thạc sĩ",
    3: "Tiến sĩ"
}

# Hàm tiện ích lấy giá trị từ dictionary
def get_label(mapping: dict, status_code):
    return mapping.get(status_code, "Lỗi trạng thái")

def get_status_code(mapping: dict, label):
    reverse_mapping = {v: k for k, v in mapping.items()}
    return reverse_mapping.get(label, "Lỗi trạng thái")
# Ví dụ sử dụng
# print(get_label(MAP_DE_TAI_NCKHSV_TIEN_DO, 2))  # Output: Đã nộp đề cương
# print(get_label(MAP_DE_TAI_NCKHGV_TRANG_THAI, 5))  # Output: Lỗi trạng thái
