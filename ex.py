import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/jldbc/coffee-quality-database/master/data/arabica_data_cleaned.csv"

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

df = load_data()

# Title
st.title("☕ Coffee Quality Dataset Explorer")

# Display Dataset
st.subheader("📋 Dataset Preview")
st.write(df.head())

# Show dataset summary
st.subheader("📊 Dataset Information")
st.write(df.describe())

# Select columns for visualization
st.subheader("📈 Data Visualization")
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

if numeric_columns:
    x_axis = st.selectbox("Select X-axis Feature", numeric_columns, index=0)
    y_axis = st.selectbox("Select Y-axis Feature", numeric_columns, index=1)
    plot_type = st.radio("Choose Plot Type", ["Scatter Plot", "Histogram"])

    fig, ax = plt.subplots()
    if plot_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue="Species", palette="viridis", ax=ax)
    elif plot_type == "Histogram":
        sns.histplot(df[x_axis], kde=True, bins=30, ax=ax)
    
    st.pyplot(fig)

else:
    st.warning("No numerical columns available for visualization.")

# Simple Chatbot
st.subheader("💬 Chatbot: Ask about the Dataset")
openai_api_key = st.text_input("Enter OpenAI API Key (Optional)", type="password")
user_query = st.text_input("Ask something about coffee dataset:")

if user_query and openai_api_key:
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant knowledgeable about the Coffee Quality dataset."},
                  {"role": "user", "content": user_query}]
    )
    st.write("🤖 Chatbot:", response['choices'][0]['message']['content'])
