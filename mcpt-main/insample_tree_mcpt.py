import pandas as pd
import numpy as np
import matplotlib
import  matplotlib.pyplot as plt
matplotlib.use("TkAgg")  # Use Tkinter-based backend for GUI (recommended for local use)

from tqdm import tqdm

from tree_strat import train_tree, tree_strategy
from bar_permute import get_permutation

df = pd.read_parquet('/home/gopika/Documents/mcpt-main/trading_data.pq')
df.index = df.index.astype('datetime64[s]')
print("df index,",df.index)

df['r'] = np.log(df['close']).diff().shift(-1)

train_df = df[(df.index.year >= 2016) & (df.index.year < 2020)]

real_tree = train_tree(train_df)
real_is_signal, real_is_pf = tree_strategy(train_df, real_tree)
print("real :::::::::::::::",real_is_signal,"real pf::::::::::::::::::",real_is_pf)
n_permutations = 100
perm_better_count = 1
permuted_pfs = []
print("In-Sample MCPT")
for perm_i in tqdm(range(1, n_permutations)):
    train_perm = get_permutation(train_df)

    perm_nn = train_tree(train_perm)
    _, perm_pf = tree_strategy(train_perm, perm_nn)
    if perm_pf >= real_is_pf:
        perm_better_count += 1

    permuted_pfs.append(perm_pf)

insample_mcpt_pval = perm_better_count / n_permutations
print(f"In-sample MCPT P-Value: {insample_mcpt_pval}")

plt.style.use('dark_background')
pd.Series(permuted_pfs).hist(color='blue', label='Permutations')
plt.axvline(real_is_pf, color='red', label='Real')
plt.xlabel("Profit Factor")
plt.title(f"In-sample MCPT. P-Value: {insample_mcpt_pval}")
plt.grid(False)
plt.legend()
plt.show()


