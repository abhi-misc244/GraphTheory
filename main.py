from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from graphtheory import Graph
from functools import partial

'''
This is a Kivy project to for Graph Theory. This creates nodes and edges.
The nodes and edges can be added using the buttons. Nodes must be created first (atleast two).
Edges are created by selecting two nodes by double click. Nodes move by drag and drop style movement. Edges adjust according to the movement of Nodes
'''


'''
This is the main class that refers to other classes such as GraphNode and GraphEdge.
'''
class GraphInterface(Widget):
    def __init__(self, **kwargs):
        super(GraphInterface, self).__init__(**kwargs)

        #Global variable that tracks all edges
        global edge_matrix
        edge_matrix = []

        #Global variable that tracks all nodes
        global node_matrix
        node_matrix = []

        self.graph = Graph()

    def createNode(self, instance):
        global node_matrix

        '''Creating a GraphNode Class.'''
        node = GraphNode(pos = (500,500))







        '''Creating a Node Matrix. Will use this matrix in APP Class for future calculations'''
        node_matrix.append(node)

        '''Setting node variable to None. Probably not required; to be investigated in future'''
        node = None

        '''Adding the Widget to the drawing screen'''
        self.add_widget(node_matrix[-1])
        node_matrix[-1].text = 'Button'+ str(len(node_matrix))
        print node_matrix[-1].text

    def createEdge(self, instance):
        '''Creating a GraphEdge Class.'''

        '''Getting reference to the global node_matrix for tracking all nodes'''
        global node_matrix
        global edge_matrix


        '''Setting initial values of Node1 and Node2 to None. Not sure if required.
        To be investigated'''
        node2 = None
        node1 = None

        '''A for loop to get two nodes that are selected by double clicking. These nodes should
        have a changed colour in user interface.'''
        for i in range (0, len(node_matrix)):
            if (node_matrix[i].selected) and (node1 == None):
                node1 = node_matrix[i]
            if (node_matrix[i].selected) and (node_matrix[i] != node1):
                node2 = node_matrix[i]

        '''Creating a generic edge called 'c'. Addign that generic edge to the main game'''
        c = GraphEdge(node1, node2)
        self.add_widget(c)

        #Future - for integration with graph class

        edge_matrix.append(c)


        print node_matrix
        print 'node matrix length is ----> ', len(node_matrix)
        print 'edge matrix length is ----> ', len(edge_matrix)

        #c = None
        '''node1 = None
        node2 = None'''

        self.graph.add_edge([edge_matrix[-1].node1,edge_matrix[-1].node2])

        print self.graph

class GraphApp(App):
    '''Generic Kivy Application'''
    def build(self):

        '''Creating an instance of GraphInterface. This is the main class where all other class
        are created.'''
        game = GraphInterface()

        '''Creating an instance of Graph class. This class is part of future project.'''
        self.graph = Graph()

        '''Creating the two buttons that are to be used for creating nodes and edges'''
        createNodeButton = Button(text = 'CreateNode', pos=(100,0))
        createEdgeButton = Button(text = 'CreateEdge')
        game.add_widget(createNodeButton)
        game.add_widget(createEdgeButton)

        '''Referencing the actions of the buttons'''
        createNodeButton.bind(on_press=game.createNode)
        createEdgeButton.bind(on_press=game.createEdge)

        '''
        For a time based update. Not used in this case
        #Clock.schedule_interval(self.update, 1.0/60)'''

        return game

    '''
    For a time based update. Not used in this case
    def update(self, dt):
        self.edge.update_edge([100,100,300,300])'''



