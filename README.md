# Assignment Recommendation System using Collaborative Filtering for Implicit Feedbacks 

This project provides APIs for recommendation of assignments for a user based on implicit feedbacks and recommendation of assignments based on implicit relations using Machine Learning. The API serves for [Alternating Least Squares](https://datasciencemadesimpler.wordpress.com/tag/alternating-least-squares/) algorithm and [Bayesian Personalised Ranking](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf) algorithm. It is used on DCT Academy's ```http://code.dctacademy.com``` code platform

# Dependencies

* python 3.x 
* numpy 1.x
* pandas 0.2x
* scipy 1.1.x
* scikit-learn 0.19.x
* statsmodels 0.9.x
* Cython 0.28.x
* Flask 1.x.x
* gunicorn 19.x.x
* implicit 0.3.x
* requests 2.xx.x
* CUDA 9.x.x (only if GPU)

# Important Files and Folders

```
dct-ml
│   README.md   
│
└───ml-api - Flask APIs serving the recommendation system
|      │
|      └───model
│      |      *_model_als.pkl - Model for Alternating Least Squares
│      |      *_model_bayes.pkl - Model for Bayesian Personalised Ranking
│      |      user_submissions_pivot.csv - Sparse Matrix of Feebacks
│      |      user_submissions.csv - DataFrame of Feebacks
|      |
|      └───app.py - Flask app serving requests
│
└───assets
│      dct_original.sql - original data dump from postgres/prodcution
│      dct.sql - dump used to local model training and testing
│      points.xlsx - Custom grading/confidence system
│      table_columns.csv - tables and their attributes in the database for reference
│      tags.csv - list of all tags for assignments
│
└───local
│      implicit-recsys-assign.ipynb - Notebook for analysis and building model (local)
│
└───production
│      dct-recsys-assign.ipynb - Notebook for analysis and building model (production)
│      dct-recsys-clean.py - Plain python script for building model (production)
│   
└───other
       Other techniques used to solve the same problem. Techniques used include K-Nearest Neighbours,Single Value Decomposition and Matrix Factorisation (not used for production)
```

# Usage - Training/Retraining the model

* ```./production/dct-recsys.ipynb``` - generates ```*_model_als.pkl, *_model_bayes.pkl,  user_submissions_pivot.csv, user_submissions.csv```
    * Trains model and generates required files in ```./ml-api/model/```
* Push changes to the dct-ml-api heroku api repository

# Usage - Request - API

A simple http GET request can be sent to the follwing URL

* Supported Algos:
    1. ```als``` - Alternating Least Squares
    2. ```bayes``` - Bayesian Personalised Ranking

* For recommending assignments to a user:  
    ```http://dct-ml-api.herokuapp.com/recommend?user_id=[id]&algo=['ALGO_NAME']&num=[n]``` where ```id``` is the User ID (integer), ```'ALGO_NAME'``` is the algorithm (string), ```num``` is the    number of recommendations required (integer) 

* For finding related assignments:  
    ```http://dct-ml-api.herokuapp.com/related?assignment_id=[id]&algo=['ALGO_NAME']&num=[n]``` where ```id``` is the Assignment ID (integer), ```'ALGO_NAME'``` is the algorithm (string), ```num``` is the number of recommendations required (integer)

* Sample API Requests:  
    ```http://dct-ml-api.herokuapp.com/related?assignment_id=10&algo=als&num=10```  
    ```http://dct-ml-api.herokuapp.com/recommend?user_id=10&algo=bayes&num=10```

# Usage - Response - API

The API returns a JSON containing the list of Assignment IDs and their correlation with the reqeusted assingment or a user.

* Sample API Response:  
```
{"80": "1.0", "124": "0.4352896", "33": "0.3462197", "50": "0.3163503", "75": "0.27723202", "102": "0.25381687", "27": "0.24722941", "37": "0.23291864", "74": "0.22682238", "62": "0.21501605"}
```

# Credits

* [Aniruddha SG](https://www.linkedin.com/in/aniruddhasg/), Co Founder and Instructor, DCT Academy 
* [Harish Nagasamudra](https://www.linkedin.com/in/harish-nagasamudra-a8512142/), Full Stack Engineer, DCT Academy 

# License

Copyright(c) 2018, [DCT Academy](https://www.dctacademy.com)

# Authors: 

* [Sudhanva Narayana](https://www.sudhanva.me)
* [Aniruddha SG](https://www.dctacademy.com)
* [Harish Nagasamudra](https://www.linkedin.com/in/harish-nagasamudra-a8512142/)
