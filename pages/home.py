import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc



dash.register_page(__name__, name = "Home", path = "/")





layout = dbc.Container([
    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ROW 1: Welcome Header:
    
    dbc.Row([
        
        dbc.Col(
            
            html.Div(
                "Welcome to the SWK211 web app!",
                style = {
                    "fontSize": "1.5rem", 
                    "family": "Arial",
                    "color": "black",
                    },
                
                className = "text-center font-weight-bold",
            ),
            
            xs = 12, sm = 12, md = 12, lg = 12, xl = 12, xxl = 12, 
        ),
        
    ]),


    #-------------------------------------------------------------------------------------------------------
    # ROW 2: Break Line
    
    
    dbc.Row([html.Br()]),
    

    #-------------------------------------------------------------------------------------------------------
    # ROW 3: Introduction from Study Guide
    
    dbc.Row([
        
        dbc.Col(xs = 0, sm = 1, md = 2, lg = 3, xl = 3, xxl = 3),
        
        dbc.Col(
            
            html.Div([
                
                "The general objective of this module is to emphasise an ",
                html.Strong("understanding"),                
                ", rather than memorising, of the ",
                html.Strong("principles governing statics"),
                " in order to stimulate ",
                html.Strong("creative thinking"),
                " and ",
                html.Strong("innovative thinking skills"),
                ". A problem-driven approach to learning is followed. Student-centred and co-operative learning and teaching methods are applied during lectures and tutorial classes in order to optimally develop the above skills, as well as to stimulate the development of communication skills, interpersonal skills and group dynamics.",
                
                html.Br(),html.Br(),
                
                "The effective use and application of mechanics are essential to the practice of civil engineering. During the course of this module, skills are developed that will enable the student to understand the fundamental behavioural concepts that civil engineers use to design infrastructure that is economic, safe and serviceable.",
                
                html.Br(),html.Br(),
                
                "This module follows on Mechanics SWK122 that the student should have completed last year. The aim of this module is to deepen understanding of mechanics to ensure that students have adequate background knowledge and understanding to prepare them for the 3rd year Civil engineering modules in the different fields within Civil Engineering.",
                
                html.Br(),
                
                "~ Prof E. Kearsley"
                
                ],
                

                style = {
                    "fontSize": "1rem", 
                    "family": "Arial",
                    "color": "black",
                    "textAlign": "justify"
                    },
                
                # className = "",
            ),
            
            xs = 12, sm = 10, md = 8, lg = 6, xl = 6, xxl = 6, 
        ),
        
        dbc.Col(xs = 0, sm = 1, md = 2, lg = 3, xl = 3, xxl = 3),
        
    ]),
    
    #-------------------------------------------------------------------------------------------------------
    # ROW 4: Break Line
    
    
    dbc.Row([html.Br()]),
    

    #-------------------------------------------------------------------------------------------------------
    # ROW 5: Built by Jurie Adendorff
    
    dbc.Row([
        
        dbc.Col(xs = 0, sm = 1, md = 2, lg = 3, xl = 3, xxl = 3),
        
        dbc.Col(
            
            html.Div([
                
                "Built by Jurie Adendorff"
                
                ],
                
                style = {
                    "fontSize": "1rem", 
                    "family": "Arial",
                    "color": "black",
                    "textAlign": "left"
                    },
                
                # className = "",
            ),
            
            xs = 12, sm = 10, md = 8, lg = 6, xl = 6, xxl = 6, 
        ),
        
        dbc.Col(xs = 0, sm = 1, md = 2, lg = 3, xl = 3, xxl = 3),
        
    ]),
    
    
    
    
    
    
], fluid = True,)