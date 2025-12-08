import matplotlib.pyplot as plt
import numpy as np


def read_values(filename):
    with open(filename, 'r') as f:
        values = [float(line.strip()) for line in f if line.strip()]
    return np.array(values)


def get_calibration_coefficients(calib_file, pressure_file, reference_pressure=95.0):
    n1 = np.mean(read_values(calib_file))
    n2 = np.mean(read_values(pressure_file))
    k = (n2 - n1) / reference_pressure
    b = n1
    return k, b


def process_velocity_profile(data_file, calib_k, calib_b, is_0txt=False, rho=1.2754):
    data_raw = read_values(data_file)

    if is_0txt:
        data_filtered = data_raw[data_raw < 2000000]
        n_data = data_filtered / 7
    else:
        data_filtered = data_raw[data_raw < 500000]
        n_data = data_filtered

    pressures = (n_data - calib_b) / calib_k
    indices_above_100 = np.where(pressures > 100)[0]
    center_idx = indices_above_100[len(indices_above_100) // 2]

    right_part = pressures[center_idx:]
    left_part = right_part[:0:-1]
    pressures_sym = np.concatenate([left_part, right_part])
    new_center_idx = len(left_part)

    positions = np.arange(len(pressures_sym)) - new_center_idx
    positions_mm = positions * 5.6e-05 * 1000
    positions_m = positions_mm / 1000

    velocities = np.sqrt(2 * pressures_sym / rho)
    velocities -= 1

    return positions_mm, velocities, positions_m


def calculate_flow_rate(positions_m, velocities, positions_mm, distance_mm):
    thresholds = {
        0: 10.0,
        10: 10.0,
        20: 10.0,
        30: 10.7,
        40: 10.0,
        50: 10.0,
        60: 10.4,
        70: 9.6
    }

    threshold = thresholds.get(distance_mm, 10.0)
    significant_indices = np.where(velocities > threshold)[0]

    if len(significant_indices) == 0:
        return 0

    start_idx = significant_indices[0]
    end_idx = significant_indices[-1]
    r = positions_m[start_idx:end_idx + 1]
    v = velocities[start_idx:end_idx + 1]

    if not np.all(np.diff(r) > 0):
        sort_idx = np.argsort(r)
        r = r[sort_idx]
        v = v[sort_idx]

    integrand = 2 * np.pi * np.abs(r) * v
    Q = np.trapz(integrand, r)
    Q_gs = Q * 1.2754 * 1000

    return Q_gs


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
    flow_rates = []
    all_positions = []
    all_velocities = []

    for i, data_info in enumerate(data_files):
        file_path = data_info['file']
        is_0txt = data_info.get('is_0txt', False)
        distance_mm = i * 10

        positions_mm, velocities, positions_m = process_velocity_profile(file_path, k, b, is_0txt)
        flow_rate = calculate_flow_rate(positions_m, velocities, positions_mm, distance_mm)
        flow_rates.append(flow_rate)

        color = colors[i % len(colors)]
        label = f"Q ({i}0мм) = {flow_rate:.2f} г/с"
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

    return flow_rates
