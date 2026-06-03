# drone/health.py

async def check_health(drone):
    """
    Check drone health before flight.

    Safety:
    - Prevents arming without GPS.
    - Prevents flight if sensors are unhealthy.
    """

    try:

        print("🩺 Checking drone health...")

        async for health in drone.telemetry.health():

            print(f"GPS OK: {health.is_global_position_ok}")
            print(f"HOME OK: {health.is_home_position_ok}")
            print(f"ARMABLE: {health.is_armable}")

            # Safety conditions
            if (
                health.is_global_position_ok
                and health.is_home_position_ok
                and health.is_armable
            ):

                print("✅ Health check passed")
                return True

            print("❌ Health check failed")
            return False

    except Exception as e:

        print(f"❌ Health check error: {e}")

    return False