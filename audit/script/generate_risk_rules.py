"""Generate all 25 risk rule YAML files from checkpoint markdown files."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


KNOWLEDGE = Path("D:\\2026年\\Food-Audit-Agent\\knowledge")
CHECKPOINT_DIR = KNOWLEDGE / "checkpoints" / "beverage" / "raw_material"
OUTPUT_DIR = KNOWLEDGE / "risk_rules" / "beverage" / "raw_material"


def parse_checkpoint(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    meta_match = re.search(r"```yaml\s*\n(.*?)\n```", content, re.DOTALL)
    meta = yaml.safe_load(meta_match.group(1)) if meta_match else {}

    # Objective
    obj_match = re.search(r"## ② Inspection Objective\s*\n+(.*?)(?=\n##)", content, re.DOTALL)
    objective = obj_match.group(1).strip() if obj_match else ""

    # Method table - extract key columns
    method_lines = []
    method_match = re.search(r"## ④ Inspection Method\s*\n\|.*?\|\n\|.*?\|\n(.*?)(?=\n##)", content, re.DOTALL)
    if method_match:
        for line in method_match.group(1).strip().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    method_lines.append({"step": parts[1], "method": parts[2], "desc": parts[3]})

    # Evidence
    evidence_list = []
    ev_match = re.search(r"## ⑤ Required Evidence\s*\n\|.*?\|\n\|.*?\|\n(.*?)(?=\n##)", content, re.DOTALL)
    if ev_match:
        for line in ev_match.group(1).strip().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    evidence_list.append({"item": parts[1], "type": parts[2], "required": parts[3]})

    # Findings
    findings = []
    find_match = re.search(r"## ⑥ Common Findings\s*\n\|.*?\|\n\|.*?\|\n(.*?)(?=\n##)", content, re.DOTALL)
    if find_match:
        for line in find_match.group(1).strip().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    findings.append({"finding": parts[1], "severity": parts[2], "desc": parts[3]})

    # Risk conditions
    risk_conds = []
    risk_match = re.search(r"## ⑦ Risk Level\s*\n\|.*?\|\n\|.*?\|\n(.*?)(?=\n##)", content, re.DOTALL)
    if risk_match:
        for line in risk_match.group(1).strip().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    risk_conds.append({"condition": parts[1], "risk": parts[2]})

    # Regulations
    regs = []
    reg_match = re.search(r"## ⑧ Regulatory Reference\s*\n(.*?)(?=\n##)", content, re.DOTALL)
    if reg_match:
        for line in reg_match.group(1).strip().splitlines():
            line = line.strip()
            if line.startswith("- `"):
                ref = re.search(r"`(.*?)`", line)
                if ref:
                    regs.append(ref.group(1))

    # AI guidance
    ai_rules = []
    ai_match = re.search(r"## ⑨ AI Guidance\s*\n\|.*?\|\n\|.*?\|\n(.*?)(?=\n##)", content, re.DOTALL)
    if ai_match:
        for line in ai_match.group(1).strip().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    ai_rules.append({"scenario": parts[1], "logic": parts[2], "action": parts[3]})

    return {
        "meta": meta,
        "objective": objective,
        "methods": method_lines,
        "evidence": evidence_list,
        "findings": findings,
        "risk_conditions": risk_conds,
        "regulations": regs,
        "ai_rules": ai_rules,
    }


def build_risk_rule(cp_id: str, data: dict) -> dict:
    meta = data["meta"]
    findings = data["findings"]
    regs = data["regulations"]
    ai_rules = data["ai_rules"]
    evidence = data["evidence"]
    risk_conds = data["risk_conditions"]

    # Map H/M → Critical/High/Medium/Low
    risk_map = {"H": "Critical", "M": "High"}
    rl = risk_map.get(meta.get("risk_level", ""), "Medium")

    # Build decision logic from AI guidance
    decision_logic = []
    for rule in ai_rules:
        scenario = rule["scenario"]
        logic = rule["logic"]
        action = rule["action"]

        if "符合" in action or action.lower().startswith("ok"):
            result = "PASS"
            severity = None
        elif "不符合" in action or "不符合" in logic or "判定不符合" in action:
            result = "FAIL"
            if "重大" in action or "重大" in logic:
                severity = "Critical"
            elif "较大" in action or "较大" in logic:
                severity = "High"
            else:
                severity = "Medium"
        elif "基本符合" in action:
            result = "WARNING"
            severity = "Low"
        elif "可疑" in logic or "疑似" in logic:
            result = "WARNING"
            severity = "Medium"
        elif "不能直接判定" in logic or "需进一步" in logic or "需确认" in logic or "需查证" in logic or "需关注" in logic:
            result = "WARNING"
            severity = "Medium"
        else:
            result = "WARNING"
            severity = "Low"

        entry = {"condition": scenario, "result": result}
        if severity:
            entry["severity"] = severity
        decision_logic.append(entry)

    if not decision_logic:
        decision_logic = [
            {"condition": "Default: all requirements met", "result": "PASS"},
            {"condition": "Default: non-compliance detected", "result": "FAIL", "severity": "High"},
        ]

    # Required evidence items
    req_evidence = [e["item"] for e in evidence if e.get("required") == "必须" or e.get("required") == "条件必选"]

    # Pass / Fail / Warning conditions
    pass_cond = f"All conditions met: {findings[0]['finding'] if findings else 'no issues'}"
    fail_cond = findings[0]["finding"] if findings else ""
    warning_cond = findings[1]["finding"] if len(findings) > 1 else "Minor issues detected"

    # Non-conformities
    nonconformities = [f["finding"] for f in findings]

    # Risk description
    risk_desc = ""
    for rc in risk_conds:
        if "RISK-01" in rc.get("risk", "") or "RISK-02" in rc.get("risk", ""):
            if risk_desc:
                risk_desc += "; "
            risk_desc += rc.get("condition", "")

    return {
        "id": f"RR-{cp_id}",
        "checkpoint_id": cp_id,
        "title": meta.get("checkpoint_name", ""),
        "version": "1.0",
        "domain": meta.get("module", ""),
        "category": meta.get("unit", ""),
        "risk_level": rl,
        "purpose": data["objective"],
        "decision_logic": decision_logic,
        "required_evidence": req_evidence,
        "pass_condition": pass_cond,
        "fail_condition": fail_cond,
        "warning_condition": warning_cond,
        "legal_basis": regs,
        "risk_description": risk_desc,
        "typical_nonconformities": nonconformities,
        "recommended_actions": [f"Investigate: {n}" for n in nonconformities[:3]],
        "output_template": {
            "status": "PASS / WARNING / FAIL",
            "reason": "",
            "risk_level": rl,
            "laws": regs,
            "recommendation": "",
        },
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    errors = []

    for md_file in sorted(CHECKPOINT_DIR.glob("CP-BEV-RM-*.md")):
        cp_id = md_file.stem
        rr_id = f"RR-{cp_id}"
        rr_path = OUTPUT_DIR / f"{rr_id}.yaml"

        if rr_path.exists():
            continue

        try:
            data = parse_checkpoint(md_file)
            rule = build_risk_rule(cp_id, data)
            with open(rr_path, "w", encoding="utf-8") as f:
                yaml.dump(rule, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            count += 1
        except Exception as e:
            errors.append(f"{cp_id}: {e}")

    print(f"Generated: {count} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  {e}")
    else:
        print("No errors")


if __name__ == "__main__":
    main()
