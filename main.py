# main.py

import asyncio
import threading

from server.server import app, set_queue, set_loop

from drone.connect import connect_drone
from drone.health import check_health
from drone.arm import arm_drone
from drone.takeoff import takeoff_drone
from drone.goto import goto_location
from drone.return_home import return_home


# -----------------------------------
# START FLASK SERVER IN SEPARATE THREAD
# -----------------------------------

def start_flask():
    """
    Run Flask server separately from MAVSDK asyncio loop.

    This prevents blocking MAVSDK telemetry/tasks.
    """

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


# -----------------------------------
# MAIN MISSION LOOP
# -----------------------------------

async def mission_loop(target_queue):

    print("🚀 Mission controller started")

    while True:

        print("\n📡 Waiting for emergency request...")

        # Wait until Flask receives GPS target
        target = await target_queue.get()

        print(f"\n🎯 New mission target: {target}")

        drone = None

        try:

            # -----------------------------------
            # CONNECT TO PIXHAWK
            # -----------------------------------

            drone = await connect_drone()

            if not drone:
                print("❌ Connection failed")
                continue

            # -----------------------------------
            # HEALTH CHECK
            # -----------------------------------

            health_ok = await check_health(drone)

            if not health_ok:
                print("❌ Health check failed")
                continue

            # -----------------------------------
            # ARM DRONE
            # -----------------------------------

            arm_ok = await arm_drone(drone)

            if not arm_ok:
                print("❌ Arming failed")
                continue

            # -----------------------------------
            # TAKEOFF
            # -----------------------------------

            takeoff_ok = await takeoff_drone(
                drone,
                altitude=5
            )

            if not takeoff_ok:
                print("❌ Takeoff failed")
                continue

            # -----------------------------------
            # GOTO TARGET
            # -----------------------------------

            goto_ok = await goto_location(
                drone,
                latitude=target["lat"],
                longitude=target["lon"],
                altitude=target["alt"]
            )

            if not goto_ok:

                print("❌ Failed reaching target")

                # Safety fallback
                await return_home(drone)

                continue

            print("✅ Target reached")

            # -----------------------------------
            # FUTURE PAYLOAD STAGE
            # -----------------------------------

            print("📦 Payload stage placeholder")

            # Future:
            # obstacle_ok = await check_obstacles()
            # await lower_winch()

            # -----------------------------------
            # RETURN HOME
            # -----------------------------------

            await return_home(drone)

            print("🏠 Drone returned home")

        except Exception as e:

            print(f"❌ Mission error: {e}")

            # Safety fallback
            try:
                if drone:
                    await return_home(drone)
            except:
                pass

        finally:

            print("🛑 Mission cycle ended")


# -----------------------------------
# MAIN ENTRY
# -----------------------------------

async def main():

    # Shared communication queue
    target_queue = asyncio.Queue()


    # Get current asyncio loop
    loop = asyncio.get_running_loop()

    # Give Flask access to queue + loop
    set_queue(target_queue)
    set_loop(loop)

    # Start Flask separately
    flask_thread = threading.Thread(
        target=start_flask,
        daemon=True
    )

    flask_thread.start()

    # Start mission controller
    await mission_loop(target_queue)


if __name__ == "__main__":

    asyncio.run(main())