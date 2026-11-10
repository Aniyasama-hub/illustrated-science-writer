# 第三方来源与适配边界

本集成 0.1.0 的总控、模板、文风规则和检查器采用根目录 MIT 许可；第三方目录保留各自许可。源文件未改写，逐文件 SHA256 与来源提交记录在 upstream.lock.json。

- upstream/content-research-writer：ComposioHQ/awesome-claude-skills 的 content-research-writer。仓库 README 声明 Apache-2.0，并提示各 skill 可能不同；本次目录未发现另行许可。原 README 留在 licenses/content-research-writer/UPSTREAM_README.md，标准 Apache-2.0 文本来自 apache.org，未冒充上游自带 LICENSE。若再发行前上游另行说明，以对应版权人的有效许可为准。
- upstream/baoyu-article-illustrator：JimLiu/baoyu-skills 中的完整对应目录。MIT；Copyright (c) 2026 Jim Liu。许可证在 licenses/baoyu-article-illustrator/LICENSE。

本集成原创 references/ 下的适配明确区分上游完整流程和本地引用式组合。没有复刻 imagegen 的实现；宿主生图能力、API 服务、用户资料和成图的许可由各自来源与服务条款决定。模型输出不自动继承本技能 MIT。

没有另装 humanizer、文献代理、发布插件或外部生图 SDK。Python 检查器仅用标准库。此包不包含密钥和上游 Git 仓库历史。
