import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

def plot_pivot_table(df, value, index, func, ylabel, xlabel, output_dir, filename, option=None):
    pivot = pd.pivot_table(df, values=value, index=index, aggfunc=func)
    if option == 'sort':
        pivot = pivot.sort_values(by=value)
    elif option == 'unstack':
        pivot = pivot.unstack()

    plt.figure(figsize=[15, 5])
    pivot.plot()
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(f"{filename.replace('_', ' ').capitalize()}")
    file_path = f"{output_dir}/{filename}.png"
    plt.savefig(file_path)
    plt.close()
    print(f"Gráfico salvo: {file_path}")

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"Diretório criado: {path}")
    else:
        print(f"Diretório já existe: {path}")

def main(months):
    base_dir = '/home/adrianoarchlinux/Downloads/Support_Exercise_M14_1'
    output_base = '/home/adrianoarchlinux/Downloads/Support_Exercise_M14_1/output'

    for month in months:
        data_file = f'{base_dir}/SINASC_RO_2019_{month}.csv'
        output_dir = f'{output_base}/2019-{month}'
        ensure_directory(output_dir)

        try:
            sinasc = pd.read_csv(data_file)
            print(f"Processando dados para {month}...")

            plot_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'Quantidade de Nascimentos',
                             'Data de Nascimento', output_dir, 'quantidade_nascimentos')
            plot_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média de Peso por Sexo',
                             'Data de Nascimento', output_dir, 'media_peso_por_sexo', 'unstack')

        except FileNotFoundError as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        months = sys.argv[1:]  # Ignora o primeiro argumento que é o nome do script
        main(months)
    else:
        print("Por favor, forneça os meses como argumentos.")

