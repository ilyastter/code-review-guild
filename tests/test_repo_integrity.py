import json
import pathlib
import subprocess
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

SKILL_FILES = [
    "skills/code-simplifier/SKILL.md",
    "skills/review-dry/SKILL.md",
    "skills/review-kiss/SKILL.md",
    "skills/review-yagni/SKILL.md",
    "skills/review-soc/SKILL.md",
    "skills/review-solid/SKILL.md",
    "skills/review-all-principles/SKILL.md",
    "skills/using-code-review-guild/SKILL.md",
]

PLUGIN_FILES = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
]

HOOK_FILES = [
    "hooks/session-start.md",
    "hooks/session-start.sh",
    "hooks/run-hook.cmd",
    "hooks/hooks-cursor.json",
]

WRAPPER_FILES = [
    "agents/dry-reviewer.md",
    "agents/kiss-reviewer.md",
    "agents/yagni-reviewer.md",
    "agents/soc-reviewer.md",
    "agents/solid-reviewer.md",
    "agents/principles-orchestrator.md",
    "commands/review-dry.md",
    "commands/review-kiss.md",
    "commands/review-yagni.md",
    "commands/review-soc.md",
    "commands/review-solid.md",
    "commands/review-all-principles.md",
]

DOC_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/README.claude.md",
    "docs/README.codex.md",
    "docs/README.cursor.md",
    "docs/README.copilot.md",
]

INSTALLER_FILES = [
    "install/install-claude.sh",
    "install/install-claude.ps1",
    "install/install-codex.sh",
    "install/install-codex.ps1",
    "install/install-cursor.sh",
    "install/install-cursor.ps1",
    "install/install-copilot-vscode.sh",
    "install/install-copilot-vscode.ps1",
]

REPORT_FILENAMES = [
    "latest-dry-review.md",
    "latest-kiss-review.md",
    "latest-yagni-review.md",
    "latest-soc-review.md",
    "latest-solid-review.md",
    "latest-principles-review.md",
]

REPORT_SECTIONS = [
    "## Scope",
    "## Summary",
    "## Must fix",
    "## Should consider",
    "## Acceptable tradeoff",
    "## Not a problem",
    "## Reusable project observations",
]


