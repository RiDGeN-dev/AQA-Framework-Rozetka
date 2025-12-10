from pathlib import Path
import pytest

from framework.core.dsl_runner import DslRunner


BDD_DIR = Path(__file__).parent / "bdd"
BDD_FILES = sorted(BDD_DIR.glob("*.bdd"))


@pytest.mark.parametrize("bdd_file", BDD_FILES, ids=lambda p: p.stem)
def test_bdd_scenario(bdd_file):
    runner = DslRunner(bdd_file)
    runner.run()
