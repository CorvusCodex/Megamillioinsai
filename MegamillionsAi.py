# Import necessary libraries
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from art import text2art

# Function to print the introduction of the program
def print_intro():
    ascii_art = text2art("MegamillionsAi")
    # Print the introduction and ASCII art
    print("============================================================")
    print("MegamillionsAi")
    print("Created by: Corvus Codex")
    print("Github: https://github.com/CorvusCodex/")
    print("Licence : MIT License")
    print("Support my work:")
    print("BTC: bc1q7wth254atug2p4v9j3krk9kauc0ehys2u8tgg3")
    print("ETH & BNB: 0x68B6D33Ad1A3e0aFaDA60d6ADf8594601BE492F0")
    print("Buy me a coffee: https://www.buymeacoffee.com/CorvusCodex")
    print("============================================================")
    print(ascii_art)
    print("Megamillions prediction artificial intelligence")

# Function to load data from a file and preprocess it
def load_data():
    # Load data from file, ignoring white spaces and accepting unlimited length numbers
    data = np.genfromtxt('data.txt', delimiter=',', dtype=int)
    # Replace all -1 values with 0
    data[data == -1] = 0
    # Split data into training and validation sets
    train_data = data[:int(0.8*len(data))]
    val_data = data[int(0.8*len(data)):]
    # Get the maximum value in the data
    max_value = np.max(data)
    return train_data, val_data, max_value

# Function to create the model
def create_model(num_features, max_value):
    # Create a sequential model
    model = keras.Sequential()
    # Add an Embedding layer, LSTM layer, and Dense layer to the model
    model.add(layers.Embedding(input_dim=max_value+1, output_dim=256000))
    model.add(layers.LSTM(1024000))
    model.add(layers.Dense(num_features, activation='softmax'))
    # Compile the model with categorical crossentropy loss, adam optimizer, and accuracy metric
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Function to train the model
def train_model(model, train_data, val_data):
    # Fit the model on the training data and validate on the validation data for 100 epochs
    history = model.fit(train_data, train_data, validation_data=(val_data, val_data), epochs=100)

def predict_numbers(model, val_data, num_features):
    # Predict probabilities for the first five numbers (excluding the Megamillions column)
    predictions_first_five = model.predict(val_data[:, :-1])

    # Get the indices that would sort the predictions, but we only want the top 5
    indices = np.argsort(predictions_first_five, axis=1)[:, -(num_features - 1):]

    # Clip indices to ensure they're within the valid range of the sliced val_data
    indices = np.clip(indices, 0, val_data[:, :-1].shape[1] - 1)

    # Get the actual predicted numbers (not just their probabilities) based on the indices
    predicted_numbers = np.take_along_axis(val_data[:, :-1], indices, axis=1)

    # Predict the Megamillions number (1-26) separately
    megaball_predictions = model.predict(val_data[:, -1:])  # Use only the last column
    megaball_predictions = np.squeeze(megaball_predictions)  # Remove an unnecessary dimension


    # Get the index of the highest probability output for the Megamillions (0-26)
    megaball_index = np.argmax(megaball_predictions, axis=-1)
    # Shift and scale the index to get a Megamillions number between 1 and 26
    megaball_number = (megaball_index % 26) + 1

    # Add the predicted Megamillions number to the other predictions
    predicted_numbers = np.insert(predicted_numbers, num_features - 1, megaball_number, axis=1)

    return predicted_numbers



# Function to print the predicted numbers
def print_predicted_numbers(predicted_numbers):
   # Print a separator line and "Predicted Numbers:"
   print("============================================================")
   print("Predicted Numbers:")
   # Print only the first row of predicted numbers
   print(', '.join(map(str, predicted_numbers[0])))
   print("============================================================")
   print("Buy me a coffee or invest in powerfull equipment: https://www.buymeacoffee.com/CorvusCodex")
   print("============================================================")

# Main function to run everything   
def main():
   # Print introduction of program 
   print_intro()
   
   # Load and preprocess data 
   train_data, val_data, max_value = load_data()
   
   # Get number of features from training data 
   num_features = train_data.shape[1]
   
   # Create and compile model 
   model = create_model(num_features, max_value)
   
   # Train model 
   train_model(model, train_data, val_data)
   
   # Predict numbers using trained model 
   predicted_numbers = predict_numbers(model, val_data, num_features)
   
   # Print predicted numbers 
   print_predicted_numbers(predicted_numbers)

# Run main function if this script is run directly (not imported as a module)
if __name__ == "__main__":
   main()
