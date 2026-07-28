"""
🧪 TEST SUITE CHO TOOL REGISTRY & DỮ LIỆU (Role 2 + Role 5)

Chạy:
    .venv/Scripts/python.exe tests/test_tools.py          # in báo cáo tool + chạy test
    .venv/Scripts/python.exe -m unittest discover tests   # chỉ chạy test

Nội dung kiểm tra:
    1. TestToolRegistry      - danh sách tool & chất lượng description (docstring)
    2. TestJobMarketSchema   - schema data/job_market_vn.json
    3. TestAdmissionsSchema  - schema data/university_admissions_vn.json
    4. TestJobMarketTools    - hành vi 4 tool xu hướng tuyển dụng
    5. TestAdmissionTools    - hành vi 4 tool tuyển sinh đại học
    6. TestCrossDataset      - khả năng nối 2 bộ dữ liệu qua nhóm ngành
"""

import inspect
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import tools  # noqa: E402


# ---------------------------------------------------------------------------
# 📋 BÁO CÁO DANH SÁCH TOOL & DESCRIPTION
# ---------------------------------------------------------------------------

def print_tool_report():
    """In bảng tool đang đăng ký: tên, tham số, mô tả ngắn (dòng đầu docstring)."""
    print("=" * 78)
    print(f"📋 TOOL REGISTRY REPORT — {len(tools.AVAILABLE_TOOLS)} tool đang đăng ký")
    print("=" * 78)
    for index, (name, func) in enumerate(tools.AVAILABLE_TOOLS.items(), start=1):
        signature = str(inspect.signature(func))
        summary = (inspect.getdoc(func) or "").strip().split("\n")[0]
        print(f"\n{index}. {name}{signature}")
        print(f"   → {summary}")
        for line in (inspect.getdoc(func) or "").splitlines():
            stripped = line.strip()
            if stripped.startswith(("industry ", "region ", "year ", "university ", "major_group ")):
                print(f"     · {stripped}")
    print("\n" + "=" * 78 + "\n")


# ---------------------------------------------------------------------------
# 1. TOOL REGISTRY & DESCRIPTION
# ---------------------------------------------------------------------------

class TestToolRegistry(unittest.TestCase):
    """Agent chỉ dùng được tool nếu description đủ rõ -> bắt buộc kiểm tra docstring."""

    EXPECTED_TOOLS = {
        "get_job_market_trend",
        "compare_regions_by_industry",
        "get_top_industries_by_region",
        "list_job_market_options",
        "get_admission_by_university",
        "get_admission_by_region",
        "get_admission_by_major_group",
        "list_admission_options",
    }

    def test_dang_ky_du_8_tool(self):
        self.assertEqual(set(tools.AVAILABLE_TOOLS), self.EXPECTED_TOOLS)

    def test_moi_tool_deu_callable(self):
        for name, func in tools.AVAILABLE_TOOLS.items():
            with self.subTest(tool=name):
                self.assertTrue(callable(func))

    def test_key_registry_trung_ten_ham(self):
        """Tránh trường hợp agent gọi đúng tên nhưng registry map sang hàm khác."""
        for name, func in tools.AVAILABLE_TOOLS.items():
            with self.subTest(tool=name):
                self.assertEqual(name, func.__name__)

    def test_moi_tool_co_docstring_du_dai(self):
        for name, func in tools.AVAILABLE_TOOLS.items():
            with self.subTest(tool=name):
                doc = inspect.getdoc(func)
                self.assertIsNotNone(doc, f"{name} thiếu docstring")
                self.assertGreaterEqual(len(doc), 60, f"{name} có description quá ngắn")

    def test_docstring_mo_ta_gia_tri_tra_ve(self):
        for name, func in tools.AVAILABLE_TOOLS.items():
            with self.subTest(tool=name):
                self.assertIn("Returns:", inspect.getdoc(func))

    def test_tool_co_tham_so_phai_mo_ta_args(self):
        for name, func in tools.AVAILABLE_TOOLS.items():
            if not inspect.signature(func).parameters:
                continue
            with self.subTest(tool=name):
                doc = inspect.getdoc(func)
                self.assertIn("Args:", doc)
                for param in inspect.signature(func).parameters:
                    self.assertIn(param, doc, f"{name} chưa mô tả tham số '{param}'")

    def test_moi_tool_tra_ve_chuoi(self):
        """ReAct loop ghép Observation dạng text nên tool phải trả str."""
        samples = {
            "get_job_market_trend": ("IT", "Miền Nam"),
            "compare_regions_by_industry": ("IT",),
            "get_top_industries_by_region": ("Miền Bắc",),
            "list_job_market_options": (),
            "get_admission_by_university": ("UIT",),
            "get_admission_by_region": ("Miền Nam",),
            "get_admission_by_major_group": ("IT",),
            "list_admission_options": (),
        }
        for name, args in samples.items():
            with self.subTest(tool=name):
                self.assertIsInstance(tools.AVAILABLE_TOOLS[name](*args), str)