class RepoIntegrityTests(unittest.TestCase):
    def test_skill_files_exist(self):
        for relative_path in SKILL_FILES:
            self.assertTrue((REPO_ROOT / relative_path).is_file(), relative_path)

    def test_skill_frontmatter_uses_trigger_descriptions(self):
        for relative_path in SKILL_FILES:
            content = (REPO_ROOT / relative_path).read_text()
            self.assertIn("---", content, relative_path)
            self.assertIn("name:", content, relative_path)
            self.assertIn("description: Use when", content, relative_path)

    def test_plugin_files_exist(self):
        for relative_path in PLUGIN_FILES:
            self.assertTrue((REPO_ROOT / relative_path).is_file(), relative_path)

    def test_plugin_manifests_reference_skills_and_hooks(self):
        codex_plugin = json.loads((REPO_ROOT / ".codex-plugin/plugin.json").read_text())
        cursor_plugin = json.loads((REPO_ROOT / ".cursor-plugin/plugin.json").read_text())
        claude_plugin = json.loads((REPO_ROOT / ".claude-plugin/plugin.json").read_text())

        self.assertEqual(codex_plugin["skills"], "./skills/")
        self.assertIn("interface", codex_plugin)
        self.assertEqual(cursor_plugin["skills"], "./skills/")
        self.assertEqual(cursor_plugin["commands"], "./commands/")
        self.assertEqual(cursor_plugin["agents"], "./agents/")
        self.assertEqual(cursor_plugin["hooks"], "./hooks/hooks-cursor.json")
        self.assertEqual(claude_plugin["name"], "code-review-guild")

    def test_hooks_and_wrappers_exist(self):
        for relative_path in HOOK_FILES + WRAPPER_FILES:
            self.assertTrue((REPO_ROOT / relative_path).is_file(), relative_path)

    def test_hook_bootstrap_references_meta_skill_and_review_contract(self):
        content = (REPO_ROOT / "hooks/session-start.md").read_text()
        self.assertIn("using-code-review-guild", content)
        for filename in REPORT_FILENAMES:
            self.assertIn(filename, content)

    def test_docs_exist_and_describe_harness_support(self):
        for relative_path in DOC_FILES:
            self.assertTrue((REPO_ROOT / relative_path).is_file(), relative_path)

        readme = (REPO_ROOT / "README.md").read_text()
        self.assertIn("skills/", readme)
        self.assertIn("code-simplifier", readme)
        self.assertIn("session-start", readme)
        self.assertIn("Claude", readme)
        self.assertIn("Codex", readme)
        self.assertIn("Cursor", readme)
        self.assertIn("GitHub Copilot", readme)
        self.assertIn(".github/copilot-instructions.md", readme)

    def test_examples_still_include_contract_reports(self):
        example_root = REPO_ROOT / "examples/python"
        self.assertTrue((example_root / "src").is_dir())
        self.assertTrue((example_root / "reports").is_dir())
        for filename in REPORT_FILENAMES:
            report_path = example_root / "reports" / filename
            self.assertTrue(report_path.is_file(), report_path)
            content = report_path.read_text()
            for section in REPORT_SECTIONS:
                self.assertIn(section, content)

    def test_shell_installers_copy_expected_package_shapes(self):
        shell_scripts = [
            (
                "install/install-claude.sh",
                [".claude-plugin/plugin.json", "skills/review-dry/SKILL.md", "skills/code-simplifier/SKILL.md", "hooks/session-start.sh", "docs/README.claude.md"],
            ),
            (
                "install/install-codex.sh",
                [".codex-plugin/plugin.json", "skills/review-dry/SKILL.md", "skills/code-simplifier/SKILL.md", "commands/review-dry.md", "docs/README.codex.md"],
            ),
            (
                "install/install-cursor.sh",
                [".cursor-plugin/plugin.json", "skills/review-dry/SKILL.md", "skills/code-simplifier/SKILL.md", "hooks/hooks-cursor.json", "agents/dry-reviewer.md"],
            ),
            (
                "install/install-copilot-vscode.sh",
                [".github/copilot-instructions.md", ".github/prompts/review-dry.prompt.md"],
            ),
        ]

        for relative_script, expected_paths in shell_scripts:
            with self.subTest(script=relative_script):
                script_path = REPO_ROOT / relative_script
                with tempfile.TemporaryDirectory() as tmp_dir:
                    destination = pathlib.Path(tmp_dir) / "package"
                    if relative_script == "install/install-copilot-vscode.sh":
                        destination.mkdir()
                    first = subprocess.run(
                        ["/bin/sh", str(script_path), "--dest", str(destination)],
                        cwd=REPO_ROOT,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(first.returncode, 0, first.stderr)
                    for expected_path in expected_paths:
                        self.assertTrue((destination / expected_path).exists(), expected_path)

                    second = subprocess.run(
                        ["/bin/sh", str(script_path), "--dest", str(destination)],
                        cwd=REPO_ROOT,
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(second.returncode, 0)
                    self.assertIn("--force", second.stderr + second.stdout)

                    third = subprocess.run(
                        ["/bin/sh", str(script_path), "--dest", str(destination), "--force"],
                        cwd=REPO_ROOT,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(third.returncode, 0, third.stderr)

    def test_powershell_scripts_expose_dest_force_and_copy_contract(self):
        for relative_path in [path for path in INSTALLER_FILES if path.endswith(".ps1")]:
            content = (REPO_ROOT / relative_path).read_text()
            self.assertIn("Destination", content, relative_path)
            self.assertIn("Force", content, relative_path)
            self.assertIn("Write-Host", content, relative_path)
            if "copilot" in relative_path:
                self.assertIn("prompts", content, relative_path)
            else:
                self.assertIn("skills", content, relative_path)


if __name__ == "__main__":
    unittest.main()
