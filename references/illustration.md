# 图文适配

上游入口：[baoyu-article-illustrator](../upstream/baoyu-article-illustrator/SKILL.md)。
在本集成中按需读取其参考：
- [图型与风格](../upstream/baoyu-article-illustrator/references/styles.md)
- [提示词构造](../upstream/baoyu-article-illustrator/references/prompt-construction.md)
- [教育等预设](../upstream/baoyu-article-illustrator/references/style-presets.md)

复用 Type × Style × Palette 的组织方法。绘图规格按 ZONES / LABELS / COLORS / STYLE / ASPECT 描述。主工作流由本技能完成；不把其他宿主的 Skill 调用、持久化偏好或重复确认逻辑假定为可用。

每张图片必须回答一个正文问题。优先选择原理/机制、输入到输出的分步关系、或案例对比。装饰封面不计解释图数量。
- 数据图：使用 matplotlib、R 等标准绘图，固定坐标与单位，保留 CSV 和制图脚本，不交给生图模型“猜”准确坐标。
- 概念插画：用运行时内置 imagegen。没有该能力时，可交付明确标记的配图方案，但不得宣称完成配图；不得悄悄改用付费 API。
- 简单可编辑流程图：可输出 SVG；这是本集成按输出用途的路由，与上游 raster-only 全流程有区别，要在 review.json 写清实际采用方式。

images.json 是数组：id、file（相对路径）、prompt（相对路径）、kind、purpose、caption、source_ids、case_ids、reviewed（真实看过后才为 true）。概念图要区分已知机制与假设，案例图注明真实/举例。图注放正文图片下方，具体解释读图方式。

默认米白底、深蓝文字、蓝/赭两种强调色，中文图注，图中文字尽量少；用户参考风格优先。同一文章的图按同一 style spec 制作。需要风格锚定时使用已看过的参考图。
