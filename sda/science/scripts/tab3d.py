# -*- coding: utf-8 -*-

# future import statements
from __future__ import print_function
from __future__ import division
from astropy.coordinates.sky_coordinate import SkyCoord

# version information
__project__ = "EXPLORE"
__author__ = "ACRI-ST"
__modifiers__ = '$Author: N. Cox $'
__date__ = '$Date: 2021-10-12 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

import os
import io
import base64
import datetime
import sys
from collections import OrderedDict
import pandas as pd

import astropy.units as u
import numpy as np

import dash
# import dash_table
# import dash_html_components as html
# import dash_core_components as dcc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from load_cube import load_cube
from load_downsampled_cube import load_downsampled_cube

import plotly.graph_objects as go
import flask

import globals

from sda import sda
# from cube_cut import cube_cut
# from load_cube import load_cube
from cube import sub_cube as subcube

""" functions """

""" creat figure to display a 3d data set (volume rendered)
"""

#VIS_CONFIG = "NobwRAzgrgDjD2AnALhAggOw-ZBDZAlvBhGAFwBmuANhAKYA0YARlMssQJIAm5LyGALQA3eNSgBbOhjBNhBCABUCyanT4AKAIwBKAAQA1MZOl6NADwZ6AnlYBeV4TSh19AEXy56yMgGMozHQA+tyeAHS+EMKyYBK4cAQYAObkoGC+ABa4WHTUfOaCaOYKMdS4gXlkYOYxoXjI1jDqVRiSgYgxFATUyHSIbgrlaryUNPRMGQTc3NIAwlk5lVS0jGAKs2JIAGIEuSPL42CIdHEJyQMQQ3T7Y3QAvgzgmdkYuXzWhcWkTGUV77WeBpNPitCTtTrdXr9QbMYbkA6rSbTOYLV5LW5MdabRA7PbwjFHE7xGCJJIXK43FYPJ6ot5VOyfEo-cp0sB2AH1RrNMCg8FMLo9Prk2HXfErCZTGYYeYvOkIzEQDbUba7aiUw7HU4k84wuGjKmPdK0ypgJzidTMv5VM0uDn4Lkgtp9CGC6GXEXqxGSlGy9HitaK7G4tVijVEs5k3Wi-X0O4AXSYuCSSWOSXwRGlxC6KTIaS6ewAcrgpPkwNSwPm1UWS1VrGXDZXuNXuezy43m3wbep40wODByAAmH50CjIchaJgAdymyAy5AALABOCZ0AhJDJjsiLgDsTDsnAwMxqVQAzDEIEhkAAhOtkcC-VkxLy+aTcUnkZCIFwPANXteh1YFAAWUSAgJAIOxo3lMA6i8OhkGbUhc3SAJglgiIojABMwGnQ94EnHhOwUKAaAg9NiEELQYnkCBCKqKi5AUABlDhjnIcA8AgABrOiwAADkXedcG4XwB2YQQAAZmAHLRBHnaSAFZBEXa5ZIk7cTwANhkvitG3RcKAYmDPDo4AwBk3xNP0yzBF8BSFO4OSKHnWSd2YTTBE0iTF2YPiT23bcFN8LQJKwphfCzf87xQwIggFbk6HMGBlWOIJ-FiqUIBUawgi7CAggkhSJJgXxcq0MIMgUmJEFwPhQqYGZfDq2oFDwDAX2a8LUJCVrsg6qoitCn8aCSJAVAyCReMK7SFL83BBBPXABz4py6G3QRcE0ndBG4E8tG4RdcAUw6+IoM8f1g7wDzfF8kOALRsMSKFcF8QhiEUB0qgFKEYhgXAUAIGgAAk1wyahQcIZIQRwNBXoIYQLViKAegIZK6CvL8IEmZJYcIJxehGT8XH5SE+gAeWYAArOhXru7DYJ2V13xjVZmExjINjBRI6DJpoatYvg0ALNwYgUDGoCx+Yaa45h4HMXH4fwKCCRevG6CY3IabemRot8Gg1EQAwFGuxLxyYeg1Fe64PDwHg6d7f6knghXiD4UCx0TOH8eV-1vr6e3IEvG8OyqO1GahAO2YljIbdq3NsOfV9maJ1YLa164ihKeOmC1Zm0meRZ8kZb4wAfE0agawFPp5J0OhJ11hT1aCkSlGVC5ZhUlRVPEO8JXOdXdJvbnLAu0XeYvShZE060rzlgRaWuXShRufcOFufXb6CsRS4NPSYTViVJFfPRH40+AZTOS7L8+7SBbleWdevl6jPewHX6Uz977fu5DXuD4jY+AFT6+k7M4RG19rRgNvtXB+dcKykzdBSACEpkQfxAV-QMO9VSv3-tqSMg9V73Hpp4bwGtLYEztuxH8NEADq40CzwFjsg387Mpa+BlnLBW3tX5pyttwAASvha6BBbqpDjMNOGrsqi+GOErI2pByzQDgJedAWAcDkRIMw1g7AuAjH4EICKGAOBQEQAABWVMgAc3BcoDmogoZQqhuQaAHPoDYRj4AmL0OYnAVi9DCAHGYSwNhHBgPcCQ+CZAIDgxfCEcIkRog50PlDXMNJ0HVAnpaVkFdjJz3vovJ+QoX7MPfm3MeGCu44mwcw3BR8iks2Ae3MAHxL6TytE06B88a5gkfvAhudTm7ejQZvAk39Kk92gjUgeSD6mGlHqyAwUDMkmi7B0vJ3S4F+0QR6YpgzSlyhGZgn+ODwx4MAfUhOyZUwaLcdmVI4B2zFm5DUNs2CQ7tJeYWR5oDzRlmwn2Qcw5RzkAUhOHCM45xkCXCuCG5Adx7hNsecy54g63nvFPPgT4IAvkPMnL89wFR-hzFvCAIEMBgQgoQ2ecEEKPLupAaJaE4mYWwrhbgQi9E0RIuDOwGjBC2MYrRPR-LTTMVYs0DiXgeJ6NCHxOyRV5yCDoFoEFTkVLKW3FoOgclcAni0nxYS3ABzziqlS0yYBNJaF8Lq7cB1BAOU0r4OSfEFLrWYNuCSJ5bIvgkhQAc25rgDgHBQMK6RIo5nvMQIIY0cxgHqqXfAUbEBRVjS1CAyBE3JqMsqDAQRsCIAkJ1eN6a80FqqENRM1BRpJtnJNPRPlyi4FlUpLQ85NLzXnBJS1ylygrQoNuCgmlmCbToFtbg856w5OpcI0RuYJKPSMX0VWGYPqdM2b9f6hBgag3BuuSGMbsDIC4YjCQyNCBo3FljUkXClaEzxQUxAFNqa0zEVS8OfRmbQSjpLeAXNXi80XQLKoQsRYEtYRkaWst5ZexvcwpdCMyFawzOxdI+s+jyIRQCyAms+Gx0odnMAeBEBO0PZInWawyUezAHBmDvdNkBwvCgYOXzQ6voQZHdmTD8OJxxcklO5tsMExafh-uOZ86f3SS0pZpYqV30dOspehSCGvxKZ-YlFTd7VJObUpTQDZnieaV8VprIZ6TtkwveT96zkDNQXsv0hxRkab-lpqZ2yZmpMaQsn5UnIFedMzA-JvTn46d7ip9BamgxVKcyJqzw9iGcXgghvheGQDUIUHQ2cDDOPEovRzcD7DIPXoJsw3hBNBEERxTO4A4jPbaz4DIugciSjxiAA"
VIS_CONFIG = "NobwRAhgxgLglgewHZgFxgGZwKYBsAmAyntrIkgKoAO+EM2YANGLTBGqJjgQHIQC2DdAA8mLOhADO2GAEkk+bKPQAGMAF9G4LHnx9BaMAE8xrKTPmLlYNZu3c9AoWABepidLkKlh21q66+s4AbhC4AK4MzGaelj6qGgC6dpBkyIY6BMS4pPDI1KxR4mwc9oFOhqLRHhbe1gCMGv6ZjgboJtVssXWGjSktQYahEUUxtVa9SSmS4VRUCABOMJIAgkhICGx5SJJoMAuRzABG4TAwyLL4hkcwSAC0UMjn4QsACribAEz4APrBn2JgnBJAAVOAwHKGAAUnwAlAACADCTwQL3h7y++Hh-3hUOEjHhRgJw0iCIAIjUYKhJLg4FBsD8zAA6KCSYJifgQOZwJAAc1KYCgAAsIOs8JU7ithMCxLgIEdxSJ3FsjFRnEhwvwFQsxFhcPQFmTgfKcldUBgwtJmEK4PhFEhESKxbg0BbcFawMDkR8FgAxByuy3YZgLbCc7l8o2SE3YM1u6QpYWipCK4yS6W7ZhyhUu9rKuiq9Wa7W6uD67CG41HU2B93BsA2u3YB1OlO5+P1r0IH3+3S1j2h8NUHm8qMxuNBxOt1MANTCkVl8tTJNGEhghcMGq1FdL5cr0ersf79cb9sdycVHeYXZ7AfNQZDYa5w8jVZr97r6kSzAgvN5od5OhyGRJAsH5VBOAGColX6BxBjzWDyjaMAVySZhzioNAVCzbAMBgNAAFZ6mYAB3W0YCFNAABYAE5rWwOBeSFfDUAAdmI1w4msAFmEkRYYAAIRMVBwGzVMxCkekFBHPYDmwTRPUkATGOPa9JAAWR5OB+DgFwjw-D0xhgIJdggsAaTpBlmVZdlvzAMiFAQEjLiGYFwjCXSgOQO4eJQ4EXPQXygUkQhzlDNBwC6ABrALgDAI4VFYgA2bAks+Ai7ggGiqPwO4qKI+o7gADlYjAqLufAMCKz5WJUDAaJUCAiLAOyzFi4B6kSOzHlAlSINE5AfkWPqbEXGAhoWEa1GiYFxuG8CwEaLNBo2BZ+F8MaflW9aEi-H9cF5YaKP4WKwBoo55QgIqoAy+oqKSiA8pUeooDuGj5SKu4MFKpKLpSpKaPwKiWs6cxlg4YAuoUozLEs0yOrsnkDWgbYQQ3dA9QNMQqAgJY4DCAAJRihVpJj4D5TdNhWMhgiKfhwn1OAqByASDkkG0+Wp+BQnoM19kOLg9wAeSOAArXJ4daiR-T3GSDPrI42aFZEtR5bAhbVBY6EWQwVh4MkxGBVnwnZx1SCio4EGELm4B5-Sr1SbnsGyXJyAiwUwhyBYZ38npUE+XiSFgWMKTYS5JfQ3HeRkG30nQLT8J-Gm6Hth9BYNCPzP4oT4LAfMZYzjg7MVk2hVD9gILsyTm3wOX+fraQcmD-ApRlSvmCHOXOCTZ0JVbzMwDE3MwCqYoCzVTdix3ZhMYrMdDwnOtrVtM9p3bNOb0WXsCFUsBB2fEd5-fDspwvYejHTGUsyXc-83XCf0C3EsZ7LA0j9TpeGxX5tz17+W1O9FvO8Dt94RlHG+D+CZ-A9zbIYOcIxFw5iGPOVcKoH5gCftPdOc8IGLw9KeH+a9d6bz9MAtOoCXzgIPMfScUsugyBds3cOEUFLBQAOrgiFDwBA5diFKSVmbKAFsrY2ztnghuQdeYACUnKw3pJLBSKM3boCgKGFOPtdjTFmPMJYqx1ibC8jsXeJwzgXDNPFW4dxgjdk1M2QEwIwQQmcFCeoCIZw2MEEgXE+JCQEhcMSFB5JKSoCgOEBUjIJAsjZByA+FN+qCiISIS+A8h6VDvujDBU8dQvz3O-cRy8mwtjPnwwBpC+z-z3k+MBeTjynz-mmfuiDUwdDHvfIs25snYP3OOXeBCil-wdiQ7e+TKmd1fNQyB8loGJNcMkppw83CgzaZPDpu4364N6d-fpsCKlDLIZ-Chh8NnyzqTslCKD5nIIQUsjJmDOmz26QvTZhTf47MGZIUpwzd6HPGT0k5Vc-wAUMSBMCAooLIVEIhXg0FjBNDKNC5CbgoWtBCBcvaYAMJYRwnhLF9lyKUVQEReixMWLsWYC4LihgADMYg+JLCEu7VJ6AJKSCkrXOJ9cFJGz6u8zSSBtK6UmaDTwJkOCCjCVZSJNkQZ4scs5cxwV3K0hcIYu4S0-KSACotexIUwpCEilIGKZo4oESOFS+oCpKo+WqjRPKaUMpHCgEccqrFFBUqShgAi2AipUSgEVGVbVjXABUF1ZgPVQXxNCeEvUzglDM0WAyKNVlmySHBEYP4KDJA-BUARFQVAoB-HqEyIUBExBaw2tEUgFaWCzVFPSatSbGS1qQPW9A9QVAdrQpAA6R0hQnWNTYAi9qipUseqOz4n0qIYGwKxTKANZ34HNfgd6BF3pFQwDSuhYN4aQ2SMK8YcMOAhuvEgZGaQkBo3QQ87GuN4CE2JqTZicsMFUxpnTBm8BmbYGNuzEcoiU58zkjkg0ItxawEzmYAuFY5YOxLqbBAqsUwawrNrHU6A9YGzUj+5WQpzaW2tsnXmu8lG00Ydsd2UBPYVg0ZS1AHFG65BDhIZh7cMVRxjuewwCcJKEaFV0zOdLBJGFzvnV+FZM5wbLhIIuP5WU1zrkB8ykjYyNNY2M8C3cZnCDmdfJBSobnoLuWsnBEyRl9NeZeDeHzuxAPKSAqplCaknOmcU9oOnB430MC0swyzH5ZOM48mhn9zOJPeZ8-ZA4HNHNM7Ulz9SXDuaZa4dJhn-PAZM38h2IXXNhZs2UneFSflUMy5OOLZzUK6eXBcgz7Tn5dKc1lrZFn16fz2XZ8hUXflPP+fumAZHYwsZAKw4EHCKLcN4bs-hpdBHCII9zADu8GPNxkc5aS8ii6KM4yotR9ANFJCAA"
#link: http://localhost:20000/#compressed=true&hideLegend=true&workflowAnnotationDisplay=annotation&config=NobwRAhgxgLglgewHZgFxgGZwKYBsAmAyntrIkgKoAO+EM2YANGLTBGqJjgQHIQC2DdAA8mLOhADO2GAEkk+bKPQAGMAF9G4LHnx9BaMAE8xrKTPmLlYNZu3c9AoWABepidLkKlh21q66+s4AbhC4AK4MzGaelj6qGgC6dpBkyIY6BMS4pPDI1KxR4mwc9oFOhqLRHhbe1gCMGv6ZjgboJtVssXWGjSktQYahEUUxtVa9SSmS4VRUCABOMJIAgkhICGx5SJJoMAuRzABG4TAwyLL4hkcwSAC0UMjn4QsACribAEz4APrBn2JgnBJAAVOAwHKGAAUnwAlAACADCTwQL3h7y++Hh-3hUOEjHhRgJw0iCIAIjUYKhJLg4FBsD8zAA6KCSYJifgQOZwJAAc1KYCgAAsIOs8JU7ithMCxLgIEdxSJ3FsjFRnEhwvwFQsxFhcPQFmTgfKcldUBgwtJmEK4PhFEhESKxbg0BbcFawMDkR8FgAxByuy3YZgLbCc7l8o2SE3YM1u6QpYWipCK4yS6W7ZhyhUu9rKuiq9Wa7W6uD67CG41HU2B93BsA2u3YB1OlO5+P1r0IH3+3S1j2h8NUHm8qMxuNBxOt1MANTCkVl8tTJNGEhghcMGq1FdL5cr0ersf79cb9sdycVHeYXZ7AfNQZDYa5w8jVZr97r6kSzAgvN5od5OhyGRJAsH5VBOAGColX6BxBjzWDyjaMAVySZhzioNAVCzbAMBgNAAFZ6mYAB3W0YCFNAABYAE5rWwOBeSFfDUAAdmI1w4msAFmEkRYYAAIRMVBwGzVMxCkekFBHPYDmwTRPUkATGOPa9JAAWR5OB+DgFwjw-D0xhgIJdggsAaTpBlmVZdlvzAMiFAQEjLiGYFwjCXSgOQO4eJQ4EXPQXygUkQhzlDNBwC6ABrALgDAI4VFYgA2bAks+Ai7ggGiqPwO4qKI+o7gADlYjAqLufAMCKz5WJUDAaJUCAiLAOyzFi4B6kSOzHlAlSINE5AfkWPqbEXGAhoWEa1GiYFxuG8CwEaLNBo2BZ+F8MaflW9aEi-H9cF5YaKP4WKwBoo55QgIqoAy+oqKSiA8pUeooDuGj5SKu4MFKpKLpSpKaPwKiWs6cxlg4YAuoUozLEs0yOrsnkDWgbYQQ3dA9QNMQqAgJY4DCAAJRihVpJj4D5TdNhWMhgiKfhwn1OAqByASDkkG0+Wp+BQnoM19kOLg9wAeSOAArXJ4daiR-T3GSDPrI42aFZEtR5bAhbVBY6EWQwVh4MkxGBVnwnZx1SCio4EGELm4B5-Sr1SbnsGyXJyAiwUwhyBYZ38npUE+XiSFgWMKTYS5JfQ3HeRkG30nQLT8J-Gm6Hth9BYNCPzP4oT4LAfMZYzjg7MVk2hVD9gILsyTm3wOX+fraQcmD-ApRlSvmCHOXOCTZ0JVbzMwDE3MwCqYoCzVTdix3ZhMYrMdDwnOtrVtM9p3bNOb0WXsCFUsBB2fEd5-fDspwvYejHTGUsyXc-83XCf0C3EsZ7LA0j9TpeGxX5tz17+W1O9FvO8Dt94RlHG+D+CZ-A9zbIYOcIxFw5iGPOVcKoH5gCftPdOc8IGLw9KeH+a9d6bz9MAtOoCXzgIPMfScUsugyBds3cOEUFLBQAOrgiFDwBA5diFKSVmbKAFsrY2ztnghuQdeYACUnKw3pJLBSKM3boCgKGFOPtdjTFmPMJYqx1ibC8jsXeJwzgXDNPFW4dxgjdk1M2QEwIwQQmcFCeoCIZw2MEEgXE+JCQEhcMSFB5JKSoCgOEBUjIJAsjZByA+FN+qCiISIS+A8h6VDvujDBU8dQvz3O-cRy8mwtjPnwwBpC+z-z3k+MBeTjynz-mmfuiDUwdDHvfIs25snYP3OOXeBCil-wdiQ7e+TKmd1fNQyB8loGJNcMkppw83CgzaZPDpu4364N6d-fpsCKlDLIZ-Chh8NnyzqTslCKD5nIIQUsjJmDOmz26QvTZhTf47MGZIUpwzd6HPGT0k5Vc-wAUMSBMCAooLIVEIhXg0FjBNDKNC5CbgoWtBCBcvaYAMJYRwnhLF9lyKUVQEReixMWLsWYC4LihgADMYg+JLCEu7VJ6AJKSCkrXOJ9cFJGz6u8zSSBtK6UmaDTwJkOCCjCVZSJNkQZ4scs5cxwV3K0hcIYu4S0-KSACotexIUwpCEilIGKZo4oESOFS+oCpKo+WqjRPKaUMpHCgEccqrFFBUqShgAi2AipUSgEVGVbVjXABUF1ZgPVQXxNCeEvUzglDM0WAyKNVlmySHBEYP4KDJA-BUARFQVAoB-HqEyIUBExBaw2tEUgFaWCzVFPSatSbGS1qQPW9A9QVAdrQpAA6R0hQnWNTYAi9qipUseqOz4n0qIYGwKxTKANZ34HNfgd6BF3pFQwDSuhYN4aQ2SMK8YcMOAhuvEgZGaQkBo3QQ87GuN4CE2JqTZicsMFUxpnTBm8BmbYGNuzEcoiU58zkjkg0ItxawEzmYAuFY5YOxLqbBAqsUwawrNrHU6A9YGzUj+5WQpzaW2tsnXmu8lG00Ydsd2UBPYVg0ZS1AHFG65BDhIZh7cMVRxjuewwCcJKEaFV0zOdLBJGFzvnV+FZM5wbLhIIuP5WU1zrkB8ykjYyNNY2M8C3cZnCDmdfJBSobnoLuWsnBEyRl9NeZeDeHzuxAPKSAqplCaknOmcU9oOnB430MC0swyzH5ZOM48mhn9zOJPeZ8-ZA4HNHNM7Ulz9SXDuaZa4dJhn-PAZM38h2IXXNhZs2UneFSflUMy5OOLZzUK6eXBcgz7Tn5dKc1lrZFn16fz2XZ8hUXflPP+fumAZHYwsZAKw4EHCKLcN4bs-hpdBHCII9zADu8GPNxkc5aS8ii6KM4yotR9ANFJCAA
def create_3d_plot(cube, axes):
    import plotly.graph_objects as go
    import numpy as np

    err_message = ""

    if (cube.size > 2e8):  ## too big/small??
        err_message = "size of cube too large!"
        return

        # values=np.log10(cube.flatten())
    values = cube.flatten()

    X, Y, Z = np.meshgrid(axes[0], axes[1], axes[2])  # original too large. needs sub-cube!

    # x,y=np.meshgrid(sub_axes[0],sub_axes[1])
    # z=np.zeros(x.shape)

    # tune "opacityscale" is "uniform", "extremes", "min", "max"
    # possible to use custom opacity scale, as "opacityscale=[[-0.5,1], [-0.2,0], [0.2,0], [0.5, 1]]"
    # mapping scalar values to relative opacity values (between 0 and 1) the max opacity is given by
    # opacity keyword. Can be used to make some ranges completely transparent
    caps_on = False

    # enable/disable caps (color coded surfaces on the sides of the visualisation domain):
    if caps_on == True:
        caps = dict(x_show=True, y_show=True, z_show=True, x_fill=1)
    else:
        caps = dict(x_show=False, y_show=False, z_show=False)

    layout3d = go.Layout(
        autosize=False,
        width=800,
        height=1000,
        # margin=go.layout.Margin(
        #     l=10,
        #     r=10,
        #     b=10,
        #     t=10,
        #     pad=4,
        # )
    )

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values,
        # isomin=np.nanmin(values),
        # isomax=1.1*np.nanmax(values),
        opacity=0.1,
        opacityscale="uniform",
        caps=caps,
        surface_count=30,
        # surface=[1,30],
        colorscale='Plasma',  # RdBu
    ),
        layout=layout3d,
    )
    return fig, err_message


