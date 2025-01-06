from pyspark.sql.functions import col, count, year, month

def process_data(spark, df):
    """Processes and prepares data for visualization."""
    df.createOrReplaceTempView("ecommerce_data")
    print("Data processing completed.")

def generate_plots(st, df):
    """Generates visualizations for the dashboard."""
    # Best-Selling Categories
    st.write("### Best-Selling Categories")
    if "category_name_1" in df.columns:
        top_categories = df.groupBy("category_name_1").agg(count("*").alias("total_orders")).orderBy(col("total_orders").desc()).limit(10)
        st.bar_chart(top_categories.toPandas().set_index("category_name_1")["total_orders"])
    else:
        st.error("Column 'category_name_1' not found in the dataset.")

    # Payment Methods and Order Status
    st.write("### Payment Method vs Order Status")
    if "payment_method" in df.columns and "status" in df.columns:
        payment_status = df.groupBy("payment_method", "status").agg(count("*").alias("total_orders")).orderBy(col("total_orders").desc()).limit(10)
        st.dataframe(payment_status.toPandas())
    else:
        st.error("Columns 'payment_method' or 'status' not found in the dataset.")

    # Monthly Order Volume
    st.write("### Monthly Order Volume by Category")
    if "created_at" in df.columns and "category_name_1" in df.columns:
        monthly_orders = df.withColumn("year", year(col("created_at"))).withColumn("month", month(col("created_at"))).groupBy("year", "month", "category_name_1").agg(count("*").alias("total_orders"))
        st.line_chart(monthly_orders.toPandas().pivot(index=["year", "month"], columns="category_name_1", values="total_orders"))
    else:
        st.error("Columns 'created_at' or 'category_name_1' not found in the dataset.")
