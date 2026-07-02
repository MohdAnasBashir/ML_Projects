import sys
import os 
from dataclasses import dataclass
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_model


@dataclass
class ModelTrainerConfig:
    trainer_model_file_path=os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        ##intilaise the object of model training config
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("spliting training test input data")

            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],train_arr[:,-1],
                test_arr[:,:-1],test_arr[:,-1]
            )

            models={
                "LinearRegression":LinearRegression(),
                "Lasso":Lasso(),
                "Ridge":Ridge(),
                "K-Neighbors Regressor":KNeighborsRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "RandomForestRegressor":RandomForestRegressor(),
                "XGBRegressor":XGBRegressor(),
                "AdaBoostRegressor":AdaBoostRegressor(),
                "GradientBoostRegressor ":GradientBoostingRegressor()
            }
            params = {

                "LinearRegression": {},

                "Lasso": {
                    "alpha": [0.01, 0.1, 1]
                },

                "Ridge": {
                    "alpha": [0.01, 0.1, 1]
                },

                "K-Neighbors Regressor": {
                    "n_neighbors": [3, 5, 7],
                    "weights": ["uniform", "distance"]
                },

                "Decision Tree": {
                    "max_depth": [None, 5, 10],
                    "min_samples_split": [2, 5]
                },

                "RandomForestRegressor": {
                    "n_estimators": [100, 200],
                    "max_depth": [None, 10, 20]
                },

                "XGBRegressor": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.05, 0.1],
                    "max_depth": [3, 5]
                },

                "AdaBoostRegressor": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.05, 0.1]
                },

                "GradientBoostRegressor": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.05, 0.1],
                    "max_depth": [3, 5]
                }

            }

            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)

           ##now we need to  select the best score from the dictionary
            best_model_score = max(model_report.values())

            ##now get taht models name
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            #threshold for perfoprmance
            if best_model_score<0.6:
                raise CustomException("No best model found", sys)
            
            logging.info(f"Best model found on both training and testing dataset")

            ##now weneed to save the model
            save_object(
                file_path=self.model_trainer_config.trainer_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(X_test)

            r2_Square=r2_score(y_test,predicted)

            return r2_Square
        except Exception as e:
            raise CustomException(e, sys)

