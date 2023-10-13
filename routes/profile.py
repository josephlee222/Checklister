import shelve
from datetime import datetime, timedelta, time

from flask import flash, Blueprint, render_template, request, session, redirect, url_for, Response

from classes.Address import Address
from forms import editProfileForm, addAddressForm, editAddressForm
from functions import flashFormErrors, loginAccess, convertHoursToTime

profile = Blueprint("profile", __name__)


@profile.route('/profile')
@loginAccess
def viewProfile():
    session["previous_url"] = url_for("profile.viewProfile")
    with shelve.open("users") as users, shelve.open("appointments") as appointments:
        user = users[session["user"]["email"]]
        appointmentArray = []
        for id, appointment in appointments.items():
            if appointment.getUserEmail() == session["user"]["email"] and appointment.getDate() > datetime.now().date():
                appointmentArray.append(appointment)

    return render_template("profile/viewProfile.html", user=user, appointments=appointmentArray)


@profile.route('/profile/edit', methods=['GET', 'POST'])
@loginAccess
def editProfile():
    form = editProfileForm(request.form)

    with shelve.open("users", writeback=True) as users:
        user = users[session["user"]["email"]]

        if request.method == "POST" and form.validate():
            print("Update profile")
            user.setName(form.name.data)
            user.setBirthday(form.birthday.data)
            user.setPhone(form.phone.data)

            flash("Your profile has been updated successfully!", category="success")
            return redirect(url_for("profile.viewProfile"))
        else:
            flashFormErrors("Unable to update your profile", form.errors)

        form.name.data = user.getName()
        form.birthday.data = user.getBirthday()
        form.phone.data = user.getPhone()
        return render_template("profile/editProfile.html", form=form, user=user)


@profile.route('/profile/address')
@loginAccess
def viewAddresses():
    try:
        with shelve.open("users") as users:
            addresses = users[session["user"]["email"]].getAddress()

        return render_template("profile/viewAddresses.html", addresses=addresses)
    except KeyError:
        flash("Unable to get your delivery addresses", category="error")
        return redirect(url_for("profile.viewProfile"))


@profile.route('/profile/address/add', methods=['GET', 'POST'])
@loginAccess
def addAddress():
    form = addAddressForm(request.form)

    if request.method == "POST" and form.validate():
        print("Add Address Here")
        try:
            with shelve.open("users", writeback=True) as users:
                user = users[session["user"]["email"]]

                address = Address(form.name.data, form.location.data)
                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.setAddress(address)
                    flash("Your new address has been added to your account", category="success")
                    return redirect(url_for("profile.viewAddresses"))
                else:
                    flash("Unable to add address because our location provider could not find your address.",
                          category="error")
        except Exception as e:
            flash("Unable to add delivery address", category="error")

    return render_template("profile/addAddress.html", form=form)


@profile.route('/profile/address/delete/<id>', methods=['GET', 'POST'])
@loginAccess
def deleteAddress(id):
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[session["user"]["email"]]
            if user.deleteAddress(id):
                flash("Your saved address has been deleted", category="success")
            else:
                flash("Unable to delete delivery address: Delivery address does not exist", category="error")
    except KeyError:
        flash("Unable to delete delivery address: Account or delivery address does not exist", category="error")

    return redirect(url_for("profile.viewAddresses"))


@profile.route('/profile/address/edit/<id>', methods=['GET', 'POST'])
@loginAccess
def editAddress(id):
    form = editAddressForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[session["user"]["email"]]

            if request.method == "POST" and form.validate():
                address = Address(form.name.data, form.location.data)
                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.editAddress(int(id), address)
                    flash("Address has been successfully edited", category="success")
                    return redirect(url_for("profile.viewAddresses"))
                else:
                    flash("Unable to edit your address because our location provider could not find your address.",
                          category="error")
            else:
                flashFormErrors("Unable to edit address", form.errors)

            if user.getAddress() is not None:
                try:
                    address = user.getAddress()[int(id)]
                    form.name.data = address.getName()
                    form.location.data = address.getLocation()
                    return render_template("profile/editAddress.html", form=form)
                except IndexError:
                    flash("Cannot edit address. Specified address ID does not exist.", category="error")
                    return redirect(url_for("profile.viewAddresses"))
            else:
                flash("Cannot edit address. No address has been added yet", category="error")
                return redirect(url_for("profile.viewAddresses"))

    except KeyError:
        flash("Unable to delete delivery address: Account or delivery address does not exist", category="error")
        return redirect(url_for("profile.viewAddresses"))
