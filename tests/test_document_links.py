"""Regressions for recursive public-document and anchor validation."""

from pathlib import Path
import tempfile
import unittest

from document_links import anchors, link_errors, public_documents


class DocumentLinkTests(unittest.TestCase):
    def test_headings_ignore_fences_and_handle_punctuation_and_duplicates(self):
        self.assertEqual(
            anchors("# v0.2.0 status\n## Same\n## Same\n```md\n# Example\n```\n"),
            {"v020-status", "same", "same-1"},
        )

    def test_nested_docs_check_relative_targets_and_anchors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            history = root / "docs/history"
            history.mkdir(parents=True)
            doc = history / "record.md"
            doc.write_text(
                "# Record\n[ok](../guide.md#current)\n[bad](../guide.md#old)\n[missing](absent.md)\n"
            )
            (root / "docs/guide.md").write_text("# Current\n")
            self.assertIn(doc, public_documents(root))
            errors = link_errors(doc, root)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any("missing anchor" in error for error in errors))
            self.assertTrue(any("missing target" in error for error in errors))
