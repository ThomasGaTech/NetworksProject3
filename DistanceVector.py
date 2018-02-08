# Project 3 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        self.vector = { name: 0 }

    def send_initial_messages(self):
        self.send_to_incoming_links()

    def process_BF(self):
        updated = False
        for msg in self.messages:         
            for node in msg["vector"].keys():
                if node not in self.vector and node != self.name:
                    if self.is_outgoing_neighbor(node):
                        weight = int(self.get_outgoing_neighbor_weight(node))
                    else:
                        weight = int(self.get_outgoing_neighbor_weight(msg["source"])) + int(msg["vector"][node])
                    self.vector[node] = weight
                    updated = True
                elif node in self.vector and node != self.name:
                    self_to_source = int(self.get_outgoing_neighbor_weight(msg["source"]))
                    source_to_node = int(msg["vector"][node])
                    new_distance = self_to_source + source_to_node
                    if self_to_source <= -99 or source_to_node <= -99 and self.vector[node] != -99:
                        self.vector[node] = -99
                        updated = True
                    else:
                        if new_distance < self.vector[node] and new_distance > -99:
                            self.vector[node] = new_distance
                            updated = True
                        elif new_distance <= -99 and self.vector[node] != -99:
                            self.vector[node] = -99
                            updated = True

        self.messages = []

        if updated:
            self.send_to_incoming_links()


    def log_distances(self): 
        seperator = ','
        link_texts = []
        for key in self.vector:
            link_texts.append(key + str(self.vector[key]))   
        link_texts.sort()
        add_entry(self.name, seperator.join(link_texts))        

    def is_outgoing_neighbor(self, nodeName):
        for link in self.outgoing_links:
            if nodeName == link.name:
                return True

    def send_to_incoming_links(self):
        for link in self.incoming_links:
            message = { "source": self.name, "vector": self.vector.copy(), "dest": link }
            self.send_msg(message, link.name)
