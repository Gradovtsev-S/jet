from plot_velocity import plot_velocity_profile


def main():
    # Настройка путей к файлам
    base_path = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Data"
    cpath = base_path + r"\Calibration"
    ipath = r"C:\Пользователь Святослав\Физтех\1 Семестр\Общеинжа\Лаба струя\jet\Images"

    # Обработка одного файла
    data_files = [
        {
            'file': base_path + fr"\{i}_cm.txt",
            'label': f'Q ({i}0 мм)',
            'is_1txt': (i == 0)
        }
        for i in range(8)
    ]

    # Файлы калибровки
    calib_file = cpath + r"\distance_calibration.txt"
    pressure_file = cpath + r"\pressure_calibration.txt"

    # Строим график
    results = plot_velocity_profile(
        data_files=data_files,
        calib_file=calib_file,
        pressure_file=pressure_file,
        save_filename=ipath + r"\velocity_profile.png"
    )

    return results


if __name__ == "__main__":
    main()