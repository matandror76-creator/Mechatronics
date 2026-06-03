# drone/goto.py

import asyncio
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate approximate distance between two GPS points.
    """

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    ) * 111139


async def goto_location(
    drone,
    latitude,
    longitude,
    altitude,
    timeout=60
):
    """
    Fly drone to GPS location using GUIDED mode.

    Safety:
    - Includes timeout protection.
    - Verifies arrival distance.
    - Prevents infinite flight state.
    """

    try:

        print("🧭 Flying to target location...")

        # Send goto command
        await drone.action.goto_location(
            latitude,
            longitude,
            altitude,
            0
        )

        start_time = asyncio.get_event_loop().time()

        while True:

            # Timeout failsafe
            current_time = asyncio.get_event_loop().time()

            if current_time - start_time > timeout:

                print("❌ GOTO timeout reached")
                return False

            async for position in drone.telemetry.position():

                current_lat = position.latitude_deg
                current_lon = position.longitude_deg

                distance = calculate_distance(
                    current_lat,
                    current_lon,
                    latitude,
                    longitude
                )

                print(f"📍 Distance to target: {distance:.2f} m")

                # Arrival threshold
                if distance < 2:

                    print("✅ Target reached")
                    return True

                break

            await asyncio.sleep(1)

    except Exception as e:

        print(f"❌ GOTO failed: {e}")

    return False