import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')

import hvplot.pandas
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
methane = pd.read_csv("C:/Users/KUTIKUPPALA KISHORE/dstoolpython/project/methane-emissions.csv")
co2 = pd.read_csv("C:/Users/KUTIKUPPALA KISHORE/dstoolpython/project/co2-emissions-per-capita.csv")
pollution = pd.read_csv("C:/Users/KUTIKUPPALA KISHORE/dstoolpython/project/long-run-air-pollution.csv")
print(methane.info())
print(co2.info())
print(pollution.info())
print(methane.isnull().sum())
print(co2.isnull().sum())
print(pollution.isnull().sum())
methane = methane[methane['Entity'] != 'World']
co2 = co2[co2['Entity'] != 'World']
pollution = pollution[pollution['Entity'] != 'World']
methane = methane.dropna()
co2 = co2.dropna()
pollution = pollution.dropna()
df = pollution.merge(co2, on=['Entity','Year'], how='left')
df = df.merge(methane, on=['Entity','Year'], how='left')
df.rename(columns={
    'CO₂ emissions per capita': 'CO2',
    'Annual methane emissions including land use': 'Methane'
}, inplace=True)
df.info()
df=df.drop(['Code','Code_y'],axis=1)
df.rename(columns={'Code_x':'Code'},inplace=True)
print(df.isnull().sum())
df = df.dropna(subset=['CO2','Methane'])
df.info()
print(df.isnull().sum())
print(df.describe())
df.shape
df['Avg Pollution'] = (
    df['Nitrogen oxides'] +
    df['Sulfur dioxide'] +
    df['Carbon monoxide'] +
    df['Black carbon'] +
    df['Ammonia'] +
    df['Non-methane volatile organic compounds']+
    df['CO2']+
    df['Methane']
) / 8
df.head()
print(np.sort(df['Year'].unique()))
mean_val = df['Avg Pollution'].mean()
median_val = df['Avg Pollution'].median()
std_val = df['Avg Pollution'].std()
print("Mean:", mean_val)
print("Median:", median_val)
print("Standard Deviation:", std_val)
idf=df.interactive()
year_slider=pn.widgets.IntSlider(name='Year slider',start=1850,end=2022,step=5,value=1850)
year_slider
country_dropdown = pn.widgets.Select(
    name='Country',
    options=sorted(df['Entity'].unique().tolist())
)
country_dropdown
yaxis_pollutants = pn.widgets.RadioButtonGroup(
    name='Select Pollutant',
    options=[
        'Nitrogen oxides',
        'Sulfur dioxide',
        'Carbon monoxide',
        'Black carbon',
        'Ammonia',
        'Non-methane volatile organic compounds',
        'CO2',
        'Methane',
        'Avg Pollution'
    ],
    button_type='success',
    
)

yaxis_pollutants
bar_pipeline = (
    idf[
        (idf.Year <= year_slider)
    ]
    .groupby(['Entity'])[yaxis_pollutants].mean()
    .to_frame()
    .reset_index()
    .sort_values(by=yaxis_pollutants, ascending=False)
    .head(20)  
)
bar_plot = bar_pipeline.hvplot(
    kind='bar',
    x='Entity',
    y=yaxis_pollutants,
    title="Top 20 Polluted Countries",
    rot=45,
    height=500,
    width=900
)
bar_plot
plt.figure(figsize=(10,6))
col = yaxis_pollutants.value
filtered_df = df[df['Year'] <= year_slider.value]

if country_dropdown.value != 'All':
    filtered_df = filtered_df[filtered_df['Entity'] == country_dropdown.value]
sns.histplot(filtered_df[col], kde=True)
plt.xlabel(col)
plt.ylabel('Frequency')
plt.axvline(filtered_df[col].mean(), color='r', linestyle='--',
            label=f"Mean: {filtered_df[col].mean():.2f}")

plt.axvline(filtered_df[col].median(), color='b', linestyle='--',
            label=f"Median: {filtered_df[col].median():.2f}")
