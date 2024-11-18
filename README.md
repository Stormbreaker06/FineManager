Overview
The Traffic Challan Management System is a Python-based application that uses the Tkinter library for GUI. It streamlines the process of managing traffic violations, vehicle information, and fines. It provides a dashboard for both police officers and drivers to interact with the system for issuing and reviewing challans (traffic fines).

Features
Police Dashboard:
  *Search for vehicle information using a vehicle number.
  *View detailed information about fines and offenses for a vehicle.
  *Add fines for specific offenses.
  *Generate and print a detailed receipt of fines for a vehicle.

Driver Dashboard:
  *View vehicle details, including fines and offense history.
Authentication:

Police login with username and password (validated from police_credentials.csv).
Driver login with a vehicle number.

Database Management:
  *Maintains vehicle information, offenses, and fines in a CSV file (database.csv).
  *Adds new vehicle details if they don’t exist in the database.
Offenses Tracking:
  *Tracks specific offenses such as speeding, reckless driving, parking violations, and more.

How to Use-

Police Login
  Use the Police Login button on the main screen.
  Enter the police credentials (username and password).
  Access the dashboard to:
  Search vehicle details.
  Add fines for traffic offenses.
  Print challan receipts.
Driver Login

  Use the Driver Login button on the main screen.
  Enter the vehicle number to view fines and offense history.
  Adding New Vehicles
  If a vehicle is not found in the database, the system prompts the user to add new vehicle details (owner name and date of registration).
  
File Structure

  *traffic_challan_system.py: Main script for the application.
*police_credentials.csv: Stores police usernames and passwords.
*database.csv: Stores vehicle and offense data.

Known Issues and Limitations
  *Does not currently support online or networked databases.
  *Basic security: Passwords are stored in plain text in the police_credentials.csv file.
  *Fine amounts are manually entered without pre-defined ranges or limits.
Future Enhancements
  *Integrate with a proper database (e.g., MySQL, SQLite).
  *Add password encryption for police credentials.
  *Implement additional offense types or custom fine categories.
  *Include analytics for viewing trends in traffic violations.
  *Add localization for multi-language support.
