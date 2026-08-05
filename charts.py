import matplotlib.pyplot as plt

def create_revenue_chart(output_path="revenue_chart.png"):
    # Demo values for now (we'll automate later)
    years = ["FY23", "FY24", "FY25"]
    revenue = [120, 145, 170]

    plt.figure(figsize=(5, 3))
    plt.plot(years, revenue, marker="o", linewidth=2)
    plt.title("Revenue Trend")
    plt.ylabel("Revenue (₹ Cr)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path