import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from functions import rockfall_physics_stable, plot_with_speed_and_energy

class RockfallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rockfall Simulation")
        self.root.geometry("350x400")

        # 左侧控制区
        control_frame = ttk.Frame(root, width=300)
        control_frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(
            control_frame,
            text="Rockfall Simulation Parameters",
            font=('Arial', 12, 'bold')
        ).pack(pady=5)

        # 参数变量
        self.cellsize = tk.DoubleVar(value=30.0)
        self.dt = tk.DoubleVar(value=0.1)
        self.friction = tk.DoubleVar(value=0.15)
        self.max_steps = tk.IntVar(value=5000)
        self.start_row = tk.IntVar(value=357)
        self.start_col = tk.IntVar(value=100)
        self.g = tk.DoubleVar(value=9.81)

        # 创建输入框
        self.entries = {}
        self._add_param(control_frame, "Cellsize (m):", self.cellsize)
        self._add_param(control_frame, "Time Step (s):", self.dt)
        self._add_param(control_frame, "Friction:", self.friction)
        self._add_param(control_frame, "Max Steps:", self.max_steps)
        self._add_param(control_frame, "Start Row:", self.start_row)
        self._add_param(control_frame, "Start Col:", self.start_col)
        self._add_param(control_frame, "Gravity:", self.g)

        # 操作按钮
        ttk.Button(control_frame, text="Load DEM", command=self.load_dem).pack(pady=10, fill='x')
        ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation).pack(pady=5, fill='x')

        self.dem = None

    def _add_param(self, parent, label, variable):
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=3)
        ttk.Label(frame, text=label, width=15).pack(side='left')
        entry = ttk.Entry(frame, textvariable=variable)
        entry.pack(side='right', fill='x', expand=True)
        self.entries[label] = entry  # 存起来备用

    def load_dem(self):
        filepath = filedialog.askopenfilename(
            title="Select DEM File",
            filetypes=[("ASCII DEM (*.asc)", "*.asc"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        try:
            self.dem = np.loadtxt(filepath, skiprows=6)
            messagebox.showinfo("Success", f"DEM loaded: shape = {self.dem.shape}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load DEM:\n{e}")

    def run_simulation(self):
        if self.dem is None:
            messagebox.showwarning("No DEM", "Please load a DEM file first.")
            return

        try:
            cellsize = self.cellsize.get()
            dt = self.dt.get()
            friction = self.friction.get()
            max_steps = self.max_steps.get()
            start_row = self.start_row.get()
            start_col = self.start_col.get()
            g = self.g.get()
        except tk.TclError:
            messagebox.showerror("Invalid Input", "Please check your parameter values.")
            return

        start = (start_row, start_col)

        try:
            path_idx, speed, energy = rockfall_physics_stable(
                self.dem, start,
                cellsize=cellsize, g=g, dt=dt,
                friction=friction, max_steps=max_steps
            )
            plot_with_speed_and_energy(self.dem, path_idx, speed, energy, start)
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RockfallGUI(root)
    root.mainloop()