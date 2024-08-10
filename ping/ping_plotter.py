import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def read_ping_data():
    with open("data.txt", 'r') as file:
        lines = file.readlines()
        ping_results = [float(line.strip().replace(',', '.')) for line in lines]
    return ping_results

def plot_ping_distribution(ping_results):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    # Escala lineal
    axs[0].hist(ping_results, bins=20, color='skyblue', edgecolor='black')
    axs[0].set_title('Distribución de tiempos de ping (Escala lineal)')
    axs[0].set_xlabel('Tiempo de ping (ms)')
    axs[0].set_ylabel('Frecuencia')
    
    # Escala log-log
    axs[1].hist(ping_results, bins=20, color='lightgreen', edgecolor='black', log=True)
    axs[1].set_title('Distribución de tiempos de ping (Escala log-log)')
    axs[1].set_xlabel('Tiempo de ping (ms)')
    axs[1].set_ylabel('Frecuencia')
    
    plt.tight_layout()
    plt.show()


def generate_pdf_report(ping_results, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    data = [['Tiempo de ping (ms)', 'Frecuencia']]
    hist, bin_edges = np.histogram(ping_results, bins=20)
    for i in range(len(hist)):
        data.append([f'{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}', hist[i]])
    
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)
    
    doc.build(elements)

if __name__ == "__main__":

    ping_results = read_ping_data()
    
    plot_ping_distribution(ping_results)
    
    generate_pdf_report(ping_results, "ping_report.pdf")