import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_combined_df(df, candidate_name, column_name, candidate_column_index=8):
    # Calculate Count for the specific candidate (as a Series, not a DataFrame to avoid 'उम्र' column)
    candidate_count = df[df[df.columns[candidate_column_index]] == candidate_name][column_name].value_counts()
    candidate_count = candidate_count.rename('Count')

    # Calculate Total count for the entire dataset (as a Series)
    total_count = df[column_name].value_counts()
    total_count = total_count.rename('Total')

    # Combine them using outer join
    combined_df = pd.DataFrame(candidate_count).join(pd.DataFrame(total_count), how='outer')

    # Fill NaN values in 'Count' with 0 since not all ages might be present for the candidate
    combined_df['Count'] = combined_df['Count'].fillna(0)

    # Calculate Percentage
    combined_df['Percentage'] = (combined_df['Count'] / combined_df['Total']) * 100

    return combined_df


def plot_pie_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values, hole=0, textinfo='label+percent')])

    # Update layout
    fig.update_layout(title_text=f"{column_name}")

    # Show the plot
    st.plotly_chart(fig)


def plot_bar_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a bar chart using Plotly with values on bars
    fig = go.Figure([go.Bar(x=data.index, y=data.values, text=data.values, textposition='auto',
                            marker_color=px.colors.qualitative.Pastel)])

    # Update layout for better visualization
    fig.update_layout(
        title_text=f"{column_name}",
        xaxis_title="Political Party",
        yaxis_title="Count",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig)


df = pd.read_excel("Suvery Complete.xlsx")

st.sidebar.title('Analysis Report')
option = st.sidebar.selectbox('Please select constituency', ['Please select here', 'Overview', 'Caste-wise Analysis',
                                                             'Age-wise Analysis', 'Profession-wise Analysis',
                                                             'Education-wise Analysis', 'Village-wise Analysis',])

if option == 'Please select here':
    st.title('Gharaunda Analysis Report')

    st.header('Name: Mr. Harvinder Kalyan')

if option == 'Overview':
    st.title('Gharaunda Analysis Report')
    st.header('1. Villages')
    plot_bar_chart(df, 'ग्राम पंचायत का नाम / नगर पालिका का नाम?')
    st.header('2. Age')
    plot_pie_chart(df, 'उम्र')
    st.header('3. Education')
    plot_pie_chart(df, df.columns[3])
    st.header('4. Caste')
    plot_bar_chart(df, df.columns[4])
    st.header('5. Employment')
    plot_pie_chart(df, df.columns[5])
    st.header('6. State Government Satisfaction')
    plot_pie_chart(df, 'क्या आप राज्य सरकार से संतुष्ट है?')
    st.header('7. MLA Satisfaction')
    plot_pie_chart(df, 'क्या आप वर्तमान विधायक से संतुष्ट हैं?')
    st.header('8. Party Choice')
    plot_bar_chart(df, 'आप किस राजनितिक पार्टी को पसंद करते है ?')
    st.header('9. Candidate Preference')
    plot_bar_chart(df, 'अगर नहीं तो आप आगामी विधनसभा में विधायक किसको चुनना पसंद करेंगे?')

if option == 'Caste-wise Analysis':
    st.title('Caste-wise Analysis')

    st.header("1. Castes")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df['जाति'].value_counts())

    with col2:
        plot_bar_chart(df, df.columns[4])

    st.header("2. Top castes for Harvinder Kalyan")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df[df[df.columns[8]] == 'हरविन्द्र कल्याण']['जाति'].value_counts())

    with col2:
        plot_bar_chart(df[df[df.columns[8]] == 'हरविन्द्र कल्याण'], 'जाति')

    st.header("3. Top castes for Virendra Rathore")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़']['जाति'].value_counts())

    with col2:
        plot_bar_chart(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़'], 'जाति')

    st.header('4. Caste-wise preference for Harvinder Kalyan')
    st.dataframe(create_combined_df(df, 'हरविन्द्र कल्याण', 'जाति'))

    st.header('5. Caste-wise preference for Virendra Rathore')
    st.dataframe(create_combined_df(df, 'वीरेंद्र सिंह राठौड़', 'जाति'))

if option == 'Age-wise Analysis':
    st.title('Age-wise Analysis')

    st.header("1. Age Distribution")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df['उम्र'].value_counts())

    with col2:
        plot_pie_chart(df, 'उम्र')

    st.header("2. Age-wise preference for Harvinder Kalyan")
    st.dataframe(create_combined_df(df, 'हरविन्द्र कल्याण', 'उम्र'))
    plot_pie_chart(df[df[df.columns[8]] == 'हरविन्द्र कल्याण'], 'उम्र')

    st.header("3. Age-wise preference for Virendra Rathore")
    st.dataframe(create_combined_df(df, 'वीरेंद्र सिंह राठौड़', 'उम्र'))
    plot_pie_chart(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़'], 'उम्र')

if option == 'Profession-wise Analysis':
    st.title('Profession-wise Analysis')

    st.header("1. Profession Distribution")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df['रोजगार'].value_counts())

    with col2:
        plot_pie_chart(df, 'रोजगार')

    st.header("2. Profession-wise preference for Harvinder Kalyan")
    st.dataframe(create_combined_df(df, 'हरविन्द्र कल्याण', 'रोजगार'))
    plot_pie_chart(df[df[df.columns[8]] == 'हरविन्द्र कल्याण'], 'रोजगार')

    st.header("3. Profession-wise preference for Virendra Rathore")
    st.dataframe(create_combined_df(df, 'वीरेंद्र सिंह राठौड़', 'रोजगार'))
    plot_pie_chart(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़'], 'रोजगार')

if option == 'Education-wise Analysis':
    st.title('Education-wise Analysis')

    st.header("1. Education Distribution")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.dataframe(df['शिक्षा'].value_counts())

    with col2:
        plot_pie_chart(df, 'शिक्षा')

    st.header("2. Education-wise preference for Harvinder Kalyan")
    st.dataframe(create_combined_df(df, 'हरविन्द्र कल्याण', 'शिक्षा'))
    plot_pie_chart(df[df[df.columns[8]] == 'हरविन्द्र कल्याण'], 'शिक्षा')

    st.header("3. Education-wise preference for Virendra Rathore")
    st.dataframe(create_combined_df(df, 'वीरेंद्र सिंह राठौड़', 'शिक्षा'))
    plot_pie_chart(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़'], 'शिक्षा')

if option == 'Village-wise Analysis':
    st.title('Village-wise Analysis')

    st.header("1. Villages Distribution")

    st.dataframe(df['ग्राम पंचायत का नाम / नगर पालिका का नाम?'].value_counts())

    plot_bar_chart(df, 'ग्राम पंचायत का नाम / नगर पालिका का नाम?')

    st.header("2. Village-wise preference for Harvinder Kalyan")
    st.dataframe(create_combined_df(df, 'हरविन्द्र कल्याण', 'ग्राम पंचायत का नाम / नगर पालिका का नाम?'))
    plot_bar_chart(df[df[df.columns[8]] == 'हरविन्द्र कल्याण'], 'ग्राम पंचायत का नाम / नगर पालिका का नाम?')

    st.header("3. Village-wise preference for Virendra Rathore")
    st.dataframe(create_combined_df(df, 'वीरेंद्र सिंह राठौड़', 'ग्राम पंचायत का नाम / नगर पालिका का नाम?'))
    plot_bar_chart(df[df[df.columns[8]] == 'वीरेंद्र सिंह राठौड़'], 'ग्राम पंचायत का नाम / नगर पालिका का नाम?')


