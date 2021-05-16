from flask import render_template, current_app, send_file
from flask_login import login_required, current_user

import os
import folium
import pandas
import requests

from app import db
from app.geomap import geomap_blueprint
from app.user.models import User
from app.company.models import Company
from app.delivery.models import Delivery
from app.order.models import Order, IncomingOrder


"""
First we save a Folium map and return folium map as an html file here. 
"""
@geomap_blueprint.route('/map')
def map():
    return render_template('geomap/basemap.html')

"""
Next we show folium map here.
Lastly, we create an iframe to call this map on another route, eg. user.dashboard
"""
@geomap_blueprint.route('/show', methods=['GET', 'POST'])
@login_required
def show():
    data = pandas.read_csv('companies.csv')
    name = list(data['NAME'])
    lat = list(data['LAT'])
    lon = list(data['LON'])

    map = folium.Map(location=[1.299426, 103.789824], 
                        zoom_start=11, 
                        tiles='Stamen Terrain', 
                        width='100%', height='100%')

    html = """
    <a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>
    %s, %s \n
    """

    fg = folium.FeatureGroup(name='My Map')

    for name, lt, ln in zip(name, lat, lon):
        iframe = folium.IFrame(html=html % (name, name, lt, ln), width=200, height=60)
        fg.add_child(folium.Marker(location=[lt, ln], 
                                    popup=folium.Popup(iframe), icon=folium.Icon(color='purple')))
        fg.add_child(folium.Marker(location=[1.299426, 103.789824], 
                                    popup='You are here.', icon=folium.Icon(color='green')))

        # Get current_user location
        username = current_user.username
        res = requests.get('https://ipinfo.io/')
        mydata = res.json()
        location = mydata['loc'].split(',')
        print(f'location') # string
        mylat = float(location[0])
        myln = float(location[1])
        fg.add_child(folium.Marker(location=[mylat, myln], popup=[username],\
                                    icon=folium.Icon(color='blue', icon='grav', prefix='fa')))

    map.add_child(fg)
    map.save(os.path.join(current_app.config['GEOMAP'],'basemap.html'))
    return render_template('geomap/geomapper.html', title='Open Street Map')


@geomap_blueprint.route('/map/delivery_requests', methods=['GET', 'POST'])
@login_required
def delivery_requests_map():
    map = folium.Map(
        location=[1.299426, 103.789824], 
        zoom_start=11, 
        tiles='Stamen Terrain', 
        width='100%', height='100%')

    fg = folium.FeatureGroup(name='My Map')

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    myln = float(location[1])
    fg.add_child(folium.Marker(location=[mylat, myln], popup='Rider',\
     icon=folium.Icon(color='purple', icon='truck', prefix='fa')))

    # Get suppliers' locations
    deliveries = Delivery.query.all()
    for delivery in deliveries:
        name = delivery.incoming_order.supplier.name
        lat = delivery.incoming_order.supplier.lat
        lon = delivery.incoming_order.supplier.lon
        print(f'{name} {lat} {lon}')

        html = """
        <a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>
        %s, %s \n
        """

        iframe = folium.IFrame(html=html % (name, name, lat, lon), width=200, height=60)
        fg.add_child(folium.Marker(location=[lat, lon], popup=folium.Popup(iframe),\
         icon=folium.Icon(color='blue', icon='shopping-bag', prefix='fa')))

    map.add_child(fg)
    map.save(os.path.join(current_app.config['GEOMAP'],'base_delivery_requests_map.html'))
    return render_template('geomap/delivery_requests_mapper.html', title='Open Street Map')


@geomap_blueprint.route('/map/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def delivery_map(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    name1 = delivery.incoming_order.supplier.name
    lat1 = delivery.incoming_order.supplier.lat
    lon1 = delivery.incoming_order.supplier.lon
    name2 = delivery.incoming_order.order.buyer.username
    lat2 = delivery.incoming_order.order.buyer.lat
    lon2 = delivery.incoming_order.order.buyer.lon

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    myln = float(location[1])

    map = folium.Map(
        location=[1.299426, 103.789824], 
        zoom_start=11, 
        tiles='Stamen Terrain', 
        width='100%', height='100%')

    html = """
    <a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>
    %s, %s \n
    """

    fg = folium.FeatureGroup(name='My Map')
    fg.add_child(folium.Marker(location=[mylat, myln], popup='Rider', icon=folium.Icon(color='purple', icon='truck', prefix='fa')))
    fg.add_child(folium.Marker(location=[lat1, lon1], popup=name1, icon=folium.Icon(color='blue', icon='shopping-bag', prefix='fa')))
    fg.add_child(folium.Marker(location=[lat2, lon2], popup=name2, icon=folium.Icon(color='green', icon='home', prefix='fa')))
    map.add_child(fg)
    map.save(os.path.join(current_app.config['GEOMAP'],'base_delivery_map.html'))
    return render_template('geomap/delivery_mapper.html', title='Open Street Map')


@geomap_blueprint.route('/map/collect/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def delivery_collect_map(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    name1 = delivery.incoming_order.supplier.name
    lat1 = delivery.incoming_order.supplier.lat
    lon1 = delivery.incoming_order.supplier.lon

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    myln = float(location[1])

    map = folium.Map(
        location=[1.299426, 103.789824], 
        zoom_start=11, 
        tiles='Stamen Terrain', 
        width='100%', height='100%')

    html = """
    <a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>
    %s, %s \n
    """

    fg = folium.FeatureGroup(name='My Map')
    fg.add_child(folium.Marker(location=[mylat, myln], popup='Rider', icon=folium.Icon(color='purple', icon='truck', prefix='fa')))
    fg.add_child(folium.Marker(location=[lat1, lon1], popup=name1, icon=folium.Icon(color='blue', icon='shopping-bag', prefix='fa')))
    map.add_child(fg)
    map.save(os.path.join(current_app.config['GEOMAP'],'base_delivery_collect_map.html'))
    return render_template('geomap/delivery_collect_mapper.html', title='Open Street Map')


@geomap_blueprint.route('/map/dropoff/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def delivery_dropoff_map(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    name = delivery.incoming_order.order.buyer.username
    lat = delivery.incoming_order.order.buyer.lat
    lon = delivery.incoming_order.order.buyer.lon

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    myln = float(location[1])

    map = folium.Map(
        location=[1.299426, 103.789824], 
        zoom_start=11, 
        tiles='Stamen Terrain', 
        width='100%', height='100%')

    html = """
    <a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>
    %s, %s \n
    """

    fg = folium.FeatureGroup(name='My Map')
    fg.add_child(folium.Marker(location=[mylat, myln], popup='Rider', icon=folium.Icon(color='purple', icon='truck', prefix='fa')))
    fg.add_child(folium.Marker(location=[lat, lon], popup=name, icon=folium.Icon(color='green', icon='home', prefix='fa')))
    map.add_child(fg)
    map.save(os.path.join(current_app.config['GEOMAP'],'base_delivery_dropoff_map.html'))
    return render_template('geomap/delivery_dropoff_mapper.html', title='Open Street Map')
