import asyncio
import os
import requests
from winrt.windows.devices import radios


def main():
    url = "http://www.kite.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as exception:
        name_of_router = 'Pfizer_5G_chIP_Gates'
        os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    asyncio.run(bluetooth_power(False))
    asyncio.run(bluetooth_power(True))


async def bluetooth_power(turn_on):
    all_radios = await radios.Radio.get_radios_async()
    for this_radio in all_radios:
        if this_radio.kind == radios.RadioKind.BLUETOOTH:
            if turn_on:
                result = await this_radio.set_state_async(radios.RadioState.ON)
            else:
                result = await this_radio.set_state_async(radios.RadioState.OFF)


if __name__ == '__main__':
    main()
