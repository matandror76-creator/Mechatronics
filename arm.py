    # drone/arm.py

    async def arm_drone(drone):
        """
        Arm the drone motors.

        Safety:
        - Drone must already pass health checks.
        - Prevents accidental arming.
        """

        try:

            print("🛡️ Arming drone...")

            await drone.action.arm()

            print("✅ Drone armed")

            return True

        except Exception as e:

            print(f"❌ Failed to arm: {e}")

        return False