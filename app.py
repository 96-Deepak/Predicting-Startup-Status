from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import pickle
import numpy as np

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("home_page.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()

def index():
    if request.method == 'POST':
        try:
            #reading input from front end

            founded_at = int(request.form['founded_at'])           
            funding_rounds = float(request.form['funding_rounds'])
            funding_total_usd = float(request.form['funding_total_usd'])
            milestones = float(request.form['milestones'])
            relationships = float(request.form['relationships'])
            lat = float(request.form['lat'])
            lng = float(request.form['lng'])
            category_code = request.form.get('category_code')
            country_code = request.form.get('country_code')

            first_list = []
            first_list.append(founded_at)
            first_list.append(funding_rounds)
            first_list.append(funding_total_usd)
            first_list.append(milestones)
            first_list.append(relationships)
            first_list.append(lat)
            first_list.append(lng)

            #category_code Data 

            category_list = ['category_code_biotech', 'category_code_consulting', 'category_code_ecommerce',
                 'category_code_education', 'category_code_enterprise','category_code_games_video',
                 'category_code_hardware', 'category_code_mobile', 'category_code_network_hosting',
                 'category_code_other', 'category_code_public_relations','category_code_search',
                 'category_code_software', 'category_code_web']
            category_code = category_code
            cat_li = []

            for i in category_list:
                if i == category_code:
                    i = 1
                    cat_li.append(i)
                else:
                    i = 0
                    cat_li.append(i)
            # for i in cat_li:
            #     print(i, end=' ')

            #country_code data

            country_list = ['country_code_BRA', 'country_code_CAN', 'country_code_DEU', 
            'country_code_ESP', 'country_code_FRA','country_code_GBR', 'country_code_IND', 
            'country_code_IRL', 'country_code_ISR', 'country_code_NLD', 'country_code_USA',
            'country_code_other']  
            country_code = country_code
            con_li = []
            for i in country_list:
                if i == country_code:
                    i = 1
                    con_li.append(i)
            #         print(i)
                else:
                    i = 0
                    con_li.append(i)
            #         print(i)

            # for i in con_li:
            #     print(i, end=' ')
            # print(country_list)

            #all data concating or merging with one list and provide to model

            final_list = first_list + cat_li + con_li

            filename = 'new_startup_model.pickle'
            loaded_model = pickle.load(open(filename,'rb'))
            predication_model = loaded_model.predict([final_list])
            df = predication_model.astype(int)
            # for i in predication_model:
            #     df = i
            # df = np.int(predication_model)
           
            if df == 1:
                return render_template('output_page.html', model_output = "Operating")
            elif df == 2:
                return render_template('output_page.html', model_output = "Acquired")
            elif df == 3:
                return render_template('output_page.html', model_output = "Closed")
            elif df == 4:
                return render_template('output_page.html', model_output = "IPO")

            return render_template('output_page.html', model_output = df)


        except Exception as e:
            print("The Exception is ", e)
            return "Something is going wrong....!"

    else:
        return render_template('home_page.html')

if __name__ == '__main__':
    app.run(debug=True)