# values3d=sub_cube
# X,Y,Z=np.meshgrid(axes[0],axes[1],axes[2])

# X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
# values3d = np.sin(X*Y*Z) / (X*Y*Z) #will sub cube

# # enable/disable caps (color coded surfaces on the sides of the visualisation domain):
caps_on = True
if caps_on == True:
    caps = dict(x_show=True, y_show=True, z_show=True, x_fill=1)
else:
    caps = dict(x_show=False, y_show=False, z_show=False)

fig3d = go.Figure(data=go.Volume(
    # x=X.flatten(),
    # y=Y.flatten(),
    # z=Z.flatten(),
    # value=values3d.flatten(),
    isomin=0.1,
    isomax=0.8,
    opacity=0.1,
    opacityscale="uniform",
    caps=caps,
    surface_count=17,
    colorscale='RdBu'
),
)


def content_3d():
    content_3d = html.Div([
        html.Div([
            html.Div([
                html.H5('Select subcube'),
                html.Label('Enter Ra-Dec-Distance (galactic) and cube size', style={'marginLeft': '10px'}),
                html.Br(),
                dcc.Input(id='3d-ra', type='number', placeholder="Ra [-360..+360] deg", size='15'),
                html.Br(),
                dcc.Input(id='3d-dec', type='number', placeholder="Dec [-90..+90] deg", size='15'),
                html.Br(),
                dcc.Input(id='3d-distance', type='number', placeholder="Distance [pc]", size='15'),
                html.Br(),
                dcc.Input(id='distance-cube', type='number', placeholder="Cube size [pc]", size='15'),
                html.Br(),
                html.Button(id='3d-get-cube', n_clicks=0, children='Extract Cube', style={'marginLeft': '10px'}),
            ], style={'padding': '5px', 'borderWidth': '2px'}),
            #
        ], style={'width': '15%', 'display': 'inline-block', 'margin': '5px'}),
        #
        html.Div([

            html.Div(id='temp3'),
            html.Div([
                # html.H6("Extinction cube at x,y,z"),
            ], id='cube-coord'),
            # dcc.Graph(id='3d-graph', figure=fig3d, config={"doubleClick": "reset"}),
            html.Div([
                # TODO read path prefix -> sda! echo in docker, print in python of path prefix see if it gets lost in python, then problem with virutual env
                # html.Iframe(src="http://localhost:8015/sda/vis/#compressed=true&presentationMode=true&integrationMode=true&hideLegend=true&config=NobwRAzgrgDjD2AnALhAggOw-ZBDZAlvBhGAFwBmuANhAKYA0YARlMssQJIAm5LyGALQBjYhyiIACtRwAmXkwBuBCABUCyanT4AKWQEoABAGEx8CYelzuhnQA8GhgJ6OAXo8U0odIwBF8uPTIZBC4ALYwWgB0whCKYExhuHAEGADm5KBgwgAWuFh01Hx2gmh2Kglg1LjMhcWV3AHITjDaZGAYUGG1iJUUBNTIdIi+KjVavJQ09Ew5BNzcdBjGeQVFU7SMYCqmMogAYgSFk1SbTIh0SSnpo6HME+Sn9AC+DOC5+Rh17U6l5aRMaq1dZgJwNJotNodLo9PoDIYjMb3OgnaZbOYLJYrT7fJ5bHbwPaHY6PNHnS7JGCpNK3cYo0mbV7vVZfEGuP4VQE1b5gVzgvDNVp8TrdYZwwbDWnI1FnMAYxbLFm4snbCC7JDE6gymZgC5XKk3JEPDYvN7ZJUgzzUbyVIE8q02piNAWQ4UwsVMfoSxF3Y142bzBXYtYMnUEolHLWhrZ6ynUqV+tHPAC6TFwaTSFzS+CIy2I-QyZCy-WOADlwlC7GAmWAS1ry2EoWCa3XuA2oXyW5G2xW+A7tCmmBwYOQAAyAugUZDkACsAGYmAB3ebIHLkAAsAHZZnQCGkctOyABGUfj3mcDCLKvtdeVCBIZAAITBZHAdpBlUCwiW3Gp5GQiDeK8qqPnu0ZMCoACyqQEGEBCuPSJpbM6gR0Mg7akEWqZgMul7wIuPB9ioUA0PBObEIIsiVMoECEe0VFKCoADKHAXOQIDAShQQXr+36YcAYCjmA2GpAiuDCIQxCqK67RegilQwLgKAEDQAASe45NQGmEOkwo4GgEkEIo2iJFAgwEJEdCPoBEBzOkBmEJ4QyTAB3ievCwwAPLMAAVnQEn8dhKGHN6f5IUwzA2TkpjdKkdCea0iD4EgfBoKWviVCo1lQLZKz+QA1sw8B2A5Rn4Ih-pgOJjl0ExhT+ZJGDsdkNBaIgABqKg8XQ16yEw9BaBJKL+HgPCBUOSlpGhpXEHwMHTmmhlORVKpycM42QA+z7tnw-K4CFCIbZFOU5CNuCZNhX4-mFrlbANDUomUFRYYkca6UWzI4iCJRPQCVTct9e2ClCIqwu53oJitsryliFrgaq6oHN28OxtcNJGlDpqfSGPwcn9758GCToQkK7Sgx6tYeT6dLauigaw198PhhqyPhbqFJo5DtM1h8OO8njtoA3wfLEy6pPQqKvTgwiXPwzDiqM2zzNIySbOowa6O+pjdA83D7T9oLwJ9l4JlgChwNupL4oyxjtMBpiCs45Vyuanb7P6vGtvRoOZsBEEdWDc5Y3scBNEAOoaDkpbwGdTMQNluU5AVRUlUt5Vu-dQ3cAASvhPEEHxF3AdVuZ8MIFzlZ1pA1tAcAPugWA4ORJDw6w7BcJM-BCIohJdEs1EqOomhQjoR5GO1veNhgtgOM4bgeCbfh+2hIThJZMRxJUHvvVkvOssUAtckb7RVqL+AyRLYOUxDXts-Lwb70raqEizquVernta9zZp7zyvy-YbP+QML7kyltfG2X85b00do-Z2z8IxvxVB-Q0kCkK60VvzABR8eQi19mLEG7owFrWptKKBDsH7KllC7Vm78OYa1lmgn+eswAG2wZaE2wDxagOtpKW+lV756zgYjV2KM6Gfxpt7S6GYszN1MBgAsmRwCth2ifasZplG9h+GopR3YVG8m0ZTMsmiWEcJ9sOMcE4pwWJwiuNcZB5w7m0uQE8Z5XDdWvGAOcd4tovjfELdon4IDfkvDdQCOsILxzAk-aCGBYLwW1mfIIGELpLlSNwPOncaIkS0q4ZuggjwD1op3ApjEIAsSQG0DiiS0L50LkWQSwkIIYDEoZKSF9iEKSUoQNSGktL7h0oWDo+klqmzCGZQglkE52TSKVZaLkwnSy8r5BqG1gpUzCpVY6uV4CxS+AlYYyVejtDShlCJUy8rCEKsVWZ6d4Yl2MgHBqpdXwtWoG1Ku7jnH9XqlnM6wcXpgDwIgKayAZpNXaPNT8adnLw2IRte8KBtrGL2gddaKSWBRVjgCq6IT3q3W+YHR6-x0Xb0LLvZhP1iVsPqGfC2ZNCE8JIYmaG0CKHrCES-FWUY1ZiJQRIxh2NH6gkPv9Y+oJOEEKtosplCS5SssESqahiDZTIM1vyvE6C+bsiwaKnBErLZX2IQw-h8rFYcoQdy2hpLjVJiYRg1hur2HWlNubEBDLpU2pZeQhVVD4Gv0tUg3larSFoKCsvZAjys7-KqSwlQEdVzRyxXA85SdLkpxuTCtmmdnK5wIiEupwBkzF1aeC7IFchhV2rMmIAA",
                html.Iframe(
                    #src=f"http://localhost:20000/#compressed=true&presentationMode=true&integrationMode=true&hideLegend=true&workflowAnnotationDisplay=annotation&config={VIS_CONFIG}",
                    src=f"{'http' if os.environ.get('LOCAL') == 'true' else 'https' }{flask.request.host_url[4:-1]}{os.environ.get('PATH_PREFIX')}vis/#compressed=true&presentationMode=true&integrationMode=true&hideLegend=true&workflowAnnotationDisplay=annotation&config={VIS_CONFIG}",
                    style={"width": "100%", "height": "800px"}, id="visualizer-frame"
                )
            ], id='3d-graph'),
            dcc.Store(id='vis-data'),
            dcc.Store(id='vis-data-result'),
            dcc.Store(id='reload-trigger'),
            dcc.Store(id='reload-success')
            # 3d volume-rendering plot [xyz] of the cube with Gaia targets
            # ra-dec-distance --> xyz (cartesian cube center coordinate)
            # extract cube at xyz with size n
            # how to search for all Gaia targets in this given volume?
            # probably simply do a box-square search centred on ra-dec coordinate
            # and then filter for distances 'close' to the subcub center
            # Limit query result to e.g. 1000(0) results, distance filter reduced the number of targets further
        ], style={'width': '80%', 'padding': '5px', 'margin': '5px', 'display': 'inline-block', 'verticalAlign': 'top',
                  'borderWidth': '2px'}),
        html.Div([
        ])
        # dcc.Download(
        #    id='3d-download',
        #    children=[html.Button(['Save data'])],
        # ),
        # in callback:
        # Input("button", "n_clicks")
        # Output("donwload-dataframe", "data")
        # return dcc.send_data_frame(df.to_csv, filename='some_name.csv')
        # return dcc.send_file("path_to_file")
    ])

    return content_3d


