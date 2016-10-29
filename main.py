from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from graphtheory import Graph
from functools import partial

class GraphInterface(Widget):

    global edge_matrix
    edge_matrix = []

    global node_matrix
    node_matrix = []


    def createNode(self, instance):
        global node_matrix

        '''Creating a GraphNode Class. Using ObjectProperty for a shell reference'''
        node = GraphNode(pos = (500,500))

        print len(node_matrix)
        print node

        '''Creating a Node Matrix. Will use this matrix in APP Class for future calculations'''
        node_matrix.append(node)

        '''Setting node variable to None. Probably not required; to be investigated in future'''
        node = None

        '''Adding the Widget to the drawing screen'''
        self.add_widget(node_matrix[-1])
        node_matrix[-1].text = 'Button'+ str(len(node_matrix))
        print node_matrix[-1].text




        '''
        vertex = GraphNode(pos = (500,500))
        #print self.node_matrix
        self.node_matrix.append(vertex)
        self.graph.add_vertex(vertex)

        self.node_matrix[-1].text = 'Button'+ str(len(self.node_matrix))
        game.add_widget(self.node_matrix[-1])
        print "Node Created"
        print self.graph
        '''

    def createEdge(self, instance):
        global node_matrix
        print "Edge Created"
        node2 = None
        node1 = None

        for i in range (0, len(node_matrix)):
            if (node_matrix[i].selected) and (node1 == None):
                node1 = node_matrix[i]
            if (node_matrix[i].selected) and (node_matrix[i] != node1):
                node2 = node_matrix[i]

        c = GraphEdge(node1, node2)
        #self.graph.add_edge(edge)

        print "Edge changed"
        #self.edge_matrix.append(c)
        self.add_widget(c)

        #print self.graph



class GraphApp(App):

    def build(self):

        game = GraphInterface()
        self.graph = Graph()

        createNodeButton = Button(text = 'CreateNode', pos=(100,0))
        createEdgeButton = Button(text = 'CreateEdge')
        game.add_widget(createNodeButton)
        game.add_widget(createEdgeButton)

        createNodeButton.bind(on_press=game.createNode)
        createEdgeButton.bind(on_press=game.createEdge)
        #Clock.schedule_interval(self.update, 1.0/60)
        return game




    def update(self, dt):
        self.edge.update_edge([100,100,300,300])



class GraphNode(Widget):
    def __init__(self, **kwargs):
        super(GraphNode, self).__init__(**kwargs)
        with self.canvas:
            Color(1,1,1)
            self.object = Ellipse(pos=(500,500))

        self.l = Label(text='New Node', color=[1,0,1,1], size=(200,200),pos=self.pos)
        self.add_widget(self.l)
        self.text = "New Node"

        self.bind(pos=self.update_object)
        self.selected = 0


    def update_object(self, *args):
        self.object.pos = self.pos
        self.l.pos = self.pos
        self.l.text = self.text
        self.remove_widget(self.l)
        self.add_widget(self.l)
        #self.l.color = [1,0,1,1]



    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
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
            touch.grab(self)
            print 'grabed item'

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos =  (touch.x, touch.y)


    def on_touch_up(self, touch):
        if touch.grab_current is self:
            print "ungrabed a button"
            touch.ungrab(self)



class GraphEdge(Widget):
    def __init__(self,node1, node2, **kwargs):
        super(GraphEdge, self).__init__(**kwargs)
        self.node1 = node1
        self.node2 = node2
        self.text = 'Edge--'+node1.text + '-' + node2.text
        self.points = list(node1.center) + list(node2.center)
        print self.text
        with self.canvas:
            Color(1,1,1)
            self.object = Line(points=self.points, width=3)


        node1.bind(pos=self.update_object)
        node2.bind(pos=self.update_object)

        print 'the line points are ------------', self.object.points

        #print self.properties()




    def update_object(self, node, pos):
        print 'con property changed'
        print 'changed pos is ', pos
        print  'node1 pos is ', self.node1.pos
        print  'node2 pos is ', self.node2.pos

        self.points = list(self.node1.center) + list(self.node2.center)



        #self.canvas.clear()

        #new = list(node1pos) + list(node2pos)
        with self.canvas:
            self.canvas.clear()
            Color(1,1,1)
            self.object= Line(points=self.points, width=3)
        print 'the line points are ------------', self.points





    pass

if __name__ == '__main__':
    GraphApp().run()
