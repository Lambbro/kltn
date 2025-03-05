from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Khoa

async def insert_khoa_data(session: AsyncSession):
    khoa_list = [
        Khoa(ma_khoa="K01", ten_khoa="Khoa Đào tạo Cơ bản", dia_chi="Nhà B101 Nguyễn Hiền, quận Hai Bà Trưng, TP .Hà Nội"),
        Khoa(ma_khoa="K02", ten_khoa="Khoa Tạo dáng công nghiệp", dia_chi="Số 422 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K03", ten_khoa="Khoa Kinh tế", dia_chi="Số 193 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K04", ten_khoa="Khoa Tài chính Ngân hàng", dia_chi="Số 422 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K05", ten_khoa="Khoa Luật", dia_chi="Số 193 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K06", ten_khoa="Viện Công nghệ Sinh học & Công nghệ thực phẩm", dia_chi="Tòa nhà C, số 301 Nguyễn Trãi, quận Thanh Xuân, TP. Hà Nội"),
        Khoa(ma_khoa="K07", ten_khoa="Khoa Công nghệ Thông tin", dia_chi="Số 96 Định Công, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K08", ten_khoa="Khoa Điện - Điện tử", dia_chi="Số 422 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K09", ten_khoa="Khoa Du lịch", dia_chi="Số 301 Nguyễn Trãi, quận Thanh Xuân, TP. Hà Nội"),
        Khoa(ma_khoa="K10", ten_khoa="Khoa Tiếng Anh", dia_chi="Số 301 Nguyễn Trãi, quận Thanh Xuân, TP. Hà Nội"),
        Khoa(ma_khoa="K11", ten_khoa="Khoa Tiếng Trung Quốc", dia_chi="Số 193 Vĩnh Hưng, quận Hoàng Mai, TP. Hà Nội"),
        Khoa(ma_khoa="K12", ten_khoa="Khoa Đào tạo Từ xa", dia_chi="Nhà B101 Nguyễn Hiền, quận Hai Bà Trưng, TP .Hà Nội"),
        Khoa(ma_khoa="K13", ten_khoa="Trung tâm Đào tạo Trực tuyến", dia_chi="Nhà B101 Nguyễn Hiền, quận Hai Bà Trưng, TP .Hà Nội"),
        Khoa(ma_khoa="K14", ten_khoa="Trung tâm Đại học Mở Hà Nội tại Đà Nẵng", dia_chi="Số 295 Nguyễn Tất Thành, Thanh Bình, Hải Châu, Đà Nẵng"),
        Khoa(ma_khoa="K15", ten_khoa="Trung tâm Giáo dục Thể chất & Quốc phòng An ninh", dia_chi="Lại Ốc, Văn Giang, Hưng Yên"),
    ]
    session.add_all(khoa_list)
    await session.commit()
