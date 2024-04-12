import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

import numpy as np, plotly.graph_objects as go
from scipy.optimize import root_scalar


########################################################################################################


dash.register_page(__name__, name = "Cables", path = "/cables")



########################################################################################################
# APP LAYOUT:

layout = dbc.Container([

    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: Label & Slider - Self Weight
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Cable Self Weight [kN/m]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(1, 10, 1, value = 5, id = "SW-slider", 
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
    # ROW 2: Label & Slider - Cable Length
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Cable Length [m]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(23, 30, 1, value = 25, id = "L-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(23, 30+1, 1)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-3"
    ),
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 3: Label & Slider - Height of B
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Height B [m]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(5, 20, 1, value = 20, id = "H-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(5, 20+1, 1)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-3"
    ),
    
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 4: Graphs
    
    dbc.Row([
        
        dbc.Col([

            html.Div(
                children = html.Label(
                                       style = {"verticalAlign": "top"},
                                       id = "cable-properties"
                            ),
                style = {
                    "fontSize": "1rem", 
                    "family": "Arial",
                    "color": "black",
                },
                className = "align-top",
            ),

        ], xs = 12, sm = 12, md = 12, lg = 3, xl = 3, xxl = 3, className = "mt-3"
        ),
        
        dbc.Col([

            dcc.Graph(id = "cable-graph"),

        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-3"
        ),

        dbc.Col(xs = 12, sm = 12, md = 12, lg = 3, xl = 3, xxl = 3, className = "mt-3"),
        

    ], align = "center", justify = "center"
    ),



], fluid = True,)




########################################################################################################
# Draw cable and calculate parameters:

@callback(
    Output("cable-graph", "figure"),
    Output("cable-properties", "children"),
    Input("SW-slider", "value"),
    Input("L-slider", "value"),
    Input("H-slider", "value")
)
def Draw_Cable(w, L, H):
    
    bx = 20
    
    fig1 = go.Figure()
    
    
    #------------------------------------------------------------------------------------------
    # Calculations:
    
    solve_for_c = lambda c: (2*c/bx)*np.sinh(0.5*bx/c) - (1/bx)*np.sqrt((L**2) - ((H-10)**2))
    c = root_scalar(solve_for_c, x0 = 10, method = "newton").root
    
    solve_for_v1 = lambda v1: c*np.cosh((bx-v1)/c) - c*np.cosh((0-v1)/c) - (H-10)
    v1 = root_scalar(solve_for_v1, x0 = 10, method = "newton").root
    
    v2 = 10 - c*np.cosh((0-v1)/c)
        
    cable = lambda x: c*np.cosh((x-v1)/c) + v2
    
    solve_for_turning = lambda x: np.sinh((x-v1)/c)
    x_turn = root_scalar(solve_for_turning, x0 = 10, method = "newton").root
    
    straight_line = lambda x: (H-10)*x/bx + 10
    max_sag = np.abs(straight_line(x_turn) - cable(x_turn))
    
    To = w*c
    
    #------------------------------------------------------------------------------------------
    # Draw Supports & line:
    fig1.add_trace(go.Scatter(x = [0], y = [10-1], mode = "markers", marker_color = "black", 
                              marker_symbol = "triangle-up", hoverinfo = "skip",
                              marker_size = 20, showlegend = False,
                              )
    )
    fig1.add_trace(go.Scatter(x = [bx], y = [H-1], mode = "markers", marker_color = "black", 
                              marker_symbol = "triangle-up", hoverinfo = "skip",
                              marker_size = 20, showlegend = False,
                              )
    )
    fig1.add_trace(go.Scatter(x = [0, bx], y = [10, H], mode = "lines", line_color = "gray", 
                              hoverinfo = "skip", showlegend = False,
                              )
    )

    
    #------------------------------------------------------------------------------------------
    # Draw Cable:
    x1 = np.linspace(0, bx, 500)
    fig1.add_trace(go.Scatter(x = x1, y = cable(x1), mode = "lines", line_color = "blue",
                              marker_size = 20, showlegend = True, name = "Cable",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    #------------------------------------------------------------------------------------------
    # Turning Point: 
    ysag = cable(x_turn)
    fig1.add_trace(go.Scatter(x = [x_turn], y = [ysag], mode = "markers+text", marker_color = "black", 
                              text = [f"x = {x_turn:.2f} m"], textposition="bottom center",
                              showlegend = False, name = "Turning Point",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    #------------------------------------------------------------------------------------------
    # Draw h:
    fig1.add_trace(go.Scatter(x = [x_turn, x_turn], y = [straight_line(x_turn) , cable(x_turn)], 
                              mode = "lines+markers", line_color = "black", showlegend = True, 
                              name = "h", hoverinfo = "skip",
                              )
    )
    
    #------------------------------------------------------------------------------------------
    # results:
    
    
    
    results = [
        # remove this html.Label and the red colouring
        html.Label([f"Remember to calculate T", html.Sub("max")], style = {"color": "red"}), html.Br(),
        "T", html.Sub("o"), f" = {To:.2f} kN", html.Br(), 
        f"c  = {c:.2f}", html.Br(),
        f"h  = {max_sag:.2f} m", html.Br(),
        "x", html.Sub("turn"), f" = {x_turn:.2f} m", html.Br(), 
    ]
    
    
    
    #------------------------------------------------------------------------------------------
    # Update layout:
    fig1.update_layout(
        plot_bgcolor = "white",
        template = "simple_white",
        autosize = True,
        annotations = [go.layout.Annotation(
            dict(x=x_turn+2, y=0.5*(straight_line(x_turn) + cable(x_turn)), xref="x", yref="y",
                text=f"h = {max_sag:.2f} m", showarrow=False,
                axref="x", ayref='y', ax=x_turn, ay=0.5*(straight_line(x_turn) + cable(x_turn)),
                bgcolor="white",
                )
        )],

    )
    fig1.update_xaxes(
        title = "x [m]",
        title_font = {"family": "Arial Black"},
        zeroline = False,
        range = [0-2, bx+2],
    )
    fig1.update_yaxes(
        title = "y [m]",
        title_font = {"family": "Arial Black"},
        zeroline = False,
        range = [0-2, 20+2],
    )
    
    
    
    return fig1, results
# end def Draw_Cable()









########################################################################################################
