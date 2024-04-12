import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

import numpy as np, plotly.graph_objects as go
from shapely.geometry import Point, LineString, Polygon
from shapely.affinity import rotate
from scipy.optimize import root_scalar


########################################################################################################


dash.register_page(__name__, name = "Friction", path = "/friction")

########################################################################################################
# DETERMINE SLIPPAGE:

def Slippage(Wt, Wb, us, angle):
    """
    Determines the case of the slippage.
    Case 1 Slippage: Top block slides UPWARDS and the bottom block slides DOWNWARDS.
    Case 2 Slippage: Top block slides DOWNWARDS and the bottom block slides UPWARDS.
    

    Args:
        Wt (float):     Mass of the top block [kN].
        Wb (float):     Mass of the bottom block [kN].
        us (float):     Coefficient of static friction.
        angle (float):  Inclination angle of blocks [deg].

    Returns:
        int: 1, 2, 0
    """
    
    Ttop1 = 0.5*Wt*np.sin(np.radians(angle)) + 0.5*us*Wt*np.cos(np.radians(angle))
    Ttop2 = 0.5*Wt*np.sin(np.radians(angle)) - 0.5*us*Wt*np.cos(np.radians(angle))
    
    Tbot1 = Wb*np.sin(np.radians(angle)) - us*(2*Wt + Wb)*np.cos(np.radians(angle))
    Tbot2 = Wb*np.sin(np.radians(angle)) + us*(2*Wt + Wb)*np.cos(np.radians(angle))
    
    if (Ttop1 <= Tbot1) and (Ttop2 < Tbot2):
        return 1
    elif (Tbot2 <= Ttop2) and (Tbot1 < Ttop1):
        return 2
    elif (Tbot1 < Ttop1) and (Ttop2 < Tbot2):
        return 0
    else:
        return 0
    
# end of def Slippage()








########################################################################################################
# APP LAYOUT:

