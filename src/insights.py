from src.analysis import RATE

def generate_insights(df):
    peak = df[RATE].max()

    covid = (
        df[df["Year"] == 2020][RATE]
        .mean()
    )

    overall = df[RATE].mean()

    return [
        f"Peak unemployment reached {peak:.2f}%",
        f"Covid year average unemployment was {covid:.2f}%",
        f"Overall average unemployment is {overall:.2f}%",
        "2020 shows clear Covid impact.",
        "Rural and urban areas show different employment patterns.",
        "Policy support should target high-unemployment states.",
    ]