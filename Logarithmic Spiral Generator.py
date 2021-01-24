import math
import sys
import traceback

import adsk.cam
import adsk.core
import adsk.fusion

COMMAND_PANEL = "SketchCreatePanel"

COMMAND_BUTTON_ID = "spiralbutton"

INITIAL_DISTANCE_INPUT_ID = "initialdistance"
INITIAL_ANGLE_INPUT_ID = "initialangle"
FINAL_DISTANCE_INPUT_ID = "finaldistance"
FINAL_ANGLE_INPUT_ID = "finalangle"
NUM_POINTS_INPUT_ID = "numpoints"

# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []


# Event handler for the commandCreated event.
class SpiralCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        cmd = eventArgs.command
        inputs = cmd.commandInputs

        initialDistanceInput = inputs.addDistanceValueCommandInput(
            id=INITIAL_DISTANCE_INPUT_ID,
            name='Initial Distance',
            initialValue=adsk.core.ValueInput.createByString('1'),
        )

        initialAngleInput = inputs.addAngleValueCommandInput(
            id=INITIAL_ANGLE_INPUT_ID,
            name='Initial Angle',
            initialValue=adsk.core.ValueInput.createByString('0 degree'),
        )

        finalDistanceInput = inputs.addDistanceValueCommandInput(
            id=FINAL_DISTANCE_INPUT_ID,
            name='Final Distance',
            initialValue=adsk.core.ValueInput.createByString('2'),
        )

        finalDistanceInput.setManipulator(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Vector3D.create(-1, 0, 0),
        )

        finalAngleInput = inputs.addAngleValueCommandInput(
            id=FINAL_ANGLE_INPUT_ID,
            name='Final Angle',
            initialValue=adsk.core.ValueInput.createByString('180 degree'),
        )
        finalAngleInput.hasMaximumValue = False

        inputs.addIntegerSpinnerCommandInput(
            id=NUM_POINTS_INPUT_ID,
            name='Number of points',
            min=1,
            max=2**31 - 1,
            spinStep=1,
            initialValue=10,
        )

        onValidate = SpiralCommandValidateInputsHandler()
        cmd.validateInputs.add(onValidate)
        handlers.append(onValidate)

        onExecutePreview = SpiralCommandExecutePreviewHandler()
        cmd.executePreview.add(onExecutePreview)
        handlers.append(onExecutePreview)


# Event handler for the validateInputs event.
class SpiralCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def notify(self, args):
        eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)
        inputs = eventArgs.inputs

        initialDistance = inputs.itemById(INITIAL_DISTANCE_INPUT_ID).value
        initialAngle = inputs.itemById(INITIAL_ANGLE_INPUT_ID).value
        finalDistance = inputs.itemById(FINAL_DISTANCE_INPUT_ID).value
        finalAngle = inputs.itemById(FINAL_ANGLE_INPUT_ID).value
        num_points = inputs.itemById(NUM_POINTS_INPUT_ID).value

        if num_points <= 0 or (finalDistance == initialDistance and finalAngle == initialAngle):
            eventArgs.areInputsValid = False


# Event handler for the executePreview event.
class SpiralCommandExecutePreviewHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        # Verify that a sketch is active.
        app = adsk.core.Application.get()
        if app.activeEditObject.objectType != adsk.fusion.Sketch.classType():
            ui = app.userInterface
            ui.messageBox('A sketch must be active for this command.')
            return False

        eventArgs = adsk.core.CommandEventArgs.cast(args)
        inputs = eventArgs.command.commandInputs

        initialDistance = inputs.itemById(INITIAL_DISTANCE_INPUT_ID).value
        initialAngle = inputs.itemById(INITIAL_ANGLE_INPUT_ID).value
        finalDistance = inputs.itemById(FINAL_DISTANCE_INPUT_ID).value
        finalAngle = inputs.itemById(FINAL_ANGLE_INPUT_ID).value
        num_points = inputs.itemById(NUM_POINTS_INPUT_ID).value

        k = math.log((finalDistance / initialDistance)**(1 / finalAngle))

        points = adsk.core.ObjectCollection.create()

        for point in range(num_points + 1):
            angle = (point * (finalAngle - initialAngle)) / num_points
            r = initialDistance * math.e**(k * angle)
            x = r * math.cos(angle + initialAngle)
            y = r * math.sin(angle + initialAngle)
            points.add(adsk.core.Point3D.create(x, y, 0))

        sketch = adsk.fusion.Sketch.cast(app.activeEditObject)
        sketch.sketchCurves.sketchFittedSplines.add(points)

        # Set the isValidResult property to use these results at the final result.
        # This will result in the execute event not being fired.
        eventArgs.isValidResult = True


def run(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        button = ui.commandDefinitions.addButtonDefinition(
            COMMAND_BUTTON_ID,
            'Logarithmic Spiral',
            'Create a logarithmic spiral as a sketch curve.',
            '.\\Resources\\Logo',
        )

        spiralCommandCreated = SpiralCommandCreatedEventHandler()
        button.commandCreated.add(spiralCommandCreated)
        handlers.append(spiralCommandCreated)

        addInsPanel = ui.allToolbarPanels.itemById(COMMAND_PANEL)
        addInsPanel.controls.addCommand(button)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        cmdDef = ui.commandDefinitions.itemById(COMMAND_BUTTON_ID)
        if cmdDef:
            cmdDef.deleteMe()

        addinsPanel = ui.allToolbarPanels.itemById(COMMAND_PANEL)
        cntrl = addinsPanel.controls.itemById(COMMAND_BUTTON_ID)
        if cntrl:
            cntrl.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
