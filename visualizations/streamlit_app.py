import streamlit as st
from pyspark.sql import SparkSession
from ecommerce_dashboard import process_data, generate_plots

# Initialize Spark session
spark = SparkSession.builder.appName("EcommerceDashboard").getOrCreate()

# Load CSV dataset
dataset_path = "./Pakistan_Largest_Ecommerce_Dataset.csv"
df = spark.read.option("header", "true").csv(dataset_path)

# Title and Overview
st.title("Ecommerce Orders Dashboard (2016 - 2018)")
st.write("### Dataset Overview")
st.write(f"Total records: {df.count()} rows")
st.write(f"Columns: {', '.join(df.columns)}")
st.dataframe(df.limit(10).toPandas())

# Analysis and Visualizations
process_data(spark, df)
generate_plots(st, df)
