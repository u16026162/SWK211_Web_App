import dash, numpy as np, plotly.graph_objects as go, matplotlib.pyplot as plt, scipy.ndimage as nd, plotly.express as px
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc



dash.register_page(__name__, name = "Resonance", path = "/resonance")


########################################################################################################


layout = dbc.Container([

    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: Label & Slider - freq 1
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Frequency 1 [rad/s]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(1, 10, 1, value = 3, id = "freq1-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(1, 10+1, 1)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-1"
    ),

    #-------------------------------------------------------------------------------------------------------
    # ROW 2: Label & Slider - Angle
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Frequency 2 [rad/s]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(1, 10, 1, value = 1, id = "freq2-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(1, 10+1, 1)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-3"
    ),
    
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 3: Graphs
    
    dbc.Row([
        
        dbc.Col([

            dcc.Graph(id = "separate-graph"),

        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-5"
        ),
                
        dbc.Col([

            dcc.Graph(id = "resonance-graph"),
            
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-5"
        ),
        

    ], align = "center", justify = "center"
    ),



], fluid = True,)


########################################################################################################
# SEPARATE SIGNALS GRAPH:

@callback(
    Output("separate-graph", "figure"),
    Input("freq1-slider", "value"),
    Input("freq2-slider", "value")
)
def Signals_Graph(w1, w2):
    
    fig1 = go.Figure()
    

    x  = np.linspace(0, 6*np.pi+0.1, 1000)
    y1 = 1.2*np.sin(w1*x)
    y2 = 0.8*np.sin(w2*x)
    
    fig1.add_trace(go.Scatter(x = x, y = y1,  mode = "lines", line_color = "blue", 
                              name = "Freq1",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    fig1.add_trace(go.Scatter(x = x, y = y2, mode = "lines", line_color = "red", 
                              name = "Freq2",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    
    fig1.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        autosize = True,
    )
    fig1.update_xaxes(
        title = "Time",
        title_font = {"family": "Arial Black"},
        range = [0, 6*np.pi],
        tickvals = np.arange(0, 6*np.pi+0.1, 0.5*np.pi),
        ticktext = ["0", "π/2", "π", "3π/2", "2π", "5π/2", "3π", "7π/2", "4π", "9π/2", "5π", "11π/2", "6π"],
    )
    fig1.update_yaxes(
        title = "Amplitude",
        title_font = {"family": "Arial Black"},
        range = [-2, 2],
        zeroline = True,
    )
    
    return fig1




########################################################################################################
# RESONANCE GRAPH:

@callback(
    Output("resonance-graph", "figure"),
    Input("freq1-slider", "value"),
    Input("freq2-slider", "value")
)
def Resonance_Graph(w1, w2):
    
    fig2 = go.Figure()
    

    x  = np.linspace(0, 6*np.pi+0.1, 1000)
    y1 = np.sin(w1*x)
    y2 = np.sin(w2*x)
    
    fig2.add_trace(go.Scatter(x = x, y = y1+y2,  mode = "lines", line_color = "black", 
                              name = "superposition",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    
    fig2.update_layout(
        title = "Superposition",
        title_x = 0.5,
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        autosize = True,
    )
    fig2.update_xaxes(
        title = "Time",
        title_font = {"family": "Arial Black"},
        range = [0, 6*np.pi],
        tickvals = np.arange(0, 6*np.pi+0.1, 0.5*np.pi),
        ticktext = ["0", "π/2", "π", "3π/2", "2π", "5π/2", "3π", "7π/2", "4π", "9π/2", "5π", "11π/2", "6π"],
    )
    fig2.update_yaxes(
        title = "Amplitude",
        title_font = {"family": "Arial Black"},
        range = [-2, 2],
        zeroline = True,
    )
    
    return fig2





