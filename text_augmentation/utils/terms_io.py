import pickle


def save_terms_as_pickle(data, pickle_dir):
    """Serialize data into pickle file."""
    print("Saving terms to pickle file...")
    try:
        file = open(pickle_dir, 'wb')
        pickle.dump(data, file)
        file.close()
    except:
        raise Exception("Failed to save terms in pickle.")
    print("Terms saved.")


def loads_terms_from_pickle(pickle_dir):
    """Load serialized data from pickle file."""
    print("Loading terms from pickle file...")
    try:
        file = open(pickle_dir, 'rb')
        data = pickle.load(file)
        file.close()
    except:
        raise Exception("Failed to load terms from pickle.")
    print("Terms loaded.")

    return data


if __name__ == '__main__':

    pickle_dir = './terms.pkl'

    data = list(range(0, 100))
    save_terms_as_pickle(data, pickle_dir)

    # data = loads_terms_from_pickle(pickle_dir)
    # print(data)