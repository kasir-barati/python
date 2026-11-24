SHELL         := /bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help

.ONESHELL:
.PHONY: help update_index

## Show this help message
help:
	@echo "Makefile targets:"
	@echo ""
	@awk '/^## /{desc = substr($$0, 4)} /^[a-zA-Z_-]+:/{if (desc) {target = $$1; sub(/:.*/, "", target); printf "  make %-20s- %s\n", target, desc; desc = ""}}' $(MAKEFILE_LIST)
	@echo ""

## Regenerates index.md and the sidebar (_includes/nav_tree.html) from all markdown files so GH Pages always shows up to date content
update_index:
	@python3 scripts/gen_nav.py
	@{
		echo "# Content"
		for f in $$(git ls-files --cached --others --exclude-standard -- '*.md' \
			| grep -vE '^(index|README|wip)\.md$$|(^|/)\.|(^|/)(AGENTS|CLAUDE|SKILL)\.md$$|node_modules/' \
			| LC_ALL=C sort); do
			title=$$(awk '/^```/ {c = !c; next} !c && /^# +/ {sub(/^# +/, ""); print; exit}' "$$f" \
				| sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g')
			printf '%s\t%s\n' "$$f" "$${title:-$$f}"
		done | awk -F'\t' '
			{
				n = split($$1, parts, "/")
				if (n > 1 && parts[1] != top) {
					top = parts[1]; split("", prev); plen = 0
					print "\n## " top "\n"
				}
				common = 0
				while (common < plen && common < n - 2 && prev[common + 1] == parts[common + 2]) common++
				for (d = common + 1; d <= n - 2; d++) printf "%*s- %s\n", (d - 1) * 2, "", parts[d + 1]
				plen = n - 2
				for (d = 1; d <= plen; d++) prev[d] = parts[d + 1]
				printf "%*s- [%s](./%s)\n", plen * 2, "", $$2, $$1
			}'
	} > index.md
