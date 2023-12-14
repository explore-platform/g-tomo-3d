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

#import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash import html

import globals
from sda import sda

def content_info():
    content_info = html.Div([
        html.Div([
            html.H5('References and additional information to use the dust extinction cubes'),
            dcc.Markdown('''            
            Details on the 3d dust map reconstruction are given in 
            [Lallement et al. 2022](https://arxiv.org/abs/2203.01627) and [Vergely et al. 2022](https://arxiv.org/abs/2205.09087)

            #### Available 3d dust extinction maps (from Lallement et al. 2022)

            Extent of the map is the distance from the center (Sun) to the edge of the map (in the galactic plane).
            For all cubes the height is 400 pc above and below the galactic plane.

            **Highest resolution**

            This 3d map is recommended for users interested in detailed structures in the galactic 
            dust distribution relative close to the Sun.

            * Extent: 3 kpc
            * Sampling: 10 pc
            * Resolution: 25 pc
            * Size: 6 x 6 x 0.8 kpc

            **Largest distance**

            This 3d map is recommend for users interested primarily in larger structures in the 
            galactic dust distribution traced to further distances from the Sun.

            * Extent: 5 kpc
            * Sampling: 20 pc
            * Resolution: 50 pc
            * Size: 10 x 10 x 0.8 kpc


            #### 3D Visualiasation and slicing


            #### Acknowledgements

            If you use data from this tool we kindly ask you to include a reference to Lallement et al. 2022, ArXiv:2203.01627.
            And include an acknowledgement to the EXPLORE project:

            ***This research has used data, tools or materials developed as part of the EXPLORE 
                    project that has received funding from the European Union’s Horizon 2020 
                    research and innovation programme under grant agreement No 101004214.***

            '''),
            #html.Br(),
            html.Hr(),
            #html.H6("This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101004214."),
            #html.Br(),
            # dcc.Link(
            #     html.Img(
            #         src=sda.get_asset_url('flag_yellow_low.jpg'),
            #         style={
            #             'width':'100px',
            #             'height':'auto',
            #             'float':'left'
            #         },
            #     ),
            #     href='https://explore-platform.eu',
            # ),                 

        ], style={'width':'100%', 'display':'inline-block', 'margin':'5px', 'padding':'50px'} ),
    ])

    return content_info

