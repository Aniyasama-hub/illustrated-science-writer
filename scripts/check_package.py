"""Offline integrity check for vendored skills and controller references."""
import hashlib,json,re,sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
errors=[]
lock=json.loads((root/"upstream.lock.json").read_text(encoding="utf-8"))
for dep in lock["dependencies"]:
    for record in dep["files"]:
        p=root/record["path"]
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=record["sha256"]:
            errors.append("Modified or missing upstream file: "+record["path"])
    if not (root/"licenses"/dep["name"]/"LICENSE").is_file():
        errors.append("Missing license for "+dep["name"])
for p in [root/"SKILL.md",*(root/"references").glob("*.md")]:
    for link in re.findall(r"\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
        if "://" in link or link.startswith("#"):continue
        if not (p.parent/link.split("#")[0]).exists():
            errors.append("Broken controller reference: "+link)
if not (root/"agents/openai.yaml").is_file():errors.append("Missing UI metadata")
print(json.dumps({"passed":not errors,"version":lock["package_version"],"upstream_files":sum(len(d["files"]) for d in lock["dependencies"]),"errors":errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
