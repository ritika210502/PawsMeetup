import pandas as pd
from .models import Dog
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


#Prepares the data for machine learning by converting categorical variables to numerical codes.
def preprocess_data():
    dogs=pd.DataFrame(list(Dog.objects.all().values()))

    if 'breed_id' in dogs.columns:
        dogs['breed'] = dogs['breed_id']      # Handle ForeignKey fields

    else:
        raise KeyError("Expected 'breed_id' column is missing from the DataFrame")

    # Convert categorical fields to numeric codes
    dogs['size']=dogs['size'].astype('category').cat.codes
    dogs['energy_level']=dogs['energy_level'].astype('category').cat.codes
    dogs['temperament']=dogs['temperament'].astype('category').cat.codes

    dogs.drop(columns=['breed_id'], inplace=True)

    return dogs

#Trains a K-Nearest Neighbors model using the features of the dogs.
def train_knn_model(dogs):
    features = dogs[['breed', 'size', 'energy_level', 'temperament']]
    labels = dogs['id']
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(features, labels)
    return model, scaler

#retrieves the target dog's features, scales them, and finds similar dogs.
def match_dogs_knn(dog_id, model, scaler):
    target_dog = Dog.objects.get(id=dog_id)
    dogs = preprocess_data()
    
    # Prepare the features DataFrame for both model and target dog
    features = dogs[['breed', 'size', 'energy_level', 'temperament']]
    features_scaled = scaler.transform(features)

    # Convert target dog attributes to numeric codes
    target_features = [
        target_dog.breed_id,  # Ensure using 'breed_id' if ForeignKey
        target_dog.size,
        target_dog.energy_level,
        target_dog.temperament
    ]

    # Convert target features to a DataFrame with the same columns as training data
    target_df = pd.DataFrame([target_features], columns=['breed', 'size', 'energy_level', 'temperament'])
    target_df = target_df.apply(lambda x: x.astype('category').cat.codes)  # Convert to numeric codes
    target_features_scaled = scaler.transform(target_df)  # Scale the target features

    # Find the nearest neighbors
    distances, indices = model.kneighbors(target_features_scaled)
    matched_dogs = dogs.iloc[indices[0]]
    return matched_dogs