# ---------------------------------------------------------------------------
# 2. SCHEMA: data/job_market_vn.json
# ---------------------------------------------------------------------------

class TestJobMarketSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = tools._load_data()
        cls.rows = [(y["year"], i["industry"], r)
                    for y in cls.data["years"]
                    for i in y["industries"]
                    for r in i["regions"]]

    @staticmethod
    def expected_trend(growth):
        if growth >= 10:
            return "tăng mạnh"
        if growth >= 3:
            return "tăng"
        if growth > -3:
            return "ổn định"
        if growth > -10:
            return "giảm"
        return "giảm mạnh"

    def test_co_dung_30_row(self):
        self.assertEqual(len(self.rows), 30)

    def test_cau_truc_nam_nganh_vung(self):
        self.assertEqual([y["year"] for y in self.data["years"]], [2024, 2025])
        for year_block in self.data["years"]:
            self.assertEqual(len(year_block["industries"]), 5)
            for industry_block in year_block["industries"]:
                self.assertEqual(len(industry_block["regions"]), 3)

    def test_moi_row_du_truong_bat_buoc(self):
        for year, industry, row in self.rows:
            with self.subTest(year=year, industry=industry, region=row["region"]):
                self.assertIn("job_postings", row)
                self.assertIn("growth_pct", row)
                self.assertIn("trend", row)
                self.assertIsInstance(row["job_postings"], int)
                self.assertGreater(row["job_postings"], 0)

    def test_growth_pct_2025_khop_so_lieu_2_nam(self):
        """Trend đã precal nên phải khớp tuyệt đối với job_postings hai năm."""
        base = {(i, r["region"]): r["job_postings"] for y, i, r in self.rows if y == 2024}
        for year, industry, row in self.rows:
            if year != 2025:
                continue
            prev = base[(industry, row["region"])]
            expected = round((row["job_postings"] - prev) / prev * 100, 1)
            with self.subTest(industry=industry, region=row["region"]):
                self.assertAlmostEqual(row["growth_pct"], expected, delta=0.05)

    def test_nhan_trend_khop_nguong(self):
        for year, industry, row in self.rows:
            with self.subTest(year=year, industry=industry, region=row["region"]):
                self.assertEqual(row["trend"], self.expected_trend(row["growth_pct"]))

    def test_meta_ghi_ro_disclaimer_du_lieu_mo_phong(self):
        self.assertIn("MÔ PHỎNG", self.data["meta"]["disclaimer"])
        self.assertEqual(self.data["meta"]["row_count"], len(self.rows))


# ---------------------------------------------------------------------------
# 3. SCHEMA: data/university_admissions_vn.json
# ---------------------------------------------------------------------------

class TestAdmissionsSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = tools._load_admissions()
        cls.rows = tools._all_majors()

    @staticmethod
    def expected_trend(change):
        if change >= 0.3:
            return "tăng"
        if change <= -0.3:
            return "giảm"
        return "ổn định"

    @staticmethod
    def expected_competition(score):
        if score >= 27:
            return "rất cao"
        if score >= 24:
            return "cao"
        if score >= 20:
            return "trung bình"
        return "dễ thở"

    def test_quy_mo_3_vung_12_truong_53_nganh(self):
        universities = [u for r in self.data["regions"] for u in r["universities"]]
        self.assertEqual(len(self.data["regions"]), 3)
        self.assertEqual(len(universities), 12)
        self.assertEqual(len(self.rows), 53)

    def test_meta_khop_so_dem_thuc_te(self):
        universities = [u for r in self.data["regions"] for u in r["universities"]]
        self.assertEqual(self.data["meta"]["university_count"], len(universities))
        self.assertEqual(self.data["meta"]["major_row_count"], len(self.rows))

    def test_diem_chuan_nam_trong_thang_30(self):
        for row in self.rows:
            with self.subTest(major=row["major"]["major_name"]):
                for year in (2024, 2025):
                    score = row["major"][f"benchmark_{year}"]
                    self.assertGreaterEqual(score, 15.0)
                    self.assertLessEqual(score, 30.0)

    def test_benchmark_change_khop_hieu_2_nam(self):
        for row in self.rows:
            major = row["major"]
            expected = round(major["benchmark_2025"] - major["benchmark_2024"], 1)
            with self.subTest(major=major["major_name"], uni=row["university"]["university_code"]):
                self.assertAlmostEqual(major["benchmark_change"], expected, delta=0.001)

    def test_benchmark_trend_khop_nguong(self):
        for row in self.rows:
            major = row["major"]
            with self.subTest(major=major["major_name"]):
                self.assertEqual(major["benchmark_trend"],
                                 self.expected_trend(major["benchmark_change"]))

    def test_competition_level_khop_diem_2025(self):
        for row in self.rows:
            major = row["major"]
            with self.subTest(major=major["major_name"]):
                self.assertEqual(major["competition_level"],
                                 self.expected_competition(major["benchmark_2025"]))

    def test_khoi_thi_ton_tai_trong_dimensions(self):
        valid = {b["code"] for b in self.data["dimensions"]["exam_blocks"]}
        for row in self.rows:
            with self.subTest(major=row["major"]["major_name"]):
                self.assertTrue(set(row["major"]["exam_blocks"]).issubset(valid))

    def test_loai_truong_va_phuong_thuc_xet_tuyen_hop_le(self):
        dim = self.data["dimensions"]
        for region_block in self.data["regions"]:
            for university in region_block["universities"]:
                with self.subTest(uni=university["university_code"]):
                    self.assertIn(university["type"], dim["university_types"])
                    self.assertTrue(set(university["admission_methods"])
                                    .issubset(set(dim["admission_methods"])))

    def test_ma_truong_khong_trung(self):
        codes = [u["university_code"] for r in self.data["regions"] for u in r["universities"]]
        self.assertEqual(len(codes), len(set(codes)))

    def test_ma_nganh_khong_trung_trong_cung_truong(self):
        for region_block in self.data["regions"]:
            for university in region_block["universities"]:
                codes = [m["major_code"] for m in university["majors"]]
                with self.subTest(uni=university["university_code"]):
                    self.assertEqual(len(codes), len(set(codes)))

    def test_moi_vung_phu_du_dai_diem(self):
        """Học sinh điểm nào cũng phải có gợi ý -> mỗi vùng cần cả ngành thấp và cao."""
        for region_block in self.data["regions"]:
            scores = [m["benchmark_2025"] for u in region_block["universities"] for m in u["majors"]]
            with self.subTest(region=region_block["region"]):
                self.assertTrue(any(s < 21 for s in scores), "thiếu ngành điểm thấp")
                self.assertTrue(any(s >= 26 for s in scores), "thiếu ngành điểm cao")

    def test_meta_ghi_ro_disclaimer_du_lieu_mo_phong(self):
        self.assertIn("MÔ PHỎNG", self.data["meta"]["disclaimer"])


# ---------------------------------------------------------------------------
# 4. HÀNH VI TOOL: XU HƯỚNG TUYỂN DỤNG
# ---------------------------------------------------------------------------

