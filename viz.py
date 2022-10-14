from mesa.visualization.modules import CanvasGrid
from plane import PlaneModel, PassengerAgent, PatchAgent,CabinAgent
import mesa.visualization.modules
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import VisualizationElement
no_of_rows = 38
colors = [
    'blue', 'cyan', 'orange', 'yellow', 'magenta', 'purple', '#103d3e', '#9fc86c',
    '#b4c2ed', '#31767d', '#31a5fa', '#ba96e0', '#fef3e4', '#6237ac', '#f9cacd', '#1e8123'
]


def agent_portrayal(agent):
    if isinstance(agent, PassengerAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "grey",
                     "r": 0.9}

        portrayal['Color'] = colors[agent.group - 1]

        if agent.state == "FINISHED":
            portrayal["Layer"] = 2
        elif agent.state == "BAGGAGE":
            portrayal["Color"] = "brown"

        portrayal['text'] = agent.unique_id
        portrayal['text_color'] = 'white'

    elif isinstance(agent, PatchAgent):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "lightgrey",
                     "w": 1,
                     "h": 1}

        # create a new instance for cabin agent, create a new class in plane then need to modify the algo abit

        if agent.type == 'CORRIDOR':
            portrayal['Color'] = 'lightgreen'
        elif agent.type == 'SEAT':
            portrayal['Color'] = '#ff6666'

    elif isinstance(agent,CabinAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "black",
                     "r": 1}

        # create a new instance for cabin agent, create a new class in plane then need to modify the algo abit
        if agent.state=="FREE":
            portrayal['Color'] = 'green'
        if agent.state=="Takem":
            portrayal["Color"] = "red"
    return portrayal

class TextElement(VisualizationElement):
    js_includes = ["TextModule.js"]
    js_code = "elements.push(new TextModule());"

luggage_vals = ['normal', 0, 1, 2, 3, 4, 5, 6, 7]

grid = CanvasGrid(agent_portrayal, no_of_rows, 9, 840, 310)

method_choice = UserSettableParameter('choice', 'Boarding method', value='Random',
                                                choices=list(PlaneModel.method_types.keys()))
shuffle_choice = UserSettableParameter('checkbox', 'Enable Shuffle', value=True)

bags_choice = UserSettableParameter('choice', 'Luggage Size', value='normal', choices=luggage_vals)

#bags_choice = UserSettableParameter('slider', 'Enable Bags', value='-1', min_value=-1, max_value=10, step=1)

server = ModularServer(PlaneModel,
                       [grid],
                       "Boarding Simulation",
                       {"method": method_choice, "shuffle_enable": shuffle_choice, 'common_bags': bags_choice})
server.port = 8521 # The default
server.launch()