class GraphNode(Widget):
    '''The Node creating Class'''

    def __init__(self, **kwargs):
        super(GraphNode, self).__init__(**kwargs)

        '''This creates a circle at specified position initally. The node can then be dragged to
        different position. '''
        with self.canvas:
            Color(1,1,1)
            self.object = Ellipse(pos=(500,500))

        '''Creating a label for the node represented by ellipse. Inital text will be New Node.
        Once its dragged from the original position, its name changes based on when its created'''
        self.l = Label(text='New Node', color=[1,0,1,1], size=(200,200),pos=self.pos)
        self.add_widget(self.l)
        self.text = "New Node"

        '''Any change to the position of the node will trigger update_object function'''
        self.bind(pos=self.update_object)

        '''This variable is used to get connection points of the edges'''
        self.selected = 0


    def update_object(self, *args):
        '''Ellipse position is set as widget position'''
        self.object.pos = self.pos

        '''The lable position is set as widget position'''
        self.l.pos = self.pos
        self.l.text = self.text

        '''Had to do this as label kept dissapearing whenever canvas was cleared.
        Not sure why this was happening. to be investigated'''
        self.remove_widget(self.l)
        self.add_widget(self.l)

    def save_settings(self, instance):
        self.text = self.textinput.text
        self.update_object()
        self.popup.dismiss()


    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos) and touch.is_triple_tap:
            print 'triple tap happended'
            box = BoxLayout(orientation='vertical')


            sub_box1 = BoxLayout(orientation='horizontal')
            sub_box1.add_widget(Label(text='Name'))
            self.textinput = TextInput(text = 'Sample Node', multiline = False)
            sub_box1.add_widget(self.textinput)

            box.add_widget(sub_box1)


            save_settings_b = Button(text = 'Save')
            box.add_widget(save_settings_b)
            self.popup = Popup(title='Settings', content=box, size_hint=(.3,.3), auto_dismiss=False)
            self.popup.open()
            save_settings_b.bind(on_press=self.save_settings)

            self.update_object()

            '''Colour changing effect when a node is selected'''
        elif self.collide_point(*touch.pos) and touch.is_double_tap:
            self.selected = not self.selected
            if self.selected:
                with self.canvas:
                    self.canvas.clear()
                    Color(1,0,1)
                    self.object = Ellipse(pos=(self.pos))
                    self.update_object()
            elif not self.selected:
                with self.canvas:
                    self.canvas.clear()
                    Color(1,1,1)
                    self.object = Ellipse(pos=(self.pos))
                    self.update_object()

        elif self.collide_point(*touch.pos):
            '''For dragging the node to new position. Grab is a kivy function'''
            touch.grab(self)
            #print 'grabed item'




    def on_touch_move(self, touch):
        '''For dragging the node to new position. Grab is a kivy function'''
        if touch.grab_current is self:
            self.pos =  (touch.x, touch.y)


    def on_touch_up(self, touch):
        '''For dragging the node to new position. Grab is a kivy function'''
        if touch.grab_current is self:
            #print "ungrabed a button"
            touch.ungrab(self)



class GraphEdge(Widget):
    '''The Edge creating class. This needs two nodes as inputs.'''

    def __init__(self,node1, node2, **kwargs):
        super(GraphEdge, self).__init__(**kwargs)
        self.node1 = node1
        self.node2 = node2

        '''This is the name of the edge'''
        self.text = 'Edge--'+node1.text + '-' + node2.text

        '''The points list of the edge.'''
        self.points = list(node1.center) + list(node2.center)

        '''Drawing a line between the two nodes given with class creation'''
        with self.canvas:
            Color(1,1,1)
            self.object = Line(points=self.points, width=3)

        '''Whenever anoy of the nodes position changes, this triggers update_object function'''
        self.node1.bind(pos=self.update_object)
        self.node2.bind(pos=self.update_object)

    def update_object(self, node, pos):
        '''With the bind function, this function gets the node object and the position of the node as inputself. '''

        '''Reassign the values of points to match the new position of node'''
        self.points = list(self.node1.center) + list(self.node2.center)

        '''Clear the canvas. Redraw the line between unmoved node and moved node'''
        with self.canvas:
            self.canvas.clear()
            Color(1,1,1)
            self.object= Line(points=self.points, width=3)
    pass

if __name__ == '__main__':
    GraphApp().run()
