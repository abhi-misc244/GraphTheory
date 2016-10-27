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


class GraphInterface(Widget):
    #node = ObjectProperty(None)
    #edge = ObjectProperty(None)
    print 'testing'





class GraphApp(App):
    def build(self):
        node = GraphNode()
        edge = GraphEdge()
        game = GraphInterface()
        self.graph = Graph()

        self.node_matrix = []
        self.edge_matrix = []

        createNodeButton = Button(text = 'CreateNode', pos=(100,0))
        createEdgeButton = Button(text = 'CreateEdge')
        game.add_widget(createNodeButton)
        game.add_widget(createEdgeButton)

        def createNode(instance):
            #print self.node_matrix
            vertex = GraphNode(pos = (500,500))
            self.node_matrix.append(vertex)
            self.graph.add_vertex(vertex)

            self.node_matrix[-1].text = 'Button'+ str(len(self.node_matrix))
            game.add_widget(self.node_matrix[-1])
            print "Node Created"
            print self.graph

        def createEdge(instance):
            c = GraphEdge()
            print "Edge Created"
            vertex2 = None
            point2 = None
            for i in range (0, len(self.node_matrix)):
                if self.node_matrix[i].background_color == [1,0,0,1]:
                    point2 = list(self.node_matrix[i].center)
                    vertex2 = self.node_matrix[i]
                    self.node_matrix[i].background_color = [1,1,1,1]

            point1 = list(self.node_matrix[-1].center)
            point = point1 + point2
            edge = [self.node_matrix[-1], vertex2]
            self.graph.add_edge(edge)


            print point
            c.update_edge(point)
            print "Edge changed"
            self.edge_matrix.append(c)
            game.add_widget(c)
            print self.graph


        createNodeButton.bind(on_press=createNode)
        createEdgeButton.bind(on_press=createEdge)
        #Clock.schedule_interval(self.update, 1.0/60)
        return game

    def update(self, dt):
        self.edge.update_edge([100,100,300,300])



class GraphNode(Button):
    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            if self.background_color == [1,0,0,1]:
                self.background_color = [1,1,1,1]
            elif self.background_color == [1,1,1,1]:
                self.background_color = [1,0,0,1]
            print "double tap"
        elif self.collide_point(*touch.pos):
            print "grabed a button"
            touch.grab(self)
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.pos =  (touch.x, touch.y)
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            print "ungrabed a button"
            touch.ungrab(self)



class GraphEdge(Widget):
    def update_edge(self, new_points):
        with self.canvas:
            self.l = Line(points=[100,100,100,200], width=3)
            self.l.points= new_points

    def getnodes(self, node_matrix):
        box = BoxLayout()
        cb_matrix = []
        no_of_nodes = len(node_matrix)
        for i in range (0, no_of_nodes):
            cb_string = node_matrix[i].text
            print cb_string
            cb = CheckBox()
            cb_matrix.append(cb)
            box.add_widget(Label(text=cb_string))
            box.add_widget(cb)

        popup = Popup(title = 'Select Nodes', content=box, size_hint=(.5,.5), auto_dismiss=True)
        popup.open()
        for i in range (0, len(cb_matrix)):
            if cb_matrix[i].active:
                vertex1 = node_matrix[i]
                print vertex1
        #print vertex1
    pass

if __name__ == '__main__':
    GraphApp().run()
