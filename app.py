# Importing required functions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from matplotlib import pyplot as plt
from matplotlib import image as mpimg 
from flask import Flask, render_template, request

# Flask constructor
app = Flask(__name__)

# Root endpoint
@app.get('/')
def upload():
    return render_template('upload-excel.html')

@app.post('/calculatetrend')
def calculatetrend():

    # Read the File using Flask request
    file = request.files['file']
    # save file in local directory
    file.save(file.filename)    
        
    data = pd.read_excel(file)
    mean_x=np.sum(data["month"])/len(data)
    mean_y=np.sum(data["values"])/len(data)
    x_meanx=[i-mean_x for i in data["month"]]
    y_meany=[i-mean_y for i in data["values"]]
    x_meanxy_meany=[i*k for i,k in zip(x_meanx,y_meany)]
    sumx_meanxy_meany=np.sum(x_meanxy_meany)
    x_meanx2=[np.square(i) for i in x_meanx]
    sumx_meanx2=np.sum(x_meanx2)
    m=np.sum([i/sumx_meanx2 for i in x_meanxy_meany])
    b=mean_y-m*mean_x
    line=(m*data["month"])+b
    plot.plot(data["month"], line)
    plot.plot(data["month"], data["values"])
    plot.savefig("static/trend_graph.png")
    image = mpimg.imread("static/trend_graph.png")
    return render_template('image_render.html')
    
# Main Driver Function
if __name__ == '__main__':
    # Run the application on the local development server
    app.run(debug=True)
    


