import matplotlib.pyplot as plt

def plot_revenue_trend(monthly_kpi):
    plt.figure()
    plt.plot(monthly_kpi["Year_Month"].astype(str), monthly_kpi["Revenue"])
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("revenue_trend.png")
    plt.close()

def plot_revenue_growth(monthly_kpi):
    plt.figure()
    plt.bar(monthly_kpi["Year_Month"].astype(str), monthly_kpi["Revenue_Growth_%"])
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Growth %")
    plt.xlabel("Month")
    plt.ylabel("Growth %")
    plt.tight_layout()
    plt.savefig("revenue_growth.png")
    plt.close()

def plot_top_products(product_kpi):
    top10 = product_kpi.head(10)
    plt.figure()
    plt.barh(top10["Product"], top10["Revenue"])
    plt.gca().invert_yaxis()
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    plt.tight_layout()
    plt.savefig("top_products.png")
    plt.close()

