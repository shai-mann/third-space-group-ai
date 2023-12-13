# Third Space Group Segmentation
This project is to construct a neural network that can handle affinity generation for the Third Space platform. This is a key aspect of the platform, as the core technology it offers is facilitated social interactions between people who it thinks would be compatible friends.

## Project Structure:

### network.py, model.keras
network.py stores the code to train and use the neural network to make affinity predictions. The model.keras file contains the stored information of the fully trained model (300 epochs).

### db.py, db_utils.py, db_connection.py
db.py handles the interfacing with the database, and uses the other two as helper files.

### Postgres
The postgres package stores SQL scripts to initialize or deconstruct the database, as well as the SQL function to extract the features of a user from the database.
