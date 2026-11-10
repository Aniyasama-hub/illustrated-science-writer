"""Reproduce explanatory charts and offline article; no user research data used."""
from pathlib import Path
import json, re, html, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
for folder in ['images', 'prompts', 'data']:
    (ROOT / folder).mkdir(exist_ok=True)
BG, INK, BLUE, OCHRE = '#F7F4EE', '#243849', '#3F7898', '#BC7541'
plt.rcParams.update({'font.family': 'Microsoft YaHei', 'font.size': 14,
                     'text.color': INK, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.fonttype': 'none', 'figure.facecolor': BG,
                     'axes.facecolor': BG, 'savefig.facecolor': BG})

def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

specs = [
 ('01-coexpression','共表达：比较跨样本的变化模式','A、B各代表一组变化相似的基因；曲线为概念示意，横向排列的是不同样本，不代表时间。','S1', 'concept'),
 ('02-soft-power','软阈值：把相关性转为连接权重','有符号网络的公式演示：β越大，较弱相关对应的权重越小；β＝6仅为举例。','S2','formula'),
 ('03-module-me','模块：把一组基因概括成一条曲线','左侧为构造举例的三条标准化表达曲线；右侧为同一矩阵的第一主成分得分，方向已对齐。','S1','computed-example'),
 ('04-trait','从模块到临床问题','先汇总模块，再检验其与性状的关系；混杂因素和多重比较影响证据强度。','S4','flowchart'),
 ('05-input','两张输入表：样本必须一一对应','表达矩阵与性状表使用相同样本编号和顺序；表内文字为字段示意，没有真实患者数据。','S3','diagram'),
 ('06-workflow','分析操作：每一步都有检查对象','流程从输入检查走向独立验证；软阈值与模块参数需记录，不能只保留最终热图。','S2','flowchart'),
 ('07-real-case','真实案例：小鼠肝脏与体重相关模块','据2006年原文摘录重绘：蓝色模块的MS是模块内基因与性状相关系数绝对值的均值，不是模块特征向量相关系数。','S5','published-data'),
 ('08-scope','适用范围：从发现线索到验证机制','左侧列出适合回答的问题；右侧列出需要其他设计或证据支持的结论。','S6','comparison')]

def canvas(title):
    f, ax = plt.subplots(figsize=(12, 6.4))
    f.suptitle(title, x=.06, ha='left', y=.97, fontsize=21, fontweight='bold')
    f.subplots_adjust(left=.1, right=.94, bottom=.15, top=.81)
    return f, ax

def save(f, name):
    f.savefig(ROOT/'images'/f'{name}.png', dpi=160)
    f.savefig(ROOT/'images'/f'{name}.svg')
    plt.close(f)

def box(ax, x, y, w, h, title, sub='', color=BLUE):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.025',
                 facecolor='white',edgecolor=color,linewidth=1.7))
    ax.text(x+w/2,y+h*.64,title,ha='center',va='center',fontsize=17,color=color,weight='bold')
    if sub: ax.text(x+w/2,y+h*.28,sub,ha='center',va='center',fontsize=12)

def arrow(ax, a, b):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':INK,'lw':1.8})

for name,title,caption,sid,kind in specs:
    if name.startswith('01'): continue
    (ROOT/'prompts'/f'{name}.md').write_text(
        f'# {title}\nTYPE: {kind}\nSTYLE: scientific flat explanatory diagram\n'
        f'COLORS: cream {BG}; navy {INK}; blue {BLUE}; ochre {OCHRE}.\n'
        f'ASPECT: 12:6.4\nPURPOSE: {caption}\nSOURCE: {sid}\n'
        'IMPLEMENTATION: build_article.py; exact labels and data defined in code.\n',encoding='utf-8')

# Formula illustration: signed adjacency, not a fit curve measured in a dataset.
r=np.linspace(-1,1,201)
f,ax=canvas(specs[1][1])
for power,col in [(1,BLUE),(6,OCHRE)]:
    ax.plot(r,((1+r)/2)**power,lw=3,color=col,label=f'β = {power}')
ax.set(xlabel='基因对的相关系数 r',ylabel='连接权重 a',xlim=(-1,1),ylim=(0,1.04))
ax.legend(frameon=False,loc='upper left')
ax.text(.40,.87,r'$a = [(1 + r) / 2]^{\beta}$',transform=ax.transAxes,fontsize=18)
f.text(.1,.035,'公式演示 · β＝6为举例，不是推荐参数',fontsize=12)
save(f,'02-soft-power')
np.savetxt(ROOT/'data'/'signed-adjacency.csv',np.c_[r,(1+r)/2,((1+r)/2)**6],delimiter=',',header='correlation,beta1,beta6',comments='')

