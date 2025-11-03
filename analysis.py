import scipy.stats as stats
import pandas as pd

experiment = "flood"
data_directory = "./data"


def welch_ttest(x, y):
    """
    Taken from https://pythonfordatascienceorg.wordpress.com/welch-t-test-python-pandas/
    :param x: the first sample
    :param y: the second sample
    """
    ## Welch-Satterthwaite Degrees of Freedom ##
    dof = (x.var() / x.size + y.var() / y.size) ** 2 / (
                (x.var() / x.size) ** 2 / (x.size - 1) + (y.var() / y.size) ** 2 / (y.size - 1))

    t, p = stats.ttest_ind(x, y, equal_var=False, alternative='greater')

    print(f"Welch's t-test= {t:.4f}", "\n",
          f"p-value = {p}", "\n",
          f"Welch-Satterthwaite Degrees of Freedom= {dof:.4f}", "\n")

def main():
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
        welch_ttest(data1_on, data2_on)

        print(f"Comparing {pair[0]} and {pair[1]} POWER OFF Factor {pair[2]}")
        welch_ttest(data1_off, data2_off)


if __name__ == "__main__":
    main()