class TestJobMarketTools(unittest.TestCase):

    # --- 🟢 Case đơn giản: tra cứu trực tiếp ---

    def test_tra_cuu_dung_so_lieu(self):
        result = tools.get_job_market_trend("IT", "Miền Nam", 2025)
        self.assertIn("25.400", result)
        self.assertIn("+13.4%", result)
        self.assertIn("TĂNG MẠNH", result)

    def test_nam_2024_so_sanh_voi_2023(self):
        result = tools.get_job_market_trend("ngân hàng", "Miền Bắc", 2024)
        self.assertIn("năm 2023", result)
        self.assertIn("-2.5%", result)

    def test_year_mac_dinh_la_2025(self):
        self.assertEqual(tools.get_job_market_trend("IT", "Miền Nam"),
                         tools.get_job_market_trend("IT", "Miền Nam", 2025))

    # --- 🟡 Case nhận diện tham số linh hoạt ---

    def test_alias_nganh(self):
        for alias in ["it", "CNTT", "phần mềm", "lập trình", "software"]:
            with self.subTest(alias=alias):
                self.assertEqual(tools._match(alias, tools._INDUSTRY_ALIASES), "IT - Phần mềm")

    def test_alias_vung_mien(self):
        cases = {"hà nội": "Miền Bắc", "hn": "Miền Bắc", "đà nẵng": "Miền Trung",
                 "huế": "Miền Trung", "TP.HCM": "Miền Nam", "sài gòn": "Miền Nam",
                 "bình dương": "Miền Nam", "cần thơ": "Miền Nam"}
        for alias, expected in cases.items():
            with self.subTest(alias=alias):
                self.assertEqual(tools._match(alias, tools._REGION_ALIASES), expected)

    def test_alias_dai_duoc_uu_tien(self):
        """'miền nam' không được nhận nhầm do chứa chuỗi con của alias khác."""
        self.assertEqual(tools._match("miền nam", tools._REGION_ALIASES), "Miền Nam")
        self.assertEqual(tools._match("miền trung", tools._REGION_ALIASES), "Miền Trung")

    # --- 🟡 Case multi-step: so sánh & xếp hạng ---

    def test_so_sanh_3_vung_sap_xep_giam_dan(self):
        result = tools.compare_regions_by_industry("Sản xuất", 2025)
        percents = [float(v) for v in re.findall(r"([+-]\d+\.\d)%", result)]
        self.assertEqual(len(percents), 4)  # 3 vùng + 1 dòng kết luận
        self.assertEqual(percents[:3], sorted(percents[:3], reverse=True))
        self.assertIn("Miền Bắc", result.splitlines()[1])

    def test_xep_hang_du_5_nganh_trong_1_vung(self):
        result = tools.get_top_industries_by_region("Đà Nẵng", 2025)
        lines = [l for l in result.splitlines() if re.match(r"^\d+\.", l)]
        self.assertEqual(len(lines), 5)
        self.assertIn("IT - Phần mềm", lines[0])

    def test_list_options_liet_ke_du_gia_tri(self):
        result = tools.list_job_market_options()
        for value in ["2024", "2025", "IT - Phần mềm", "Miền Bắc", "Miền Nam", "Miền Trung"]:
            self.assertIn(value, result)

    # --- 🔴 Edge case: bẫy Guardrail ---

    def test_nganh_khong_ton_tai(self):
        result = tools.get_job_market_trend("Thời trang", "Miền Nam", 2025)
        self.assertTrue(result.startswith("LỖI:"))
        self.assertIn("IT - Phần mềm", result)  # gợi ý giá trị hợp lệ

    def test_vung_khong_ton_tai(self):
        result = tools.get_job_market_trend("IT", "Atlantis", 2025)
        self.assertTrue(result.startswith("LỖI:"))
        self.assertIn("Miền Bắc", result)

    def test_nam_ngoai_dai_du_lieu(self):
        result = tools.get_job_market_trend("IT", "Miền Nam", 2030)
        self.assertTrue(result.startswith("LỖI:"))
        self.assertIn("2024, 2025", result)

    def test_nam_khong_phai_so(self):
        result = tools.get_job_market_trend("IT", "Miền Nam", "ngày 32/13/2026")
        self.assertTrue(result.startswith("LỖI:"))

    def test_tham_so_rong(self):
        self.assertTrue(tools.get_job_market_trend("", "Miền Nam").startswith("LỖI:"))
        self.assertTrue(tools.get_job_market_trend("IT", "").startswith("LỖI:"))


# ---------------------------------------------------------------------------
# 5. HÀNH VI TOOL: TUYỂN SINH ĐẠI HỌC
# ---------------------------------------------------------------------------

