# illustrated-science-writer

按限定结构写中文图解科普文章：先核实资料和案例，再统一正文、解释图与图注。当前技能版本 **0.1.0**。

这是一个可阅读、可修改的集成技能：原创中控结合 `content-research-writer` 的研究与写作方法、`baoyu-article-illustrator` 的图型与风格规划。上游快照保留原文件和提交哈希；本项目不宣称完整运行了两套上游插件。

## 下载与使用

- [技能安装包](packages/illustrated-science-writer-0.1.0.zip?raw=true)：约104KB，不包含文章示例；附[SHA256](packages/illustrated-science-writer-0.1.0.sha256)。
- 完整源码、示例与文档：GitHub 的 **Code → Download ZIP**。本仓库当前为私有，需要已获授权的账号下载；下载后可以交给其他AI读取。
- 支持目录型技能的宿主：将安装包中的 `illustrated-science-writer` 文件夹放入该宿主支持的技能目录，按宿主规则启用。
- 不支持技能的智能体：读取根目录 [SKILL.md](SKILL.md) 及其中用到的适配文档，再执行你的选题要求。纯聊天产品可先提供这些文本，再按需要提供上游参考文件。

使用示例：

```text
使用 illustrated-science-writer。
选题：WGCNA分析
读者：没有专业背景的临床/科研工作者
篇幅：2000字左右
结构：定义解释 → 分析原理 → 分析操作 → 适用范围 → 参考与致谢
配图：8张，风格统一
案例优先使用可核实的真实案例。
```

## 仓库内容

| 入口 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 单一中控工作流 |
| [references/](references/) | 写作、文风、图文适配和可调默认约定 |
| [docs/PORTABILITY.md](docs/PORTABILITY.md) | 在不同智能体中运行与微调 |
| [benchmarks/](benchmarks/) | 同题要求、来源快照模式和评审记录模板 |
| [examples/wgcna/article.md](examples/wgcna/article.md) | 约2000字、8张图的WGCNA成稿 |
| [examples/mean-and-spread/article.md](examples/mean-and-spread/article.md) | 约950字、2张图的统计入门示例 |
| [scripts/](scripts/) | 标准库校验器，无需API密钥 |
| [upstream.lock.json](upstream.lock.json) | 两个上游的固定版本、38个文件的哈希 |

图文网页位于各示例的 `preview.html`；下载到本机后用浏览器打开，GitHub文件页不会运行HTML。示例中的来源、案例、数据、提示词和审阅记录均随文保存。示例展示当前生成效果，不作为其他模型必须模仿的标准答案。

## 验证

需要Python 3.9或更高版本；两个校验器和单元测试仅使用标准库。

```sh
python -X utf8 scripts/check_package.py
python -X utf8 scripts/validate_article.py examples/wgcna
python -X utf8 scripts/validate_article.py examples/mean-and-spread
python -X utf8 -m unittest discover -s tests -v
```

示例的重绘脚本另需numpy、matplotlib；浏览器版式检查另需Playwright。这些不属于技能检查器的运行依赖。

当前示例由同一生成助手检查，未进行跨模型盲评或独立专家审稿。机械检查可验证结构、资源与来源ID的对应，不能证明科学结论正确，也不代表“去AI检测”能力。

## 来源与许可

原创中控与脚本使用[MIT](LICENSE)；上游Apache-2.0和MIT材料分别保留原许可及说明，见[第三方声明](THIRD_PARTY_NOTICES.md)。示例中的文献和模型成图不自动继承技能代码的MIT许可。仓库不包含API密钥、个人研究数据或原工作站设置。
