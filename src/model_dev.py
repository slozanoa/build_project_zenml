import logging
from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression

class Model(ABC):
    @abstractmethod
    def train(self, X_train, y_train):
        """
        Trains the model
        Args:
            X_train: training data
            y_train: training labels
            return
            None
        """
        pass

class LinearRegressionModel(Model):
    """
    Linear regression 
    """
    def train(self, X_train, y_train, **kwargs):
        """
        trains the model
        Args:
            X_train: training data
            y_labels: trainig labels

            Returns:
                None
        """

        try: 
            reg = LinearRegression(**kwargs)
            reg.fit(X_train,y_train)
            logging.info("model training completed")
            return reg
        except Exception as e:
            logging.error("Error in training model: {}".format(e))
            raise e