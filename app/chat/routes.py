import json
from datetime import datetime

from flask import current_app, flash, g, jsonify, redirect, render_template, \
    request, session, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.user import user_blueprint
from app.chat import chat_blueprint
from app.chat.forms import MessageForm
from app.user.models import User
from app.chat.models import Chats, Messages, Notification



@chat_blueprint.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@chat_blueprint.route('/chats')
def chats():
    if current_user.is_anonymous:
        abort(404)
    chats = current_user.mychats().all()
    chats.sort(reverse=True, key=lambda x:x.last_msg().timestamp if isinstance(x, str) else "") # Sort with timestamp of last msg of each chat
    return render_template('chat/chats.html', title='My Chats', chats=chats)


@chat_blueprint.route('/chat/<recipient>', methods=['GET', 'POST'])
@login_required
def chat(recipient):
    chat_user = User.query.filter_by(username=recipient).first_or_404()
    this_chat = current_user.mychats().filter(or_(Chats.user1 == chat_user.id,Chats.user2 == chat_user.id)).first() #Get chat if exists
    if(this_chat): # Check if chat exists, if not make session None
        session['chat_session'] = [this_chat.id,chat_user.id]
        messages = this_chat.msgs.order_by(Messages.timestamp.asc())
        for msg in this_chat.msgs.order_by(Messages.timestamp.desc()).limit(current_user.unread_msgs(this_chat.id)): #Get all the unread msgs and change its flag
            if(msg.author != current_user):
                msg.receiver_read = True
        current_user.add_notification('unread_chats',current_user.unread_chats())

        session['CHAT'] = current_user.unread_chats()
        print('Session Unread Messages: ' + str(session['CHAT']))

        db.session.commit()
        return render_template('chat/chat.html', title='Chat with ' + recipient, chat_user=chat_user, messages=messages)
    else:
        session['chat_session'] = ['None',chat_user.id]
        return render_template('chat/chat.html',title='Chat with ' + recipient, chat_user=chat_user, messages='None')

