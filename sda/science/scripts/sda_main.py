# -*- coding: utf-8 -*-

# future import statements
from __future__ import print_function
from __future__ import division

# version information
__project__ = "EXPLORE"
__author__  = "ACRI-ST"
__modifiers__ = '$Author: N. Cox $'
__date__ = '$Date: 2021-10-12 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

from dash import dcc
from dash import html
#import dash_core_components as dcc
#import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#from flask_caching import Cache

import globals

from sda import sda
#from cube_cut import cube_cut
#from load_cube import load_cube
#from reddening import reddening

from tab3d import *
from tab3i import *

""" main figure layout """

layout=html.Div([
    dcc.Store(id='store-lab', storage_type='session'),
    dcc.Store(id='1d-data-store', storage_type='session'),
    dcc.Store(id='signal'),
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Pre("v1.0"),
            dcc.Link(
                html.Img(
                    src=sda.get_asset_url('gtomo_text.png'),
                    style={
                        'width':'100px',
                        'height':'auto',
                        'float':'left'
                    },
                ),
                href='https://explore-platform.eu',
                style={'display':'inline-block', 'height':'80px'},
            ),                 
            html.H3("EXPLORE: G-Tomo", 
                style={'display':'inline-block','height':'80px','float':'center','marginLeft':'100px', 'marginRight':'100px', 'paddingTop':'15px'},
            ),
            html.Div([
                dcc.Dropdown(
                    id='cube-dropdown',
                    options=[
                        {'label':'Resolution 25pc (sampling: 10pc - extend: 3 kpc)', 'value': 'cube1'},
                        {'label':'Resolution 50pc (sampling: 20pc - extend: 5 kpc)', 'value': 'cube2'},
                        #{'label':'Cube 3 - Best of both', 'value': 'cube3'},
                    ],
                    value='cube2',
                    clearable=False,
                    style={'width':'400px', 'fontSize':'12px', 'paddingTop':'10px'},
                ),
                #html.Pre("selected cube: "),
                html.Div(id='cubeselection'),
            ], style={'display':'inline-block', 'height':'80px', 'float':'right', 'marginLeft':'200px'}),
        ], style={'width':'100%', 'display':'flex', 'justifyContent':'center'}),
        html.Div([
            dcc.Tabs(
                id='tabs', 
                value='None', 
                children=[
                    dcc.Tab(label='3D Visualisor and Slicer', value='tab-4'),
                    dcc.Tab(label='Information', value='tab-3'),
                ],
            ),       
        ]),
        dcc.Loading(
            id='load-tab',
            type='circle',
            fullscreen=False,
            children=[
                html.Div(
                        id='tabs-content', style={'width': '100%', 'float': 'left'},
                        children=[],
                ),
            ],
        ),
    ]),
    html.Div(
    id='funder',
    children=[
        html.Img(
            src=sda.get_asset_url('flag_yellow_low.jpg'),
            style={
                'width':'75px',
                'height':'auto',
                'float':'left',
                'marginRight':'20px'
            },
        ),
        html.Br(),
        html.Pre("EXPLORE. This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 101004214."),
    ], style={'width':'100%', 'float':'left', 'marginTop':'20px'}),
    dcc.Store(id='vis-status')
])


@sda.callback(
    [Output('tabs-content', 'children')],
    [Input('tabs', 'value')], [State('store-lab', 'data')]
)
def update_tab(tab, store_lab):

    #print('store content', store_lab)

    if tab == 'None':
        raise PreventUpdate

    if tab == 'tab-3':
        tab_content = html.Div([
                            content_info(),
                        ], id='3d')
    elif tab == 'tab-4':
    	tab_content = html.Div([
                            content_3d(),
                        ], id='4d')

    return [tab_content]


@sda.callback(
    [Output('cubeselection', 'children')],
    [Input('cube-dropdown', 'value')]
)
def load_cube(cubename):
    
    ctx = dash.callback_context

    if ctx.triggered:
        globals.initialise(cubename)

    if cubename == 'cube1':
        selectedcube = "Cube: Resolution 25pc (sampling: 10pc - extend: 3 kpc)"
    if cubename == 'cube2':
        selectedcube = "Cube: Resolution 50pc (sampling: 20pc - extend: 5 kpc)"

    return [html.Div(html.Pre(selectedcube))]

sda.clientside_callback(
    """
    function eventListener(n_clicks) {
        window.addEventListener('message',function(event) {
            console.log("handle event from parent", event);
        },false);
        return '';
    }
    """,
    [Output("vis-status", "data")],
    [Input("4d", "n_clicks")]
)