plt.legend()
plt.title(f"Distribution of {col}")
plt.show()
year_slider
scatter_pipeline = (
    idf[
        (idf.Year == year_slider)
    ]
    .groupby(['Entity','Year','CO2'])['Avg Pollution'].mean()
    .to_frame()
    .reset_index()
)
scatter_plot = scatter_pipeline.hvplot(
    kind='scatter',
    x='CO2',
    y='Avg Pollution',
    by='Entity',
    size=80,
    alpha=0.6,
    legend=False,
    title="CO2 vs Avg Pollution"
)
scatter_plot
corr = df.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(8,6))
heatmap=sns.heatmap(
    corr,
    annot=True,       
    cmap='coolwarm',     
    fmt=".2f"
)
plt.title("Correlation Heatmap")
heatmap
plt.figure(figsize=(10,6))
col = yaxis_pollutants.value
filtered_df = df[df['Year'] <= year_slider.value]
if country_dropdown.value != 'All':
    filtered_df = filtered_df[filtered_df['Entity'] == country_dropdown.value]
sns.boxplot(y=filtered_df[col])
plt.title(f"{col} Distribution (Box Plot)")
plt.ylabel(col)
plt.show()
pair_plot = sns.pairplot(
    df[['Nitrogen oxides','Sulfur dioxide','Carbon monoxide','CO2','Methane','Avg Pollution']]
)
pair_plot
plt.figure(figsize=(8,8))
filtered_df = df[df['Year'] == year_slider.value]
pollutants_avg = {
    'Nitrogen oxides': filtered_df['Nitrogen oxides'].mean(),
    'Sulfur dioxide': filtered_df['Sulfur dioxide'].mean(),
    'Carbon monoxide': filtered_df['Carbon monoxide'].mean(),
    'Black carbon': filtered_df['Black carbon'].mean(),
    'Ammonia': filtered_df['Ammonia'].mean(),
    'NMVOC': filtered_df['Non-methane volatile organic compounds'].mean(),
    'CO2': filtered_df['CO2'].mean(),
    
}
plt.pie(
    pollutants_avg.values(),
    labels=pollutants_avg.keys(),
    autopct='%1.1f%%'
)
plt.title(f"Pollutant Contribution for Year {year_slider.value}")
plt.show()
heatmap_pane = pn.pane.Matplotlib(fig, tight=True)
pair_pane = pn.pane.Matplotlib(pair_plot.fig, tight=True)
fig_pie, ax_pie = plt.subplots(figsize=(6,6))
filtered_df = df[df['Year'] == year_slider.value]
pollutants_avg = {
    'Nitrogen oxides': filtered_df['Nitrogen oxides'].mean(),
    'Sulfur dioxide': filtered_df['Sulfur dioxide'].mean(),
    'Carbon monoxide': filtered_df['Carbon monoxide'].mean(),
    'Black carbon': filtered_df['Black carbon'].mean(),
    'Ammonia': filtered_df['Ammonia'].mean(),
    'NMVOC': filtered_df['Non-methane volatile organic compounds'].mean(),
    'CO2': filtered_df['CO2'].mean(),
}
ax_pie.pie(
    pollutants_avg.values(),
    labels=pollutants_avg.keys(),
    autopct='%1.1f%%'
)
ax_pie.set_title(f"Pollutant Contribution for Year {year_slider.value}")
pie_pane = pn.pane.Matplotlib(fig_pie, tight=True)
template = pn.template.FastListTemplate(
    title='ANALYSIS OF AIR POLLUTANTS AND GREENHOUSE GAS EMISSIONS OVER TIME',
    sidebar=[
        pn.pane.Markdown("# Air Pollution Analysis"),
        
        pn.pane.Markdown(
        "#### This dashboard analyzes air pollutants and greenhouse gas emissions over time. "
        "It helps in understanding trends, relationships, and distributions of pollutants such as "
        "NOx, SO₂, CO, Methane, and CO₂ across different countries and years."
        ),

        pn.pane.Markdown("## Settings"),
        year_slider,
        country_dropdown,
        yaxis_pollutants
    ],
    main=[
        pn.Row(
            pn.Column(bar_plot, margin=(0,20)),
            pn.Column(scatter_plot)
        ),

        pn.Row(
            pn.Column(heatmap_pane, margin=(0,20)),
            pn.Column(pie_pane)
        ),

        pn.Row(
            pn.Column(pair_pane)
        )
    ],
    accent_base_color="#670D2F",
    header_background="#670D2F",
)
template.show()
