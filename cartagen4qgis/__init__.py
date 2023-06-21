__author__ = 'Guillaume Touya, Justin Berli'
__date__ = '2023-05-11'
__copyright__ = '(C) 2023 by Guillaume Touya, Justin Berli'

import cartagen4py

def classFactory(iface):
    """
    Load CartAGen4QGIS class from file CartAGen4QGIS.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .cartagen4qgis import CartAGen4QGISPlugin
    return CartAGen4QGISPlugin()