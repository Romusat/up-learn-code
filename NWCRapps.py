import tkinter as tk
from tkinter import messagebox

class TransportationSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Problem Solver")

        # Labels and Inputs for Supply and Demand
        tk.Label(root, text="Nama Pengirim dan Jumlah Muatan:").grid(row=0, column=0, columnspan=3)
        self.supply_names = []
        self.supply_entries = []
        for i in range(3):
            name_entry = tk.Entry(root, width=10)
            name_entry.grid(row=i + 1, column=0)
            self.supply_names.append(name_entry)

            tk.Label(root, text=f"Jumlah Muatan {i + 1}").grid(row=i + 1, column=1)
            entry = tk.Entry(root)
            entry.grid(row=i + 1, column=2)
            self.supply_entries.append(entry)

        tk.Label(root, text="Nama Penerima dan Muatan yang Dibutuhkan:").grid(row=0, column=3, columnspan=3)
        self.demand_names = []
        self.demand_entries = []
        for i in range(3):
            name_entry = tk.Entry(root, width=10)
            name_entry.grid(row=i + 1, column=3)
            self.demand_names.append(name_entry)

            tk.Label(root, text=f"Jumlah Muatan {i + 1}").grid(row=i + 1, column=4)
            entry = tk.Entry(root)
            entry.grid(row=i + 1, column=5)
            self.demand_entries.append(entry)

        # Cost Matrix
        tk.Label(root, text="Cost Matrix (dalam Rupiah):").grid(row=5, column=0, columnspan=6)
        self.cost_matrix_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = tk.Entry(root, width=5)
                entry.grid(row=i + 6, column=j)
                row_entries.append(entry)
            self.cost_matrix_entries.append(row_entries)

        # Buttons to Solve
        self.nwcr_button = tk.Button(root, text="Solve with NWCR", command=self.solve_nwcr)
        self.nwcr_button.grid(row=10, column=0, columnspan=2)

        self.least_cost_button = tk.Button(root, text="Solve with Least Cost", command=self.solve_least_cost)
        self.least_cost_button.grid(row=10, column=2, columnspan=2)

        self.vam_button = tk.Button(root, text="Solve with VAM", command=self.solve_vam)
        self.vam_button.grid(row=10, column=4, columnspan=2)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.grid(row=11, column=0, columnspan=6)

        # Output Section
        self.output_text = tk.Text(root, height=25, width=70)
        self.output_text.grid(row=12, column=0, columnspan=6)

    def solve_nwcr(self):
        self.solve_method(self.north_west_corner, "NWCR")

    def solve_least_cost(self):
        self.solve_method(self.least_cost_method, "Least Cost")

    def solve_vam(self):
        self.solve_method(self.vogel_approximation_method, "VAM")

    def solve_method(self, method, method_name):
        try:
            supplies = [int(entry.get()) for entry in self.supply_entries]
            demands = [int(entry.get()) for entry in self.demand_entries]
            supply_names = [entry.get() for entry in self.supply_names]
            demand_names = [entry.get() for entry in self.demand_names]
            cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_matrix_entries]
        except ValueError:
            messagebox.showerror("Input Error", "Pastikan semua input adalah angka valid!")
            return

        if sum(supplies) != sum(demands):
            messagebox.showerror("Balance Error", "Total supply harus sama dengan total demand!")
            return

        allocation, total_cost, details = method(supplies[:], demands[:], cost_matrix, supply_names, demand_names)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Hasil {method_name}:\n")
        self.output_text.insert(tk.END, "Allocation Matrix:\n")
        for row in allocation:
            self.output_text.insert(tk.END, "\t".join(map(str, row)) + "\n")
        self.output_text.insert(tk.END, details + "\n")
        self.output_text.insert(tk.END, f"Total Cost: Rp {total_cost:,}\n")

    def reset(self):
        for entry in self.supply_entries + self.demand_entries + self.supply_names + self.demand_names:
            entry.delete(0, tk.END)
        for row in self.cost_matrix_entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)

    def north_west_corner(self, supplies, demands, cost_matrix, supply_names, demand_names):
        allocation = [[0] * len(demands) for _ in range(len(supplies))]
        i, j = 0, 0
        total_cost = 0
        details = ""
        while i < len(supplies) and j < len(demands):
            alloc = min(supplies[i], demands[j])
            allocation[i][j] = alloc
            cost = alloc * cost_matrix[i][j]
            total_cost += cost
            details += f"{supply_names[i]} -> {demand_names[j]}: Quantity = {alloc}, Cost = Rp {cost:,}\n"
            supplies[i] -= alloc
            demands[j] -= alloc
            if supplies[i] == 0:
                i += 1
            elif demands[j] == 0:
                j += 1
        return allocation, total_cost, details

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportationSolverApp(root)
    root.mainloop()