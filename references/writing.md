# 写作适配

上游入口：[content-research-writer](../upstream/content-research-writer/SKILL.md)。按任务读取 “Understand the Writing Project / Conduct Research / Section Feedback / Voice Preservation” 等相关部分。本集成采用其资料—提纲—逐节修改方法，不采用营销式 Hook、泛化结尾或强制 Call to action。

工具适配：把 WebSearch / WebFetch 对应为运行时实际检索和网页读取工具；不要照抄不存在的命令。保持固定章节优先于上游通用 Hook / Introduction / Conclusion。上游询问的信息若用户已提供，直接使用，不重复采访。

sources.json 是数组：每项含 id、title、url、accessed、supports（具体支持何种事实）。引用真实打开的来源；检索摘要不能当全文证据。可另加 locator 标明章节/页码。正文在相关事实附近使用 Markdown 来源链接。

cases.json 是数组：每项含 id、kind（hypothetical 或 real）、label、source_ids、explanation；real 还需 locator 和 provenance（原始资料或已授权数据的定位）。自行构造的数字标注举例；不能用“某研究发现”包装。数字表和计算脚本随文保存。
