import matplotlib.pyplot as plt
import numpy as np


def read_values(filename):
    with open(filename, 'r') as f:
        values = [float(line.strip()) for line in f if line.strip()]
    return np.array(values)


def get_calibration_coefficients(calib_file, pressure_file, reference_pressure=96.0):
    n1 = np.mean(read_values(calib_file))
    n2 = np.mean(read_values(pressure_file))
    k = reference_pressure / (n2 - n1)
    b = -k * n1
    return k, b


def process_velocity_profile(data_file, calib_k, calib_b, is_1txt=False, rho=1.29):
    data_raw = read_values(data_file)

    if is_1txt:
        data_filtered = data_raw[data_raw < 2000000]
        n_data = data_filtered / 7
    else:
        data_filtered = data_raw[data_raw < 500000]
        n_data = data_filtered

    pressures = calib_k * n_data + calib_b
    center_idx = np.argmax(pressures)

    right_part = pressures[center_idx:]
    left_part = right_part[:0:-1]
    pressures_sym = np.concatenate([left_part, right_part])
    new_center_idx = len(left_part)

    positions = np.arange(len(pressures_sym)) - new_center_idx
    positions_mm = positions * 5.6e-05 * 1000

    velocities = np.sqrt(2 * pressures_sym / rho)

    return positions_mm, velocities


def plot_velocity_profile(data_files, calib_file, pressure_file, save_filename=None):
    k, b = get_calibration_coefficients(calib_file, pressure_file)

    plt.figure(figsize=(10, 7))
    plt.minorticks_on()
    plt.grid(which='major', color='gray', linestyle='-', linewidth=0.6)
    plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)

    plt.ylabel('Скорость воздуха, м/с')
    plt.xlabel('Положение трубки Пито относительно центра струи, мм')
    plt.title('Скорость потока воздуха в сечении затопленной струи')

    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

    all_positions = []
    all_velocities = []

    q_labels = [
        'Q (00 мм)',
        'Q (10 мм)',
        'Q (20 мм)',
        'Q (30 мм)',
        'Q (40 мм)',
        'Q (50 мм)',
        'Q (60 мм)',
        'Q (70 мм)'
    ]

    for i, data_info in enumerate(data_files):
        file_path = data_info['file']
        is_1txt = data_info.get('is_1txt', False)

        if i < len(q_labels):
            label = q_labels[i]
        else:
            label = f'Файл {i + 1}'

        color = colors[i % len(colors)]

        positions_mm, velocities = process_velocity_profile(file_path, k, b, is_1txt)

        plt.plot(positions_mm, velocities, color=color, linewidth=2, label=label)

        all_positions.append(positions_mm)
        all_velocities.append(velocities)

    plt.legend(loc='upper left', frameon=True)

    if all_positions:
        all_positions_concat = np.concatenate(all_positions)
        all_velocities_concat = np.concatenate(all_velocities)

        plt.xlim(np.min(all_positions_concat) - 5, np.max(all_positions_concat) + 5)
        plt.ylim(0, max(25, np.max(all_velocities_concat) * 1.1))

    plt.tight_layout()

    if save_filename:
        plt.savefig(save_filename, dpi=300)

    plt.show()