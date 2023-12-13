"""
This is where code related to the neural network goes. The network has the goal
of optimizing the weight selection process such that groups are selected well.
"""
import numpy as np
import sys
sys.path.insert(0, 'src')
from db import Database
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

def run_training_and_plot_results():
    """
    Runs the training process, plots the results, and saves the model.
    """
    # Initialize database and train the network
    network = Network()
    # history = network.train()

    # Save the trained model
    # network.save()
    network.load()
    
    # Print the final loss and MAE for the training and validation sets
    # final_train_loss, final_train_mae = history.history['loss'][-1], history.history['mae'][-1]
    # final_val_loss, final_val_mae = history.history['val_loss'][-1], history.history['val_mae'][-1]
    # print(f"Final Training Loss: {final_train_loss:.4f}")
    # print(f"Final Training MAE: {final_train_mae:.4f}")
    # print(f"Final Validation Loss: {final_val_loss:.4f}")
    # print(f"Final Validation MAE: {final_val_mae:.4f}")

    # Plot the training and validation loss and MAE
    # db = Database()
    # db.plot_results(history)

    while True:
        age_difference = input("What is their age difference? Type in a number ")
        buddies = input("Are they buddies? Type 1 or 0. ")
        friends = input("Are they friends? Type 1 or 0. ")
        common_friends = input("Do they have any common friends? Type in a number ")
        common_hobbies = input("Do they have any common hobbies? Type in a number ")
        common_groups = input("Do they have any common groups? Type in a number ")
        features = np.array([[int(age_difference), int(buddies), int(friends), int(common_friends), int(common_hobbies), int(common_groups)]])
        prediction = network.predict(features)
        print(f"Predicted Affinity Score: {prediction[0][0]:.2f}")

class Network:

    def __init__(self) -> None:
         self.model = Sequential()
         self.db = Database()

    def train(self):
        x_train, y_train, x_test, y_test = self.db.prepare_data()
        
        # Normalize y to be between 0 and 1
        y_train = y_train / 100.0
        y_test = y_test / 100.0

        self.model.add(Dense(128, input_shape=(6,), activation='relu', kernel_regularizer=l2(0.001)))
        self.model.add(Dropout(0.3))  # Slightly reduce dropout
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.3))  # Slightly reduce dropout
        # Output layer with sigmoid activation for output between 0 and 1
        self.model.add(Dense(1, activation='sigmoid'))

        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-5)
        model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)

        history = self.model.fit(
            x_train, y_train, epochs=200,  # Reduced the number of epochs
            validation_data=(x_test, y_test), 
            batch_size=32, 
            verbose=1,
            callbacks=[early_stopping, reduce_lr, model_checkpoint]  # Added callbacks
        )

        # Load the best weights saved by the ModelCheckpoint
        self.model.load_weights('best_model.h5')

        return history

    def predict(self, features):
        # Scale features between 0 and 1 if not already done
        prediction = self.model.predict(features)
        # Scale the prediction back to the original range (0 to 100)
        prediction = prediction * 100
        # Round the prediction to the nearest integer
        return np.round(prediction).astype(int)
    
    def save(self):
        self.model.save("src/model.keras")

    def load(self):
        self.model = load_model("src/model.keras")

