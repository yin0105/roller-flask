from flask import flash, render_template, request, redirect, url_for, \
    current_app, abort, session
from flask_login import current_user, login_required

import os
import folium
import pandas
import requests
import math
from math import radians, sin, cos, asin, sqrt
from geopy import distance

from app import db
from app.delivery import delivery_blueprint
from app.delivery.models import Delivery
from app.user.models import User
from app.company.models import Company
from app.order.models import Order, IncomingOrder


@delivery_blueprint.route('/dispatch/incoming_order/<int:incoming_order_id>', methods=['GET', 'POST'])
@login_required
def dispatch(incoming_order_id):
    incoming_order = IncomingOrder.query.get_or_404(incoming_order_id)
    company = incoming_order.supplier
    if incoming_order.order.buyer.lat and incoming_order.order.buyer.lon != None:
        dropoff_dist = round(incoming_order.get_distance(),2)
        unit = 'km'
        delivery = Delivery(incoming_order_id=incoming_order.id, dropoff_dist=dropoff_dist, unit=unit)
        db.session.add(delivery)
        db.session.commit()
        flash('Delivery request dispatched')
        return redirect(url_for('order.incoming', incoming_order_id=incoming_order.id, company_id=company.id))
    else:
        
        flash("Buyer's address missing!")
        return redirect(url_for('order.incoming', incoming_order_id=incoming_order.id, company_id=company.id))


@delivery_blueprint.route('/show_all')
@login_required
def jobs(): 
    deliveries = Delivery.query.order_by(Delivery.created_on.desc()).all()
    new_deliveries = Delivery.query.filter(Delivery.accepted==False).all()
    past_deliveries = Delivery.query.filter(Delivery.completed==True and Delivery.cancelled==True).all()
    return render_template('delivery/jobs.html', title='Delivery Jobs', 
                                                    deliveries=deliveries,
                                                    new_deliveries=new_deliveries,
                                                    past_deliveries=past_deliveries)


@delivery_blueprint.route('/show/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def show_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    courier = current_user

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    mylon = float(location[1])

    # Get distance between rider and collection point
    def get_collect_distance():
        lat1 = delivery.incoming_order.supplier.lat
        lon1 = delivery.incoming_order.supplier.lon
        lat2 = mylat
        lon2 = mylon
        radius = 6371 # approximate value for spherical Earth formula in km
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
             * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return round(d, 2)

    delivery.collect_dist = get_collect_distance()
    return render_template('delivery/show.html', title='Delivery Job', 
                                                        delivery=delivery,
                                                        courier=courier)


@delivery_blueprint.route('/collect/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def accept(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    courier = current_user

    # Get current_user location
    res = requests.get('https://ipinfo.io/')
    mydata = res.json()
    location = mydata['loc'].split(',')
    print(f'location') # string
    mylat = float(location[0])
    mylon = float(location[1])

    # Get distance between rider and collection point
    def get_collect_distance():
        lat1 = delivery.incoming_order.supplier.lat
        lon1 = delivery.incoming_order.supplier.lon
        lat2 = mylat
        lon2 = mylon
        radius = 6371 # approximate value for spherical Earth formula in km
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
             * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return round(d, 2)

    delivery.accepted = True
    delivery.collect_dist = get_collect_distance()
    delivery.couriers.append(courier)
    db.session.commit()
    return render_template('delivery/accepted.html', title='go to vendor', 
                                                        delivery=delivery,
                                                        courier=courier)


@delivery_blueprint.route('/dropoff/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def collect(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('delivery/collected.html', title='go to customer', 
                                                        delivery=delivery)


@delivery_blueprint.route('/delivered/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def delivered(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.completed = True
    db.session.commit()
    flash('Yay! Delivery completed. You rock!')
    return redirect(url_for('delivery.jobs'))


@delivery_blueprint.route('/cancel/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def cancel_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.cancelled = True
    #delivery.couriers = []
    #db.session.delete(delivery)
    #db.session.commit()
    flash('Delivery job cancelled.')
    return redirect(url_for('delivery.jobs'))

