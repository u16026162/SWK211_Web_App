import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc



dash.register_page(__name__, name = "Vibrations", path = "/vibrations")





layout = dbc.Container([
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: 
    
    dbc.Row([
        
        html.Div([html.Label("Vibrations Page !")])
        
    ]),

    
    
    
    
    
    
    
], fluid = True,)