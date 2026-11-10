"""Behavioral checks using a real article bundle, including deliberately damaged copies."""
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
base=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("validator",base/"scripts/validate_article.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ArticleContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="science-article-test-")
        self.root=Path(self.temp.name)/"article"
        shutil.copytree(base/"examples/mean-and-spread",self.root)
    def tearDown(self):self.temp.cleanup()
    def change(self,name,fn):
        p=self.root/(name+".json");d=json.loads(p.read_text(encoding="utf-8"))
        fn(d);p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
    def test_complete_bundle(self):
        self.assertTrue(module.validate(self.root)["passed"])
    def test_missing_image_is_failure(self):
        (self.root/"images/01-concept.png").unlink()
        self.assertFalse(module.validate(self.root)["passed"])
    def test_false_real_case_is_failure(self):
        self.change("cases",lambda d:d[0].update(kind="real"))
        self.assertFalse(module.validate(self.root)["passed"])
    def test_unresolved_evidence_is_failure(self):
        self.change("images",lambda d:d[0].update(source_ids=["invented-source"]))
        self.assertFalse(module.validate(self.root)["passed"])
    def test_wrong_heading_order_is_failure(self):
        self.change("brief",lambda d:d["sections"].reverse())
        self.assertFalse(module.validate(self.root)["passed"])
    def test_user_defined_titles_are_respected(self):
        p=self.root/"article.md";s=p.read_text(encoding="utf-8")
        d=json.loads((self.root/"brief.json").read_text(encoding="utf-8"))
        names=["先看问题","再看原理","具体例子","操作建议","参考资料"]
        for old,new in zip(d["sections"],names):s=s.replace("## "+old,"## "+new)
        p.write_text(s,encoding="utf-8")
        self.change("brief",lambda d:d.update(sections=names))
        self.assertTrue(module.validate(self.root)["passed"])
    def test_fenced_example_does_not_add_sections(self):
        p=self.root/"article.md";s=p.read_text(encoding="utf-8")
        s=s.replace("## 参考资料","~~~markdown\n## 这只是代码示例\n~~~\n\n## 参考资料")
        p.write_text(s,encoding="utf-8")
        self.assertTrue(module.validate(self.root)["passed"])
    def test_path_escape_is_failure(self):
        outside=Path(self.temp.name)/"outside.png";outside.write_bytes((self.root/"images/01-concept.png").read_bytes())
        self.change("images",lambda d:d[0].update(file="../outside.png"))
        p=self.root/"article.md";p.write_text(p.read_text(encoding="utf-8").replace("images/01-concept.png","../outside.png"),encoding="utf-8")
        self.assertFalse(module.validate(self.root)["passed"])
if __name__=="__main__":unittest.main()
