import matplotlib.pyplot as plt
import numpy as np


def boussinesq_stress(x, z, P=1.0):
    """Рассчитывает вертикальное напряжение сигма_z по формуле Буссинеска.

    x - горизонтальное удаление от источника z - глубина (z > 0) P -
    сосредоточенная сила
    """
    # Защита от деления на ноль в точке приложения силы
    r = np.sqrt(x**2 + z**2)
    r = np.where(r == 0, 1e-5, r)

    # Классическая формула Буссинеска для 3D полупространства
    sigma_z = (3 * P * z**3) / (2 * np.pi * r**5)
    return sigma_z


# 1. Создаем сетку координат (x - по горизонтали, z - по вертикали/глубине)
x_coord = np.linspace(-3, 3, 400)
z_coord = np.linspace(0.01, 5, 400)  # Начинаем чуть ниже 0, чтобы избежать NaN
X, Z = np.meshgrid(x_coord, z_coord)

# 2. Считаем относительное давление (принимаем P = 1.0, тогда sigma_z и есть p/P0)
# Дополнительно нормируем для наглядности графика, как на исходной схеме
Z_stress = boussinesq_stress(X, Z, P=5.0)
# Ограничиваем максимальное значение сверху, чтобы график не «выгорал» в точке 0
Z_stress = np.clip(Z_stress, 0, 1.0)

# 3. Настройка графического окна
plt.figure(figsize=(9, 8))

# Уровни изолиний точно как на вашей схеме
levels = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00]

# Цветовая палитра: от синего через желтый к красному (спектральная)
cmap = plt.cm.get_cmap("jet").copy()

# Рисуем закрашенные зоны распределения давления
contour_filled = plt.contourf(
    X, Z, Z_stress, levels=levels, cmap=cmap, extend="max"
)

# Рисуем сами изолинии (пунктирные линии)
contour_lines = plt.contour(
    X, Z, Z_stress, levels=levels, colors="black", linewidths=0.8, linestyles="--"
)
plt.clabel(contour_lines, inline=True, fmt="%.3f", fontsize=9)

# 4. Оформление графика
plt.gca().invert_yaxis()  # Разворачиваем ось Y, чтобы глубина шла вниз
plt.title("Распределение давления в грунте от точечного источника", fontsize=12)
plt.xlabel("Удаление от оси источника (x)")
plt.ylabel("Глубина заложения (z)")

# Добавляем точку источника нагрузки
plt.plot(0, 0, marker="v", color="black", markersize=12)
plt.text(0, -0.15, "Источник (P₀)", ha="center", weight="bold")

# Боковая цветовая шкала (легенда)
cbar = plt.colorbar(contour_filled, ticks=levels)
cbar.set_label("Относительное давление p/P₀")

plt.grid(True, alpha=0.3, linestyle=":")
plt.tight_layout()

# Показываем результат
plt.show()
