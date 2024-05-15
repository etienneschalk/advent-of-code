import tomllib
from pathlib import Path


def main():
    project_home_path = Path(__file__).parent.parent
    print(project_home_path)

    pyproject_file_path = project_home_path / "pyproject.toml"

    with pyproject_file_path.open(mode="rb") as fp:
        toml_content = tomllib.load(fp)

    toml_path = "tool.poetry.group.docs.dependencies"
    docs_sections = toml_content
    for section in toml_path.split("."):
        docs_sections = docs_sections[section]

    requirements_txt_content = f"""
# DO NOT UPDATE MANUALLY
# AUTO-GENERATED FROM {Path(__file__).relative_to(project_home_path)}

# Workaround: adapted from pyproject.toml as poetry groups are non standard.

{"\n".join(f"{k}=={v.replace("^", "")}" for k,v in docs_sections.items())}
"""

    print(requirements_txt_content)

    requirements_txt_file_path = project_home_path / "docs/source/requirements.txt"
    requirements_txt_file_path.write_text(requirements_txt_content)

    print(f"Written to {requirements_txt_file_path}")


if __name__ == "__main__":
    main()
