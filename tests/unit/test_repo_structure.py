from pathlib import Path


def test_core_directories_exist() -> None:
    required = [
        "data/raw",
        "data/processed",
        "data/external",
        "src/ingestion",
        "src/pipelines",
        "src/transformations",
        "api",
        "dashboard",
        "docs",
    ]
    for rel_path in required:
        assert Path(rel_path).exists(), f"Missing required path: {rel_path}"
