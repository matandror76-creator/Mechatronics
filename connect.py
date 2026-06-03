# drone/connect.py

from mavsdk import System


async def connect_drone():
    """
    Connect to Pixhawk through serial connection.

    Safety:
    - Verifies successful connection before continuing.
    - Returns None if connection fails.
    """

    try:

        drone = System()

        print("🔌 Connecting to Pixhawk...")

        await drone.connect(
            system_address="serial:///dev/ttyACM0:115200"
        )

        async for state in drone.core.connection_state():

            if state.is_connected:

                print("✅ Connected to Pixhawk")
                return drone

    except Exception as e:

        print(f"❌ Connection failed: {e}")

    return None