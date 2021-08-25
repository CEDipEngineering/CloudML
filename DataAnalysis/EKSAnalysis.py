import matplotlib.pyplot as plt

data = [0.05, 0.04, 0.09, 0.13]
index = [  4,    8,   16,   32]

cost_offset = 2*0.75*0.0464
data = [i+cost_offset for i in data]

plt.figure(figsize=(8,5))
ax = plt.subplot(1,1,1)

green = "xkcd:bright blue"
plt.title("Custos EKS por Categoria")
ax.set_xticks(index)
ax.grid(True)
l1, = ax.plot(index, data, color=green, lw=2, ls="--")
ax.set_xlabel("Número de Tarefas")
ax.set_ylabel("Gastos Totais (U$)", color=green)
ax.tick_params(axis="y", labelcolor=green)
plt.savefig("EKS_plot.png")