# Explicit synthetic illustration and actual SVD, not fitted biological results.
x=np.array([[1,2,3,2,4,5],[1.1,1.8,3.2,2.1,3.9,5.2],[.9,2.2,2.8,1.9,4.1,4.8]]).T
z=(x-x.mean(0))/x.std(0,ddof=1)
u,s,vt=np.linalg.svd(z,full_matrices=False)
me=u[:,0]*s[0]
if np.corrcoef(me,z.mean(1))[0,1]<0: me=-me
f,ax=canvas(specs[2][1]); ax.remove()
a=f.add_axes([.09,.22,.34,.52]); b=f.add_axes([.62,.22,.29,.52])
for j,style in enumerate(['-','--',':']): a.plot(range(1,7),z[:,j],style,color=BLUE,lw=2,label=f'基因 {j+1}')
a.set(xlabel='样本编号（非时间）',ylabel='标准化表达');a.legend(fontsize=10,frameon=False)
b.plot(range(1,7),me,color=BLUE,lw=3,marker='o');b.set(xlabel='样本编号（非时间）',ylabel='第一主成分得分')
f.text(.48,.5,'→\n汇总',ha='center',fontsize=19);f.text(.09,.055,'构造举例 · 曲线来自同一组数据的计算',fontsize=12)
save(f,'03-module-me')
np.savetxt(ROOT/'data'/'synthetic-module.csv',np.c_[range(1,7),x,z,me],delimiter=',',header='sample,gene1,gene2,gene3,z1,z2,z3,PC1_score',comments='')
dump('data/calculations.json',{'synthetic_pc1_variance_fraction':float(s[0]**2/s.dot(s)),
      'signed_beta6_r_08':float(.9**6),'case_values':'Transcribed publication summaries, not recalculated from raw microarrays.'})

f,ax=canvas(specs[3][1]);ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
for xx,tt,sub in [(.02,'模块基因','一组共表达基因'),(.37,'模块特征向量','每个样本一个汇总值'),(.72,'临床性状','体重／连续指标／分组')]:
    box(ax,xx,.58,.26,.32,tt,sub)
arrow(ax,(.29,.74),(.35,.74));arrow(ax,(.7,.74),(.64,.74))
box(ax,.29,.04,.42,.30,'相关或回归检验','考虑混杂因素；报告效应量与FDR',OCHRE)
arrow(ax,(.5,.55),(.5,.37));save(f,'04-trait')

f,ax=canvas(specs[4][1]);ax.axis('off')
cols=[['样本编号','基因1','基因2','…'],['S01','表达值','表达值','…'],['S02','表达值','表达值','…'],['S03','表达值','表达值','…']]
traits=[['样本编号','体重(g)','批次','…'],['S01','测量值','A','…'],['S02','测量值','B','…'],['S03','测量值','A','…']]
for data,bbox,title in [(cols,[0,.19,.46,.59],'表达矩阵：行＝样本，列＝基因'),(traits,[.54,.19,.46,.59],'性状表：行＝同一批样本')]:
    tab=ax.table(cellText=data,cellLoc='center',bbox=bbox);tab.auto_set_font_size(False);tab.set_fontsize(12)
    for (i,j),cell in tab.get_celld().items():
        cell.set_edgecolor('#D8D7D0');cell.set_facecolor('#E4EDF1' if i==0 or j==0 else 'white');cell.set_text_props(color=INK)
    ax.text(bbox[0]+bbox[2]/2,.88,title,ha='center',fontsize=16,color=BLUE)
ax.text(.5,.04,'先按样本编号匹配，再检查顺序与缺失值',ha='center',fontsize=17,color=OCHRE)
save(f,'05-input')

f,ax=canvas(specs[5][1]);ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
steps=[('01 输入与质控','匹配样本；检查缺失与离群'),('02 表达预处理','过滤低表达；归一化与变换'),('03 选择软阈值','同时查看拟合与连接度'),('04 识别模块','TOM、聚类、剪切与合并'),('05 关联与筛选','效应量、FDR、模块内连接'),('06 验证与保存','独立队列／实验；数据与参数')]
positions=[(.02,.57),(.37,.57),(.72,.57),(.72,.05),(.37,.05),(.02,.05)]
for (tt,sub),(xx,yy) in zip(steps,positions):box(ax,xx,yy,.26,.32,tt,sub)
for a,b in [((.29,.73),(.35,.73)),((.64,.73),(.70,.73)),((.85,.55),(.85,.39)),((.70,.21),(.64,.21)),((.35,.21),(.29,.21))]:arrow(ax,a,b)
save(f,'06-workflow')

