"""ReportExporter v2.0 — exports AuditWritingResult to formal regulatory Word (.docx) documents.

Produces a 12-section inspection report matching the format used by
Chinese Market Supervision Administration (市场监督管理局).

Independent module. No imports from RuleEngine, InspectionPipeline,
PromptEngine, ContextEngine, or WritingEngine.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Pt, Cm, RGBColor, Emu

from .writing_engine import AuditWritingResult

logger = logging.getLogger(__name__)

_REPORT_TITLE = "食品生产企业监督检查报告"
_ENTERPRISE_PASS = "企业通过检查"
_ENTERPRISE_FAIL = "企业需要整改"


@dataclass
class ReportExportResult:
    """Result of a Word export operation."""
    filepath: str = ""
    filename: str = ""
    generated_time: str = ""
    success: bool = False
    error: str = ""


class ReportExporter:
    """Exports audit writing results to formal Word documents.

    Usage
    -----
    exporter = ReportExporter()
    result = exporter.export_word(writing_result, output_path="report.docx")
    """

    def __init__(self) -> None:
        self._doc: Optional[Document] = None

    # ── Public API ───────────────────────────────────────────────

    def export_word(
        self,
        writing_result: AuditWritingResult,
        output_path: str = "",
    ) -> ReportExportResult:
        """Generate a Word document from an ``AuditWritingResult``.

        When *output_path* is empty or ends with a separator, a unique
        filename is auto-generated as::

            {enterprise_name}_监督检查报告_{YYYYMMDD}_{HHMMSS}.docx

        Existing files are never overwritten — a counter suffix is
        appended if needed.

        Parameters
        ----------
        writing_result
            The output of ``AuditWritingEngine.generate_all()`` or
            ``AuditWritingEngine.generate_all_offline()``.
        output_path
            Path for the output ``.docx`` file.  When empty or a
            directory, a unique filename is auto-generated inside
            ``reports/output/``.

        Returns
        -------
        ReportExportResult
            Status and metadata for the export operation.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = ReportExportResult(
            filepath="", filename="",
            generated_time=ts, success=False, error="",
        )

        try:
            # ── Resolve output path (auto-generate if needed) ──
            if not output_path or output_path.endswith(("/", "\\")):
                base_dir = Path(output_path) if output_path else Path("reports") / "output"
                out = self._generate_unique_path(base_dir, writing_result)
            else:
                out = Path(output_path)
                # If the path points to an existing directory, generate inside it
                if out.is_dir():
                    out = self._generate_unique_path(out, writing_result)

            # ── Ensure output directory exists ──
            out.parent.mkdir(parents=True, exist_ok=True)

            # ── Build document in memory ──
            self._create_document(writing_result)

            # ── Save (catch PermissionError with friendly message) ──
            try:
                self._doc.save(str(out))
            except PermissionError:
                result.error = (
                    "当前 Word 文件可能正在被打开，请关闭 Word 后重新导出。\n"
                    "或重新执行导出，系统会自动生成新的文件名。"
                )
                logger.error(
                    "PermissionError saving report to %s — file may be open in Word",
                    out,
                )
                return result

            result.filepath = str(out.resolve())
            result.filename = out.name
            result.success = True
            logger.info("Report exported: %s", result.filepath)

        except Exception as exc:
            result.error = f"[{type(exc).__name__}] {exc}"
            logger.error("Report export failed: %s", exc)

        return result

    # ── Unique Filename Helpers ──────────────────────────────────

    @staticmethod
    def _generate_unique_path(base_dir: Path, writing_result: AuditWritingResult) -> Path:
        """Return a non-colliding ``.docx`` path under *base_dir*.

        Naming pattern::

            {enterprise_name}_监督检查报告_{YYYYMMDD}_{HHMMSS}.docx

        If the enterprise name is empty, falls back to::

            食品生产企业监督检查报告_{YYYYMMDD}_{HHMMSS}.docx

        When a collision is detected, a counter suffix ``_01``, ``_02``,
        … is appended before the extension.
        """
        now = datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        name = writing_result.metadata.get("facility_name", "").strip()
        if name:
            stem = f"{name}_监督检查报告_{ts}"
        else:
            stem = f"食品生产企业监督检查报告_{ts}"

        candidate = base_dir / f"{stem}.docx"
        counter = 1
        while candidate.exists():
            candidate = base_dir / f"{stem}_{counter:02d}.docx"
            counter += 1
        return candidate

    # ── Document Builder ─────────────────────────────────────────

    def _create_document(self, wr: AuditWritingResult) -> None:
        """Build the full 12-section Word document in memory."""
        self._doc = Document()

        # ── Page setup ───────────────────────────────────────────
        section = self._doc.sections[0]
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.17)
        section.right_margin = Cm(3.17)

        # ── Default font ─────────────────────────────────────────
        style = self._doc.styles["Normal"]
        font = style.font
        font.name = "宋体"
        font.size = Pt(12)
        rpr = style.element.get_or_add_rPr()
        rFonts = rpr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = rpr.makeelement(qn("w:rFonts"), {})
            rpr.append(rFonts)
        rFonts.set(qn("w:eastAsia"), "宋体")

        # ── Build sections ───────────────────────────────────────
        self._add_title_block()
        self._doc.add_page_break()

        self._add_text_section("一、企业基本信息", wr.enterprise_info)
        self._add_text_section("二、检查基本情况", wr.inspection_overview)
        self._add_text_section("三、检查项目统计", wr.inspection_statistics)
        self._add_inspection_table(wr, "四、现场检查情况")

        findings = wr.findings or wr.nonconformity
        self._add_text_section("五、发现问题及不符合项", findings or "经现场检查，本次未发现不符合项。")

        self._add_text_section("六、风险分析", wr.risk_analysis)
        self._add_regulation_section(wr)
        cr = wr.corrective_requirements or wr.corrective_action
        self._add_text_section("八、整改要求", cr)
        self._add_enterprise_conclusion(wr)
        self._add_text_section("十、检查结论", wr.audit_conclusion)
        self._add_text_section("十一、附件目录", wr.appendix)
        self._add_text_section("十二、检查人员签字", wr.signature)

        # ── Footer ───────────────────────────────────────────────
        self._add_footer()
        self._add_page_numbers()

    # ── Title Block ──────────────────────────────────────────────

    def _add_title_block(self) -> None:
        """Add cover title and sub-header info."""
        title_p = self._doc.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title_p.add_run(_REPORT_TITLE)
        run.bold = True
        run.font.size = Pt(22)
        self._set_run_font(run, "黑体")

        self._doc.add_paragraph()
        subtitle_p = self._doc.add_paragraph()
        subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sr = subtitle_p.add_run("（正式监管检查报告）")
        sr.font.size = Pt(14)
        sr.font.name = "宋体"
        self._set_east_asian(sr, "宋体")

        self._doc.add_paragraph()
        self._doc.add_paragraph()

    # ── Text Section ─────────────────────────────────────────────

    def _add_text_section(self, heading: str, body: str) -> None:
        """Add a numbered section with heading and body text."""
        h = self._doc.add_paragraph()
        run = h.add_run(heading)
        run.bold = True
        run.font.size = Pt(16)
        self._set_run_font(run, "黑体")

        text = body.strip() if body else "（无内容）"
        bp = self._doc.add_paragraph(text)
        bp.paragraph_format.first_line_indent = Cm(0.74)

        # Add spacing after section
        spacing = self._doc.add_paragraph()
        spacing.paragraph_format.space_after = Pt(6)

    # ── Inspection Table (Section 4) ─────────────────────────────

    def _add_inspection_table(self, wr: AuditWritingResult, heading: str) -> None:
        """Add Section 4 — 现场检查情况 with a structured table."""
        h = self._doc.add_paragraph()
        run = h.add_run(heading)
        run.bold = True
        run.font.size = Pt(16)
        self._set_run_font(run, "黑体")

        rows_data: List[Tuple[str, str, str, str, str, str]] = wr.metadata.get("inspection_rows", [])

        if not rows_data:
            bp = self._doc.add_paragraph("本次检查未匹配具体检查项目。")
            bp.paragraph_format.first_line_indent = Cm(0.74)
            self._doc.add_paragraph()
            return

        # Table headers
        headers = ["序号", "检查项目", "检查内容", "检查结果", "检查依据"]
        ncols = len(headers)

        table = self._doc.add_table(rows=1 + len(rows_data), cols=ncols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        self._set_table_borders(table)

        # Header row
        for j, hdr in enumerate(headers):
            cell = table.rows[0].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(hdr)
            run.bold = True
            run.font.size = Pt(10)
            self._set_east_asian(run, "宋体")
            self._shade_cell(cell, "D9E2F3")

        # Data rows
        for i, row_tuple in enumerate(rows_data):
            seq, cid, name, content, result, basis = row_tuple
            vals = [seq, name, content, result, basis]
            for j, val in enumerate(vals):
                cell = table.rows[i + 1].cells[j]
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j >= 2 else WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(str(val))
                run.font.size = Pt(9)
                self._set_east_asian(run, "宋体")
                # Set column widths
                if j == 0:
                    cell.width = Cm(1.2)
                elif j == 1:
                    cell.width = Cm(3.5)
                elif j == 3:
                    cell.width = Cm(2.0)
                elif j == 4:
                    cell.width = Cm(4.0)

        self._doc.add_paragraph()

    # ── Regulation Section (Section 7) ───────────────────────────

    def _add_regulation_section(self, wr: AuditWritingResult) -> None:
        """Add Section 7 — 法规依据 with table + narrative."""
        h = self._doc.add_paragraph()
        run = h.add_run("七、法规依据")
        run.bold = True
        run.font.size = Pt(16)
        self._set_run_font(run, "黑体")

        regs: List[Tuple[str, str, int, str]] = wr.metadata.get("regulation_table", [])

        if regs:
            headers = ["序号", "法规编号", "法规名称", "引用检查项", "说明"]
            ncols = len(headers)
            table = self._doc.add_table(rows=1 + len(regs), cols=ncols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            self._set_table_borders(table)

            for j, hdr in enumerate(headers):
                cell = table.rows[0].cells[j]
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(hdr)
                run.bold = True
                run.font.size = Pt(9)
                self._set_east_asian(run, "宋体")
                self._shade_cell(cell, "D9E2F3")

            for i, row in enumerate(regs):
                # row is (reg_id, reg_name, count, description)
                reg_id = row[0] if len(row) > 0 else ""
                reg_name = row[1] if len(row) > 1 else ""
                count = row[2] if len(row) > 2 else 0
                desc = row[3] if len(row) > 3 else ""
                vals = [str(i + 1), reg_id, reg_name, str(count), desc[:60]]
                for j, val in enumerate(vals):
                    cell = table.rows[i + 1].cells[j]
                    cell.text = ""
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j in (1, 2, 4) else WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run(val)
                    run.font.size = Pt(8)
                    self._set_east_asian(run, "宋体")
                    # Column widths
                    if j == 0:
                        cell.width = Cm(0.8)
                    elif j == 1:
                        cell.width = Cm(3.0)
                    elif j == 3:
                        cell.width = Cm(1.5)
                    elif j == 4:
                        cell.width = Cm(5.0)

            self._doc.add_paragraph()

        # Narrative part
        text = wr.regulation_reference.strip() if wr.regulation_reference else "本次检查依据相关法律法规进行判定。"
        bp = self._doc.add_paragraph(text)
        bp.paragraph_format.first_line_indent = Cm(0.74)
        self._doc.add_paragraph()

    # ── Enterprise Conclusion (Section 9) ────────────────────────

    def _add_enterprise_conclusion(self, wr: AuditWritingResult) -> None:
        """Add Section 9 — 企业综合判定 with visual emphasis."""
        h = self._doc.add_paragraph()
        run = h.add_run("九、企业综合判定")
        run.bold = True
        run.font.size = Pt(16)
        self._set_run_font(run, "黑体")

        ent = wr.metadata.get("enterprise_evaluation")
        overall_result = ""
        summary = ""
        total = 0
        compliant = 0
        non_compliant = 0

        if ent is not None:
            overall_result = getattr(ent, "overall_result", "")
            summary = getattr(ent, "summary", "")
            total = getattr(ent, "total_checkpoints", 0)
            compliant = getattr(ent, "compliant_count", 0)
            non_compliant = getattr(ent, "non_compliant_count", 0)

        # Also check metadata fallback
        if not overall_result:
            overall_result = wr.metadata.get("enterprise_overall", "")

        # Extract compliance rate
        rate = f"{round(compliant / total * 100, 1)}%" if total > 0 else "0.0%"

        # Decision box — large colored text
        decision_p = self._doc.add_paragraph()
        decision_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        decision_p.paragraph_format.space_before = Pt(12)
        decision_p.paragraph_format.space_after = Pt(12)

        if overall_result == _ENTERPRISE_PASS or (total > 0 and "通过" in overall_result):
            run = decision_p.add_run(f"  {_ENTERPRISE_PASS}  ")
            run.bold = True
            run.font.size = Pt(18)
            run.font.color.rgb = _RGB_GREEN
            self._set_east_asian(run, "黑体")
            pass_text = "企业食品安全管理体系运行有效，持续符合食品安全管理要求。"
        else:
            run = decision_p.add_run(f"  {_ENTERPRISE_FAIL}  ")
            run.bold = True
            run.font.size = Pt(18)
            run.font.color.rgb = _RGB_RED
            self._set_east_asian(run, "黑体")
            pass_text = "企业食品安全管理体系存在缺陷，需按规定期限完成整改。"
            deadline = self._doc.add_paragraph()
            deadline.alignment = WD_ALIGN_PARAGRAPH.CENTER
            dr = deadline.add_run("整改期限由监督检查人员依法确定。")
            dr.font.size = Pt(12)
            dr.font.color.rgb = _RGB_RED

        # Stats table
        stats = self._doc.add_table(rows=3, cols=4)
        stats.alignment = WD_TABLE_ALIGNMENT.CENTER
        self._set_table_borders(stats)

        stats_data = [
            ["检查项目总数", str(total), "合规率", rate],
            ["合格项", str(compliant), "不合格项", str(non_compliant) if non_compliant else "0"],
        ]
        if hasattr(ent, "not_applicable_count"):
            na = getattr(ent, "not_applicable_count", 0)
            stats_data.append(["不适用项", str(na), "", ""])
        else:
            stats_data.append(["", "", "", ""])

        for i, row_data in enumerate(stats_data):
            for j, val in enumerate(row_data):
                cell = stats.rows[i].cells[j]
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.font.size = Pt(10)
                self._set_east_asian(run, "宋体")
                if j in (0, 2):
                    run.bold = True
                    self._shade_cell(cell, "F2F2F2")

        self._doc.add_paragraph()

        # Overall narrative
        if summary:
            sp = self._doc.add_paragraph(summary)
            sp.paragraph_format.first_line_indent = Cm(0.74)

        np = self._doc.add_paragraph(pass_text)
        np.paragraph_format.first_line_indent = Cm(0.74)

        self._doc.add_paragraph()

    # ── Footer ───────────────────────────────────────────────────

    def _add_footer(self) -> None:
        """Add footer to the document section."""
        footer = self._doc.sections[0].footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = fp.add_run("Food Audit Agent v2.0  |  食品安全监督检查报告系统")
        run.font.size = Pt(9)
        run.font.color.rgb = _RGB_GREY

    def _add_page_numbers(self) -> None:
        """Add page number field to footer (right-aligned)."""
        footer = self._doc.sections[0].footer
        # Add page number in a new paragraph
        pp = footer.add_paragraph()
        pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        # Page number XML field
        run = pp.add_run()
        fld_char_begin = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._element.append(fld_char_begin)

        run2 = pp.add_run()
        instr = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
        run2._element.append(instr)

        run3 = pp.add_run()
        fld_char_end = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run3._element.append(fld_char_end)

    # ── Formatting Helpers ───────────────────────────────────────

    @staticmethod
    def _set_run_font(run, font_name: str) -> None:
        """Set both ASCII and East-Asian font on a run."""
        run.font.name = font_name
        rpr = run._element.get_or_add_rPr()
        rFonts = rpr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = rpr.makeelement(qn("w:rFonts"), {})
            rpr.append(rFonts)
        rFonts.set(qn("w:eastAsia"), font_name)
        rFonts.set(qn("w:ascii"), font_name)
        rFonts.set(qn("w:hAnsi"), font_name)

    @staticmethod
    def _set_east_asian(run, font_name: str) -> None:
        """Set East-Asian font only."""
        rpr = run._element.get_or_add_rPr()
        rFonts = rpr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = rpr.makeelement(qn("w:rFonts"), {})
            rpr.append(rFonts)
        rFonts.set(qn("w:eastAsia"), font_name)

    @staticmethod
    def _shade_cell(cell, color_hex: str) -> None:
        """Apply background shading to a table cell."""
        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>'
        )
        cell._element.get_or_add_tcPr().append(shading)

    @staticmethod
    def _set_table_borders(table) -> None:
        """Apply all borders to a table."""
        tbl = table._tbl
        tblPr = tbl.tblPr if tbl.tblPr is not None else tbl._add_tblPr()
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            '  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '  <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '</w:tblBorders>'
        )
        tblPr.append(borders)


# ── Colour Constants ─────────────────────────────────────────────

_RGB_RED = RGBColor(0xCC, 0x00, 0x00)
_RGB_GREEN = RGBColor(0x00, 0x7A, 0x33)
_RGB_GREY = RGBColor(0x99, 0x99, 0x99)
