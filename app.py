from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('rf_flight.pkl', 'rb'))

@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        date_dep = request.form['Dep_Time']
        journey_day = int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').day)
        journey_month = int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').month)

        dep_hour = int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').hour)
        dep_min = int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').minute)

        date_arr = request.form['Arrival_Time']
        arrival_hour = int(pd.to_datetime(date_arr, format='%Y-%m-%dT%H:%M').hour)
        arrival_min = int(pd.to_datetime(date_arr, format='%Y-%m-%dT%H:%M').minute)

        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)

        Total_stops = int(request.form['Stops'])

        airline = request.form['airline']

        Airline_AirIndia, Airline_GoAir, Airline_IndiGo, Airline_JetAirways, Airline_MultipleCarriers, Airline_SpiceJet, Airline_Vistara, Airline_Other = 0, 0, 0, 0, 0, 0, 0, 0
        if airline=='Jet Airways':
            Airline_JetAirways = 1
        elif airline == 'IndiGo':
            Airline_IndiGo = 1
        elif airline == 'Air India':
            Airline_AirIndia = 1
        elif airline == 'Multiple carriers':
            Airline_MultipleCarriers = 1
        elif airline == 'SpliceJet':
            Airline_SpiceJet = 1
        elif airline == 'Vistara':
            Airline_Vistara = 1
        elif airline == 'GoAir':
            Airline_GoAir = 1
        else:
            Airline_Other = 1

        Source_Delhi, Source_Kolkata, Source_Mumbai, Source_Chennai = 0, 0, 0, 0
        Source = request.form['Source']
        if Source == 'Delhi':
            Source_Delhi = 1
        elif Source == 'Kolkata':
            Source_Kolkata = 1
        elif Source == 'Chennai':
            Source_Chennai = 1
        elif Source == 'Mumbai': 
            Source_Mumbai = 1
        
        Destination_Delhi, Destination_Kolkata, Destination_Hydrabad, Destination_Cochin = 0, 0, 0, 0
        Destination = request.form['Destination']
        if Destination == 'Delhi':
            Destination_Delhi = 1
        elif Destination == 'Kolkata':
            Destination_Kolkata = 1
        elif Destination == 'Mumbai':
            Destination_Mumbai = 1
        elif Destination == 'Chennai':
            Destination_Chennai = 1

        
        prediction = model.predict([[Total_stops,
                                     journey_day,
                                     journey_month,
                                     dep_hour,
                                     dep_min,
                                     arrival_hour,
                                     arrival_min,
                                     Duration_hour,
                                     Duration_mins,
                                     Airline_AirIndia,
                                     Airline_GoAir,
                                     Airline_IndiGo,
                                     Airline_JetAirways,
                                     Airline_MultipleCarriers,
                                     Airline_Other,
                                     Airline_SpiceJet,
                                     Airline_Vistara,
                                     Source_Chennai,
                                     Source_Delhi,
                                     Source_Kolkata,
                                     Source_Mumbai,
                                     Destination_Cochin,
                                     Destination_Delhi, 
                                     Destination_Hydrabad,
                                     Destination_Kolkata]])
        


        output = round(prediction[0], 2)
        return render_template('home.html', prediction_text=f'Your Flight Price is Rs. {output}')
    
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)