case_rows=[('体重',.395,'g'),('腹部脂肪质量',.323,'g'),('其他脂肪库总质量',.309,'g')]
with (ROOT/'data'/'published-case.csv').open('w',encoding='utf-8-sig',newline='') as h:
    w=csv.writer(h);w.writerow(['trait','MS','trait_unit','source_locator']);w.writerows([(a,b,c,'Ghazalpour2006 Results / Figure2') for a,b,c in case_rows])
f,ax=canvas(specs[6][1]);y=np.arange(3)
ax.barh(y,[a[1] for a in case_rows],color=BLUE,height=.48)
ax.set_yticks(y,[a[0]+'（g）' for a in case_rows]);ax.invert_yaxis();ax.set(xlim=(0,.5),xlabel='MS：平均绝对相关（无单位）')
for j,(_,v,_) in enumerate(case_rows):ax.text(v+.012,j,f'{v:.3f}',va='center',fontsize=17)
f.subplots_adjust(left=.27);f.text(.27,.035,'真实研究 · 135只雌性小鼠 · 原文汇总值重绘',fontsize=12)
save(f,'07-real-case')

f,ax=canvas(specs[7][1]);ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
box(ax,.02,.08,.44,.79,'适合回答', '哪些基因共同变化？\n\n哪些模块与性状有关？\n\n哪些候选值得进一步验证？',BLUE)
box(ax,.54,.08,.44,.79,'还需其他证据', '哪个基因直接调控另一个？\n\n改变它是否改变疾病？\n\n能否用于临床诊断或治疗？',OCHRE)
# Move titles upward to separate longer multiline contents.
for t in ax.texts:
    if t.get_text() in ['适合回答','还需其他证据']: t.set_y(.76)
    else:t.set_y(.40)
save(f,'08-scope')

sources=[
 {'id':'S1','title':'Langfelder & Horvath (2008). WGCNA: an R package for weighted correlation network analysis.','url':'https://link.springer.com/article/10.1186/1471-2105-9-559','locator':'Abstract; implementation categories 1–4','supports':'共表达、模块、TOM、模块特征向量和候选基因解释'},
 {'id':'S2','title':'Langfelder & Horvath. Tutorial I, 2.a: automatic network construction.','url':'https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-02-networkConstr-auto.pdf','locator':'pp.2–4','supports':'软阈值诊断、blockwiseModules及模块参数'},
 {'id':'S3','title':'Langfelder & Horvath. Tutorial I, 1: data input and cleaning.','url':'https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-01-dataInput.pdf','locator':'pp.1–3','supports':'135个起始样本、表达矩阵方向、缺失和离群、样本匹配'},
 {'id':'S4','title':'Langfelder & Horvath. Tutorial I, 3: relating modules to external information.','url':'https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-03-relateModsToExt.pdf','locator':'pp.2–5','supports':'ME与性状相关、GS、MM、结果输出'},
 {'id':'S5','title':'Ghazalpour et al. (2006). Integrating Genetic and Network Analysis to Characterize Genes Related to Mouse Weight.','url':'https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.0020130','locator':'Results: Physiological Relevance of Gene Modules; Figure2 and legend','supports':'真实小鼠研究、135只雌鼠、蓝色模块MS定义及0.395/0.323/0.309'},
 {'id':'S6','title':'WGCNA package FAQ, Langfelder & Horvath (updated 2020).','url':'https://edo98811.github.io/WGCNA_official_documentation/faq.html','locator':'Data analysis questions 1–6','supports':'样本量经验建议、过滤策略、RNA-seq处理、异质性、signed与unsigned'},
 {'id':'S7','title':'Tutorials for WGCNA: dataset description.','url':'https://edo98811.github.io/WGCNA_official_documentation/','locator':'Tutorial I data description','supports':'教程3600个表达探针、与原始研究数据及结论的关系'}]
for item in sources:item['accessed']='2026-11-10'
dump('sources.json',sources)
dump('brief.json',{'schema_version':1,'topic':'WGCNA分析','audience':'没有专业背景的临床/科研工作者','language':'zh-CN','sections':['定义解释','分析原理','分析操作','适用范围','参考与致谢'],'body_chars':[1800,2400],'min_cases':1,'min_images':8,'style':{'palette':[BG,INK,BLUE,OCHRE],'voice':'清晰、严谨、统一；去除套话','image_backend':'native imagegen + matplotlib'},'include_references_in_length':False})
dump('cases.json',[
 {'id':'C1','kind':'real','label':'真实案例：小鼠肝脏与体重','source_ids':['S5','S3','S7'],'locator':'2006原文Figure2及相邻Results；教程I.1 p.1','provenance':'原文HTML Results的MS数值逐项摘录至data/published-case.csv；没有重新分析原始微阵列','explanation':'MS为平均绝对基因–性状相关；与教程的ME相关分析区分，不混用模块颜色或结果。'},
 {'id':'C2','kind':'hypothetical','label':'构造举例','source_ids':['S1','S2'],'explanation':'六个样本三条人为表达曲线用于SVD汇总示意；软阈值β=1和6仅用于公式演示。'}])
