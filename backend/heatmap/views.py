from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import JsonResponse
from sklearn.externals import joblib
from rest_framework.decorators import api_view
from rest_framework import viewsets

from toronto_restaurants.models import Restaurant
from .serializers import HeatMapSerializer
from .models import HeatMap

import numpy as np
import json

class HeatMapView(viewsets.ModelViewSet):
    serializer_class = HeatMapSerializer

    def get_queryset(self):
        queryset = HeatMap.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        return queryset

'''
Let this block handle all the code related to Model classes and functions
'''
class Model():
    """
    Model is an abstract class which other models will extend. The purpose is to unify function definitions.
    """

    def __init__(self):
        raise Exception("calling abstract class, Model. Need to extent it first and define functions")

    def update_model(self):
        raise NotImplementedError("calling abstract class, Model. Need to extent it first and define functions")

    def get_probability(self):
        raise NotImplementedError("calling abstract class, Model. Need to extent it first and define functions")


class NWModel(Model):
    """
    Normal-Wishart model for continuous dimensions.
    k and v are parameters
    """

    v = 0
    k = 0

    df = 0

    mu_0 = None
    T_0 = None

    mu = None
    T_0 = None

    df = 0

    data = None
    ui_data = None
    domains = None



    def __init__(self, data, k, v):
        self.k = k
        self.v = v
        self.df = v - len(data.dtype.names) + 1
        self.data = data

        # domains of continuous data
        self.domains = get_domains(data)[0]

        self.ui_data = np.empty((0, len(self.domains) + 1))


        # find the mean of the domain for continuous dimentions
        self.mu_0 = np.array([np.mean(self.domains[dname]) for dname in self.domains.keys()])

        # add time dimension
        self.mu_0 = np.append(self.mu_0, 0)


        # for the starting covariance, we make a n+1 x n+1 matrix of zeros (extra dimension for time)
        self.T_0 = np.zeros((len(self.domains) + 1, len(self.domains) + 1))

        # time covariance
        self.T_0[len(self.domains), len(self.domains)] = 1

        for i in range(len(self.domains)):
            #d is domain of ith dimension
            d = self.domains[list(self.domains.keys())[i]]
            self.T_0[i, i] = (d[1] - d[0]) / 10


        self.mu = self.mu_0
        self.T = self.T_0

        self.df = v - len(self.mu_0) + 1

        print("NW model created")
        # print(self.mu_0)
        # print(self.T_0)

    def update_model(self, observation):
        """

        @param observation is a dictionary
        """
        # add the observation to list
        new_observation_vector = [observation[k] for k in self.domains.keys()]
        new_observation_vector.append(len(self.ui_data))
        self.ui_data = np.vstack([self.ui_data, new_observation_vector])

        #update the model if more than one observation has arrived
        if len(self.ui_data) > 1:
            d = len(self.mu)
            df = self.v - d + 1

            n = len(self.ui_data)
            x_bar = sum(self.ui_data)/n

            S = (n-1) * np.cov(np.transpose(self.ui_data))

            self.T_n = self.T_0 + S + ((self.k * n)/(self.k + n)) * np.dot(np.transpose(np.matrix(self.mu_0 - x_bar)), np.matrix(self.mu_0 - x_bar))


            self.v_n = self.v + n
            self.k_n = self.k + n


            new_scale = ((self.k_n + 1)/(self.k_n * (self.v_n - d + 1))) * self.T_n
            new_loc = (self.k * self.mu_0 + n * x_bar)/(self.k + n)
            new_df = self.v_n - d + 1



            self.df = new_df
            self.mu = new_loc
            self.T = new_scale

        print("model updated; number of observations: ", len(self.ui_data))


def get_domains(data):
    '''
    given the structured numpy array (data), this function find the domain
    of each dimention

    @return two dictionaries with {'continuous_dim_name': [min, max] }, {'dicrete_dim_name': list_of_values}

    '''
    continuous_domains = {}
    discrete_domains = {}
    for dim_name in data.dtype.names:
        if data.dtype[dim_name] is np.dtype('float'):
            #print(dim_name, "is continuous")
            continuous_domains[dim_name] = [np.min(data[dim_name]), np.max(data[dim_name])]
        else:
            #print(dim_name, "is discrete")
            discrete_domains[dim_name] = list(np.unique(data[dim_name]))

    return continuous_domains, discrete_domains


'''
this block contains all the functions needed for building and maintaining models
'''
def t_pdf(x, df, mu, sigma):
    d = len(x)

    #final formula is (a/b)*c
    a = sp.gamma((df+d) / 2.0)
    b = sp.gamma(df/2.0) * df**(d/2.0) * math.pi**(d/2.0) * np.linalg.det(sigma)**(1/2.0)
    c = (1 + (1.0/df)*np.dot(np.transpose(x - mu), np.linalg.solve(sigma, (x - mu))))**(-(df + d)/2.0)

    ans = (a/b)*c

    return ans

'''
Filters only relevant categories for all restaurants once, and determines
the continous and discrete domains of our data.
'''

# Retrieve and format all restaurants form queryObject to dictionaries
restaurants = Restaurant.objects.all()
restaurants = [model_to_dict(restaurant) for restaurant in restaurants]

# Filter out the latitude, longitude, and general category from all restaurants
filtered_restaurants = [tuple(r[k] for k in ('latitude','longitude','generalCategory')) for r in restaurants]

# Create a numpy array of all our filtered restaurants with type 'dtype'
data = np.array(filtered_restaurants, dtype=[('x', '<f8'), ('y', '<f8'), ('type', '<U30')])

continuous_domain, discrete_domain = get_domains(data)
dims = ['x', 'y', 'type']

'''
Loads model for 'username' and calculates the probability for each
[latitude, longitude] coordinate. This information is then serialized and
displayed in json format.
'''

@api_view(['GET'])
def heatmap_list(request):
    global restaurants, filtered_restaurants, data, continuous_domain, discrete_domain, dims

    username = request.GET['username']

    #Nw continuous model for 'username' is retrieved from models folder
    cm = joblib.load(username+"_cm")

    # Retrieve all longitude and latitude coordinates
    all_x = np.linspace(continuous_domain['x'][0], continuous_domain['x'][1], 100)
    all_y = np.linspace(continuous_domain['y'][0], continuous_domain['y'][1], 100)

    # Array of Heatmap models, describing probabilities for each coordinate pair
    heatmap = [HeatMap(x=x,y=y,probability=cm.get_probability({'x': x, 'y': y})) for x in all_x for y in all_y]

    # Serialize all fields in Heatmap model
    serializer = HeatMapSerializer(heatmap, many=True)

    # Return the serialized information in json format
    return JsonResponse(serializer.data, safe=False)
