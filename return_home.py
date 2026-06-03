# drone/return_home.py

import asyncio


async def return_home(drone):
    """
    Return drone to launch position using RTL.

    Safety:
    - Uses ArduPilot RTL mode.
    - Allows autopilot to safely navigate home.
    """

    try:

        print("🏠 Returning home...")

        await drone.action.return_to_launch()

        # Wait for RTL sequence
        await asyncio.sleep(20)

        print("✅ RTL command sent")

        return True

    except Exception as e:

        print(f"❌ RTL failed: {e}")

    return False