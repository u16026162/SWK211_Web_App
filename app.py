import dash
from dash import html, dcc
import dash_bootstrap_components as dbc





#################################################################################
# APP:

app = dash.Dash(
    
    __name__,
    
    external_stylesheets = [
        dbc.themes.CERULEAN
    ],
    
    title = "SWK211",
    
    use_pages = True
    
)




#################################################################################
# NAVBAR:

Navbar = dbc.Nav([
    
    dbc.NavLink(html.Div("Home", className = "ms-2"),        href = "/",            active = "exact"),    
    dbc.NavLink(html.Div("Centroids", className = "ms-2"),   href = "/centroids",   active = "exact"),    
    dbc.NavLink(html.Div("Deflections", className = "ms-2"), href = "/deflections", active = "exact"),    
    dbc.NavLink(html.Div("Friction", className = "ms-2"),    href = "/friction",    active = "exact"),    
    dbc.NavLink(html.Div("Cables", className = "ms-2"),      href = "/cables",      active = "exact"),
    dbc.NavLink(html.Div("Vibrations", className = "ms-2"),  href = "/vibrations",  active = "exact"),
    dbc.NavLink(html.Div("Resonance", className = "ms-2"),   href = "/resonance",   active = "exact"),
    
    ],
    
    vertical = False,
    pills = True,
    className = "nav-justified"
    
)




#################################################################################
# LAYOUT:


app.layout = dbc.Container([
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Main Header:
    
    ## Heading:
    dbc.Row([
        
        dbc.Col(
            
            html.Div(
                "SWK211",
                style = {
                    "fontSize": "2.5rem", 
                    "family": "Arial",
                    "color": "black",
                    },
                
                className = "text-center font-weight-bold",
            ),
            
            xs = 12, sm = 12, md = 12, lg = 12, xl = 12, xxl = 12, 
        ),
        
    ]),
    
    
    ## Links:
    dbc.Row([
        
        dbc.Col(
            
            Navbar,
            
            xs = 12, sm = 12, md = 12, lg = 12, xl = 12, xxl = 12
        ),
        
        
    ]),
    
    # Line
    dbc.Row([
        dbc.Col(
            
            html.Hr(
                style = {"height": "2px", "color": "black", "border": "none", "backgroundColor": "black"}
            ),
            
            xs = 12, sm = 12, md = 12, lg = 12, xl = 12, xxl = 12
        ),
    ]),
    
    # dbc.Row([
    #     html.Div(i for i in dash.page_registry.values())
    # ]),
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Content of each page:
    
    dbc.Row([
        dbc.Col(
            dcc.Loading(dash.page_container, type = "circle"),
            xs = 12, sm = 12, md = 12, lg = 12, xl = 12, xxl = 12
        ),
    ]),
        
        
], fluid = True,)








#################################################################################
# RUN APP:



if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8050)


















