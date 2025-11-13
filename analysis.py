import scipy.stats as stats
import pandas as pd

experiment_use = "flood"
data_directory = "./data"

def wilcoxon_test(x, y):
    t, p = stats.wilcoxon(x, y, alternative="greater")
    print(f"Wilcoxon test= {t:4f}", "\n",
          f"p-value = {p}", "\n")
    return 1

def analyze_algorithm(experiment):
    comparison_pairs = [
        ("VANILLA", "EIGENCRAFT", 4),
        ("VANILLA", "EIGENCRAFT", 6),
        ("VANILLA", "EIGENCRAFT", 8),
        ("VANILLA", "EIGENCRAFT", 10),
        ("VANILLA", "ALTERNATE_CURRENT", 20),
        ("EIGENCRAFT", "ALTERNATE_CURRENT", 1),
    ]

    for pair in comparison_pairs:
        df1 = pd.read_csv(f"{data_directory}/{experiment}/{pair[0]}/data.csv")
        df2 = pd.read_csv(f"{data_directory}/{experiment}/{pair[1]}/data.csv")

        data1_on = df1.PowerOnNanos
        data2_on = df2.PowerOnNanos * pair[2]
        data1_off = df1.PowerOffNanos
        data2_off = df2.PowerOffNanos * pair[2]

        print(f"Comparing {pair[0]} and {pair[1]} POWER ON Factor {pair[2]}")
        wilcoxon_test(data1_on, data2_on)

        print(f"Comparing {pair[0]} and {pair[1]} POWER OFF Factor {pair[2]}")
        wilcoxon_test(data1_off, data2_off)

def main():
    analyze_algorithm(experiment_use)


if __name__ == "__main__":
    main()
