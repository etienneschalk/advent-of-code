from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, kw_only=True)
class ExampleInputsStore:
    _parsed_toml: dict[str, Any]

    def retrieve(self, test_file_path: str, content_id: str = "EXAMPLE_INPUT") -> str:
        test_file_path = Path(test_file_path).stem

        content = self._parsed_toml[test_file_path][content_id]
        content = str(content)  # should only contain str, not anything else.
        return content
