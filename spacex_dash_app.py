from pathlib import Path
import pandas as pd
from dash import Dash,dcc,html,Input,Output
import plotly.express as px
p=Path(__file__).resolve().parent/'data'/'dataset_part_2.csv'
df=pd.read_csv(p)
app=Dash(__name__)
site_col='LaunchSite';payload_col='PayloadMass'
sites=sorted(df[site_col].dropna().unique().tolist())
lo,hi=float(df[payload_col].min()),float(df[payload_col].max())
app.layout=html.Div([html.H2('SpaceX Falcon 9 Landing Outcomes'),
 dcc.Dropdown(['ALL']+sites,'ALL',id='site'),
 dcc.RangeSlider(lo,hi,value=[lo,hi],id='payload',tooltip={'placement':'bottom'}),
 dcc.Graph(id='pie'),dcc.Graph(id='scatter')],style={'maxWidth':'1100px','margin':'auto'})
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def update(site,rng):
    d=df if site=='ALL' else df[df[site_col]==site]
    d=d[d[payload_col].between(*rng)].copy()
    d['Outcome']=d['Class'].map({1:'Successful landing',0:'Unsuccessful landing'})
    pie=px.pie(d,names='Outcome',title=f'Landing outcomes: {site}')
    scatter=px.scatter(d,x=payload_col,y='Class',color='Outcome',hover_data=[site_col],
        title='Payload mass vs landing outcome')
    return pie,scatter
if __name__=='__main__':app.run(debug=True)
