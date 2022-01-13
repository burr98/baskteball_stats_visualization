import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np 
import base64

#setting up the layout
st.title('NBA Player Stats Explorer')

st.markdown("""
The purpose of this code is to perform a simple web scraping of data of NBA player stats
""")

st.sidebar.header('User Input features')

year_select = st.sidebar.selectbox('Year', list(range(1950, 2020)))


#Web Scraping
def load_data(year):
 	link = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
 	html = pd.read_html(link, header = 0) #read in html format
 	df = html[0]

 	file = df.drop(df[df.Age == 'Age'].index).astype(str).fillna(0) #delete repeating headers in content and replace NaN values with 0

 	stats = file.drop(['Rk'], axis = 1)

 	return stats


player_stats = load_data(1959)

#Selecting team with sidebar
team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', team)

#selecting team with positions
position = ['C', 'F', 'G', 'PF', 'PG', 'SF', 'SG']
selected_position = st.sidebar.multiselect('Position', position)


#Data filtering
final_select = player_stats[(player_stats.Tm.isin(team)) & (player_stats.Pos.isin(position))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(final_select.shape[0]) + ' rows and ' + str(final_select.shape[1
    ]) + ' columns.')
st.dataframe(final_select)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(final_select), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    final_select.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()