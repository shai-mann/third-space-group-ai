# Third Space Group Segmentation
This project is to construct a neural network that can handle group segmentation for the Third Space platform. This is a key aspect of the platform, as the core technology it offers is facilitated social interactions between people who it thinks would be compatible friends.

## Project Structure:

### Models
The models package stores database models, for internal use in the segmentation and training process.

### Weights
The weights package stores files related to the neural network, which is trained to suggest weights.

### db.py
db.py handles the interfacing with the database.

### Postgres
The postgres package stores SQL scripts to initialize or deconstruct the database.
