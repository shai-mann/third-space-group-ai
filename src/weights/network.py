"""
This is where code related to the neural network goes. The network has the goal
of optimizing the weight selection process such that groups are selected well.
"""
import sys
sys.path.insert(0, 'src')
from db import Database
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

def run_training_and_plot_results():
        """
        Runs the training process and plots the results.
        """
        # Initialize database and train the network
        network = Network()
        history = network.train()

        while (True):
             age_difference = input("What is their age difference? Type in a number ")
             buddies = input("Are they buddies? Type 1 or 0. ")
             friends = input("Are they friends? Type 1 or 0. ")
             common_friends = input("Do they have any common friends? Type in a number ")
             common_hobbies = input("Do they have any common hobbies? Type in a number ")
             common_groups = input("Do they have any common groups? Type in a number ")
             
             features = [int(age_difference), int(buddies), int(friends), int(common_friends), int(common_hobbies), int(common_groups)]
             print(network.predict([features]))
        db = Database()

        db.plot_results(history)

class Network:

    def __init__(self) -> None:
         self.model = Sequential()
         self.db = Database()

    def train(self):
        """
        Trains the model to understand user affinities.
        """
        db = self.db
        x_train, y_train = db.prepare_training_data()
        y_train = to_categorical(y_train)  # Convert y_train to categorical

        x_test, y_test = db.get_test_data()  # Fetch test data
        y_test = to_categorical(y_test)  # Convert y_test to categorical

        model = self.model
        model.add(Dense(128, input_shape=(len(x_train[0]),)))  # Adjust input shape based on features
        model.add(Dense(64, activation='relu'))  # 'relu' is generally used in hidden layers
        model.add(Dense(y_train.shape[1], activation='softmax'))  # Output layer size based on classes

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=300, validation_data=(x_test, y_test), verbose=1)

        # Evaluate the model on test data
        score = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        return history

    def predict(self, user):
        """
        Assigns an affinity to a user based on the model.
        """
        print('user:', user if user is not None else 'None')
        return self.model.predict(user)



