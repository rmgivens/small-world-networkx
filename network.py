# Author: Robin M. Givens
# Created: July 18, 2020

# Network class for a 2-mode (person-to-group) network that provides methods 
# for getting the list of persons; the list of groups; 
# the person-to-group network as a matrix (list of lists);
# the person-to-person network as a matrix (list of lists);
# the binary person-to-person network as a matrix (list of lists);
# the largest component as a Network;
# the proportion of persons and groups in the largest component;
# and for the binary person-to-person network: mean co-enrollments,
# mean unique co-enrollments, # the number of unique edges (connections/links) 
# between persons, network density, average clustering coefficient,
# characteristic path length, and network diameter.
# Provides == for testing.

# Also provides a method to print all the analysis for the methods
# described above and methods to get the person-to-group and person-to-person
# networks as NetworkX objects for ease of drawing.

import networkx as nx
import numpy as np

class Network:
    # creates a 2-mode network from a file containing edges of the form
    # person,group on each line, a list of files each of the form described
    # previously, or from a list of lists of the form [person,group]
    def __init__(self, edges):
        # get the edges/links
        self._links = []
        
        # single file
        if isinstance(edges, str):
            # use UTF-8-sig to ignore errant BOM characters
            file = open(edges, 'r', encoding = 'utf-8-sig')
            for line in file:
                result = line.strip().split(',')
                self._links.append(result)
            file.close()
        elif isinstance(edges, list):
            # lists of edges
            if (len(edges) != 0 and isinstance(edges[0], list)):
                for edge in edges:
                    self._links.append(list(edge))
                    
            # list of files
            elif (len(edges) != 0 and isinstance(edges[0], str)):
                for item in edges:
                    # use UTF-8-sig to ignore errant BOM characters
                    file = open(item, 'r', encoding = 'utf-8-sig')
                    for line in file:
                        result = line.strip().split(',')
                        self._links.append(result)
                    file.close()
            else:
                raise Exception("Constructor needs a file name, a list of file names, or list of edges.")            
        else:
            raise Exception("Constructor needs a file name, a list of file names, or list of edges.")
        
        # list of persons, list of groups
        persons = set()
        groups = set()
        for link in self._links:
            persons.add(link[0])
            groups.add(link[1])
        self._persons = list(persons)
        self._groups = list(groups)
        self._persons.sort()
        self._groups.sort()
                
        # binary person to person network as a networkx graph
        network = self.getBinPersonToPerson()
        self._network = nx.Graph()
        
        for i in range(len(network)):
            for k in range(len(network)):
                if i!=k and network[i][k] == 1:
                    self._network.add_edge(self._persons[i], self._persons[k])        
        
    
    # return the list of persons
    def getPersons(self):
        return list(self._persons)
    
    # return the list of groups
    def getGroups(self):
        return list(self._groups)
    
    # return the binary person to person as a networkx
    # useful for drawing the network and analysis in other methods
    def getBinPersonToPersonNetworkX(self):
        return nx.Graph(self._network)

    # create the bipartite 2-mode graph from persons and groups
    # as a matrix (list of lists)
    def _getBipartiteGraph(self):
        persons = list(self.getPersons())
        groups = list(self.getGroups())
        persons.sort()
        groups.sort()
        
        matrix = []
        for i in range(len(persons)):
            matrix.append([0]*len(groups))
        
        for connect in self._links:
            row = persons.index(connect[0])
            col = groups.index(connect[1])
            
            matrix[row][col] = 1
            
        return matrix
    
    # get the person-to-group matrix (a list of lists)
    def getPersonToGroupMatrix(self):
        return self._getBipartiteGraph()  
    
    # get the person-to-group network as a networkx
    # useful for drawing the network    
    def getPersonToGroupNetworkX(self):
        # create networkx person-to-group graph
        network = nx.Graph()
        for link in self._links:
            network.add_edge(link[0], link[1])
            
        return network
    
    
    
    # get the betweenness centrality of the person-to-group network
    def getBetweennessCentrality(self):
        # create networkx person-to-group graph
        network = self.getPersonToGroupNetworkX()
            
        # get betweenness centrality
        result = nx.betweenness_centrality(network)
        nodes = result.keys()
        cent = []
        for node in nodes:
            cent.append(result[node])
        return sum(cent)/len(cent)
    
    # returns the set of nodes in the the largest component of the network
    def _getPersonsGroupsLargestComp(self):
        matrix = self._getBipartiteGraph()
        
        graph = nx.Graph()
        
        # create 2-mode networkx graph
        for i in range(len(self._persons)):
            for k in range(len(self._groups)):
                if matrix[i][k] == 1:
                    graph.add_edge(self._persons[i], self._groups[k])
        
        # gets the largest component        
        largest = max(nx.connected_components(graph), key=len)
        return largest
    
    # returns the largest component as a new Network
    def largestComponentToNetwork(self):
        # find persons, groups in largest component
        largest = self._getPersonsGroupsLargestComp()
        persons = []
        groups = []
        for n in largest:
            if n in self._persons:
                persons.append(n)
            else:
                groups.append(n)
        
        # find edges in largest component            
        edges = []
        for p in persons:
            for g in groups:
                if [p,g] in self._links:
                    edges.append([p,g])
        return Network(edges)    
    
    
    # returns a list containing the proportion of persons in largest component
    # and proportion of groups in largest component as [p, g]
    def getLargestProportion(self):
        largest = self._getPersonsGroupsLargestComp()
        
        countP = 0
        countG = 0
        
        for n in largest:   # all the nodes in the largest component
            if n in self._persons:
                countP = countP + 1
            elif n in self._groups:
                countG = countG + 1
            else:
                print("Cannot find node:", n)
                
        return [countP/len(self._persons), countG/len(self._groups)]
    
  
    # creates the person-to-person matrix (list of lists) using matrix
    # multiplication
    def getPersonToPerson(self):
        matrix = np.array(self.getPersonToGroupMatrix())
        return np.dot(matrix, np.transpose(matrix)).tolist()
    
    # creates the binary person-to-person matrix (list of lists) by
    # dichotomizing the person-to-person matrix
    def getBinPersonToPerson(self):
        matrix = np.array(self.getPersonToPerson())
        return np.where(matrix > 0, 1, 0).tolist()
    
    # counts all the coenrollments in the person-to-person matrix and 
    # averages them over all persons
    def getMeanCoEnrollments(self):
        total = 0
        network = self.getPersonToPerson()
        for i in range(len(network)):
            for k in range(len(network)):
                if i != k:
                    total = total + network[i][k]
                    
        return total / len(network)
    
    # counts all the unique coenrollments (neighbors) in the binary 
    # person-to-person graph and averages them over all persons
    def getMeanUniqueCoEnrollments(self):
        total = 0
        for n in self._network:
            # self._network[n] is the adjacency dictionary of node n
            result = [n for n in self._network[n]]
            #print(result)
            amount = len(result)
            total = total + amount            
                    
        return total / len(self._network)
    
    # counts the number of edges (links) between persons (binary)
    def getUniqueEdges(self):
        return self._network.size()
    
    # gets the network density (binary)
    def getNetworkDensity(self):
        return nx.density(self._network)
    
    # gets the average clustering coefficient (binary)
    def getAverageClusterCoeff(self):
        return nx.average_clustering(self._network)
    
    # gets the characteristic path length, the average distance between
    # persons (binary)
    # does NOT work for a graph that is not connected, returns -1.0 if error
    def getCharPathLength(self):
        return self._getData(0)['path']
        
    
    # gets the network diameter (binary)
    # does NOT work for a graph that is not connected, returns -1 if error
    def getNetworkDiameter(self):
        return self._getData(0)['diameter']
        
    # get the k-step reach of the proportion of person pairs that can be 
    # linked in k steps, 
    # if multiple is true, returns reach for 0, 1, 2, 3, ... k as a list
    def getKStepReach(self, k, multiple=False):
        result = self._getData(k)['reach']
        if multiple:
            return result
        else:
            return result[k]
    
    # gets the characteristic path length, network diameter, and k-step reach
    # all at once to reduce calculation time
    # returns a dictionary with keywords 'path', 'diameter' and 'reach' 
    # associated with the results
    # if graph is not connected, 'path' is -1.0 and diameter is -1
    def _getData(self, k):
        path = dict(nx.all_pairs_shortest_path_length(self._network))
        totalLen = 0        # sum of the path lengths or -1.0
        numPairs = 0        # total number of node pairs
        count = [0]*(k+1)   # pair count for k-step reach
        diameter = 0        # diameter
        
        result = {}         # result dictionary
        
        for i in range(len(self._persons)):
            for j in range(i+1, len(self._persons)):
                n = self._persons[i]
                m = self._persons[j]
                numPairs = numPairs + 1

                try:
                    # to calculate characteristic path length
                    if totalLen >= 0:
                        totalLen = totalLen + path[n][m]
                    # to determine diameter
                    if diameter >= 0 and path[n][m] > diameter:
                        diameter = path[n][m]
                    # to calculate k-step reach
                    for x in range(1, k+1): # always 0 for k=0
                        if path[n][m] <= x:
                            count[x] = count[x] + 1
                except: # graph is not connected
                    totalLen = -1.0
                    diameter = -1
        
        # calculate results         
        for i in range(len(count)):
            count[i] = count[i] / numPairs
        result['reach'] = count
        if totalLen >= 0:
            result['path'] = totalLen / numPairs
        else:
            result['path'] = -1.0
        result['diameter'] = diameter
        
        return result
            
        
    # print all data for network for largest component
    def printNetworkData(self):
        print()
        print("Person-to-Group Data:")
        print("----------------------------------------")
        compData = self.getLargestProportion()
        print("Persons:                     %10d"     % (len(self.getPersons())))
        print("Groups:                      %10d"     % (len(self.getGroups())))
        print("Proportion of persons:       %10.5f"   % (compData[0]))
        print("Proportion of groups:        %10.5f"   % (compData[1]))
        print("Betweenness Centrality:      %10.5f\n" % (self.getBetweennessCentrality()))
        if compData[0] == 1.0 and compData[1] == 1.0:
            print("Person-to-Person Whole Network Data:")
            print("----------------------------------------")
            print("Mean co-enrollements:        %10.5f"   % (self.getMeanCoEnrollments()))
            print("Mean unique co-enrollements: %10.5f"   % (self.getMeanUniqueCoEnrollments()))   
            print("Unique edges (links):        %10d"     % (self.getUniqueEdges()))
            print("Network density:             %10.5f"   % (self.getNetworkDensity()))
            print("Clustering coefficient:      %10.5f"   % (self.getAverageClusterCoeff())) 
            result = self._getData(4)
            print("Characteristic path length:  %10.5f"   % (result['path']))
            print("Network diameter:            %10d"     % (result['diameter']))
            print("1-step reach:                %10.5f"   % (result['reach'][1]))
            print("2-step reach:                %10.5f"   % (result['reach'][2]))
            print("3-step reach:                %10.5f"   % (result['reach'][3]))
            print("4-step reach:                %10.5f\n" % (result['reach'][4]))              
        
        else:
            comp = self.largestComponentToNetwork()
            print("Person-to-Person Largest Component Data:")
            print("----------------------------------------")
            print("Persons:                     %10d"     % (len(comp.getPersons())))
            print("Groups:                      %10d"     % (len(comp.getGroups())))
            print("Mean co-enrollements:        %10.5f"   % (comp.getMeanCoEnrollments()))
            print("Mean unique co-enrollements: %10.5f"   % (comp.getMeanUniqueCoEnrollments()))   
            print("Unique edges (links):        %10d"     % (comp.getUniqueEdges()))
            print("Network density:             %10.5f"   % (comp.getNetworkDensity()))
            print("Clustering coefficient:      %10.5f"   % (comp.getAverageClusterCoeff())) 
            result = comp._getData(4)
            print("Characteristic path length:  %10.5f"   % (result['path']))
            print("Network diameter:            %10d"     % (result['diameter']))
            print("1-step reach:                %10.5f"   % (result['reach'][1]))
            print("2-step reach:                %10.5f"   % (result['reach'][2]))
            print("3-step reach:                %10.5f"   % (result['reach'][3]))
            print("4-step reach:                %10.5f\n" % (result['reach'][4]))  
        
        
    # two Networks are equal if they have the same persons, groups, and links,
    # the latter is tested by comparing the person-to-group matrix
    # this does not determine if two Networks are isomorphic
    def __eq__(self, other):
        if isinstance(other, Network):
            if self.getPersons() == other.getPersons():
                if self.getGroups() == self.getGroups():
                    if self.getPersonToGroupMatrix() == self.getPersonToGroupMatrix():
                        return True
        return False
