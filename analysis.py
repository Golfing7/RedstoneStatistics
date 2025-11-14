import numpy as np
import scipy.stats as stats
import scikit_posthocs as sp
import pandas as pd

experiment_use = "flood"
data_directory = "./data"

def wilcoxon_test(x, y):
    t, p = stats.wilcoxon(x, y, alternative="greater")
    print(f"Wilcoxon test= {t:4f}", "\n",
          f"p-value = {p}", "\n")
    return 1

def analyze_algorithm_wilcoxon(experiments):
    comparison_pairs = [
        ("VANILLA", "EIGENCRAFT", 4),
        ("VANILLA", "EIGENCRAFT", 6),
        ("VANILLA", "EIGENCRAFT", 8),
        ("VANILLA", "EIGENCRAFT", 10),
        ("VANILLA", "ALTERNATE_CURRENT", 20),
        ("EIGENCRAFT", "ALTERNATE_CURRENT", 1),
    ]

    for pair in comparison_pairs:
        data1_on = []
        data2_on = []
        data1_off = []
        data2_off = []
        for experiment in experiments:
            df1 = pd.read_csv(f"{data_directory}/{experiment}/{pair[0]}/data.csv")
            df2 = pd.read_csv(f"{data_directory}/{experiment}/{pair[1]}/data.csv")
            data1_on.extend(df1.PowerOnNanos.values)
            data2_on.extend(df2.PowerOnNanos.values * pair[2])
            data1_off.extend(df1.PowerOffNanos.values)
            data2_off.extend(df2.PowerOffNanos.values * pair[2])

        print(f"Comparing {pair[0]} and {pair[1]} POWER ON Factor {pair[2]}")
        wilcoxon_test(data1_on, data2_on)

        print(f"Comparing {pair[0]} and {pair[1]} POWER OFF Factor {pair[2]}")
        wilcoxon_test(data1_off, data2_off)

def analyze_algorithm_friedman(experiments):
    algorithms = [
        ("VANILLA", 1),
        ("EIGENCRAFT", 4),
        ("EIGENCRAFT", 6),
        ("EIGENCRAFT", 8),
        ("EIGENCRAFT", 10),
        ("ALTERNATE_CURRENT", 20),
    ]

    inputs = list(range(len(experiments)))
    time_dict = {}
    for algorithm, factor in algorithms:
        for experiment in experiments:
            df1 = pd.read_csv(f"{data_directory}/{experiment}/{algorithm}/data.csv")
            time_dict.setdefault(f"{algorithm}_{factor}x", []).append((df1.PowerOnNanos * factor).mean())

    df = pd.DataFrame({
        'input': np.repeat(inputs, len(algorithms)),
        'algorithm': np.tile([f"{pair[0]}_{pair[1]}x" for pair in algorithms], len(experiments)),
        'time': np.concatenate([time_dict[f"{pair[0]}_{pair[1]}x"] for pair in algorithms])
    })

    groups = [group['time'].values for name, group in df.groupby('algorithm')]
    stat, p = stats.friedmanchisquare(*groups)
    p_values = sp.posthoc_nemenyi_friedman(
        df,
        melted=True,
        block_col='input',
        block_id_col='input',
        group_col='algorithm',
        y_col='time'
    )
    print(p_values.round(4).to_string())


def main():
    analyze_algorithm_friedman([f"{experiment_use}_{i}" for i in range(1, 15)])
    # analyze_algorithm_wilcoxon([f"{experiment_use}_{i}" for i in range(1, 15)])


if __name__ == "__main__":
    main()