images=[]
for k,(name,title,caption,sid,kind) in enumerate(specs,1):
    images.append({'id':f'I{k}','file':f'images/{name}.png','prompt':f'prompts/{name}.md','kind':kind,'purpose':title,'caption':f'图{k}｜{caption}','source_ids':[sid],'case_ids':['C1'] if k==7 else ['C2'] if k in [2,3] else [],'reviewed':False})
dump('images.json',images)
dump('review.json',{'semantic_checked':False,'status':'pending image and editorial review'})

article='''# WGCNA分析：把成千上万个基因整理成可以追问的线索

## 定义解释

一份转录组结果包含成千上万个基因。临床研究常关心：哪些基因共同变化，这些变化与体重、炎症指标或疾病分组有什么联系？WGCNA，即加权基因共表达网络分析，把跨样本变化相似的基因归入“模块”，再研究模块与性状的关系。[方法论文](https://link.springer.com/article/10.1186/1471-2105-9-559)给出了这套框架。

这里的“共表达”是统计上的一起变化。两个基因可以因同一种细胞增多而同时升高，也可以受共同因素影响；一条网络连线本身不能说明谁调控谁。模块颜色只是编号，换一批数据或参数，同名颜色未必代表同一生物过程。

{I1}

## 分析原理

分析先比较每对基因的表达模式，计算相关性，再把相关性转换成连接权重。软阈值通过幂运算连续压低弱连接，保留连接强弱的区别。图2演示有符号网络：强正相关获得较大权重，负相关受到压低；无符号网络则可能把强负相关也视为强连接。

{I2}

接着利用拓扑重叠度（TOM）考察两基因是否还连接着相似的邻居，结合聚类树划分模块。每个模块用第一主成分概括主要变化，称为“模块特征向量”（ME）。它给每个样本一个汇总分数，不是某一个真实基因，也不是简单平均值。

{I3}

将ME与临床指标关联，就能把“几千个基因”缩成“哪些模块值得追查”。模块成员度（MM）表示单个基因与ME的相似程度；模块内连接度表示它与同模块其他基因连接的强弱。二者有联系，但不是同一指标。筛选枢纽基因时还需结合性状关联和后续验证。[模块与性状教程](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-03-relateModsToExt.pdf)展示了具体做法。

{I4}

## 分析操作

**准备两张表。** 一张是表达矩阵，一张是同批样本的性状表。常用WGCNA函数要求表达矩阵“行是样本、列是基因”。必须按样本编号匹配两表，不能仅凭行数相同就拼接。检查缺失值、重复编号和离群样本；离群的处理应结合测序质量和生物背景。[输入教程](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-01-dataInput.pdf)从这些检查开始。

{I5}

**处理表达数据。** RNA-seq数据先过滤低表达基因、做样本间归一化，再采用方差稳定化等变换。先用差异分析筛出显著基因再建网，会把网络限制在预选信号里；可按表达量或变异程度过滤。批次、组织来源及细胞组成也要核查，避免把技术差异或细胞比例变化直接解释为基因调控。

**建网并识别模块。** 用`pickSoftThreshold`考察候选幂值，同时查看拓扑拟合和平均连接度；拟合指标不是研究质量的总分。再用`blockwiseModules`识别模块，记录网络类型、相关方法、最小模块大小、树剪切和模块合并参数。图2的β＝6只是构造举例，不能直接移作项目设置。[建网教程](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-02-networkConstr-auto.pdf)提供了完整示范。

{I6}

**关联、解释并验证。** 连续指标可做相关分析；需要调整年龄、性别等因素时，可将ME放入回归模型。报告效应量、样本数和多重比较校正结果，再结合功能富集、模块成员度和模块内连接筛选候选。保存表达矩阵、模块归属、关联表及参数，便于在独立数据中检验。

**真实案例：小鼠肝脏与体重。** Ghazalpour等在135只雌性小鼠中研究肝脏基因表达与生理性状。原文报告蓝色模块与体重的模块显著性MS为0.395，与腹部脂肪质量的MS为0.323。这里的MS是模块内各基因与性状相关系数绝对值的均值，不能写成“模块ME与体重相关系数为0.395”。[原始研究](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.0020130)还结合遗传信息追查相关线索。

{I7}

后续WGCNA教程从该研究数据整理出3600个表达探针用于演示；起始样本数为135，质控后再开展建网。教程的模块划分与原文不完全相同，复现时应明确采用哪套流程，不能拼接两套结果。[教程数据说明](https://edo98811.github.io/WGCNA_official_documentation/)列出了其来源。

## 适用范围

WGCNA适合在一组可比较、具有足够独立样本的数据中寻找共变化模式，尤其适合把转录组与连续临床指标联系起来。它补充单基因差异分析，提供模块层面的候选线索。

[作者FAQ](https://edo98811.github.io/WGCNA_official_documentation/faq.html)不建议对少于15个样本的数据尝试常规WGCNA，条件允许时至少20个；这是经验建议，不能替代针对研究设计的样本量评估。多个细胞来自同一受试者时，细胞数量也不能直接当作独立受试者数量。疾病分组与批次完全重合时，统计校正难以分辨两种来源。

{I8}

一个高连接基因可以作为后续实验对象；要判断它是否推动疾病变化，仍需时间顺序、干预实验等证据。要形成诊断模型，还需独立队列验证预测性能。把网络发现与验证设计接起来，候选线索才有机会成为可靠结论。

## 参考与致谢

1. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. *BMC Bioinformatics*. 2008;9:559. [全文与DOI](https://link.springer.com/article/10.1186/1471-2105-9-559)。
2. Ghazalpour A, et al. Integrating Genetic and Network Analysis to Characterize Genes Related to Mouse Weight. *PLoS Genetics*. 2006;2(8):e130. [全文与DOI](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.0020130)。
3. Langfelder P, Horvath S. WGCNA教程I：[数据清理](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-01-dataInput.pdf)、[建网与模块](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-02-networkConstr-auto.pdf)、[性状关联](https://edo98811.github.io/WGCNA_official_documentation/FemaleLiver-03-relateModsToExt.pdf)。2014年版；链接为作者文档的公开镜像。
4. [WGCNA FAQ](https://edo98811.github.io/WGCNA_official_documentation/faq.html)，更新于2020年；访问日期：2026年11月10日。

感谢方法作者及原始研究团队公开论文、教程和数据。图1为共表达概念插画，图2—6、8为本篇制作的解释图，图7按原文汇总值重绘；均未直接复制论文图片。
'''
for k,i in enumerate(images,1):
    article=article.replace('{I'+str(k)+'}',f'![{specs[k-1][1]}]({i["file"]})\n\n{i["caption"]}')
