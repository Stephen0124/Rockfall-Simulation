import numpy as np
import matplotlib.pyplot as plt

# ======================
# 双线性插值采样函数
# ======================
def bilinear_sample(arr, yf, xf):
    """在浮点索引 (yf=row, xf=col) 上采样 2D 数组 arr 的双线性插值值。"""
    rows, cols = arr.shape
    if yf < 0 or xf < 0 or yf > rows - 1 or xf > cols - 1:
        return np.nan
    i0 = int(np.floor(yf)); j0 = int(np.floor(xf))
    i1 = min(i0 + 1, rows - 1); j1 = min(j0 + 1, cols - 1)
    dy = yf - i0; dx = xf - j0
    v00 = arr[i0, j0]; v10 = arr[i1, j0]; v01 = arr[i0, j1]; v11 = arr[i1, j1]
    return (v00 * (1 - dy) * (1 - dx) +
            v10 * dy * (1 - dx) +
            v01 * (1 - dy) * dx +
            v11 * dy * dx)


# ======================
# 稳定版落石物理模拟
# ======================
def rockfall_physics_stable(dem, start_idx, cellsize=1.0,
                            g=9.81, dt=0.1, friction=0.3,
                            max_steps=20000, speed_tol=1e-2, slope_tol=1e-3):
    """
    稳定版落石运动模拟，包含半隐式积分与低坡度停止判断。
    返回路径 (row, col)、速度数组、动能数组。
    """
    rows, cols = dem.shape
    grad_y_full, grad_x_full = np.gradient(dem, cellsize, cellsize)

    start_row, start_col = start_idx
    pos_y = start_row * cellsize
    pos_x = start_col * cellsize
    vx, vy = 0.0, 0.0

    path_indices = [(start_row, start_col)]
    path_speed = [0.0]
    path_energy = [0.0]  # 动能 (0.5 * v^2)，假设单位质量=1

    for step in range(max_steps):
        frac_row = pos_y / cellsize
        frac_col = pos_x / cellsize

        if frac_row < 1 or frac_row > rows - 2 or frac_col < 1 or frac_col > cols - 2:
            break

        dg_dx = bilinear_sample(grad_x_full, frac_row, frac_col)
        dg_dy = bilinear_sample(grad_y_full, frac_row, frac_col)
        if np.isnan(dg_dx) or np.isnan(dg_dy):
            break

        grad_norm = np.hypot(dg_dx, dg_dy)
        denom = np.sqrt(1.0 + grad_norm**2)

        # 半隐式积分
        a_x = -g * dg_dx / denom - friction * vx
        a_y = -g * dg_dy / denom - friction * vy

        vx += a_x * dt
        vy += a_y * dt
        pos_x += vx * dt
        pos_y += vy * dt

        speed = np.hypot(vx, vy)
        kinetic_E = 0.5 * speed**2

        path_indices.append((pos_y / cellsize, pos_x / cellsize))
        path_speed.append(speed)
        path_energy.append(kinetic_E)

        if speed < speed_tol or grad_norm < slope_tol:
            break

    return np.array(path_indices), np.array(path_speed), np.array(path_energy)


# ======================
# 绘图函数（在独立弹窗中显示）
# ======================
def plot_with_speed_and_energy(dem, path_idx, speed, energy, start_idx, cmap='terrain'):
    plt.figure(figsize=(14, 6))
    gs = plt.GridSpec(1, 2, width_ratios=[2, 1])

    # ---- 左图：DEM + 路径 ----
    ax1 = plt.subplot(gs[0])
    im = ax1.imshow(dem, cmap=cmap, origin='upper')
    plt.colorbar(im, ax=ax1, label='Elevation (m)')

    if len(path_idx) > 1:
        for k in range(len(path_idx)-1):
            y0, x0 = path_idx[k]
            y1, x1 = path_idx[k+1]
            s = speed[k]
            ax1.plot([x0, x1], [y0, y1], color=plt.cm.autumn_r(min(1.0, s/10.0)), linewidth=2)

    ax1.scatter([start_idx[1]], [start_idx[0]], c='k', s=60, label='Start', zorder=3)
    ax1.set_title('Rockfall Path (color ≈ speed)')
    ax1.legend()
    ax1.invert_yaxis()

    # ---- 右图：动能曲线 ----
    ax2 = plt.subplot(gs[1])
    ax2.plot(energy, color='orange', linewidth=2)
    ax2.set_title("Kinetic Energy vs Step")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Energy (J/kg)")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()  # 原生 Matplotlib 弹窗（含放大/缩放/回退功能）
