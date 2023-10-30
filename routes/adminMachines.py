import os
import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

from classes.ChecklistItem import ChecklistItem
from classes.Machine import Machine
from classes.MachineType import MachineType
from forms import createMachineTypeForm, createMachineForm, selectNfcMachineForm, createChecklistFileForm, \
    editChecklistFileForm
from functions import flashFormErrors, adminAccess

adminMachines = Blueprint("adminMachines", __name__)


@adminMachines.route("/admin/machines/types", methods=['GET', 'POST'])
@adminAccess
def viewMachineTypes():
    with shelve.open("machineTypes") as types:
        return render_template("admin/machines/viewMachineTypes.html", types=types)


@adminMachines.route("/admin/machines/types/add", methods=['GET', 'POST'])
@adminAccess
def createMachineType():
    form = createMachineTypeForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data

        new_type = MachineType(name, description)

        with shelve.open("machineTypes") as types:
            types[str(new_type.id)] = new_type
            flash("Machine type successfully created. Edit the machine type to add a checklist", category="success")
            return redirect(url_for("adminMachines.viewMachineTypes"))
    else:
        flashFormErrors("Unable to create the machine type", form.errors)

    return render_template("admin/machines/createMachineType.html", form=form)


@adminMachines.route("/admin/machines/types/<id>")
@adminMachines.route("/admin/machines/types/<id>/new", endpoint="createMachineTypeFile", methods=['GET', 'POST'])
@adminMachines.route("/admin/machines/types/<id>/edit/<itemId>", endpoint="editMachineTypeFile", methods=['GET', 'POST'])
@adminAccess
def viewMachineTypeDetails(id, itemId=0):
    with shelve.open("machineTypes", writeback=True) as types:
        t = types[id]

        match request.endpoint:
            case "adminMachines.createMachineTypeFile":
                form = createChecklistFileForm()
                if form.validate_on_submit():
                    name = form.name.data
                    filename = form.filename.data
                    checklistFile = ChecklistItem(name)
                    bPath = "static/uploads/checklists/" + str(checklistFile.id)
                    os.makedirs(bPath)

                    sPath = secure_filename(filename.filename)
                    path = os.path.join(bPath, sPath)
                    filename.save(path)
                    checklistFile.path = path
                    t.createChecklistItem(checklistFile)
                    print(vars(checklistFile))
                    flash("Successfully uploaded checklist PDF", category="success")
                    return redirect(url_for("adminMachines.viewMachineTypeDetails", id=id))
                else:
                    flashFormErrors("Unable to upload the PDF checklist", form.errors)

                return render_template("admin/machines/createChecklistFile.html", type=t, form=form)
            case "adminMachines.editMachineTypeFile":
                form = editChecklistFileForm()
                f = t.checklist[int(itemId)]
                if form.validate_on_submit():
                    name = form.name.data
                    filename = form.filename.data

                    f.filename = name
                    if filename:
                        bPath = "static/uploads/checklists/" + str(f.id)
                        sPath = secure_filename(filename.filename)
                        path = os.path.join(bPath, sPath)
                        filename.save(path)
                        f.path = path
                    flash("Successfully uploaded checklist PDF", category="success")
                    return redirect(url_for("adminMachines.viewMachineTypeDetails", id=id))
                else:
                    flashFormErrors("Unable to upload the PDF checklist", form.errors)

                form.name.data = f.filename

                return render_template("admin/machines/editChecklistFile.html", type=t, form=form, f=f)




    return render_template("admin/machines/viewMachineType.html", type=t)


@adminMachines.route("/admin/machines", methods=['GET', 'POST'])
@adminAccess
def viewMachines():
    with shelve.open("machineTypes") as types:
        m_types = dict(types)

    with shelve.open("machines") as machines:
        m = dict(machines)

    return render_template("admin/machines/viewMachines.html", types=m_types, machines=m)


@adminMachines.route("/admin/machines/add", methods=['GET', 'POST'])
@adminAccess
def createMachine():
    form = createMachineForm(request.form)

    choices = []
    with shelve.open("machineTypes") as types:
        for type in types:
            choices.append((types[type].id, types[type].name))

    form.machineType.choices = choices

    if request.method == "POST" and form.validate():
        name = form.name.data
        notes = form.notes.data
        machineType = form.machineType.data

        new_machine = Machine(name, notes, machineType)

        with shelve.open("machines") as machines:
            machines[str(new_machine.id)] = new_machine
            flash("Machine successfully created", category="success")
            return redirect(url_for("adminMachines.viewMachines"))
    else:
        flashFormErrors("Unable to create the machine type", form.errors)

    return render_template("admin/machines/createMachine.html", form=form)


@adminMachines.route("/admin/machines/nfc", methods=['GET', 'POST'])
@adminMachines.route("/admin/machines/nfc/<id>", methods=['GET', 'POST'])
@adminAccess
def tagMachine(id=None):
    form = selectNfcMachineForm(request.form)

    choices = []
    with shelve.open("machines") as machines:
        for machine in machines:
            choices.append((machines[machine].id, machines[machine].name))

    form.name.choices = choices

    #If its a post request
    if request.method == "POST" and form.validate():
        id = form.name.data
        form.name.default = id

        with shelve.open("machines") as machines:
            return render_template("admin/machines/tagMachineNfc.html", form=form, id=id, selected=machines[id].name)


    # If ID exist, start the write process
    if id:
        form.name.default = id
        with shelve.open("machines") as machines:
            return render_template("admin/machines/tagMachineNfc.html", form=form, id=id, selected=machines[id].name)

    return render_template("admin/machines/tagMachineNfc.html", form=form)