class TestAdmissionTools(unittest.TestCase):

    # --- 🟢 Theo trường ---

    def test_tra_cuu_theo_truong(self):
        result = tools.get_admission_by_university("UIT", 2025)
        lines = [l for l in result.splitlines() if re.match(r"^\d+\.", l)]
        self.assertEqual(len(lines), 5)
        self.assertIn("Trí tuệ nhân tạo", lines[0])
        self.assertIn("28.8", lines[0])
        self.assertIn("Học phí: 35 triệu/năm", result)

    def test_nganh_trong_truong_sap_xep_diem_giam_dan(self):
        result = tools.get_admission_by_university("Bách khoa Hà Nội", 2025)
        scores = [float(s) for s in re.findall(r": (\d+\.\d) điểm", result)]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_alias_truong(self):
        cases = {"bách khoa hà nội": "BKA", "bkhn": "BKA", "bách khoa đà nẵng": "DDK",
                 "bách khoa TP.HCM": "QSB", "kinh tế quốc dân": "NEU", "ueh": "UEH",
                 "cần thơ": "TCT", "học viện ngân hàng": "BAV", "đại học huế": "DHT"}
        for alias, expected in cases.items():
            with self.subTest(alias=alias):
                university, _, error = tools._match_university(alias)
                self.assertIsNone(error)
                self.assertEqual(university["university_code"], expected)

    # --- 🟢 Theo vùng miền ---

    def test_tra_cuu_theo_vung(self):
        result = tools.get_admission_by_region("miền trung", 2025)
        self.assertIn("3 trường, 13 ngành", result)
        self.assertIn("thấp nhất 17.0", result)
        self.assertIn("cao nhất 27.0", result)

    def test_truong_trong_vung_sap_xep_theo_diem_cao_nhat(self):
        result = tools.get_admission_by_region("Miền Nam", 2025)
        lines = [l for l in result.splitlines() if re.match(r"^\d+\.", l)]
        self.assertEqual(len(lines), 4)
        self.assertIn("UIT", lines[0])

    # --- 🟢 Theo nhóm ngành ---

    def test_tra_cuu_theo_nhom_nganh_toan_quoc(self):
        result = tools.get_admission_by_major_group("IT", "", 2025)
        lines = [l for l in result.splitlines() if re.match(r"^\d+\.", l)]
        self.assertEqual(len(lines), 12)
        self.assertIn("toàn quốc", result)

    def test_loc_nhom_nganh_theo_vung(self):
        result = tools.get_admission_by_major_group("IT", "miền nam", 2025)
        lines = [l for l in result.splitlines() if re.match(r"^\d+\.", l)]
        self.assertEqual(len(lines), 7)
        self.assertNotIn("Miền Bắc", result)

    def test_nhan_dien_nhom_nganh_theo_tu_khoa_nguoi_dung(self):
        for alias in ["IT", "cntt", "phần mềm"]:
            with self.subTest(alias=alias):
                self.assertIn("IT - Phần mềm", tools.get_admission_by_major_group(alias))
        self.assertIn("Kinh tế - Tài chính - Ngân hàng",
                      tools.get_admission_by_major_group("ngân hàng"))

    def test_nhom_nganh_khac(self):
        result = tools.get_admission_by_major_group("Ngành khác")
        self.assertIn("Sư phạm Toán học", result)
        self.assertIn("Nông học", result)

    # --- 🟡 Xử lý năm cũ: không được gán nhầm chỉ số của năm mới ---

    def test_nam_2024_khong_hien_chi_so_cua_2025(self):
        """benchmark_change & competition_level tính theo 2025, không áp cho 2024."""
        result = tools.get_admission_by_major_group("IT", "miền trung", 2024)
        self.assertIn("26.5", result)
        self.assertNotIn("cạnh tranh", result)
        self.assertNotIn("Xu hướng chung", result)

    def test_nam_2025_hien_day_du_chi_so(self):
        result = tools.get_admission_by_major_group("IT", "miền trung", 2025)
        self.assertIn("cạnh tranh", result)
        self.assertIn("Xu hướng chung", result)
        self.assertIn("so với 2024", result)

    def test_bao_cao_vung_nam_2024_khong_co_dong_bien_dong(self):
        self.assertNotIn("Biến động", tools.get_admission_by_region("Miền Nam", 2024))
        self.assertIn("Biến động", tools.get_admission_by_region("Miền Nam", 2025))

    # --- 🔴 Edge case: bẫy Guardrail ---

    def test_ten_truong_nhap_nhang(self):
        """'bách khoa' khớp 3 trường -> phải báo lỗi kèm danh sách để agent hỏi lại."""
        result = tools.get_admission_by_university("bách khoa")
        self.assertTrue(result.startswith("LỖI:"))
        for code in ("BKA", "DDK", "QSB"):
            self.assertIn(code, result)

    def test_truong_khong_ton_tai(self):
        result = tools.get_admission_by_university("Đại học Harvard")
        self.assertTrue(result.startswith("LỖI:"))
        self.assertIn("list_admission_options", result)

    def test_nhom_nganh_khong_ton_tai(self):
        result = tools.get_admission_by_major_group("Thời trang")
        self.assertTrue(result.startswith("LỖI:"))

    def test_vung_khong_ton_tai(self):
        self.assertTrue(tools.get_admission_by_region("Atlantis").startswith("LỖI:"))
        self.assertTrue(tools.get_admission_by_major_group("IT", "Atlantis").startswith("LỖI:"))

    def test_nam_ngoai_dai_du_lieu(self):
        for result in (tools.get_admission_by_university("UIT", 2030),
                       tools.get_admission_by_region("Miền Nam", 2030),
                       tools.get_admission_by_major_group("IT", "", 2030)):
            self.assertTrue(result.startswith("LỖI:"))
            self.assertIn("2024, 2025", result)

    def test_list_options_liet_ke_du_12_truong(self):
        result = tools.list_admission_options()
        for code in ("BKA", "NEU", "UET", "BAV", "TMU", "DDK", "DDQ", "DHT",
                     "QSB", "UIT", "UEH", "TCT"):
            self.assertIn(code, result)


