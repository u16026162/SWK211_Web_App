import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

from shapely.geometry import Point, Polygon
import numpy as np, plotly.graph_objects as go

dash.register_page(__name__, name = "Centroids", path = "/centroids")





########################################################################################################
# FUNCTION - SECTOR()

def sector(center, start_angle, end_angle, radius=1, steps=500):
    
    def polar_point(origin_point, angle,  distance):
        return [origin_point.x + np.cos(np.radians(angle)) * distance, 
                origin_point.y + np.sin(np.radians(angle)) * distance]

    if start_angle > end_angle:
        start_angle = start_angle - 360
    else:
        pass
    # end if else
    
    step_angle_width = (end_angle-start_angle) / steps
    sector_width     = (end_angle-start_angle) 
    segment_vertices = []

    segment_vertices.append(polar_point(center, 0,0))
    segment_vertices.append(polar_point(center, start_angle,radius))

    for z in np.arange(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width, radius)))
    # end for z
    
    segment_vertices.append(polar_point(center, start_angle+sector_width,radius))
    segment_vertices.append(polar_point(center, 0,0))
    
    return Polygon(segment_vertices)

# end def sector()


########################################################################################################
# LAYOUT:

layout = dbc.Container([

    
    #-------------------------------------------------------------------------------------------------------
    # ROW 1: Label & Slider - Starting angle
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Starting Angle [deg]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(0, 180, 45, value = 0, id = "SA-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(0, 180+1, 45)
                           }
            ),
            xs = 12, sm = 12, md = 12, lg = 10, xl = 10, xxl = 10, style = {"height": "5vh"}

        )

    ], className = "mt-1"
    ),

    #-------------------------------------------------------------------------------------------------------
    # ROW 2: Label & Slider - Ending Angle
    
    dbc.Row([

        dbc.Col(

            html.Div(html.Label("Ending Angle [deg]: ", style = {"color": "black"})),
            xs = 12, sm = 12, md = 12, lg = 2, xl = 2, xxl = 2

        ),

        dbc.Col(

            dcc.Slider(45, 360, 45, value = 45, id = "EA-slider", 
                       marks = {i: {"label": f"{i}",
                                    "style": {"transform": "rotate(-45deg)", "color": "black"}
                            } for i in range(45, 360+1, 45)
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

            dcc.Graph(id = "line-centroid-graph"),

        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-5"
        ),
                
        dbc.Col([

            dcc.Graph(id = "area-centroid-graph"),
            
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, className = "mt-5"
        ),
        

    ], align = "center", justify = "center"
    ),



], fluid = True,)





########################################################################################################
# LINE CENTROID:

@callback(
    Output("line-centroid-graph", "figure"),
    Input("SA-slider", "value"),
    Input("EA-slider", "value")
)
def Line_Centroid_Graph(SA, EA):
    
    fig1 = go.Figure()
    
    if SA >= EA:
        fig1.update_layout(title = "Starting angle must be smaller than ending angle!",
                           title_x = 0.5)
        return fig1
    # end if
    
    #----------------------------------------------------------------------------------------------------
    ## Draw circle:
    
    sec = sector(Point(0, 0), SA, EA)
    x1, y1 = sec.exterior.xy

    fig1.add_trace(go.Scatter(x = np.array(x1)[1:-2], y = np.array(y1)[1:-2],  mode = "lines", 
                              line_color = "black", showlegend = False,
                              name = " ",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    #----------------------------------------------------------------------------------------------------
    ## Calculate Centroids:
    
    L = 1*np.radians(EA-SA)
    xx = (1**2)*np.sin(np.radians(EA)) - (1**2)*np.sin(np.radians(SA))
    yy = (1**2)*-1*np.cos(np.radians(EA)) - (1**2)*-1*np.cos(np.radians(SA))
    
    X = xx/L
    Y = yy/L
    
    fig1.add_trace(go.Scatter(x = [X], y = [Y],  mode = "markers", marker_color = "red", 
                              marker_symbol = "x", marker_size = 10,
                              showlegend = False, name = "Centroid",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    #----------------------------------------------------------------------------------------------------
    ## Update Layout:
     
    fig1.update_layout(
        title = "Line Centroid",
        title_x = 0.5,
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        # margin=dict(l=0, r=0, t=0, b=0),
        autosize = True,
        annotations = [go.layout.Annotation(
            dict(x=X+0.35, y=Y, xref="x", yref="y",
                text=f"({X:.2f}, {Y:.2f})", showarrow=False,
                axref="x", ayref='y', ax=X, ay=Y,
                bgcolor="white",
                )
        )],
    )
    fig1.update_xaxes(
        range = [-1.1, 1.1],
        zeroline = True,
    )
    fig1.update_yaxes(
        range = [-1.1, 1.1],
        scaleanchor = "x",
        scaleratio = 1,
        zeroline = True,
    )
    
    return fig1







########################################################################################################
# AREA CENTROID:

@callback(
    Output("area-centroid-graph", "figure"),
    Input("SA-slider", "value"),
    Input("EA-slider", "value")
)
def Area_Centroid_Graph(SA, EA):
    
    fig2 = go.Figure()
    
    if SA >= EA:
        fig2.update_layout(title = "Starting angle must be smaller than ending angle!",
                           title_x = 0.5)
        return fig2
    # end if
    
    
    #----------------------------------------------------------------------------------------------------
    ## Draw circle:
    
    sec = sector(Point(0, 0), SA, EA)
    x1, y1 = sec.exterior.xy

    fig2.add_trace(go.Scatter(x = np.array(x1), y = np.array(y1),  mode = "lines", fill = "toself",
                              line_color = "#b4b4b4", hoverinfo = "skip",
                              showlegend = False, name = " "))
    
    #----------------------------------------------------------------------------------------------------
    ## Calculate Centroids:
    
    A = (1**2)*np.radians(EA-SA)/2
    xx = ((1**3)*np.sin(np.radians(EA))/3) - ((1**3)*np.sin(np.radians(SA))/3)
    yy = ((1**3)*-1*np.cos(np.radians(EA))/3) - ((1**3)*-1*np.cos(np.radians(SA))/3)
    
    X = xx/A
    Y = yy/A
    
    fig2.add_trace(go.Scatter(x = [X], y = [Y],  mode = "markers", marker_color = "red", 
                              marker_symbol = "x", marker_size = 10,
                              showlegend = False, name = "Centroid",
                              hovertemplate='(%{x:.2f}, %{y:.2f})',
                              )
    )
    
    #----------------------------------------------------------------------------------------------------
    ## Update Layout:
     
    fig2.update_layout(
        title = "Area Centroid",
        title_x = 0.5,
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        template = "simple_white",
        # margin=dict(l=0, r=0, t=0, b=0),
        autosize = True,
        annotations = [go.layout.Annotation(
            dict(x=X+0.35, y=Y, xref="x", yref="y",
                text=f"({X:.2f}, {Y:.2f})", showarrow=False,
                axref="x", ayref='y', ax=X, ay=Y,
                bgcolor="white",
                )
        )],
    )
    fig2.update_xaxes(
        range = [-1.1, 1.1],
        zeroline = True,
    )
    fig2.update_yaxes(
        range = [-1.1, 1.1],
        scaleanchor = "x",
        scaleratio = 1,
        zeroline = True,
    )
    
    return fig2