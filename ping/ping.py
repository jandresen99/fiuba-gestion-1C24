import subprocess
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import csv

def run_ping():
    ping_command = f"ping -c 7200 -i 1 google.com.ar"
    ping_process = subprocess.Popen(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    ping_output = []
    counter = 1
    for line in ping_process.stdout:
        print(counter)
        counter += 1
        if line.startswith('64 bytes'):
            time_match = re.search(r"time=([0-9.]+) ms", line)
            if time_match:
                ping_output.append(float(time_match.group(1)))
    
    ping_process.wait()  # Esperar a que termine el proceso de ping
    return ping_output

def plot_distribution(data, scale):
    plt.hist(data, bins=30, density=True)
    plt.yscale(scale)
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Densidad')
    plt.title(f'Distribución de tiempos de ping ({scale} scale)')
    plt.show()

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tiempo (ms)'])
        for value in data:
            writer.writerow([value])

if __name__ == "__main__":
    print("Haciendo ping al host durante 1 minuto...")
    ping_data = run_ping()
    print("Ping completado.")

    save_to_csv(ping_data, 'ping_data.csv')