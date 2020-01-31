# GUI To Graph Pressure

The following PyQT application is designed to be able to set a sampling rate, connect to a serial device and plot the output of the serial device and send an email notification if there is a pressure drop.

The GUI uses the PyQT5 Library with PyQT5 Charts.

MainWindow.py is generated from main.ui
main.py contains the main logic of the GUI and is how the application should be started
email_warning.py has the code to send the warning email.
dummy_pressure.py uses a random number generator to return a number between 0 and 1. 
detect_pressure_drop.py has the code to detect a pressure drop
pressure_test is the unit test for detect_pressure_drop.py
receive_data.py connects to the serial port to get a voltage reading.
