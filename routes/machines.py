import os
import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

from classes.Machine import Machine
from classes.MachineType import MachineType
from functions import flashFormErrors, adminAccess, loginAccess
from forms import submitChecklistFileForm
from classes.ChecklistSubmission import ChecklistSubmission

machines = Blueprint("machines", __name__)


@machines.route("/machine/<id>")
@machines.route("/machine/<id>/checklist", endpoint="selectMachineChecklist")
@machines.route("/machine/<id>/checklist/<cid>", endpoint="submitMachineChecklist", methods=["GET", "POST"])
@loginAccess
def viewMachineDetails(id, cid=0):
    m = ""
    t = ""
    with shelve.open("machines") as machines:
        m = machines[id]

    with shelve.open("machineTypes") as types:
        t = types[m.machineType]

    match request.endpoint:
        case "machines.selectMachineChecklist":
            return render_template("machines/selectChecklist.html", type=t, machine=m)

        case "machines.submitMachineChecklist":
            c = t.checklist[int(cid)]
            form = submitChecklistFileForm()

            if request.method == "POST":
                if form.validate_on_submit():
                    with shelve.open("submissions") as submissions:
                        filename = form.filename.data
                        if filename:
                            bPath = "static/uploads/submissions/" + str(id)
                            if not os.path.exists(bPath):
                                os.makedirs(bPath)

                            sPath = secure_filename(filename.filename)
                            path = os.path.join(bPath, sPath)
                            filename.save(path)

                            s = ChecklistSubmission(session["user"]["email"], id, path)
                            submissions[str(s.id)] = s
                            flash("Successfully uploaded checklist PDF", category="success")
                else:
                    flashFormErrors("Unable to upload the PDF checklist", form.errors)

            return render_template("machines/submitChecklist.html", type=t, machine=m, form=form, c=c)



    return render_template("machines/machineDetails.html", type=t, machine=m)