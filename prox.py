import os
import argparse
import asyncio
from xbox360controller import Xbox360Controller
from joycontrol.controller import Controller
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server
from joycontrol.controller_state import button_press, button_release
from joycontrol.transport import NotConnectedError


controller_state = None
trigger_threshold = 0.3
zl_pressed = False
zr_pressed = False


def a_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'a'), loop=loop)


def a_released(button):
    asyncio.ensure_future(button_release(controller_state, 'a'), loop=loop)


def b_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'b'), loop=loop)


def b_released(button):
    asyncio.ensure_future(button_release(controller_state, 'b'), loop=loop)


def x_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'x'), loop=loop)


def x_released(button):
    asyncio.ensure_future(button_release(controller_state, 'x'), loop=loop)


def y_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'y'), loop=loop)


def y_released(button):
    asyncio.ensure_future(button_release(controller_state, 'y'), loop=loop)


def l_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'l'), loop=loop)


def l_released(button):
    asyncio.ensure_future(button_release(controller_state, 'l'), loop=loop)


def r_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'r'), loop=loop)


def r_released(button):
    asyncio.ensure_future(button_release(controller_state, 'r'), loop=loop)


def ls_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'l_stick'), loop=loop)


def ls_released(button):
    asyncio.ensure_future(button_release(controller_state, 'l_stick'), loop=loop)


def rs_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'r_stick'), loop=loop)


def rs_released(button):
    asyncio.ensure_future(button_release(controller_state, 'r_stick'), loop=loop)


def home_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'home'), loop=loop)


def home_released(button):
    asyncio.ensure_future(button_release(controller_state, 'home'), loop=loop)


def plus_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'plus'), loop=loop)


def plus_released(button):
    asyncio.ensure_future(button_release(controller_state, 'plus'), loop=loop)


def minus_pressed(button):
    asyncio.ensure_future(button_press(controller_state, 'minus'), loop=loop)


def minus_released(button):
    asyncio.ensure_future(button_release(controller_state, 'minus'), loop=loop)


def lt_moved(trigger):
    global zl_pressed
    if trigger.value >= trigger_threshold:
        if not zl_pressed:
            zl_pressed = True
            asyncio.ensure_future(button_press(controller_state, 'zl'), loop=loop)
    else:
        if zl_pressed:
            zl_pressed = False
            asyncio.ensure_future(button_release(controller_state, 'zl'), loop=loop)


def rt_moved(trigger):
    global zr_pressed
    if trigger.value >= trigger_threshold:
        if not zr_pressed:
            zr_pressed = True
            asyncio.ensure_future(button_press(controller_state, 'zr'), loop=loop)
    else:
        if zr_pressed:
            zr_pressed = False
            asyncio.ensure_future(button_release(controller_state, 'zr'), loop=loop)


def hat_moved(hat):
    if hat.x == -1:
        asyncio.ensure_future(button_press(controller_state, 'left'), loop=loop)
    elif hat.x == 1:
        asyncio.ensure_future(button_press(controller_state, 'right'), loop=loop)
    else:
        asyncio.ensure_future(button_release(controller_state, 'left'), loop=loop)
        asyncio.ensure_future(button_release(controller_state, 'right'), loop=loop)
    if hat.y == -1:
        asyncio.ensure_future(button_press(controller_state, 'down'), loop=loop)
    elif hat.y == 1:
        asyncio.ensure_future(button_press(controller_state, 'up'), loop=loop)
    else:
        asyncio.ensure_future(button_release(controller_state, 'down'), loop=loop)
        asyncio.ensure_future(button_release(controller_state, 'up'), loop=loop)


def axis_l_moved(axis):
    controller_state.l_stick_state.set_h(int((axis.x + 1) * 0x7FF))
    controller_state.l_stick_state.set_v(int(((-axis.y) + 1) * 0x7FF))


def axis_r_moved(axis):
    controller_state.r_stick_state.set_h(int((axis.x + 1) * 0x7FF))
    controller_state.r_stick_state.set_v(int(((-axis.y) + 1) * 0x7FF))


async def main(args):
    global controller_state

    if not os.path.exists('/dev/input/js0'):
        print('Controller not plugged')
        return

    # parse the spi flash
    if args.spi_flash:
        with open(args.spi_flash, 'rb') as spi_flash_file:
            spi_flash = FlashMemory(spi_flash_file.read())
    else:
        # Create memory containing default controller stick calibration
        spi_flash = FlashMemory()

    controller = Controller.PRO_CONTROLLER

    factory = controller_protocol_factory(controller, spi_flash=spi_flash)
    ctl_psm, itr_psm = 17, 19
    transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                  ctl_psm=ctl_psm,
                                                  itr_psm=itr_psm, capture_file=None,
                                                  device_id=args.device_id)
    controller_state = protocol.get_controller_state()

    with Xbox360Controller(0, axis_threshold=-1) as xcontroller:
        if args.xbox_layout:
            xcontroller.button_a.when_pressed = a_pressed
            xcontroller.button_a.when_released = a_released
            xcontroller.button_b.when_pressed = b_pressed
            xcontroller.button_b.when_released = b_released
            xcontroller.button_x.when_pressed = x_pressed
            xcontroller.button_x.when_released = x_released
            xcontroller.button_y.when_pressed = y_pressed
            xcontroller.button_y.when_released = y_released
        else:
            xcontroller.button_a.when_pressed = b_pressed
            xcontroller.button_a.when_released = b_released
            xcontroller.button_b.when_pressed = a_pressed
            xcontroller.button_b.when_released = a_released
            xcontroller.button_x.when_pressed = y_pressed
            xcontroller.button_x.when_released = y_released
            xcontroller.button_y.when_pressed = x_pressed
            xcontroller.button_y.when_released = x_released
        xcontroller.button_trigger_l.when_pressed = l_pressed
        xcontroller.button_trigger_l.when_released = l_released
        xcontroller.button_trigger_r.when_pressed = r_pressed
        xcontroller.button_trigger_r.when_released = r_released
        xcontroller.button_thumb_l.when_pressed = ls_pressed
        xcontroller.button_thumb_l.when_released = ls_released
        xcontroller.button_thumb_r.when_pressed = rs_pressed
        xcontroller.button_thumb_r.when_released = rs_released
        xcontroller.button_mode.when_pressed = home_pressed
        xcontroller.button_mode.when_released = home_released
        xcontroller.button_start.when_pressed = plus_pressed
        xcontroller.button_start.when_released = plus_released
        xcontroller.button_select.when_pressed = minus_pressed
        xcontroller.button_select.when_released = minus_released

        xcontroller.trigger_l.when_moved = lt_moved
        xcontroller.trigger_r.when_moved = rt_moved
        xcontroller.hat.when_moved = hat_moved
        xcontroller.axis_l.when_moved = axis_l_moved
        xcontroller.axis_r.when_moved = axis_r_moved

        while True:
            try:
                await controller_state.send()
            except NotConnectedError:
                print('Connection Lost')
                return


if __name__ == '__main__':
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device_id')
    parser.add_argument('--spi_flash')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    parser.add_argument('-x', '--xbox_layout', action='store_true')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            main(args)
        )
    except KeyboardInterrupt:
        os._exit(0)
