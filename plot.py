#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Ler a matriz da entrada padrão
input_data = sys.stdin.read().strip()

# Converter a entrada para uma matriz NumPy
matrix = np.array([list(map(float, line.split())) for line in input_data.split("\n")])

# Criar o mapa de calor
plt.figure()
sns.heatmap(matrix, annot=False, cmap="coolwarm", linewidths=0, cbar=False)
plt.axis('off')

# Salvar a imagem
plt.savefig("heatmap.png", bbox_inches='tight')
plt.show()