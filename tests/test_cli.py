import json
from pathlib import Path

from metadata_preview.cli import main


def test_cli_json_output(tmp_path: Path, capsys):
    source = tmp_path / "sample.txt"
    source.write_text("sample", encoding="utf-8")
    assert main([str(source), "--hash"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == 1
    assert payload["files"][0]["name"] == "sample.txt"
    assert len(payload["files"][0]["sha256"]) == 64


def test_cli_report_file(tmp_path: Path):
    source = tmp_path / "sample.txt"
    output = tmp_path / "reports" / "metadata.json"
    source.write_text("x", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8"))["files"][0]["size_bytes"] == 1


def test_cli_partial_failure(tmp_path: Path, capsys):
    source = tmp_path / "ok.txt"
    source.write_text("ok", encoding="utf-8")
    assert main([str(source), str(tmp_path / "missing")]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert "error" in payload["files"][1]


def test_cli_requires_input(capsys):
    assert main([]) == 2
    assert "provide at least one" in capsys.readouterr().err
