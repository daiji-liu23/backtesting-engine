import matplotlib.pyplot as plt

from metrics import drawdown_series


def plot_equity_curve(equity_curve, output_path):
    dd = drawdown_series(equity_curve["equity"])

    fig, (ax_equity, ax_dd) = plt.subplots(
        2, 1, sharex=True, figsize=(10, 6), gridspec_kw={"height_ratios": [2, 1]}
    )

    ax_equity.plot(equity_curve.index, equity_curve["equity"], color="tab:blue")
    ax_equity.set_ylabel("Equity ($)")
    ax_equity.set_title("Equity Curve")

    ax_dd.fill_between(equity_curve.index, dd, 0, color="tab:red", alpha=0.4)
    ax_dd.set_ylabel("Drawdown")
    ax_dd.set_xlabel("Date")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
