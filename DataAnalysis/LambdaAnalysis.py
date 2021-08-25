import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
df
COST = 0.0000166667 # $/GBs
df["BilledDurationInGBSeconds"] = df["BilledDurationInGBSeconds"]*COST

df["Adj. Timestamp"] = df["Timestamp"].astype('datetime64[m]')

time2count = df["Adj. Timestamp"].value_counts()

index = df["Adj. Timestamp"].value_counts().index.tolist()

time2count_final = time2count[index]

df2 = df[[a in list(time2count_final.keys()) for a in df["Adj. Timestamp"]]].copy()
df2["Category"] = df2.apply(lambda x: time2count_final[x["Adj. Timestamp"]], axis=1)
def mean_above_7(l):
    i = [a for a in l if a > 7]
    return sum(i)/len(i)
mean = df2[["BilledDurationInGBSeconds", "Category"]].groupby(["Category"], axis=0).mean()
total = df2[["BilledDurationInGBSeconds", "Category"]].groupby(["Category"], axis=0).sum()

experiments = {}
for i in time2count_final.keys():
    experiments[i] = df[df["Adj. Timestamp"] ==i][["BilledDurationInGBSeconds", "Adj. Timestamp"]]

plt.figure(figsize=(8,5))
ax = plt.subplot(1,1,1)

red, green = "xkcd:red", "xkcd:green"
plt.title("Custos Lambda por Categoria")
ax.set_xticks(time2count_final.values.tolist())
ax.grid(True)
l1, = ax.plot(mean.index, mean["BilledDurationInGBSeconds"], color=green, lw=2, ls="--", label="Média")
for cost, cat in zip(df2["BilledDurationInGBSeconds"], df2["Category"]):
    ax.scatter(cat, cost, color=green, alpha=0.3)
ax.set_xlabel("Número de Disparos Concorrentes")
ax.set_ylabel("Gastos Individuais (U$)", color=green)
ax.tick_params(axis="y", labelcolor=green)
ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

ax2 = ax.twinx()
ax2.scatter(total.index, total["BilledDurationInGBSeconds"], color=red, lw=3)
l2, = ax2.plot(total.index, total["BilledDurationInGBSeconds"], color=red, alpha=0.5,ls="--")
ax2.set_ylabel("Gasto total (U$)", color=red)
ax2.tick_params(axis="y", labelcolor=red)

ax.legend((l1, l2), ('Média', 'Total por Categoria'), loc='lower right', shadow=True, fontsize = "x-large")
plt.savefig("lambda_plot.png")

"""
Percent increases:
Cat. Cost.          Ratio:
64	433.2335		64/32	2.007676498
48	329.5385		48/32	1.527136525
32	215.7885			
"""



