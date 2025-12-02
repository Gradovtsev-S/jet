import matplotlib.pyplot as plt
import numpy as np


def read_values(filename):
    with open(filename, 'r') as f:
        values = [float(line.strip()) for line in f if line.strip()]
    return np.array(values)

path = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Data\Calibration"

acp_values = read_values(path + r"\distance_calibration.txt")
s_values = read_values(path + r"\pressure_calibration.txt")

n1 = np.mean(acp_values)
n2 = np.mean(s_values)
p2 = 96.0
p1 = 0.0

p_points = np.array([p1, p2])
n_points = np.array([n1, n2])

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(p_points, n_points, 'ro', label='Измерения', markersize=8)
ax.plot([p1, p2], [n1, n2], 'b-', linewidth=2, label='Линейная зависимость')

ax.set_title('Зависимость показаний АЦП от давления', fontsize=14)
ax.set_xlabel('Давление [Па]', fontsize=12)
ax.set_ylabel('Отсчёты АЦП', fontsize=12)

n_min, n_max = min(n1, n2), max(n1, n2)
n_range = n_max - n_min

ax.set_xlim(p1 - 5, p2 + 10)
ax.set_ylim(n_min - 0.1 * n_range, n_max + 0.1 * n_range)

ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, loc='best')

plt.tight_layout()
ipath = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Images"
plt.savefig(ipath + r"\pressure-calibration.png", dpi=300)
plt.show()
