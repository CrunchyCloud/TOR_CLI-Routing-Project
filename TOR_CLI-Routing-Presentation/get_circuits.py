from stem import Signal
from stem.control import Controller

try:
    with Controller.from_port(port=9051) as controller:  # Default Tor control port
        controller.authenticate()  # Make sure we authenticate
        circuits = controller.get_circuits()  # Retrieve the list of circuits

        # Output circuit information
        for circuit in circuits:
            print(f"Circuit ID: {circuit.id}")
            print(f"Status: {circuit.status}")
            for path in circuit.path:
                print(f"  {path}")
            print("-" * 40)
except Exception as e:
    print(f"Error fetching Tor circuit info: {e}")

