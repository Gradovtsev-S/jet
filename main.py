from plot_velocity import plot_velocity_profile
from plot_flow import plot_flow_position


def main():
    base_path = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Data"
    cpath = base_path + r"\Calibration"
    ipath = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Images"

    data_files = [
        {
            'file': base_path + fr"\{i}_cm.txt" if i != 1 else base_path + fr"\{i}_cm_alt.txt",
            'label': f'Q ({i}0 мм)',
            'is_0txt': (i == 0)
        }
        for i in range(8)
    ]

    calib_file = cpath + r"\distance_calibration.txt"
    pressure_file = cpath + r"\pressure_calibration.txt"

    flow_rates = plot_velocity_profile(
        data_files=data_files,
        calib_file=calib_file,
        pressure_file=pressure_file,
        save_filename=ipath + r"\velocity_profile.png"
    )

    plot_flow_position(flow_rates, save_filename=ipath + r"\flow_profile.png")

    return flow_rates


if __name__ == "__main__":
    main()