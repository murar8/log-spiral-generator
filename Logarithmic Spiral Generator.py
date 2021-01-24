import math
import sys
import traceback

import adsk.cam
import adsk.core
import adsk.fusion

PANEL = "SketchCreatePanel"

SPIRAL_BUTTON_ID = "logarithmicspiralbutton"

POLAR_SLOPE_INPUT_ID = "polarslope"
SCALE_INPUT_ID = "scale"
RADIUS_INPUT_ID = "radius"
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

        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)

        inputs.addAngleValueCommandInput(
            id=POLAR_SLOPE_INPUT_ID,
            name='Polar Slope',
            initialValue=adsk.core.ValueInput.createByString('10 degree'),
        )

        inputs.addFloatSpinnerCommandInput(
            id=SCALE_INPUT_ID,
            name='Scale',
            unitType=des.unitsManager.defaultLengthUnits,
            min=0,
            max=sys.float_info.max,
            spinStep=1,
            initialValue=1,
        )

        inputs.addFloatSpinnerCommandInput(
            id=RADIUS_INPUT_ID,
            name='Radius',
            unitType=des.unitsManager.defaultLengthUnits,
            min=0,
            max=sys.float_info.max,
            spinStep=1,
            initialValue=100.0,
        )

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

        onExecute = SpiralCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


# Event handler for the validateInputs event.
class SpiralCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def notify(self, args):
        eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)
        inputs = eventArgs.inputs

        polarSlope = inputs.itemById(POLAR_SLOPE_INPUT_ID).value
        scale = inputs.itemById(SCALE_INPUT_ID).value
        radius = inputs.itemById(RADIUS_INPUT_ID).value
        num_points = inputs.itemById(NUM_POINTS_INPUT_ID).value

        if scale <= 0 or radius <= 0 or num_points <= 0 or polarSlope == 0:
            eventArgs.areInputsValid = False


# Event handler for the execute event.
class SpiralCommandExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        # Verify that a sketch is active.
        app = adsk.core.Application.get()
        if app.activeEditObject.objectType != adsk.fusion.Sketch.classType():
            ui = app.userInterface
            ui.messageBox('A sketch must be active for this command.')
            return False

        eventArgs = adsk.core.CommandEventArgs.cast(args)
        inputs = eventArgs.command.commandInputs

        polarSlope = inputs.itemById(POLAR_SLOPE_INPUT_ID).value
        radius = inputs.itemById(RADIUS_INPUT_ID).value
        num_points = inputs.itemById(NUM_POINTS_INPUT_ID).value

        a = 2
        k = math.tan(polarSlope)
        max_angle = math.log(radius, math.e**k)

        points = adsk.core.ObjectCollection.create()
        # points.add(adsk.core.Point3D.create(0, 0, 0))

        for point in range(num_points + 1):
            angle = (point * max_angle) / num_points
            r = a * math.e**(k * angle)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            points.add(adsk.core.Point3D.create(x, y, 0))

        sketch = adsk.fusion.Sketch.cast(app.activeEditObject)
        sketch.sketchCurves.sketchFittedSplines.add(points)


def run(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        button = ui.commandDefinitions.addButtonDefinition(
            SPIRAL_BUTTON_ID,
            'Logarithmic Spiral',
            'Create a logarithmic spiral as a sketch curve.',
            '.\\Resources\\Logo',
        )

        spiralCommandCreated = SpiralCommandCreatedEventHandler()
        button.commandCreated.add(spiralCommandCreated)
        handlers.append(spiralCommandCreated)

        addInsPanel = ui.allToolbarPanels.itemById(PANEL)
        addInsPanel.controls.addCommand(button)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        cmdDef = ui.commandDefinitions.itemById(SPIRAL_BUTTON_ID)
        if cmdDef:
            cmdDef.deleteMe()

        addinsPanel = ui.allToolbarPanels.itemById(PANEL)
        cntrl = addinsPanel.controls.itemById(SPIRAL_BUTTON_ID)
        if cntrl:
            cntrl.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
