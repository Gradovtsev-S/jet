import matplotlib.pyplot as plt


def plot_flow_position(flow_rates, save_filename=None):
    plt.figure(figsize=(10, 7))
    plt.minorticks_on()
    plt.grid(which='major', color='gray', linestyle='-', linewidth=0.6, alpha=0.7)
    plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.5)

    plt.xlabel('Положение трубки Пито относительно центра струи, мм')
    plt.ylabel('Расход воздуха Q, г/с')
    plt.title('Зависимость расхода от положения трубки Пито')

    distances = [i * 10 for i in range(len(flow_rates))]

    plt.plot(distances, flow_rates, 'bo-', linewidth=2, markersize=8)

    plt.xlim(-5, distances[-1] + 5)
    plt.ylim(0, max(flow_rates) * 1.2)

    plt.tight_layout()
    plt.savefig(save_filename, dpi=300)
    plt.show()