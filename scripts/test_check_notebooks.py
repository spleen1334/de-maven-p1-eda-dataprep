"""Focused stdlib tests: run .venv/bin/python -m unittest discover -s scripts."""
from pathlib import Path
import unittest

from check_notebooks import PATH_EXAMPLES, input_paths, local_target, markdown_links


class CheckerTests(unittest.TestCase):
    def test_literal_inputs_and_sqlite_not_mysql(self):
        source = """import pandas as pd
pd.read_csv('../../data/a.csv')
pd.read_excel(io='../../data/Sales Tables.xlsx')
sqlite3.connect('../../data/maven.db')
mysql.connector.connect(database='my_new_db')
pd.read_sql('SELECT * FROM courses', conn)
!pip install mysql-connector-python
"""
        self.assertEqual(list(input_paths(source)), [
            "../../data/a.csv", "../../data/Sales Tables.xlsx", "../../data/maven.db"])

    def test_local_url_decoding_and_remote_exclusion(self):
        self.assertEqual(local_target(Path("/repo"), "data/Sales%20Tables.xlsx#sheet"),
                         Path("/repo/data/Sales Tables.xlsx"))
        for url in ("https://example.com/data", "mailto:alice@example.com", "#heading"):
            self.assertIsNone(local_target(Path("/repo"), url))

    def test_markdown_notebook_links_and_references(self):
        text = ("[notebook](notebooks/a%20b.ipynb) "
                "[sheet](<data/Sales Tables.xlsx>)\n[ref]: docs/setup.md\n")
        self.assertEqual(list(markdown_links(text)), [
            "notebooks/a%20b.ipynb", "data/Sales Tables.xlsx", "docs/setup.md"])

    def test_path_examples_are_explicit_and_limited(self):
        self.assertEqual(len(PATH_EXAMPLES), 3)
        self.assertTrue(all(path.endswith("section04_gathering_data_code.ipynb")
                            for path, _ in PATH_EXAMPLES))


if __name__ == "__main__":
    unittest.main()
