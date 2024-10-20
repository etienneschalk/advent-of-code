from coverage import coverage

cov = coverage()
cov.load()
total = cov.report()

print(total)
badge_md_img = (
    f"![pytest-cov](https://img.shields.io/badge/coverage-{total:.0f}%25-purple)"
)

print(badge_md_img)
