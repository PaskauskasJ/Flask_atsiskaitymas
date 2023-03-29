from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Groups, Bills
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def groups():
    if request.method == 'POST':

        group = request.form.get('group')
        if len(group) < 3:
            flash('Group name must be greater than 3 characters.', category='error')
        else:

            new_group = Groups(name=group)
            db.session.add(new_group)
            db.session.commit()
            flash('Group added!', category='success')
    groups = Groups.query.all()

    return render_template("groups.html", groups=groups, user=current_user, title='Groups')


@views.route('/group/<int:groups_id>', methods=['GET', 'POST'])
@login_required
def bills(groups_id):
    if request.method == 'POST':

        bill = request.form.get('bill')
        price = request.form.get('price')

        new_bill = Bills(bill=bill, price=price,
                         group_id=groups_id, user_id=current_user.id)
        db.session.add(new_bill)
        db.session.commit()
        flash('Bill added!', category='success')

    bills = Bills.query.filter_by(group_id=groups_id).join(Bills.user).all()

    return render_template("bills.html", bills=bills, user=current_user, groups_id=groups_id, title='Bills')


@views.route('/delete-bill', methods=['POST'])
def delete_bill():

    bills = json.loads(request.data)
    billsId = bills['billsId']
    bills = Bills.query.get(billsId)
    if bills:
        if bills.user_id == current_user.id:
            db.session.delete(bills)
            db.session.commit()

    return jsonify({})


@views.route('/delete-group', methods=['POST'])
def delete_group():

    groups = json.loads(request.data)
    groupsId = groups['groupsId']
    groups = Groups.query.get(groupsId)
    if groups:
        db.session.delete(groups)
        db.session.commit()

    return jsonify({})
