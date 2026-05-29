import pandas as pd

def load_outbreak_data():

    # you can replace with WHO / Kaggle dataset later
    data = {
        "disease": ["Flu", "Dengue", "COVID", "Food Poisoning"],
        "risk_level": [1.3, 1.5, 1.6, 1.2],
        "season": ["rainy", "rainy", "all", "hot"]
    }

    return pd.DataFrame(data)


def outbreak_factor(medicine):

    df = load_outbreak_data()

    if "flu" in medicine:
        return 1.3
    if "antibiotic" in medicine:
        return 1.2

    return 1.0