def correct_cube_distance(mid_point, distance_cube):
    """
    corrects the distance of sub-cube, if necessary, so that the sub-cube is inside the original cube

    :param mid_point:
    :param distance_cube:
    :return: corrected distance of cube
    """
    corrected_distance_cube = distance_cube
    axes_indices = [0, 1, 2]
    for index in axes_indices:
        total_distance = mid_point[index] + distance_cube
        if (total_distance > globals.max_axes[index]):
            new_distance_cube = abs(globals.max_axes[index] - mid_point[index])
            if (new_distance_cube < corrected_distance_cube):
                corrected_distance_cube = new_distance_cube

        total_distance = mid_point[index] - distance_cube
        if (total_distance < globals.min_axes[index]):
            new_distance_cube = abs(globals.min_axes[index] - mid_point[index])
            if (new_distance_cube < corrected_distance_cube):
                corrected_distance_cube = new_distance_cube
    return corrected_distance_cube


def correct_cube_distance_per_axis(mid_point, distance_cube):
    """
    corrects the distance of sub-cube, if necessary, so that the sub-cube is inside the original cube

    :param mid_point:
    :param distance_cube:
    :return: corrected distance of cube
    """
    corrected_distance_cube = []
    axes_indices = [0, 1, 2]
    for index in axes_indices:
        distance_down = mid_point[index] - distance_cube
        if (distance_down < globals.min_axes[index]):
            distance_down = abs(globals.min_axes[index] - mid_point[index])
        else:
            distance_down = distance_cube

        distance_up = mid_point[index] + distance_cube
        if (distance_up > globals.max_axes[index]):
            distance_up = abs(globals.max_axes[index] - mid_point[index])
        else:
            distance_up = distance_cube
        corrected_distance_cube.append([abs(distance_down), abs(distance_up)])
    return corrected_distance_cube


