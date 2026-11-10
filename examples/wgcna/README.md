# WGCNA图解科普文章

打开 `preview.html` 阅读图文成稿；`article.md` 便于编辑。正文按用户指定五节编排，约2000字，8张解释图。

- `images/`：8张PNG；其中7张另附SVG。
- `prompts/`：生图提示词原文、图文规划及每张图的制图规格。
- `data/`：公式演示数据、构造举例矩阵和从原文摘录的真实案例汇总值。
- `sources.json`、`cases.json`：来源定位和案例性质。
- `review.json`：语义和图像检查记录。
- `validation.json`、`preview-checks.json`：机械校验和桌面/手机页面检查。

概念图1使用内置image_gen生成；其余图由matplotlib绘制。没有运行原始研究的WGCNA分析，也没有使用当前工作区的研究数据。案例图中的MS数据是原文摘录，不能视为重新分析原始微阵列所得。

重绘图2—8：`python -X utf8 build_article.py`，需要numpy和matplotlib及Microsoft YaHei字体。此命令会重新生成本目录内的文章和清单，并将审阅状态重置为待核查；图1保留已有文件，不调用生图服务。重绘后须重新核对图文及补全审阅状态，再运行技能的validate_article.py。页面检查脚本check_preview.py需要Playwright及Chromium。

文中引用的论文和教程权利归原作者；本篇概念图和重绘图未直接复制原文图片。