# ---------------------------------------------------------------------------
# 6. NỐI 2 BỘ DỮ LIỆU QUA NHÓM NGÀNH
# ---------------------------------------------------------------------------

class TestCrossDataset(unittest.TestCase):
    """Agent phải ghép được 'điểm chuẩn ngành X' với 'xu hướng tuyển dụng ngành X'."""

    def test_nhom_nganh_tuyen_sinh_trung_ten_nhom_nganh_tuyen_dung(self):
        job_market_groups = set(tools._INDUSTRY_ALIASES)
        admission_groups = {row["group"] for row in tools._all_majors()}
        self.assertTrue(admission_groups.issubset(job_market_groups | {tools._OTHER_GROUP}))

    def test_moi_nhom_nganh_chinh_deu_co_nganh_dao_tao(self):
        groups = {row["group"] for row in tools._all_majors()}
        for group in tools._INDUSTRY_ALIASES:
            with self.subTest(group=group):
                self.assertIn(group, groups)

    def test_gom_nhom_nganh_dung(self):
        cases = {
            "Khoa học máy tính": "IT - Phần mềm",
            "An toàn thông tin": "IT - Phần mềm",
            "Mạng máy tính và truyền thông dữ liệu": "IT - Phần mềm",
            "Quản trị kinh doanh": "Quản trị - Nhân sự",
            "Kinh doanh quốc tế": "Kinh tế - Tài chính - Ngân hàng",
            "Marketing thương mại": "Marketing - Truyền thông",
            "Kỹ thuật ô tô": "Sản xuất - Cơ khí",
            "Kỹ thuật Cơ điện tử": "Sản xuất - Cơ khí",
            "Sư phạm Toán học": tools._OTHER_GROUP,
            "Nuôi trồng thủy sản": tools._OTHER_GROUP,
        }
        for major_name, expected in cases.items():
            with self.subTest(major=major_name):
                self.assertEqual(tools._major_group(major_name), expected)

    def test_kich_ban_huong_nghiep_day_du(self):
        """Học sinh 27 điểm khối A01 muốn học IT ở miền Nam -> tra điểm rồi tra việc làm."""
        admission = tools.get_admission_by_major_group("IT", "miền nam", 2025)
        self.assertIn("Kỹ thuật phần mềm", admission)
        job_market = tools.get_job_market_trend("IT", "miền nam", 2025)
        self.assertIn("TĂNG MẠNH", job_market)


if __name__ == "__main__":
    # unittest in kết quả ra stderr nên phải set encoding cả hai luồng,
    # nếu không docstring tiếng Việt sẽ bị lỗi font trên Windows Console.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    print_tool_report()
    unittest.main(verbosity=2)
