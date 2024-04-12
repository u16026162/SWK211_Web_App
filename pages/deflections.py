import dash, numpy as np, plotly.graph_objects as go, matplotlib.pyplot as plt
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

from shapely.geometry import Point, LineString, Polygon
from shapely.affinity import rotate
from shapely import centroid

dash.register_page(__name__, name = "Deflections", path = "/deflections")

########################################################################################################

Ix, Iy = 759_071, 9_941_055
O, R   = 5_350_063, 4_590_992

########################################################################################################


layout = dbc.Container([

    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: Label & Slider - E-value
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Choose E [GPa]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(100, 200, 10, value = 100, id = "E-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(100, 200+1, 10)
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

            html.Div(html.Label("Choose Angle [degrees]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(0, 90, 5, value = 0, id = "angle-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(0, 90+1, 5)
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

            dcc.Graph(id = "mohr-circle-graph", style = {"height": "45vh", "width": "45vh"}),
            html.Div(id = "results", style = {"family": "Arial", "color": "black"}),

        ], xs = 12, sm = 12, md = 6, lg = 6, xl = 3, xxl = 3, className = "mt-5"
        ),
                
        dbc.Col([

            dcc.Graph(id = "channel-graph"),
            
        ], xs = 12, sm = 12, md = 6, lg = 6, xl = 3, xxl = 3, className = "mt-3"
        ),
        
        dbc.Col([

            html.Div(dcc.Graph(id = "beam-deflection-graph", style = {"height": "60vh"})),
            
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 6, xxl = 6, className = "mt-3"
        ),


    ], align = "center", justify = "center"
    ),



], fluid = True,)


########################################################################################################
# MOHR CIRCLE GRAPH:

@callback(
    Output("mohr-circle-graph", "figure"),
    Output("results", "children"),
    Input("angle-slider", "value")
)
def Mohr_Circle_Graph(angle):
    
    fig1 = go.Figure()
    
    a  = 2*R*np.cos(np.radians(angle))
    b  = a*np.cos(np.radians(angle))
    
    Iu = Iy - b
    
    a  = 2*R*np.sin(np.radians(angle))
    b  = a*np.sin(np.radians(angle))
    
    Iv = Iy - b


    x = np.linspace(Ix, Iy, 500)
    y1 = np.sqrt((R**2) - (x - O)**2)
    
    fig1.add_trace(go.Scatter(x = x, y = y1,  mode = "lines", line_color = "black", showlegend = False,
                              name = "Mohr Circle",
                              hovertemplate='(%{x:.0f}, %{y:.0f})',
                              )
    )
    fig1.add_trace(go.Scatter(x = x, y = -y1, mode = "lines", line_color = "black", showlegend = False,
                              name = "Mohr Circle",
                              hovertemplate='(%{x:.0f}, %{y:.0f})',
                              )
    )
    
    # Point 1:
    x1 = Iu
    y1 = -1*np.sqrt((R**2) - (x1 - O)**2)
    
    # Point 2:
    x2 = Iv
    y2 = np.sqrt((R**2) - (x2 - O)**2)
    
    fig1.add_trace(go.Scatter(x = [x1, x2], y = [y1, y2], mode = "lines+markers", line_color = "red", 
                              showlegend = False, name = "(Ix/Iy, Ixy)",
                              hovertemplate='(%{x:.0f}, %{y:.0f})',
                              )
    )
    
    results = [f"Iu  = {Iu:.3e} mm", html.Sup(4), html.Br(), 
               f"Iv  = {Iv:.3e} mm", html.Sup(4), html.Br(), 
               f"Iuv = {y1:.3e} mm", html.Sup(4)]
    
    
     
    fig1.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        margin=dict(l=0, r=0, t=0, b=0),
        autosize = True
    )
    fig1.update_xaxes(
        range = [0, 10e6],
    )
    fig1.update_yaxes(
        range = [-5e6 - Ix/2, 5e6 + Ix/2],
        scaleanchor = "x",
        scaleratio = 1,
        zeroline = True,
    )
    
    return fig1, results










########################################################################################################
# ROTATE CHANNEL:

