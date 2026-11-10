from pathlib import Path
import csv,json,math,statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
out=Path(__file__).resolve().parent
font=FontProperties(fname="C:/Windows/Fonts/msyh.ttc")
plt.rcParams.update({"font.family":font.get_name(),"svg.fonttype":"path"})
values={"A":[4,5,5,6],"B":[1,3,7,9]}
colors={"A":"#3F7898","B":"#BC7541"}
with (out/"data/readings.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.writer(f);w.writerow(["group","observation","value_mm"])
 for group,nums in values.items():
  for i,value in enumerate(nums,1):w.writerow([group,i,value])
stats={group:{"mean":statistics.mean(nums),"range":max(nums)-min(nums),"sample_variance":statistics.variance(nums),"sample_sd":statistics.stdev(nums)} for group,nums in values.items()}
assert stats["A"]["mean"]==stats["B"]["mean"]==5
assert math.isclose(stats["A"]["sample_variance"],2/3)
assert math.isclose(stats["B"]["sample_variance"],40/3)
assert round(stats["A"]["sample_sd"],2)==.82 and round(stats["B"]["sample_sd"],2)==3.65
(out/"data/statistics.json").write_text(json.dumps(stats,indent=2)+"\n")
fig,axes=plt.subplots(2,1,figsize=(10,4.8),sharex=True,facecolor="#F7F4EE")
for ax,(group,nums) in zip(axes,values.items()):
 ax.set_facecolor("#F7F4EE");seen={}
 for n in nums:
  y=seen.get(n,0)*.22
  ax.scatter(n,y,s=145,color=colors[group],edgecolor="#F7F4EE",linewidth=1.5,zorder=4)
  ax.annotate(str(n),(n,y),xytext=(12,0) if nums.count(n)>1 else (0,13),textcoords="offset points",ha="left" if nums.count(n)>1 else "center",va="center" if nums.count(n)>1 else "baseline",fontsize=11,color="#243849")
  seen[n]=seen.get(n,0)+1
 ax.axvline(5,color="#243849",linestyle="--",lw=1,zorder=2)
 ax.set_xlim(0,10);ax.set_ylim(-.18,.65);ax.set_yticks([])
 ax.set_title(group+"   "+("4、5、5、6 mm" if group=="A" else "1、3、7、9 mm"),loc="left",fontsize=13,color=colors[group])
 for pos in ["top","left","right"]:ax.spines[pos].set_visible(False)
 ax.spines["bottom"].set_color("#AEB9BD")
 ax.tick_params(axis="x",colors="#243849")
 ax.set_xticks(range(0,11));ax.tick_params(labelbottom=True)
axes[1].set_xlabel("读数 / mm",fontsize=12,color="#243849")
fig.suptitle("平均值都是 5 mm，分散程度不同",fontproperties=font,fontsize=18,color="#243849",x=.1,ha="left")
fig.subplots_adjust(left=.1,right=.96,top=.8,bottom=.14,hspace=.8)
fig.savefig(out/"images/02-case.svg",facecolor=fig.get_facecolor())
fig.savefig(out/"images/02-case-preview.png",dpi=140,facecolor=fig.get_facecolor())
plt.close(fig)
print("PASS independently recalculated means, ranges and sample variances; saved chart/CSV.")
