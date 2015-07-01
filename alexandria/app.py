# coding=utf-8

from flask import Flask
from flask import jsonify
from flask import request
import config
import models
import pprint
import configuration_item
from alexandria.drivers import Driver

# Initialise Flask
app = Flask(__name__)
app.debug = True


@app.route("/drivers", methods = ["GET"])
def api_drivers():
    """Return drivers.

    :param nome
    :type na
    :returns:  http response

    """
    data = {"drivers" : conf_file.get_drivers()}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/drivers/<driver_name>")
def api_driver(driver_name):
    data = {driver_name : conf_file.get_driver_info(driver_name)}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/bruno', methods=['POST'])
def bruno():
    coucou = "Coucou " + request.json["Server"]
    #coucou = "Coucou"
    return coucou

@app.route('/ci', methods=['POST'])
def create_ci():
    
    ci = configuration_item.ConfigurationItem(request.json["uuid"],
                              request.json["ip_mgmt"],
                              request.json["login"],
                              request.json["password"])
    
    # Error cas uuid already available
    alexandria_cis.update({request.json["uuid"]: ci })
    
    driver_list = conf_file.get_drivers()
    
    #for driver in driver_list:
        #driver.get(ci)
    
    return ("ok")

@app.route('/ci', methods=['PUT'])
def update_ci():
    pass

@app.route("/", methods = ["GET"])
def api_root():
    
    #global alexandria
    data = {
        "Service"  : "Alexandria",
        "Version" : alexandria.version
    }

    resp = jsonify(data)
    resp.status_code = 200

    resp.headers["AuthorSite"] = "http://uggla.fr"

    return resp

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class Alexandria(object):
    def __init__(self):
        self.version = "0.1"
        self.model = models.Model()
        
        driver_name_list = conf_file.get_drivers()
        
        self.drivers = []
        
        # Create objects !!!! TO BE CONTINUED !!!!
        for driver_name in driver_name_list:
            setattr(self, driver_name, Driver)
        


if __name__ == "__main__":
    # Vars  
    global alexandria
    
    alexandria = Alexandria()
    
    
    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)
    
    # Configuration file
    conf_file = config.AlexandriaConfiguration("alexandria.conf")

    # Model
    models = models.Model()

    # Define a structure to handle ci
    alexandria_cis = {}
    
    print models.reference_items
    #pp.pprint(models.EthernetInterface)  # debugging example.
    #pp.pprint(models.Manager)  # debugging example.
    app.run(port=int(conf_file.get_alexandria_port()))
