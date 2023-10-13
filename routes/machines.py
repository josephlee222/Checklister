import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for

from classes.Machine import Machine
from classes.MachineType import MachineType
from functions import flashFormErrors, adminAccess, loginAccess

machines = Blueprint("machines", __name__)


@machines.route("/machine/<id>", methods=['GET', 'POST'])
@loginAccess
def viewMachineDetails(id):
    m = ""
    t = ""
    with shelve.open("machines") as machines:
        m = machines[id]

    with shelve.open("machineTypes") as types:
        t = types[m.machineType]

    return render_template("machines/machineDetails.html", type=t, machine=m)