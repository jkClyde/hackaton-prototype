from flask import Flask, render_template,url_for,flash, redirect
from forms import LoginForm, RegistrationForm
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
import numpy as np


app = Flask(__name__)

app.config['SECRET_KEY']='clyde_test'

dummy_data = [{   "barangay_name": "Lubas",        "population": 1231,        "stunted": 5,        "overweight": 10,        "underweight": 3    }, 
              {        "barangay_name": "Puguis",        "population": 2408,        "stunted": 7,        "overweight": 13,        "underweight": 1    },    
              {        "barangay_name": "Poblacion",        "population": 3089,        "stunted": 3,        "overweight": 8,        "underweight": 2    },    
              {        "barangay_name": "Cruz",        "population": 1867,        "stunted": 6,        "overweight": 9,        "underweight": 4    },    
              {        "barangay_name": "Wangal",        "population": 1934,        "stunted": 4,        "overweight": 11,        "underweight": 2    }]



# Extract the values from the dummy data
populations = [data['population'] for data in dummy_data]
stunted_rates = [data['stunted'] for data in dummy_data]
overweight_rates = [data['overweight'] for data in dummy_data]
underweight_rates = [data['underweight'] for data in dummy_data]

  # Create a list of years from 2010 to 2014
years = range(2010, 2015)

    # Create a list of stunted rates for each year
stunted_rates = [5, 7, 3, 6, 4]


# Create a list of barangay names
barangays = [data['barangay_name'] for data in dummy_data]


# Create a bar chart of the populations by barangay
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
ax.bar([data['barangay_name'] for data in dummy_data], [data['population'] for data in dummy_data])
ax.set_title('Population by Barangay')
ax.set_xlabel('Barangay')
ax.set_ylabel('Population')
output = io.BytesIO()
canvas.print_png(output)
plot_url1 = base64.b64encode(output.getvalue()).decode('utf8')

# Create a pie chart of the prevalence of stunted, overweight, and underweight rates across all barangays
labels = ['Stunted', 'Overweight', 'Underweight']
sizes = [sum(stunted_rates) / len(dummy_data), sum(overweight_rates) / len(dummy_data), sum(underweight_rates) / len(dummy_data)]
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
ax.set_title('Prevalence of Stunted, Overweight, and Underweight Rates Across All Barangays')
output = io.BytesIO()
canvas.print_png(output)
plot_url2 = base64.b64encode(output.getvalue()).decode('utf8')




@app.route("/")
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET','POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Create for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    form = RegistrationForm()
    return render_template('dashboard.html', title='dashboard')

@app.route("/layout")
def layout():
    return render_template('layouts/layout.html')

@app.route("/form")
def form():
       return render_template('layouts/form.html',title='form')

@app.route("/sidebar")
def sidebar():
    return render_template('layouts/sidebar.html')

@app.route("/table")
def table():
    return render_template('layouts/table.html',title='table')

@app.route("/import")
def save():
    return render_template('layouts/import.html',title='Import')

@app.route("/users")
def users():
    return render_template('layouts/users.html',title='Users')    

@app.route("/analytics")
def analytics():
    # Generate the charts
    populations = [data['population'] for data in dummy_data]
    plt.bar([data['barangay_name'] for data in dummy_data], populations)
    plt.title('Population by Barangay')
    plt.xlabel('Barangay')
    plt.ylabel('Population')
    plt.savefig('static/population_chart.png', transparent=True)
    plt.clf()

    # Create a pie chart of the prevalence of stunted, overweight, and underweight rates across all barangays
    labels = ['Stunted', 'Overweight', 'Underweight']
    sizes = [sum(stunted_rates) / len(dummy_data), sum(overweight_rates) / len(dummy_data), sum(underweight_rates) / len(dummy_data)]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Prevalence of Stunted, Overweight, and Underweight Rates Across All Barangays')
    plt.savefig('static/pie_chart.png', transparent=True)
    plt.clf()

  
    # Create a line chart
    plt.plot(years, stunted_rates)
    plt.title('Stunted Rates Over Time')
    plt.xlabel('Year')
    plt.ylabel('Stunted Rate')
    plt.savefig('static/line_chart.png',transparent=True)
    plt.clf()



    # Create a scatter plot
    plt.scatter(stunted_rates, overweight_rates)
    plt.title('Relationship between Stunted and Overweight Rates')
    plt.xlabel('Stunted Rate')
    plt.ylabel('Overweight Rate')
    plt.savefig('static/scatter_plot.png',transparent=True)
    plt.clf()

   


 

    # Create a stacked bar chart
    fig, ax = plt.subplots()
    ax.bar(barangays, underweight_rates, label='Underweight')
    ax.bar(barangays, stunted_rates, bottom=underweight_rates, label='Stunted')
    ax.bar(barangays, overweight_rates, bottom=np.array(underweight_rates) + np.array(stunted_rates), label='Overweight')
    ax.set_title('Distribution of Underweight, Stunted, and Overweight Children per Barangay')
    ax.set_xlabel('Barangay')
    ax.set_ylabel('Number of Children')
    ax.legend()
    plt.savefig('static/sb_chart.png')
    plt.clf()




    
    # Render the template with the charts
    return render_template('/layouts/analytics.html', population_chart=url_for('static', filename='population_chart.png'),
                           pie_chart=url_for('static', filename='pie_chart.png'),
                           line_chart=url_for('static', filename='line_chart.png'),
                           scatter_plot=url_for('static', filename='scatter_plot.png'),
                           sb_chart=url_for('static', filename='sb_chart.png'))

if __name__ == '__main__':
    app.run(debug=True)