@callback(
    Output("channel-graph", "figure"),
    Input("angle-slider", "value")
)
def Rotate_Graph(angle):
        
    fig2 = go.Figure()
    
    #--------------------------------------------------------------------------
    # Draw channel:
    
    t = 5
    
    channel = Polygon([[25, 100], [25, 175], [275, 175], [275, 100], [255, 100], [255, 100+t],
                       [275-t, 100+t], [275-t, 175-t], [25+t, 175-t], [25+t, 100+t], [45, 100+t], [45, 100]])
    c_x, c_y = centroid(channel).xy
    
    line = LineString([[0, c_y[0]], [300, c_y[0]]])
    
    
    
    channelx, channely = rotate(channel, angle, (c_x[0], c_y[0])).exterior.xy
    fig2.add_trace(go.Scatter(x = np.array(channelx), y = np.array(channely),  
                              mode = "lines", fill = "toself", hoverinfo = "skip", line_color = "black",
                              fillcolor = "black", showlegend = False, name = " ",
                              )
    )
    
    fig2.add_trace(go.Scatter(x = [0, 300], y = [c_y[0], c_y[0]], 
                              mode = "lines", line_color = "black", 
                              showlegend = False,  hoverinfo = "skip",
                              )
    )
    
    linex, liney = rotate(line, angle, (c_x[0], c_y[0])).xy
    fig2.add_trace(go.Scatter(x = np.array(linex), y = np.array(liney), 
                              mode = "lines", line_color = "red", 
                              showlegend = False,  hoverinfo = "skip",
                              )
    )    
    
    
    fig2.update_layout(
        hovermode = False,
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig2.update_xaxes(
        showticklabels=False,
        showgrid = False,
        zeroline = False,
        visible = False,
        scaleanchor = "y",
        scaleratio = 1,
        range = [-50, 300]
    )
    fig2.update_yaxes(
        showticklabels=False,
        showgrid = False,
        zeroline = False,
        visible = False,
        range = [-50, 300]
    )
    
    return fig2
    




########################################################################################################
# BEAM DEFLECTION:

@callback(
    Output("beam-deflection-graph", "figure"),
    Input("angle-slider", "value"),
    Input("E-slider", "value")
)
def Beam_Deflection(angle, E):
    
    P = 5e3   # N
    L = 5e3   # mm
    E *= 1000 # MPa
    
    x1 = np.linspace(0, L/2, 100)
    x2 = np.linspace(L/2, L, 100)
    
    a  = 2*R*np.cos(np.radians(angle))
    b  = a*np.cos(np.radians(angle))
    
    Iu = Iy - b
    
    defl1 = -P*x1*( (3*(L**2)) - (4*(x1**2)))/(48*E*Iu)
    defl2 = defl1[::-1]
    
    fig3 = go.Figure()
    
    # Deflections:
    fig3.add_trace(go.Scatter(x = x1, y = defl1, mode = "lines", line_color = "blue", showlegend = False, 
                              name = "Deflection",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    fig3.add_trace(go.Scatter(x = x2, y = defl2, mode = "lines", line_color = "blue", showlegend = False,
                              name = "Deflection",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    # Supports:
    fig3.add_trace(go.Scatter(x = [0], y = [-11], mode = "markers", marker_color = "black", 
                              marker_symbol = "triangle-up", hoverinfo = "skip",
                              marker_size = 20, showlegend = False,
                              )
    )
    fig3.add_trace(go.Scatter(x = [5000], y = [-11], mode = "markers", marker_color = "black", 
                              marker_symbol = "circle", hoverinfo = "skip",
                              marker_size = 20, showlegend = False,
                              )
    )
    
    # Maximum Deflection: 
    fig3.add_trace(go.Scatter(x = [x2[0]], y = [defl2[0]], mode = "markers+text", marker_color = "black", 
                              text = f"{defl2[0]:.2f} mm", textposition="bottom center",
                              showlegend = False, name = "Maximum Deflection",
                              hovertemplate='%{y:.2f} mm',
                              )
    )
    
    # Update Layout:
    fig3.update_layout(
        plot_bgcolor = "white",
        template = "simple_white",
        autosize = True,
        annotations = [go.layout.Annotation(
            dict(x=2500, y=0, xref="x", yref="y",
                text="10 kN", showarrow=True,
                axref="x", ayref='y', ax=2500, ay=50,
                arrowhead=1, arrowwidth=3, arrowcolor='red',
                )
        )],
    )
    fig3.update_xaxes(
        showticklabels=False,
        showgrid = False,
        zeroline = False,
        visible = False,
    )
    fig3.update_yaxes(
        title = "Deflection [mm]",
        title_font = {"family": "Arial Black"},
        showticklabels=True,
        range = [-200, 50],
    )
    
    
    return fig3





########################################################################################################