layout = dbc.Container([

    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: Label & Slider - Top Mass
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Top Mass [kg]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(10, 100, 10, value = 50, id = "TMass-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(10, 100+1, 10)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-1"
    ),

    #-------------------------------------------------------------------------------------------------------
    # ROW 2: Label & Slider - Bottom Mass
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Bottom Mass [kg]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(10, 100, 10, value = 50, id = "BMass-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(10, 100+1, 10)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-3"
    ),
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 3: Label & Slider - Friction Coefficient
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Friction Coefficient: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(1, 20, 1, value = 8, id = "Friction-slider", 
                       marks = {i: {"label": f"{i/20}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(1, 20+1, 1)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-3"
    ),
    
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 4: Label & Slider - Angle
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Angle [deg]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(0, 90, 5, value = 10, id = "Angle-slider", 
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
    # ROW 4: Graphs
    
    dbc.Row([
        
        dbc.Col([

            html.Div(
                children = html.Label(
                                "Two blocks are kept in position with a cable and a pulley system. Assume that the coefficient of static friction (μs) on all surfaces is the same. Determine in which direction the blocks will slide, if they slide at all.",
                                style = {"verticalAlign": "top", "textAlign": "justify"},
                                id = "question"
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

            dcc.Graph(id = "blocks-graph"),

        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-3"
        ),

        dbc.Col([

            html.Div(
                children = html.Label(
                                style = {"verticalAlign": "top", "textAlign": "justify"},
                                id = "blocks"
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
        

    ], align = "center", justify = "center"
    ),



], fluid = True,)




########################################################################################################
# Calculate angle and draw blocks:

@callback(
    Output("blocks-graph", "figure"),
    Output("blocks", "children"),
    Input("TMass-slider", "value"),
    Input("BMass-slider", "value"),
    Input("Angle-slider", "value"),
    Input("Friction-slider", "value")
)
def Calculate_Rotation(TMass, BMass, angle, us):
    
    
    fig1 = go.Figure()
    
    #------------------------------------------------------------------------------------------
    # Calculate Angle:
    
    Wt = TMass*9.81
    Wb = BMass*9.81
    us /= 20
    
    slip_case = Slippage(Wt, Wb, us, angle)
    
    if slip_case == 1:
        dtop = 0
        dbot = 0.5
    elif slip_case == 2:
        dtop = 0.5
        dbot = 0
    elif slip_case == 0:
        dtop = 0
        dbot = 0
    # end if else
            
    #------------------------------------------------------------------------------------------
    # Generate Figures:
    
    
    
    Line1    = LineString([[0, 2], [0, 0], [5, 0]])
    BlockBot = Polygon([[2.5+dbot, 0], [2.5+dbot, 1], [4+dbot, 1], [4+dbot, 0]])
    BlockTop = Polygon([[2.5+dtop, 1], [2.5+dtop, 2], [4+dtop, 2], [4+dtop, 1]])
    
    PulleyBot = Point(0.75, 0.875).buffer(0.375)
    PulleyTop = Point(1.75, 1.50).buffer(0.25)
    
    PulleyLine1 = LineString([[0.75, 0.5], [2.50+dbot, 0.50]])
    PulleyLine2 = LineString([[0.75, 1.25], [1.75, 1.25]])
    PulleyLine3 = LineString([[0.00, 1.75], [1.75, 1.75]])
    
    PulleyLine4 = LineString([[0.00, 0.875], [0.75, 0.875]])
    PulleyLine5 = LineString([[1.75, 1.50], [2.50+dtop, 1.50]])
    
    #------------------------------------------------------------------------------------------
    # Plot Lines:
    
    fig1.add_trace(go.Scatter(x = [0, 5], y = [0, 0],  mode = "lines", hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )

    Line1x, Line1y = rotate(Line1, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(Line1x), y = np.array(Line1y),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    
    #------------------------------------------------------------------------------------------
    # Plot Pulleys:
    
    ## Bot:
    PulleyBotx, PulleyBoty = rotate(PulleyBot, -1*angle, (5, 0)).exterior.xy
    fig1.add_trace(go.Scatter(x = np.array(PulleyBotx), y = np.array(PulleyBoty),  
                              mode = "lines", fill = "toself", hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )

    ## Top:
    PulleyTopx, PulleyTopy = rotate(PulleyTop, -1*angle, (5, 0)).exterior.xy
    fig1.add_trace(go.Scatter(x = np.array(PulleyTopx), y = np.array(PulleyTopy),  
                              mode = "lines", fill = "toself", hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )

    #------------------------------------------------------------------------------------------
    # Plot Pulley lines:
    
    x1, y1 = rotate(PulleyLine1, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(x1), y = np.array(y1),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    x2, y2 = rotate(PulleyLine2, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(x2), y = np.array(y2),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    x3, y3 = rotate(PulleyLine3, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(x3), y = np.array(y3),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    x4, y4 = rotate(PulleyLine4, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(x4), y = np.array(y4),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    x5, y5 = rotate(PulleyLine5, -1*angle, (5, 0)).xy
    fig1.add_trace(go.Scatter(x = np.array(x5), y = np.array(y5),  
                              mode = "lines",  hoverinfo = "skip",
                              line_color = "black", showlegend = False, name = " ",
                              )
    )
    
    #------------------------------------------------------------------------------------------
    # Plot Blocks:
    
    ## Bot:
    BlockBotx, BlockBoty = rotate(BlockBot, -1*angle, (5, 0)).exterior.xy
    fig1.add_trace(go.Scatter(x = np.array(BlockBotx), y = np.array(BlockBoty),  
                              mode = "lines", fill = "toself",
                              line_color = "black", showlegend = False, 
                              name = f"Mass = {BMass} kg",
                              )
    )

    ## Top:
    BlockTopx, BlockTopy = rotate(BlockTop, -1*angle, (5, 0)).exterior.xy
    fig1.add_trace(go.Scatter(x = np.array(BlockTopx), y = np.array(BlockTopy),  
                              mode = "lines", fill = "toself", 
                              line_color = "blue", showlegend = False, 
                              name = f"Mass = {TMass} kg",
                              )
    )

    if slip_case == 1:
        results = [
            "The top block slides ", html.Strong("UPWARDS"), "." ,html.Br(),
            html.Br(),
            "The bottom block slides ", html.Strong("DOWNWARDS"), ".",
        ]
    elif slip_case == 2:
        results = [
            "The top block slides ", html.Strong("UPWARDS"), "." ,html.Br(),
            html.Br(),
            "The bottom block slides ", html.Strong("DOWNWARDS"), ".",
        ]
    elif slip_case == 0:
        results = [
            "The blocks ", html.Strong("DO NOT"), " slide." ,html.Br(),
        ]
    # end if else
    
    
    
    #------------------------------------------------------------------------------------------
    # Update layout:
    fig1.update_layout(
        plot_bgcolor = "white",
        template = "simple_white",
        autosize = True,
    )
    fig1.update_xaxes(
        showticklabels=False,
        showgrid = False,
        zeroline = False,
        visible = False,
    )
    fig1.update_yaxes(
        showticklabels=False,
        showgrid = False,
        zeroline = True,
        visible = False,
        scaleanchor = "x",
        scaleratio = 1,
    )
    
    
    return fig1, results
    
# end def Calculate_Rotation() 
    
    