def get_suitable_downsampling(mid_point, distance_cube):
    """
    returns a most suitable downsampling rate

    :param mid_point:
    :param distance_cube:
    :return:
    """
    axes_indices = [0, 1, 2]
    total_points = 0
    for index in axes_indices:
        axis_total_points = round(abs(mid_point[index] - distance_cube[index][0]) / globals.step[index])
        axis_total_points = axis_total_points + round(
            abs(mid_point[index] + distance_cube[index][1]) / globals.step[index])
        if (total_points == 0):
            total_points = axis_total_points
        else:
            total_points = total_points * axis_total_points

    if (total_points < globals.RENDERABLE_CUBE_DATA_POINTS):
        return 1
    downsampling_rate_list = [2, 4, 8, 27, 125, 216, 343, 512, 1000]
    for downsampling_rate in downsampling_rate_list:
        if (round(total_points / downsampling_rate) < globals.RENDERABLE_CUBE_DATA_POINTS):
            if (downsampling_rate == 2):
                # The representation of cubes with a down-sampling rate of two does not look so good.
                # TODO check and fix
                return 4
            return downsampling_rate;
    return 1000;


def get_closes_index(axes, target_value):
    import bisect
    position = bisect.bisect_left(axes, target_value)
    if position == 0:
        return 0
    if position == len(axes):
        return len(axes) - 1
    value_position_before = axes[position - 1]
    value_position_current = axes[position]
    if value_position_current - target_value < target_value - value_position_before:
        return position
    else:
        return position - 1


