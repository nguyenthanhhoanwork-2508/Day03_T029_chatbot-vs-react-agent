"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.

Hai bộ dữ liệu đang phục vụ đề tài HƯỚNG NGHIỆP:
1. data/job_market_vn.json          - xu hướng tuyển dụng (năm -> nhóm ngành -> vùng)
2. data/university_admissions_vn.json - tuyển sinh đại học (vùng -> trường -> ngành)
"""

import json
import os
import unicodedata

# ---------------------------------------------------------------------------
# 📦 NẠP DỮ LIỆU (load 1 lần rồi cache lại để không đọc file mỗi lần gọi tool)
# ---------------------------------------------------------------------------

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BASE_DIR, "data")

_JSON_CACHE = {}


def _load_json(file_name: str):
    """Đọc một file JSON trong thư mục data/ (có cache theo tên file)."""
    if file_name not in _JSON_CACHE:
        with open(os.path.join(_DATA_DIR, file_name), "r", encoding="utf-8") as f:
            _JSON_CACHE[file_name] = json.load(f)
    return _JSON_CACHE[file_name]


def _load_data():
    """Dữ liệu xu hướng tuyển dụng."""
    return _load_json("job_market_vn.json")


def _load_admissions():
    """Dữ liệu tuyển sinh đại học."""
    return _load_json("university_admissions_vn.json")


# ---------------------------------------------------------------------------
# 🔍 CHUẨN HOÁ & NHẬN DIỆN THAM SỐ (người dùng gõ "HCM", "IT", "phía Bắc"...)
# ---------------------------------------------------------------------------

def _norm(text: str) -> str:
    """Bỏ dấu tiếng Việt, đưa về chữ thường để so khớp linh hoạt."""
    text = str(text).lower().strip().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


# Từ khoá nhận diện vùng miền -> tên vùng chuẩn trong file JSON
_REGION_ALIASES = {
    "Miền Bắc": ["mien bac", "phia bac", "bac bo", "ha noi", "hanoi", "bac ninh",
                 "hai phong", "north", "hn", "bac"],
    "Miền Trung": ["mien trung", "phia trung", "trung bo", "da nang", "danang",
                   "hue", "khanh hoa", "nha trang", "central", "trung"],
    "Miền Nam": ["mien nam", "phia nam", "nam bo", "ho chi minh", "tp.hcm", "tphcm",
                 "sai gon", "saigon", "binh duong", "dong nai", "can tho",
                 "south", "hcm", "nam"],
}

# Từ khoá nhận diện nhóm ngành -> tên ngành chuẩn trong file JSON
_INDUSTRY_ALIASES = {
    "IT - Phần mềm": ["cong nghe thong tin", "phan mem", "lap trinh", "software",
                      "developer", "cntt", "tech", "it", "dev"],
    "Quản trị - Nhân sự": ["quan tri nhan su", "nhan su", "quan tri", "hanh chinh",
                           "human resource", "tuyen dung", "hr"],
    "Kinh tế - Tài chính - Ngân hàng": ["tai chinh ngan hang", "ngan hang", "tai chinh",
                                        "kinh te", "ke toan", "kiem toan", "chung khoan",
                                        "banking", "finance", "accounting"],
    "Marketing - Truyền thông": ["truyen thong", "quang cao", "marketing", "content",
                                 "digital", "media", "pr"],
    "Sản xuất - Cơ khí": ["san xuat", "co khi", "manufacturing", "nha may",
                          "ky thuat", "engineering", "production"],
}


def _match(value: str, aliases: dict):
    """Tìm giá trị chuẩn khớp với chuỗi người dùng nhập. Trả None nếu không khớp."""
    query = _norm(value)
    if not query:
        return None

    # Ưu tiên khớp đúng tên chuẩn trước
    for canonical in aliases:
        if _norm(canonical) == query:
            return canonical

    # Sau đó khớp theo từ khoá, alias dài được xét trước để tránh nhầm lẫn
    candidates = sorted(
        ((alias, canonical) for canonical, keys in aliases.items() for alias in keys),
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    for alias, canonical in candidates:
        if alias in query:
            return canonical
    return None


def _parse_year(year):
    """Ép kiểu năm về int. Trả None nếu không hợp lệ."""
    try:
        return int(str(year).strip())
    except (TypeError, ValueError):
        return None


def _available_years():
    return [y["year"] for y in _load_data()["years"]]


def _num(value: int) -> str:
    """Định dạng số kiểu Việt Nam: 18500 -> 18.500"""
    return f"{value:,}".replace(",", ".")


def _arrow(growth_pct: float) -> str:
    return "📈" if growth_pct > 0 else ("📉" if growth_pct < 0 else "➖")


def _lookup(year: int, industry: str, region: str):
    """Lấy đúng 1 dòng dữ liệu (năm, ngành, vùng). Trả None nếu không có."""
    for year_block in _load_data()["years"]:
        if year_block["year"] != year:
            continue
        for industry_block in year_block["industries"]:
            if industry_block["industry"] != industry:
                continue
            for region_row in industry_block["regions"]:
                if region_row["region"] == region:
                    return region_row
    return None


# ---------------------------------------------------------------------------
# 🧰 CÁC TOOL AGENT ĐƯỢC PHÉP GỌI
# ---------------------------------------------------------------------------

def get_job_market_trend(industry: str, region: str, year=2025) -> str:
    """
    Tra cứu xu hướng tuyển dụng của MỘT nhóm ngành tại MỘT vùng miền trong một năm.

    Args:
        industry (str): Nhóm ngành (Ví dụ: 'IT', 'Tài chính - Ngân hàng', 'Sản xuất')
        region (str): Vùng miền (Ví dụ: 'Miền Bắc', 'Miền Nam', 'TP.HCM', 'Đà Nẵng')
        year (int): Năm cần tra cứu, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Số tin tuyển dụng, mức tăng/giảm so với năm trước và nhãn xu hướng.
    """
    matched_industry = _match(industry, _INDUSTRY_ALIASES)
    if matched_industry is None:
        return (f"LỖI: Không nhận diện được nhóm ngành '{industry}'. "
                f"Các nhóm ngành có sẵn: {', '.join(_INDUSTRY_ALIASES)}.")

    matched_region = _match(region, _REGION_ALIASES)
    if matched_region is None:
        return (f"LỖI: Không nhận diện được vùng miền '{region}'. "
                f"Các vùng có sẵn: {', '.join(_REGION_ALIASES)}.")

    parsed_year = _parse_year(year)
    if parsed_year not in _available_years():
        return (f"LỖI: Không có dữ liệu cho năm '{year}'. "
                f"Chỉ hỗ trợ các năm: {', '.join(map(str, _available_years()))}.")

    row = _lookup(parsed_year, matched_industry, matched_region)
    if row is None:
        return (f"LỖI: Không tìm thấy dữ liệu cho {matched_industry} - "
                f"{matched_region} năm {parsed_year}.")

    return (
        f"Xu hướng tuyển dụng {matched_industry} tại {matched_region} năm {parsed_year}:\n"
        f"- Số tin tuyển dụng: {_num(row['job_postings'])} tin\n"
        f"- Thay đổi so với năm {parsed_year - 1}: {row['growth_pct']:+.1f}% "
        f"{_arrow(row['growth_pct'])}\n"
        f"- Đánh giá xu hướng: {row['trend'].upper()}"
    )


def compare_regions_by_industry(industry: str, year=2025) -> str:
    """
    So sánh xu hướng tuyển dụng của MỘT nhóm ngành trên TẤT CẢ các vùng miền.
    Dùng khi cần biết vùng nào tuyển nhiều nhất / tăng trưởng mạnh nhất.

    Args:
        industry (str): Nhóm ngành (Ví dụ: 'IT', 'Marketing', 'Sản xuất - Cơ khí')
        year (int): Năm cần so sánh, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Bảng xếp hạng các vùng miền theo mức tăng trưởng tuyển dụng.
    """
    matched_industry = _match(industry, _INDUSTRY_ALIASES)
    if matched_industry is None:
        return (f"LỖI: Không nhận diện được nhóm ngành '{industry}'. "
                f"Các nhóm ngành có sẵn: {', '.join(_INDUSTRY_ALIASES)}.")

    parsed_year = _parse_year(year)
    if parsed_year not in _available_years():
        return (f"LỖI: Không có dữ liệu cho năm '{year}'. "
                f"Chỉ hỗ trợ các năm: {', '.join(map(str, _available_years()))}.")

    rows = []
    for region in _REGION_ALIASES:
        row = _lookup(parsed_year, matched_industry, region)
        if row is not None:
            rows.append(row)

    rows.sort(key=lambda r: r["growth_pct"], reverse=True)
    lines = [f"So sánh tuyển dụng ngành {matched_industry} theo vùng miền năm {parsed_year}:"]
    for rank, row in enumerate(rows, start=1):
        lines.append(
            f"{rank}. {row['region']}: {_num(row['job_postings'])} tin, "
            f"{row['growth_pct']:+.1f}% {_arrow(row['growth_pct'])} ({row['trend']})"
        )
    lines.append(f"=> Vùng tăng trưởng mạnh nhất: {rows[0]['region']} "
                 f"({rows[0]['growth_pct']:+.1f}%)")
    return "\n".join(lines)


def get_top_industries_by_region(region: str, year=2025) -> str:
    """
    Xếp hạng TẤT CẢ các nhóm ngành tại MỘT vùng miền theo mức tăng trưởng tuyển dụng.
    Dùng khi cần tư vấn nên học/chuyển sang ngành nào ở một khu vực.

    Args:
        region (str): Vùng miền (Ví dụ: 'Miền Bắc', 'TP.HCM', 'Đà Nẵng')
        year (int): Năm cần tra cứu, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Danh sách nhóm ngành xếp theo mức tăng trưởng giảm dần.
    """
    matched_region = _match(region, _REGION_ALIASES)
    if matched_region is None:
        return (f"LỖI: Không nhận diện được vùng miền '{region}'. "
                f"Các vùng có sẵn: {', '.join(_REGION_ALIASES)}.")

    parsed_year = _parse_year(year)
    if parsed_year not in _available_years():
        return (f"LỖI: Không có dữ liệu cho năm '{year}'. "
                f"Chỉ hỗ trợ các năm: {', '.join(map(str, _available_years()))}.")

    rows = []
    for industry in _INDUSTRY_ALIASES:
        row = _lookup(parsed_year, industry, matched_region)
        if row is not None:
            rows.append((industry, row))

    rows.sort(key=lambda item: item[1]["growth_pct"], reverse=True)
    lines = [f"Xếp hạng nhóm ngành tại {matched_region} năm {parsed_year} "
             f"(theo mức tăng trưởng tuyển dụng):"]
    for rank, (industry, row) in enumerate(rows, start=1):
        lines.append(
            f"{rank}. {industry}: {_num(row['job_postings'])} tin, "
            f"{row['growth_pct']:+.1f}% {_arrow(row['growth_pct'])} ({row['trend']})"
        )
    return "\n".join(lines)


def list_job_market_options() -> str:
    """
    Liệt kê các giá trị hợp lệ của bộ dữ liệu (năm, nhóm ngành, vùng miền).
    Agent nên gọi tool này khi không chắc tham số nào được hỗ trợ.

    Returns:
        str: Danh sách năm, nhóm ngành và vùng miền có trong dữ liệu.
    """
    return (
        "Bộ dữ liệu xu hướng tuyển dụng Việt Nam hỗ trợ:\n"
        f"- Năm: {', '.join(map(str, _available_years()))}\n"
        f"- Nhóm ngành: {', '.join(_INDUSTRY_ALIASES)}\n"
        f"- Vùng miền: {', '.join(_REGION_ALIASES)}"
    )


# ===========================================================================
# 🎓 TUYỂN SINH ĐẠI HỌC (data/university_admissions_vn.json)
# ===========================================================================

# Từ khoá nhận diện trường -> mã trường trong file JSON.
# Lưu ý: có 3 trường "Bách khoa" nên alias phải kèm địa danh để không nhập nhằng.
_UNIVERSITY_ALIASES = {
    "BKA": ["bach khoa ha noi", "bach khoa hn", "bkhn", "hust", "bka"],
    "NEU": ["kinh te quoc dan", "ktqd", "neu"],
    "UET": ["cong nghe dhqghn", "cong nghe ha noi", "uet"],
    "BAV": ["hoc vien ngan hang", "hvnh", "bav"],
    "TMU": ["dai hoc thuong mai", "thuong mai", "tmu"],
    "DDK": ["bach khoa da nang", "bach khoa dn", "ddk"],
    "DDQ": ["kinh te da nang", "kinh te dn", "ddq"],
    "DHT": ["khoa hoc hue", "dai hoc hue", "dht"],
    "QSB": ["bach khoa tp.hcm", "bach khoa tphcm", "bach khoa ho chi minh",
            "bach khoa sai gon", "qsb"],
    "UIT": ["cong nghe thong tin dhqg", "cong nghe thong tin tp.hcm", "uit"],
    "UEH": ["kinh te tp.hcm", "kinh te tphcm", "kinh te ho chi minh", "ueh"],
    "TCT": ["dai hoc can tho", "can tho", "tct"],
}

# Gom ngành đào tạo về nhóm ngành (trùng tên với nhóm ngành của job_market_vn.json
# để agent đối chiếu được điểm chuẩn với xu hướng tuyển dụng).
_MAJOR_GROUP_ALIASES = {
    "IT - Phần mềm": ["khoa hoc may tinh", "cong nghe thong tin", "tri tue nhan tao",
                      "ky thuat phan mem", "khoa hoc du lieu", "an toan thong tin",
                      "mang may tinh"],
    "Quản trị - Nhân sự": ["quan tri nhan luc", "quan tri kinh doanh", "nhan luc", "quan tri"],
    "Kinh tế - Tài chính - Ngân hàng": ["kinh doanh quoc te", "luat kinh te", "tai chinh",
                                        "ngan hang", "ke toan", "kinh te"],
    "Marketing - Truyền thông": ["marketing", "bao chi", "truyen thong"],
    "Sản xuất - Cơ khí": ["ky thuat dien tu", "dien tu - vien thong", "ky thuat xay dung",
                          "ky thuat nang luong", "ky thuat vat lieu", "ky thuat hoa hoc",
                          "ky thuat o to", "co dien tu", "ky thuat dien", "co khi"],
}

_OTHER_GROUP = "Ngành khác"


def _major_group(major_name: str) -> str:
    """Xác định nhóm ngành của một ngành đào tạo."""
    return _match(major_name, _MAJOR_GROUP_ALIASES) or _OTHER_GROUP


def _all_majors():
    """Trả về danh sách phẳng (vùng, trường, ngành, nhóm ngành) của toàn bộ dữ liệu."""
    rows = []
    for region_block in _load_admissions()["regions"]:
        for university in region_block["universities"]:
            for major in university["majors"]:
                rows.append({
                    "region": region_block["region"],
                    "university": university,
                    "major": major,
                    "group": _major_group(major["major_name"]),
                })
    return rows


def _admission_years():
    return _load_admissions()["meta"]["years_covered"]


def _latest_admission_year():
    """Năm mới nhất - chỉ năm này mới có dữ liệu biến động & mức cạnh tranh."""
    return max(_admission_years())


def _benchmark(major: dict, year: int) -> float:
    return major[f"benchmark_{year}"]


def _match_university(value: str):
    """
    Tìm trường theo mã hoặc tên. Trả về (university_dict, region, error_message).
    Nếu nhập mơ hồ (ví dụ 'bách khoa') sẽ trả lỗi kèm danh sách trường trùng khớp.
    """
    query = _norm(value)
    matches = []
    for region_block in _load_admissions()["regions"]:
        for university in region_block["universities"]:
            code = university["university_code"]
            haystack = _norm(f"{code} {university['university_name']} {university['city']}")
            aliases = _UNIVERSITY_ALIASES.get(code, [])
            if query == _norm(code) or any(alias in query for alias in aliases):
                return university, region_block["region"], None
            if query and query in haystack:
                matches.append((university, region_block["region"]))

    if len(matches) == 1:
        return matches[0][0], matches[0][1], None
    if len(matches) > 1:
        names = ", ".join(f"{u['university_code']} ({u['university_name']})" for u, _ in matches)
        return None, None, (f"LỖI: Tên trường '{value}' bị trùng với nhiều trường. "
                            f"Vui lòng nêu rõ một trong các trường sau: {names}.")

    all_codes = ", ".join(_UNIVERSITY_ALIASES)
    return None, None, (f"LỖI: Không tìm thấy trường '{value}'. "
                        f"Các mã trường có sẵn: {all_codes}. "
                        f"Gọi list_admission_options để xem tên đầy đủ.")


def _check_admission_year(year):
    """Trả về (year_int, error_message)."""
    parsed = _parse_year(year)
    if parsed not in _admission_years():
        return None, (f"LỖI: Không có dữ liệu tuyển sinh năm '{year}'. "
                      f"Chỉ hỗ trợ các năm: {', '.join(map(str, _admission_years()))}.")
    return parsed, None


def _format_major_line(row: dict, year: int, show_school: bool = True) -> str:
    """
    Một dòng kết quả: tên ngành, điểm chuẩn, biến động, mức cạnh tranh.
    benchmark_change và competition_level trong dữ liệu đều tính theo năm mới nhất,
    nên chỉ hiển thị khi tra cứu đúng năm đó để tránh gán nhầm cho năm cũ.
    """
    major = row["major"]
    score = _benchmark(major, year)
    parts = [f"{major['major_name']}"]
    if show_school:
        parts.append(f"({row['university']['university_code']} - {row['region']})")
    line = " ".join(parts) + f": {score} điểm"
    if year == _latest_admission_year():
        line += (f" ({major['benchmark_change']:+.1f} {_arrow(major['benchmark_change'])} "
                 f"{major['benchmark_trend']})")
    line += f" | khối {'/'.join(major['exam_blocks'])}"
    if year == _latest_admission_year():
        line += f" | cạnh tranh {major['competition_level']}"
    return line


def _overall_direction(changes: list) -> str:
    """Xu hướng chung từ biến động điểm chuẩn trung bình."""
    if not changes:
        return "không xác định"
    avg = sum(changes) / len(changes)
    if avg >= 0.2:
        return "TĂNG"
    if avg <= -0.2:
        return "GIẢM"
    return "ỔN ĐỊNH"


def get_admission_by_university(university: str, year=2025) -> str:
    """
    Tra cứu điểm chuẩn và xu hướng điểm của TẤT CẢ các ngành trong MỘT trường đại học.

    Args:
        university (str): Tên hoặc mã trường (Ví dụ: 'Bách khoa Hà Nội', 'UIT', 'ĐH Cần Thơ')
        year (int): Năm tuyển sinh, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Danh sách ngành kèm điểm chuẩn, mức tăng/giảm so với năm trước và độ cạnh tranh.
    """
    matched, region, error = _match_university(university)
    if error:
        return error

    parsed_year, error = _check_admission_year(year)
    if error:
        return error

    rows = [r for r in _all_majors() if r["university"]["university_code"] == matched["university_code"]]
    rows.sort(key=lambda r: _benchmark(r["major"], parsed_year), reverse=True)
    changes = [r["major"]["benchmark_change"] for r in rows]
    scores = [_benchmark(r["major"], parsed_year) for r in rows]

    lines = [
        f"{matched['university_name']} ({matched['university_code']}) - {matched['city']}, {region}",
        f"Loại hình: {matched['type']} | Học phí: {matched['tuition_million_vnd_per_year']} triệu/năm",
        f"Phương thức xét tuyển: {', '.join(matched['admission_methods'])}",
        f"Điểm chuẩn {parsed_year} ({len(rows)} ngành, từ {min(scores)} đến {max(scores)} điểm):",
    ]
    for rank, row in enumerate(rows, start=1):
        lines.append(f"{rank}. {_format_major_line(row, parsed_year, show_school=False)} "
                     f"| chỉ tiêu {row['major']['quota_2025']} | nhóm ngành: {row['group']}")
    if parsed_year == _latest_admission_year():
        lines.append(f"=> Xu hướng điểm chuẩn chung của trường: {_overall_direction(changes)} "
                     f"({sum(changes) / len(changes):+.2f} điểm/ngành so với {parsed_year - 1})")
    return "\n".join(lines)


def get_admission_by_region(region: str, year=2025) -> str:
    """
    Tra cứu mặt bằng điểm chuẩn và xu hướng của TẤT CẢ các trường trong MỘT vùng miền.
    Dùng khi học sinh muốn học ở một khu vực nhưng chưa biết chọn trường nào.

    Args:
        region (str): Vùng miền (Ví dụ: 'Miền Bắc', 'Miền Nam', 'Đà Nẵng', 'TP.HCM')
        year (int): Năm tuyển sinh, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Thống kê điểm chuẩn của vùng và danh sách trường kèm dải điểm từng trường.
    """
    matched_region = _match(region, _REGION_ALIASES)
    if matched_region is None:
        return (f"LỖI: Không nhận diện được vùng miền '{region}'. "
                f"Các vùng có sẵn: {', '.join(_REGION_ALIASES)}.")

    parsed_year, error = _check_admission_year(year)
    if error:
        return error

    rows = [r for r in _all_majors() if r["region"] == matched_region]
    scores = [_benchmark(r["major"], parsed_year) for r in rows]
    changes = [r["major"]["benchmark_change"] for r in rows]
    up = sum(1 for r in rows if r["major"]["benchmark_trend"] == "tăng")
    down = sum(1 for r in rows if r["major"]["benchmark_trend"] == "giảm")
    flat = len(rows) - up - down

    lowest = min(rows, key=lambda r: _benchmark(r["major"], parsed_year))
    highest = max(rows, key=lambda r: _benchmark(r["major"], parsed_year))

    lines = [
        f"Điểm chuẩn & xu hướng tuyển sinh tại {matched_region} năm {parsed_year}:",
        f"- Quy mô: {len({r['university']['university_code'] for r in rows})} trường, {len(rows)} ngành",
        f"- Điểm chuẩn: thấp nhất {min(scores)} ({lowest['major']['major_name']} - "
        f"{lowest['university']['university_code']}), cao nhất {max(scores)} "
        f"({highest['major']['major_name']} - {highest['university']['university_code']}), "
        f"trung bình {sum(scores) / len(scores):.1f}",
    ]
    if parsed_year == _latest_admission_year():
        lines.append(f"- Biến động so với {parsed_year - 1}: {up} ngành tăng điểm, "
                     f"{flat} ngành ổn định, {down} ngành giảm "
                     f"=> xu hướng chung: {_overall_direction(changes)}")
    lines.append("Chi tiết theo trường:")

    for region_block in _load_admissions()["regions"]:
        if region_block["region"] != matched_region:
            continue
        universities = sorted(
            region_block["universities"],
            key=lambda u: max(_benchmark(m, parsed_year) for m in u["majors"]),
            reverse=True,
        )
        for rank, university in enumerate(universities, start=1):
            uni_scores = [_benchmark(m, parsed_year) for m in university["majors"]]
            lines.append(
                f"{rank}. {university['university_code']} - {university['university_name']} "
                f"({university['city']}): {len(uni_scores)} ngành, điểm {min(uni_scores)}-{max(uni_scores)}, "
                f"học phí {university['tuition_million_vnd_per_year']} triệu/năm"
            )
    return "\n".join(lines)


def get_admission_by_major_group(major_group: str, region="", year=2025) -> str:
    """
    Tra cứu điểm chuẩn và xu hướng của MỘT nhóm ngành trên cả nước (hoặc trong 1 vùng).
    Dùng khi học sinh đã biết mình thích lĩnh vực nào và cần biết cần bao nhiêu điểm.

    Args:
        major_group (str): Nhóm ngành (Ví dụ: 'IT', 'Kinh tế - Tài chính', 'Marketing',
                           'Quản trị - Nhân sự', 'Sản xuất - Cơ khí')
        region (str): Lọc theo vùng miền, để trống nghĩa là xét toàn quốc.
        year (int): Năm tuyển sinh, mặc định 2025. Dữ liệu có sẵn: 2024, 2025.

    Returns:
        str: Danh sách ngành thuộc nhóm, xếp theo điểm chuẩn giảm dần, kèm xu hướng chung.
    """
    # Tên 5 nhóm ngành trùng với nhóm ngành của job_market_vn.json nên dùng lại
    # bộ từ khoá _INDUSTRY_ALIASES để hiểu cách người dùng gõ ('IT', 'HR', 'ngân hàng'...)
    if _norm(major_group) in (_norm(_OTHER_GROUP), "khac"):
        matched_group = _OTHER_GROUP
    else:
        matched_group = _match(major_group, _INDUSTRY_ALIASES)
    if matched_group is None:
        return (f"LỖI: Không nhận diện được nhóm ngành '{major_group}'. "
                f"Các nhóm ngành có sẵn: {', '.join(_MAJOR_GROUP_ALIASES)}, {_OTHER_GROUP}.")

    parsed_year, error = _check_admission_year(year)
    if error:
        return error

    matched_region = None
    if str(region).strip():
        matched_region = _match(region, _REGION_ALIASES)
        if matched_region is None:
            return (f"LỖI: Không nhận diện được vùng miền '{region}'. "
                    f"Các vùng có sẵn: {', '.join(_REGION_ALIASES)}.")

    rows = [r for r in _all_majors() if r["group"] == matched_group]
    if matched_region:
        rows = [r for r in rows if r["region"] == matched_region]
    if not rows:
        return (f"LỖI: Không có ngành nào thuộc nhóm {matched_group} tại {matched_region}.")

    rows.sort(key=lambda r: _benchmark(r["major"], parsed_year), reverse=True)
    scores = [_benchmark(r["major"], parsed_year) for r in rows]
    changes = [r["major"]["benchmark_change"] for r in rows]

    scope = matched_region if matched_region else "toàn quốc"
    lines = [f"Nhóm ngành {matched_group} - điểm chuẩn {parsed_year} ({scope}, {len(rows)} ngành):"]
    for rank, row in enumerate(rows, start=1):
        lines.append(f"{rank}. {_format_major_line(row, parsed_year)} "
                     f"| học phí {row['university']['tuition_million_vnd_per_year']} triệu/năm")
    summary = (f"=> Dải điểm: {min(scores)} - {max(scores)} "
               f"| Trung bình: {sum(scores) / len(scores):.1f}")
    if parsed_year == _latest_admission_year():
        summary += (f" | Xu hướng chung: {_overall_direction(changes)} "
                    f"({sum(changes) / len(changes):+.2f} điểm/ngành so với {parsed_year - 1})")
    lines.append(summary)
    return "\n".join(lines)


def list_admission_options() -> str:
    """
    Liệt kê các giá trị hợp lệ của dữ liệu tuyển sinh (năm, vùng, trường, nhóm ngành).
    Agent nên gọi tool này khi không chắc tên trường hoặc nhóm ngành nào được hỗ trợ.

    Returns:
        str: Danh sách năm, vùng miền, trường (kèm mã) và nhóm ngành.
    """
    lines = [
        "Dữ liệu tuyển sinh đại học hỗ trợ:",
        f"- Năm: {', '.join(map(str, _admission_years()))}",
        f"- Nhóm ngành: {', '.join(_MAJOR_GROUP_ALIASES)}, {_OTHER_GROUP}",
        "- Trường theo vùng miền:",
    ]
    for region_block in _load_admissions()["regions"]:
        names = ", ".join(f"{u['university_code']} ({u['university_name']})"
                          for u in region_block["universities"])
        lines.append(f"  + {region_block['region']}: {names}")
    return "\n".join(lines)


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    # Xu hướng tuyển dụng
    "get_job_market_trend": get_job_market_trend,
    "compare_regions_by_industry": compare_regions_by_industry,
    "get_top_industries_by_region": get_top_industries_by_region,
    "list_job_market_options": list_job_market_options,
    # Tuyển sinh đại học
    "get_admission_by_university": get_admission_by_university,
    "get_admission_by_region": get_admission_by_region,
    "get_admission_by_major_group": get_admission_by_major_group,
    "list_admission_options": list_admission_options,
}
