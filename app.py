import tkinter as tk
from tkinter import ttk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi değişkenleri
mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
timeofday = ctrl.Antecedent(np.arange(0, 3, 1), 'timeofday')  # 0: Sabah, 1: Öğlen, 2: Akşam
activity = ctrl.Antecedent(np.arange(0, 3, 1), 'activity')    # 0: Ev, 1: Arkadaş, 2: Davet

# Çıktı değişkenleri
perfume_type = ctrl.Consequent(np.arange(0, 4, 1), 'perfume_type')  # 4 tür
intensity = ctrl.Consequent(np.arange(0, 3, 1), 'intensity')        # 3 yoğunluk seviyesi

# Üyelik fonksiyonları
mood.automf(3)
temperature.automf(3)
humidity.automf(3)
timeofday.automf(3)
activity.automf(3)

perfume_type['ciceksi'] = fuzz.trimf(perfume_type.universe, [0, 0, 1])
perfume_type['meyvemsi'] = fuzz.trimf(perfume_type.universe, [0, 1, 2])
perfume_type['odunsu'] = fuzz.trimf(perfume_type.universe, [1, 2, 3])
perfume_type['oryantal'] = fuzz.trimf(perfume_type.universe, [2, 3, 3])

intensity.automf(3)  # poor, average, good

# Kurallar
rules = [
    ctrl.Rule(mood['poor'] & temperature['poor'], perfume_type['ciceksi']),
    ctrl.Rule(mood['average'] & activity['average'], perfume_type['meyvemsi']),
    ctrl.Rule(mood['good'] & timeofday['good'], perfume_type['oryantal']),
    ctrl.Rule(mood['good'] & temperature['good'], perfume_type['odunsu']),
    
    ctrl.Rule(humidity['good'] & activity['good'], intensity['good']),
    ctrl.Rule(humidity['poor'] & temperature['good'], intensity['average']),
    ctrl.Rule(activity['poor'] | timeofday['poor'], intensity['poor']),
]

# Kontrol sistemi
perfume_ctrl = ctrl.ControlSystem(rules)
perfume_sim = ctrl.ControlSystemSimulation(perfume_ctrl)

# Arayüz fonksiyonu
def run_fuzzy():
    try:
        perfume_sim.input['mood'] = int(mood_slider.get())
        perfume_sim.input['temperature'] = int(temp_slider.get())
        perfume_sim.input['humidity'] = int(hum_slider.get())
        perfume_sim.input['timeofday'] = int(time_dropdown.get()[0])
        perfume_sim.input['activity'] = int(act_dropdown.get()[0])
        perfume_sim.compute()

        perfume_val = perfume_sim.output['perfume_type']
        intensity_val = perfume_sim.output['intensity']

        perfume_names = ['Çiçeksi', 'Meyvemsi', 'Odunsu', 'Oryantal']
        perfume_index = int(round(perfume_val))
        perfume_index = min(max(perfume_index, 0), 3)

        intensity_names = ['Hafif', 'Orta', 'Yoğun']
        intensity_index = int(round(intensity_val))
        intensity_index = min(max(intensity_index, 0), 2)

        result = f"Parfüm Türü: {perfume_names[perfume_index]}\nYoğunluk: {intensity_names[intensity_index]}"
        result_label.config(text=result)
    except Exception as e:
        result_label.config(text=f"Hata oluştu: {e}")

# Tkinter arayüzü
app = tk.Tk()
app.title("Fuzzy Parfüm Önerici")
app.geometry("400x450")
app.configure(bg="#fbeffb")

tk.Label(app, text="Ruh Hali (0-10)", bg="#fbeffb").pack()
mood_slider = tk.Scale(app, from_=0, to=10, orient="horizontal", bg="#fbeffb")
mood_slider.pack()

tk.Label(app, text="Sıcaklık (°C)", bg="#fbeffb").pack()
temp_slider = tk.Scale(app, from_=0, to=40, orient="horizontal", bg="#fbeffb")
temp_slider.pack()

tk.Label(app, text="Nem (%)", bg="#fbeffb").pack()
hum_slider = tk.Scale(app, from_=0, to=100, orient="horizontal", bg="#fbeffb")
hum_slider.pack()

tk.Label(app, text="Günün Saati", bg="#fbeffb").pack()
time_dropdown = ttk.Combobox(app, values=["0: Sabah", "1: Öğlen", "2: Akşam"])
time_dropdown.current(0)
time_dropdown.pack()

tk.Label(app, text="Aktivite", bg="#fbeffb").pack()
act_dropdown = ttk.Combobox(app, values=["0: Ev", "1: Arkadaş", "2: Davet"])
act_dropdown.current(0)
act_dropdown.pack()

tk.Button(app, text="Öner", command=run_fuzzy, bg="#d8a1c4", fg="white").pack(pady=15)
result_label = tk.Label(app, text="", bg="#fbeffb", font=("Arial", 12))
result_label.pack()

app.mainloop()