def get_sub_cube_positons(axes, mid_point, distance_cube):
    """
    :param axes:
    :param mid_point:
    :param distance_cube:
    :return:
    """
    '''
    min_x = get_closes_index(axes[0], (mid_point[0] - distance_cube[0][0]))
    max_x = get_closes_index(axes[0], (mid_point[0] + distance_cube[0][1]))
    pos_x = [min_x, max_x]

    min_y = get_closes_index(axes[1], (mid_point[1] - distance_cube[1][0]))
    max_y = get_closes_index(axes[1], (mid_point[1] + distance_cube[1][1]))
    pos_y = [min_y, max_y]
    '''
    min_y = get_closes_index(axes[0], (mid_point[0] - distance_cube[0][0]))
    max_y = get_closes_index(axes[0], (mid_point[0] + distance_cube[0][1]))
    pos_y = [min_y, max_y]

    min_x = get_closes_index(axes[1], (mid_point[1] - distance_cube[1][0]))
    max_x = get_closes_index(axes[1], (mid_point[1] + distance_cube[1][1]))
    pos_x = [min_x, max_x]

    min_z = get_closes_index(axes[2], (mid_point[2] - distance_cube[2][0]))
    max_z = get_closes_index(axes[2], (mid_point[2] + distance_cube[2][1]))
    pos_z = [min_z, max_z]

    return (pos_x, pos_y, pos_z)


