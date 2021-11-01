import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import os
warnings.filterwarnings("ignore")

class Model(object):
    def __init__(self):
        #Load dataset 
        self.dataset=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+'/input/train.csv')

        #Filtering out fields with low correlationship to price range
        self.corr = self.dataset.corr()
        top_fields_corr = self.corr.sort_values(by=["price_range"],ascending=False).iloc[0].sort_values(ascending=False).head(6)
        self.top_fields = []
        for index,val in top_fields_corr.iteritems():
            self.top_fields.append(index)
        self.dataset =self.dataset.drop(columns = [col for col in self.dataset if col not in self.top_fields])


        #Setting x and y. Splitting data into train and test
        X = self.dataset.drop('price_range',axis=1)
        y = self.dataset['price_range'].values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33, random_state=101)


        #Training model with KNN
        self.knn = KNeighborsClassifier(n_neighbors=10)
        self.knn.fit(self.X_train,self.y_train)
        self.knn.score(self.X_test,self.y_test)
        pred = self.knn.predict(self.X_test)
        print(classification_report(self.y_test,pred))


    def show_heatmap(self):
        

        #Show correlation map
        
        fig = plt.figure(figsize=(9,7))
        r = sns.heatmap(self.corr, cmap='Purples')
        r.set_title("Correlation")

        plt.show()

    def show_boxplot(self):
        

        #Show boxplot for ram and price_range
            
        fig1 = plt.figure(figsize=(9,7))
        r1 = sns.boxplot(x="price_range", y="ram", data=self.dataset)
        plt.show()

    def show_pointplot(self):
        

        #Show pointplot
        sns.pointplot( x="price_range", y="battery_power", data=self.dataset)
        plt.show()

    def show_scatterplot(self):
        

        #Show scatterplot
        sns.scatterplot(data = self.dataset, x = "ram",y = "battery_power",  hue='price_range')
        plt.show()


    def test_model(self,pred):

        #Load test data and predict
        data_test=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+'/input/test.csv')
        data_test =data_test.drop(columns = [col for col in data_test if col not in self.top_fields])
        predicted_price=self.knn.predict(data_test)
        data_test['price_range']=predicted_price
        matrix = confusion_matrix(self.y_test,pred)
        plt.figure(figsize = (10,7))
        sns.heatmap(matrix,annot=True, fmt = "d")
        plt.show()
        

    def predict(self,battery_power,int_memory,px_height,px_width,ram):
        
        #Input custom data
        dict = {'battery_power':[battery_power],
                'int_memory':[int_memory],
                'px_height':[px_height],
                'px_width':[px_width],
                'ram':[ram],
               }
        predicted_price=self.knn.predict(pd.DataFrame(dict))
        return predicted_price[0]




