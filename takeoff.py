# drone/takeoff.py

import asyncio


async def takeoff_drone(drone, altitude=5):
    """
    Takeoff to a safe altitude.

    Safety:
    - Uses controlled altitude.
    - Waits for stable takeoff.
    """

    try:

        print(f"🚀 Taking off to {altitude} meters...")

        # Set target altitude
        await drone.action.set_takeoff_altitude(altitude)

        # Start takeoff
        await drone.action.takeoff()

        # Wait for stabilization
        await asyncio.sleep(10)

        print("✅ Takeoff completed")

        return True

    except Exception as e:

        print(f"❌ Takeoff failed: {e}")

    return False