def calculate3DData(cube, axes, raw = False):
    X, Y, Z = np.meshgrid(axes[0], axes[1], axes[2])
    data = np.stack((X.flatten(), Y.flatten(), Z.flatten(), cube.flatten()), axis=-1)
    dataframe = pd.DataFrame(data=data, columns=['x', 'y', 'z', 'value'])
    # dataframe.to_csv("./sample.csv", index=False, float_format='%.25f')
    # dataframe.to_csv("/media/mrauch/data2/data/workspaces/explore/sda/g-tomo/_data/app_data/data.csv", index=False, float_format='%.25f')
    if raw:
        return dataframe
    else:
        return dataframe.to_csv()

@sda.callback(
    [Output("3d-graph", "figure"),
     Output('temp3', 'children'),
     # Output('reload-trigger', 'data'),
     # Output('vis-data', 'data')
    ],
    [Input("3d-get-cube", "n_clicks"),
    ],
    [State("3d-ra", "value"),
     State("3d-dec", "value"),
     State("3d-distance", "value"),
     State("distance-cube", "value"),
     ],
)
def update_3d_graph(n_clicks, ra, dec, distance, distance_cube):
    if not n_clicks:  # ((n_clicks == 0) or (n_clicks == None)):
        raise PreventUpdate

    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
        raise PreventUpdate

    import json
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs,
        # 'outputs': ctx.outputs_list,
    }, indent=2)

    err_message = None

    if ra is None:
        sc = None
        # err_message = "coordinate-distance not correct"
    elif dec is None:
        sc = None
        # err_message = "coordinate-distance not correct"
    elif distance is None:
        sc = None
    elif distance_cube is None:
        sc = None
        # err_message = "coordinate-distance not correct"
    else:
        # sc="coord"
        # sc = SkyCoord(ra*u.deg, dec*u.deg, frame='galactic')
        # sub_cube, sub_axes = subcube(globals.cube, globals.axes, sc=sc, step=5.0, size_pc=100.0, center_distance=distance)

        visdata = []
        sc = SkyCoord(
            ra,
            dec,
            distance=distance,
            unit=('deg', 'deg', 'pc'),
            frame='galactic'
        )
        mid_point = sc.represent_as('cartesian').get_xyz().value
        distance_cube = correct_cube_distance_per_axis(mid_point, distance_cube)
        downsampling_rate =  get_suitable_downsampling(mid_point, distance_cube)
        if (downsampling_rate > 1):
            file_name_base = os.path.splitext(os.path.basename(globals.filename))[0]
            downsampled_file_name = file_name_base + "__" + str(downsampling_rate) + "X.h5"
            #hdf5file = os.path.join(globals.basepath + "/" + file_name_base + "/" + downsampled_file_name)
            hdf5file = os.path.join(globals.basepath, file_name_base, downsampled_file_name)
            headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_downsampled_cube(hdf5file)

            pos_x, pos_y, pos_z = get_sub_cube_positons(axes, mid_point, distance_cube)
            sub_cube = cube[pos_x[0]:pos_x[1] + 1, pos_y[0]:pos_y[1] + 1, pos_z[0]:pos_z[1] + 1]
            sub_axes = [axes[0][pos_x[0]:pos_x[1] + 1], axes[1][pos_y[0]:pos_y[1] + 1], axes[2][pos_z[0]:pos_z[1] + 1]]
            visdata = calculate3DData(sub_cube, sub_axes)

        else:
            pos_x, pos_y, pos_z = get_sub_cube_positons(globals.axes, mid_point, distance_cube)
            sub_cube = globals.cube[pos_x[0]:pos_x[1] + 1, pos_y[0]:pos_y[1] + 1, pos_z[0]:pos_z[1] + 1]
            sub_axes = [globals.axes[0][pos_x[0]:pos_x[1] + 1], globals.axes[1][pos_y[0]:pos_y[1] + 1],
                        globals.axes[2][pos_z[0]:pos_z[1] + 1]]
            visdata = calculate3DData(sub_cube, sub_axes)


    msg = html.Div([
        html.Pre(err_message),
    ])

    return [fig3d, msg]


