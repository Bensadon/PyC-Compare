import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('results', exist_ok=True)

# Dados C (100k inteiros)
c_data = {
    'hash_insercao': 0.241, 'hash_busca': 0.219, 'hash_remocao': 0.032,
    'insertion_sort': 0.930, 'merge_sort': 0.028, 'quick_sort': 0.008
}
c_mem = 802816

# Dados Python (100k inteiros)
py_data = {
    'dict_insercao': 0.038758, 'dict_busca': 0.044040, 'dict_remocao': 0.052866,
    'sorted': 0.019936
}
py_mem = 10303980

# --- Gráfico 1: Hash Table C vs Python Dict ---
fig, ax = plt.subplots(figsize=(12, 6))
ops = ['Inserção', 'Busca', 'Remoção']
c_vals = [c_data['hash_insercao'], c_data['hash_busca'], c_data['hash_remocao']]
py_vals = [py_data['dict_insercao'], py_data['dict_busca'], py_data['dict_remocao']]

x = range(len(ops))
width = 0.35
bars_c = ax.bar([i - width/2 for i in x], c_vals, width, label='C (hash table)', color='#2196F3', edgecolor='white')
bars_py = ax.bar([i + width/2 for i in x], py_vals, width, label='Python (dict)', color='#FF9800', edgecolor='white')

ax.set_ylabel('Tempo (segundos)', fontsize=12)
ax.set_title('Hash Table: C vs Python — 100.000 inteiros', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ops, fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

for bar in bars_c:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
            f'{bar.get_height():.3f}s', ha='center', va='bottom', fontsize=9)
for bar in bars_py:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
            f'{bar.get_height():.3f}s', ha='center', va='bottom', fontsize=9)

fig.tight_layout()
fig.savefig('results/hash_c_vs_python_100k.png', dpi=150)
plt.close()
print('Salvo: results/hash_c_vs_python_100k.png')

# --- Gráfico 2: Ordenação ---
fig, ax = plt.subplots(figsize=(10, 6))
sort_ops = ['Insertion Sort\n(C)', 'Merge Sort\n(C)', 'Quick Sort\n(C)', 'sorted()\n(Python)']
sort_vals = [c_data['insertion_sort'], c_data['merge_sort'], c_data['quick_sort'], py_data['sorted']]
colors = ['#F44336', '#4CAF50', '#2196F3', '#FF9800']

bars = ax.bar(sort_ops, sort_vals, color=colors, edgecolor='white')

ax.set_ylabel('Tempo (segundos)', fontsize=12)
ax.set_title('Ordenação: C vs Python sorted() — 100.000 inteiros', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
            f'{bar.get_height():.3f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')

fig.tight_layout()
fig.savefig('results/ordenacao_c_vs_python_100k.png', dpi=150)
plt.close()
print('Salvo: results/ordenacao_c_vs_python_100k.png')

# --- Gráfico 3: Memória ---
fig, ax = plt.subplots(figsize=(8, 5))
mem_labels = ['C (hash table)', 'Python (dict)']
mem_vals = [c_mem / 1024, py_mem / 1024]
colors = ['#2196F3', '#FF9800']

bars = ax.bar(mem_labels, mem_vals, color=colors, edgecolor='white', width=0.5)

ax.set_ylabel('Memória (KB)', fontsize=12)
ax.set_title('Pico de memória na inserção — 100.000 inteiros', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 100,
            f'{bar.get_height():.0f} KB', ha='center', va='bottom', fontsize=11, fontweight='bold')

fig.tight_layout()
fig.savefig('results/memoria_100k.png', dpi=150)
plt.close()
print('Salvo: results/memoria_100k.png')
