from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from sklearn.externals import joblib
from rest_framework.decorators import api_view
from rest_framework import viewsets

from toronto_restaurants.models import Restaurant
from user_input.models import UserClick
from .models import Users
from .serializers import UsersSerializer

from scipy import special as sp
import random
import math
import numpy as np


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


    def get_probability(self, x):
        #x is a dictionary
        new_x_vector = [x[k] for k in self.domains.keys()]
        new_x_vector.append(len(self.ui_data))
        return t_pdf(new_x_vector, self.df, self.mu, self.T)


class DirichletModel(Model):
    """
    Dirichlet model for discrete dimensions
    alpha is the model parameter
    """

    alpha = None
    m = None
    mu = None

    data = None
    ui_data = None

    names = None
    domains = None

    def __init__(self, var_name, data, alpha):
        self.alpha = alpha
        self.data = data

        self.domains = np.unique(self.data)
        self.names = var_name

        self.m = np.zeros(len(self.domains))

        self.ui_data = np.array([])

        self.mu = (self.alpha + self.m)/(np.sum(self.alpha + self.m))
        #print(self.domains)
        #print(self.m)

        print('Dirichlet model created')


    def update_model(self, observation):
        obs = observation[self.names]
        self.ui_data = np.append(self.ui_data, obs)

        self.m[list(self.domains).index(obs)] += 1
        self.mu = (self.alpha + self.m)/(np.sum(self.alpha + self.m))


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


def generate_colors(n, a=1):
    '''
    generates n random colors in RGBA format
    '''
    ret = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for i in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 255
        ret.append((r/255,g/255,b/255, a))
    return ret

'''
Processes any clicks that haven't been inputted in the model
'''

def process_clicks(username, iteration, queryset):

    # Retrieve user clicks for 'username'
    user_clicks = UserClick.objects.filter(username=username)

    # Load the continuous and discrete models for 'username'
    cm = joblib.load(username+"_cm")
    dm = joblib.load(username+"_dm")

    # Subset unprocessed user clicks and convert to dictionary type
    user_clicks = user_clicks[iteration:]
    user_clicks = [model_to_dict(click) for click in user_clicks]

    # Retrieve the ids of all restaurants our user has clicked, order preserved
    ids = [user_clicks[id]['id'] for id in range(len(user_clicks))]

    # Retrieve information on all restaurants in user click chronological order
    res_clicks = [restaurants[index] for index in ids]

    # Enumerate all restaurant clicks in chronological order (for ML compatibility)
    [res_clicks[i].update({'time_stamp': i+iteration}) for i in range(len(res_clicks))]

    # Filter out the relevant features from all restaurants the user clicked on
    filtered_clicks = [tuple(r[k] for k in ('time_stamp','latitude','longitude','generalCategory')) for r in res_clicks]

    if debug: print(f"{filtered_clicks} was added to the model")

    # Create a numpy array of all our filtered clicks with type 'dtype'
    ui_data = np.array(filtered_clicks, dtype=[('time_stamp', '<i4'),('x', '<f8'), ('y', '<f8'), ('type', '<U30')])

    # Update both models
    for x in ui_data[dims]:
        toadd = {dims[i]: x[i] for i in range(len(dims))}
        cm.update_model(toadd)
        dm.update_model(toadd)
        queryset.update(timestamp = iteration + 1)

    # Save both models for future use
    joblib.dump(cm, username+"_cm")
    joblib.dump(dm, username+"_dm")


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

debug = True

class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer

    def get_queryset(self):
        global restaurants, filtered_restaurants, data, continuous_domain, discrete_domain, dims, debug

        # Retrieve all users
        queryset = Users.objects.all()
        username = self.request.query_params.get('username', None)

        if username is not None:
            # Retrieve information on user 'username'
            queryset = queryset.filter(username=username)

            # If 'username' has signed in
            if queryset.count() != 0:

                # Check how many restaurants the user has clicked on
                user = model_to_dict(queryset[0])
                iteration = user["timestamp"]

                if debug: print(f"Current timestamp: {iteration}")

                # If the user hasn't clicked anything yet
                if not iteration:

                    # Create models for 'username'
                    cm = NWModel(data[dims], 0.1,3)
                    dm = DirichletModel('type', data['type'], np.ones(len(discrete_domain['type'])))

                    # Store the models for future use
                    joblib.dump(cm, username+"_cm")
                    joblib.dump(dm, username+"_dm")

                    # Process the first click
                    process_clicks(username, iteration, queryset)

                else:
                    # Retrieve user clicks for 'username'
                    user_clicks = UserClick.objects.filter(username=username)

                    # If new clicks haven't been processed
                    if len(user_clicks) + 1 - iteration > 0:

                        # Add unprocessed clicks to 'username's model
                        process_clicks(username, iteration, queryset)

        return queryset
