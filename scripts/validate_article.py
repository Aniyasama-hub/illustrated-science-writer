"""Validate article structure, evidence references and assets; not scientific truth."""
import argparse, hashlib, json, re, sys
from pathlib import Path
import xml.etree.ElementTree as ET

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def visible_lines(text):
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(\x60{3,}|~{3,})", line)
        if match:
            token = match.group(1)[0]
            fence = None if fence == token else token if fence is None else fence
        elif fence is None:
            result.append(line)
    return result

def body_length(text, sections):
    lines = visible_lines(text)
    if sections[-1] in {"参考资料", "参考与致谢", "参考文献"}:
        lines = lines[:next((i for i,l in enumerate(lines) if l.strip()=="## "+sections[-1]),len(lines))]
    value = "\n".join(l for l in lines if not re.match(r"^#{1,6}\s",l))
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return len(re.sub(r"\s", "", value))

def validate(directory):
    root = Path(directory).resolve()
    errors, warnings = [], []
    def fail(message):
        errors.append(message)
    def asset(name):
        if not isinstance(name,str) or not name:
            fail("Missing asset path"); return None
        p = (root/name).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            fail("Missing or escaping asset: "+name); return None
        return p
    try:
        brief, sources, cases, images, review = [read(root/(n+".json")) for n in ["brief","sources","cases","images","review"]]
        text = (root/"article.md").read_text(encoding="utf-8")
        if not isinstance(brief,dict) or any(not isinstance(v,list) for v in [sources,cases,images]):
            raise ValueError("Invalid manifest container")
        sections = brief["sections"]
        if not sections or any(not isinstance(h,str) or not h for h in sections):
            raise ValueError("Invalid sections")
        headings = [m.group(1).strip() for l in visible_lines(text) if (m:=re.match(r"^##\s+(.+)$",l))]
        if headings != sections: fail("Heading order mismatch: "+repr(headings))
        count = body_length(text,sections)
        low,high = brief["body_chars"]
        if not low<=count<=high: fail(f"Body length {count}, expected {low}–{high}")
        def ids(records,kind):
            values = [r["id"] for r in records]
            if len(values)!=len(set(values)): fail("Duplicate "+kind+" IDs")
            return set(values)
        sids,cids = ids(sources,"source"),ids(cases,"case")
        ids(images,"image")
        for s in sources:
            if not all(s.get(k) for k in ["title","supports","accessed"]) or not re.match(r"^https?://",s.get("url","")):
                fail("Incomplete source "+s["id"])
            if s.get("url") not in text: warnings.append("Unused source "+s["id"])
        if len(cases)<brief.get("min_cases",1): fail("Not enough cases")
        for c in cases:
            if c["kind"] not in {"real","hypothetical"}: fail("Unknown case kind")
            if not c.get("label") or c["label"] not in text: fail("Case label missing")
            if not c.get("explanation"): fail("Case explanation missing")
            if not set(c.get("source_ids",[]))<=sids: fail("Unknown case source")
            if c["kind"]=="real" and not all(c.get(k) for k in ["source_ids","locator","provenance"]):
                fail("Real case lacks traceable evidence")
            if c["kind"]=="hypothetical" and not re.search(r"举例|假设|构造",c["label"]):
                fail("Hypothetical case is not explicitly labelled")
        if len(images)<brief.get("min_images",2): fail("Not enough illustrations")
        embedded = re.findall(r"!\[[^\]]*\]\(([^)]+)\)",text)
        if set(embedded)!={i["file"] for i in images}: fail("Image manifest and article differ")
        hashes = {}
        for i in images:
            if not all(i.get(k) for k in ["purpose","caption","kind"]): fail("Incomplete image")
            if i.get("caption") not in text: fail("Image caption absent")
            if i.get("reviewed") is not True: fail("Image not visually reviewed")
            if not set(i.get("source_ids",[]))<=sids or not set(i.get("case_ids",[]))<=cids: fail("Unknown image evidence")
            prompt=asset(i.get("prompt"))
            if prompt and not prompt.read_text(encoding="utf-8").strip(): fail("Empty image specification")
            p=asset(i.get("file"))
            if p:
                b=p.read_bytes()
                if p.suffix.lower()==".png" and not b.startswith(b"\x89PNG\r\n\x1a\n"): fail("Invalid PNG")
                if p.suffix.lower()==".svg":
                    try:
                        if ET.fromstring(b).tag.split("}")[-1]!="svg": fail("Invalid SVG root")
                    except ET.ParseError: fail("Malformed SVG")
                hashes[i["file"]]=hashlib.sha256(b).hexdigest()
        if not isinstance(review,dict) or review.get("semantic_checked") is not True: fail("Semantic editorial review missing")
        for phrase in ["作为AI","作为 AI","在当今","不构成任何建议","值得注意的是","让我们一起","综上所述"]:
            if phrase in text: warnings.append("Review contextual filler: "+phrase)
        return {"passed":not errors,"body_chars":count,"image_sha256":hashes,"errors":errors,"warnings":warnings,
                "scope":"Mechanical checks only; review declarations do not prove scientific correctness."}
    except (OSError,ValueError,KeyError,TypeError) as e:
        return {"passed":False,"errors":[*errors,str(e)],"warnings":warnings}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("directory");p.add_argument("--report");args=p.parse_args()
    result=validate(args.directory);output=json.dumps(result,ensure_ascii=False,indent=2)
    if args.report: Path(args.report).write_text(output+"\n",encoding="utf-8")
    print(output);sys.exit(0 if result["passed"] else 1)