(ROOT/'article.md').write_text(article,encoding='utf-8')

def inline(s):
    s=html.escape(s)
    s=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',r'<img alt="\1" src="\2" loading="lazy">',s)
    s=re.sub(r'\[([^]]*)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    return s
parts=[]
for para in article.strip().split('\n\n'):
    if para.startswith('# '):parts.append('<h1>'+inline(para[2:])+'</h1><p class="subtitle">图解方法 · 临床与科研入门</p>')
    elif para.startswith('## '):parts.append('<h2>'+inline(para[3:])+'</h2>')
    else:parts.append('<p'+(' class="caption"' if para.startswith('图') else '')+'>'+inline(para).replace('\n','<br>')+'</p>')
css='''body{margin:0;background:#F7F4EE;color:#243849;font-family:"Microsoft YaHei",sans-serif;line-height:1.95}main{max-width:860px;margin:auto;padding:50px 26px 90px}h1{font-size:36px;line-height:1.4;letter-spacing:-.5px}h2{font-size:25px;margin-top:56px;border-top:1px solid #d9d8d0;padding-top:30px}p{font-size:17px;margin:22px 0}a{color:#3F7898;text-underline-offset:4px;overflow-wrap:anywhere}img{display:block;width:100%;height:auto;border-radius:12px}code{font-size:.86em;overflow-wrap:anywhere}.caption,.subtitle{font-size:14px;color:#647583;line-height:1.7}.subtitle{letter-spacing:2px;color:#BC7541}@media(max-width:500px){main{padding:25px 18px 60px}h1{font-size:28px}h2{font-size:22px}p{font-size:16px}}'''
(ROOT/'preview.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>图解WGCNA分析</title><style>'+css+'</style><main>'+''.join(parts)+'</main></html>',encoding='utf-8')
print('Article and seven reproducible charts built:',ROOT)