sda.clientside_callback(
    """
    function sendData(n, filename, ra, dec, dist, c_dist) {
        var algorithmId = '29bff9b3-bec5-45da-906b-d141ba9d7ec2'
        var frame = window.frames['visualizer-frame'];
        
        var cubeName = "";
        if (filename === 'cube2') cubeName = 'explore_cube_density_values_050pc_v1.h5'
        else cubeName = 'explore_cube_density_values_025pc_v1.h5'
           
        frame.contentWindow.postMessage({ 
            key: 'rerunAlgo', 
            value: { params: { cube_file: cubeName, ra: ra, dec: dec, distance: dist, cube_distance: c_dist, overwrite: true }, 
            algo: algorithmId, 
            targetVis: { type: 'volumen', id: '1' } }, 
            name: 'cube_data' 
        }, '*');

        return 'send data';
    }
    """,
    [Output("vis-data-result", "data")],
    [Input("3d-get-cube", "n_clicks"),
     Input('cube-dropdown', 'value')
    ],
    [State("3d-ra", "value"),
     State("3d-dec", "value"),
     State("3d-distance", "value"),
     State("distance-cube", "value"),
    ],
)

sda.clientside_callback(
    """
    function reloadPage(value) {
        var frame = window.frames['visualizer-frame'];
        frame.contentWindow.postMessage({key: 'reload'}, '*');
        return 'reload page';
    }
    """,
    [Output("reload-success", "data")],
    [Input("reload-trigger", "data")]
)

