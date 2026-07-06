import os

import pytest

from ms408.env import load_env, require


def test_load_env_parses_and_does_not_override(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# comment\n\nFOO=bar\nQUOTED='hello world'\nEXISTING=from_file\nBROKEN LINE\n"
    )
    monkeypatch.setenv("EXISTING", "from_shell")
    monkeypatch.delenv("FOO", raising=False)
    pairs = load_env(env_file)
    assert pairs == {"FOO": "bar", "QUOTED": "hello world", "EXISTING": "from_file"}
    assert os.environ["FOO"] == "bar"
    assert os.environ["QUOTED"] == "hello world"
    assert os.environ["EXISTING"] == "from_shell"  # shell wins


def test_require_missing_raises(monkeypatch):
    monkeypatch.delenv("MS408_NOT_A_REAL_VAR", raising=False)
    with pytest.raises(RuntimeError, match="MS408_NOT_A_REAL_VAR"):
        require("MS408_NOT_A_REAL_VAR")


def test_require_reads_project_env_file():
    # the real .env (if present) should satisfy the key the pipeline needs
    if not (load_env() or os.environ.get("ANTHROPIC_API_KEY")):
        pytest.skip("no project .env present")
    assert require("ANTHROPIC_API_KEY").startswith("sk-ant-")
