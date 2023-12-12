from db import initialize_database, assign_affinities, random_affinities
from db_utils import drop_database
from weights.network import run_training_and_plot_results

def main():
    # Drop database if needed. This is useful for testing.
    # drop_database()
    # Initialize database
    # initialize_database()

    # for data set construction only:
    # assign_affinities()
    # for assigning random_affinities() only:
    # random_affinities()

    # for training set construction only:
    run_training_and_plot_results()


if __name__ == "__main__":
    main()
