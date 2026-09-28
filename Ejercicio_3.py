import tkinter as tk
from tkinter import messagebox, ttk


# ==========================================
# CLASE USUARIO (LOGIN)
# ==========================================
class Usuario:

  def __init__(self):
    self._usuario = "programacion"
    self._password = "programacion"

  def validar(self, usuario_ingresado, password_ingresada):
    return (
        usuario_ingresado == self._usuario
        and password_ingresada == self._password
    )


# ==========================================
# CLASE AUTOLAVADO
# ==========================================
class AutoLavado:

  def __init__(self, placa, hora_ingreso, tarifa_hora):
    self._placa = placa
    self._hora_ingreso = float(hora_ingreso)
    self._tarifa_hora = float(tarifa_hora)
    self._hora_salida = None

  def registrar_ingreso(self, hora):
    self._hora_ingreso = float(hora)

  def registrar_salida(self, hora):
    self._hora_salida = float(hora)

  def calcular_pago(self, hora_salida):
    salida = float(hora_salida)
    if salida < self._hora_ingreso:
      raise ValueError("Exit time cannot be earlier than entry time.")
    self.registrar_salida(salida)
    horas_transcurridas = self._hora_salida - self._hora_ingreso
    return horas_transcurridas * self._tarifa_hora

  def obtener_placa(self):
    return self._placa


# ==========================================
# INTERFAZ GRÁFICA (TKINTER)
# ==========================================
class LoginWindow:

  def __init__(self, root):
    self.root = root
    self.root.title("Car Wash System - Login")
    self.root.geometry("350x250")
    self.root.config(bg="#f0f0f0")

    self.user_manager = Usuario()

    # Título
    tk.Label(
        root,
        text="System Login",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0",
        fg="#333",
    ).pack(pady=15)

    # Frame de formulario
    form_frame = tk.Frame(root, bg="#f0f0f0")
    form_frame.pack(pady=5)

    tk.Label(
        form_frame,
        text="Username:",
        font=("Arial", 10),
        bg="#f0f0f0",
        anchor="w",
    ).grid(row=0, column=0, sticky="w", pady=5)
    self.entry_user = tk.Entry(form_frame, font=("Arial", 10), width=20)
    self.entry_user.grid(row=0, column=1, pady=5)

    tk.Label(
        form_frame,
        text="Password:",
        font=("Arial", 10),
        bg="#f0f0f0",
        anchor="w",
    ).grid(row=1, column=0, sticky="w", pady=5)
    self.entry_pass = tk.Entry(
        form_frame, font=("Arial", 10), width=20, show="*"
    )
    self.entry_pass.grid(row=1, column=1, pady=5)

    # Botón Login
    tk.Button(
        root,
        text="Login",
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        width=15,
        command=self.handle_login,
    ).pack(pady=15)

  def handle_login(self):
    user = self.entry_user.get()
    password = self.entry_pass.get()

    if self.user_manager.validar(user, password):
      messagebox.showinfo("Success", "Login successful! Welcome.")
      self.root.destroy()
      main_root = tk.Tk()
      CarWashApp(main_root)
      main_root.mainloop()
    else:
      messagebox.showerror(
          "Access Denied", "Invalid username or password. Please try again."
      )


class CarWashApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Car Wash Management System")
    self.root.geometry("600x450")

    self.car_list = []  # Lista interna para registrar los autos

    # Título Principal
    tk.Label(
        root, text="Car Wash Control Panel", font=("Arial", 14, "bold")
    ).pack(pady=10)

    # Frame de Registro de Ingreso
    reg_frame = tk.LabelFrame(
        root, text=" Register Car Entry ", font=("Arial", 10, "bold")
    )
    reg_frame.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

    tk.Label(reg_frame, text="License Plate:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_plate = tk.Entry(reg_frame, width=15)
    self.entry_plate.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(reg_frame, text="Entry Time (hr e.g. 8.5):").grid(
        row=0, column=2, sticky="w", padx=5, pady=5
    )
    self.entry_time_in = tk.Entry(reg_frame, width=10)
    self.entry_time_in.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(reg_frame, text="Hourly Rate ($):").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_rate = tk.Entry(reg_frame, width=15)
    self.entry_rate.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(
        reg_frame,
        text="Register Entry",
        bg="#2196F3",
        fg="white",
        command=self.register_car,
    ).grid(row=1, column=3, padx=5, pady=5, sticky="e")

    # Tabla / Listado de Autos Activos
    list_frame = tk.LabelFrame(
        root, text=" Active Cars in Wash ", font=("Arial", 10, "bold")
    )
    list_frame.pack(fill="both", expand=True, padx=15, pady=10)

    self.tree = ttk.Treeview(
        list_frame, columns=("Plate", "Entry Time", "Rate"), show="headings"
    )
    self.tree.heading("Plate", text="License Plate")
    self.tree.heading("Entry Time", text="Entry Time")
    self.tree.heading("Rate", text="Hourly Rate ($)")
    self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Frame de Salida y Cobro
    exit_frame = tk.Frame(root)
    exit_frame.pack(fill="x", padx=15, pady=10)

    tk.Label(exit_frame, text="Exit Time (hr e.g. 10.5):").pack(
        side="left", padx=5
    )
    self.entry_time_out = tk.Entry(exit_frame, width=10)
    self.entry_time_out.pack(side="left", padx=5)

    tk.Button(
        exit_frame,
        text="Register Exit & Calculate Payment",
        bg="#FF9800",
        fg="white",
        command=self.process_exit,
    ).pack(side="right", padx=5)

  def register_car(self):
    plate = self.entry_plate.get().strip()
    time_in = self.entry_time_in.get().strip()
    rate = self.entry_rate.get().strip()

    if not plate or not time_in or not rate:
      messagebox.showerror("Error", "All fields must be filled out.")
      return

    try:
      # Validar creación y datos numéricos usando la clase AutoLavado
      new_car = AutoLavado(plate, time_in, rate)
      self.car_list.append(new_car)

      # Actualizar tabla visual
      self.tree.insert("", "end", values=(plate, time_in, rate))

      # Limpiar campos
      self.entry_plate.delete(0, tk.END)
      self.entry_time_in.delete(0, tk.END)
      self.entry_rate.delete(0, tk.END)

      messagebox.showinfo("Success", f"Car with plate {plate} registered.")
    except ValueError:
      messagebox.showerror(
          "Error", "Entry time and hourly rate must be valid numbers."
      )

  def process_exit(self):
    selected_item = self.tree.selection()
    if not selected_item:
      messagebox.showwarning(
          "Warning", "Please select a car from the list to process exit."
      )
      return

    time_out = self.entry_time_out.get().strip()
    if not time_out:
      messagebox.showerror("Error", "Please enter the exit time.")
      return

    try:
      item_index = self.tree.index(selected_item[0])
      car_obj = self.car_list[item_index]

      # Calcular pago usando el método de la clase
      total_payment = car_obj.calcular_pago(time_out)

      messagebox.showinfo(
          "Payment Details",
          f"Car Plate: {car_obj.obtener_placa()}\nTotal Time Cost: ${total_payment:.2f}",
      )

      # Remover de la lista interna y de la vista
      self.car_list.pop(item_index)
      self.tree.delete(selected_item[0])
      self.entry_time_out.delete(0, tk.END)

    except ValueError as e:
      messagebox.showerror("Error", str(e))


if __name__ == "__main__":
  root = tk.Tk()
  app = LoginWindow(root)
  root.mainloop()
