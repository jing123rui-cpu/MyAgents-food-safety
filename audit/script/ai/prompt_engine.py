"""PromptEngine — template-driven prompt builder.

Completely independent of the AI provider layer.
Loads templates from disk, performs placeholder replacement,
and returns ready-to-use prompt strings.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_VAR_RE = re.compile(r"\{\{(\w+)\}\}")


class PromptEngine:
    """Builds structured prompts from Markdown templates on disk.

    Usage
    -----
    engine = PromptEngine()
    prompt = engine.build_inspection_prompt(context)
    """

    def __init__(self, templates_dir: Optional[str] = None) -> None:
        """Initialise with a path to the templates directory.

        Parameters
        ----------
        templates_dir
            Directory containing ``.md`` template files.  Defaults to
            ``core/ai/templates/`` relative to this file.
        """
        if templates_dir is not None:
            self._templates_dir = Path(templates_dir)
        else:
            self._templates_dir = (
                Path(__file__).resolve().parent / "templates"
            )
        self._cache: Dict[str, str] = {}

        if not self._templates_dir.is_dir():
            raise FileNotFoundError(
                f"Templates directory not found: {self._templates_dir}"
            )
        logger.info("PromptEngine templates dir: %s", self._templates_dir)

    # ── Public Builders ──────────────────────────────────────────

    def build_inspection_prompt(
        self,
        *,
        task: str = "",
        checkpoint_id: str = "",
        checkpoint_name: str = "",
        checkpoint_domain: str = "",
        checkpoint_module: str = "",
        checkpoint_objective: str = "",
        checkpoint_risk_level: str = "",
        checkpoint_details: str = "",
        risk_rules: str = "",
        evidence: str = "",
        regulations: str = "",
        expected_output: str = "",
    ) -> str:
        """Build a combined inspection prompt from individual fields.

        Parameters are keyword-only for clarity.  Each corresponds to
        a ``{{placeholder}}`` in the ``inspection.md`` template.

        Returns
        -------
        str
            The rendered inspection prompt.
        """
        return self._render(
            "inspection",
            {
                "task": task,
                "checkpoint_id": checkpoint_id,
                "checkpoint_name": checkpoint_name,
                "checkpoint_domain": checkpoint_domain,
                "checkpoint_module": checkpoint_module,
                "checkpoint_objective": checkpoint_objective,
                "checkpoint_risk_level": checkpoint_risk_level,
                "checkpoint_details": checkpoint_details,
                "risk_rules": risk_rules,
                "evidence": evidence,
                "regulations": regulations,
                "expected_output": expected_output,
            },
        )

    def build_checkpoint_prompt(
        self,
        *,
        checkpoint_id: str = "",
        checkpoint_name: str = "",
        checkpoint_objective: str = "",
        checkpoint_risk_level: str = "",
        inspection_methods: str = "",
        required_evidence: str = "",
        evidence: str = "",
        regulations: str = "",
    ) -> str:
        """Build a prompt for evaluating a single checkpoint.

        Returns
        -------
        str
            The rendered checkpoint evaluation prompt.
        """
        return self._render(
            "checkpoint",
            {
                "checkpoint_id": checkpoint_id,
                "checkpoint_name": checkpoint_name,
                "checkpoint_objective": checkpoint_objective,
                "checkpoint_risk_level": checkpoint_risk_level,
                "inspection_methods": inspection_methods,
                "required_evidence": required_evidence,
                "evidence": evidence,
                "regulations": regulations,
            },
        )

    def build_report_prompt(
        self,
        *,
        facility_name: str = "",
        auditor_name: str = "",
        audit_date: str = "",
        inspection_summary: str = "",
        checkpoints: str = "",
        evaluation_results: str = "",
        regulations: str = "",
    ) -> str:
        """Build a prompt for drafting an audit report.

        Returns
        -------
        str
            The rendered report generation prompt.
        """
        return self._render(
            "report",
            {
                "facility_name": facility_name,
                "auditor_name": auditor_name,
                "audit_date": audit_date,
                "inspection_summary": inspection_summary,
                "checkpoints": checkpoints,
                "evaluation_results": evaluation_results,
                "regulations": regulations,
            },
        )

    def build_question_prompt(
        self,
        *,
        question: str = "",
        context: str = "",
    ) -> str:
        """Build a prompt for answering a free-form audit question.

        Returns
        -------
        str
            The rendered question prompt.
        """
        return self._render(
            "question",
            {
                "question": question,
                "context": context,
            },
        )

    # ── Template Helpers ─────────────────────────────────────────

    def load_template(self, name: str) -> str:
        """Read a template from disk (with caching).

        Parameters
        ----------
        name
            Template name without extension (e.g. ``"inspection"``).

        Returns
        -------
        str
            Raw template content.

        Raises
        ------
        FileNotFoundError
            If ``{name}.md`` does not exist in the templates directory.
        """
        if name not in self._cache:
            path = self._templates_dir / f"{name}.md"
            if not path.is_file():
                raise FileNotFoundError(
                    f"Template not found: {path}"
                )
            self._cache[name] = path.read_text(encoding="utf-8")
        return self._cache[name]

    def list_templates(self) -> List[str]:
        """Return the names of all available templates (without extension).

        Returns
        -------
        List[str]
            e.g. ``["checkpoint", "inspection", "question", "report"]``
        """
        return sorted(
            p.stem for p in self._templates_dir.glob("*.md")
        )

    def render(self, template_name: str, variables: Dict[str, str]) -> str:
        """Load a template and replace ``{{placeholders}}`` with values.

        Parameters
        ----------
        template_name
            Template name (without ``.md``).
        variables
            Mapping of placeholder name → replacement string.

        Returns
        -------
        str
            The filled-in prompt.
        """
        return self._render(template_name, variables)

    # ── Internal ─────────────────────────────────────────────────

    def _render(self, template_name: str, variables: Dict[str, str]) -> str:
        """Load template and substitute ``{{var}}`` placeholders.

        Unrecognised placeholders are left as-is in the output so that
        missing variables are visible rather than silently dropped.
        """
        template = self.load_template(template_name)

        def _replace(match: re.Match) -> str:
            key = match.group(1)
            return variables.get(key, match.group(0))

        return _VAR_RE.sub(_replace, template)

    @property
    def templates_dir(self) -> Path:
        """Path to the templates directory."""
        return self._templates_dir
