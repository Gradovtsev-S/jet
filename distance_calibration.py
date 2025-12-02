import matplotlib.pyplot as plt
import numpy as np

x_factor = 5.6e-05
displacement_cm = 5.0
total_steps = 900

steps = np.linspace(0, total_steps, 100)
displacement = steps * x_factor * 100

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(steps, displacement, 'b-', linewidth=2, label=f'Калибровочная зависимость\nx = {x_factor} * step [м]')

ax.set_title('Калибровочный график\nЗависимость перемещения трубки Пито от шага двигателя', fontsize=14)
ax.set_xlabel('Количество шагов', fontsize=12)
ax.set_ylabel('Перемещение трубки Пито [см]', fontsize=12)

ax.set_xlim(-50, total_steps + 50)
ax.set_ylim(-0.5, displacement_cm + 0.5)

ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True)

plt.tight_layout()
plt.show()
