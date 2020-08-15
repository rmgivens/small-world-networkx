# Author: Robin M. Givens
# Created: July 18, 2020

# Tester and example of use for most of the Network methods.

from network import Network
import unittest

net1 = Network('test1.csv')
net2 = Network('test2.csv')
net3 = Network('test3.csv')

class NetworkTester(unittest.TestCase):
    
    def testGetPersons(self):
        expected1 = ['A','B','C','D','E']
        expected2 = ['A','B','C','D','E','F','G']
        expected3 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
        
        self.assertEqual(net1.getPersons(), expected1)
        self.assertEqual(net2.getPersons(), expected2)
        self.assertEqual(net3.getPersons(), expected3)
    
    def testGetGroups(self):
        expected1 = ['G1','G2','G3','G4']
        expected2 = ['G1','G2','G3','G4','G5']
        expected3 = ['G1','G2','G3','G4','G5','G6','G7','G8']
        
        
        self.assertEqual(net1.getGroups(), expected1)
        self.assertEqual(net2.getGroups(), expected2)
        self.assertEqual(net3.getGroups(), expected3)        
    
    def testGetPersonToGroupMatrix(self):
        expected1 = [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 1, 1, 1]]
        expected2 = [[1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]
        expected3 = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0, 0, 1], [0, 1, 1, 0, 1, 0, 0, 0]]
        
        self.assertEqual(net1.getPersonToGroupMatrix(), expected1)
        self.assertEqual(net2.getPersonToGroupMatrix(), expected2)
        self.assertEqual(net3.getPersonToGroupMatrix(), expected3)
    
    def testLargestComponentToNetwork(self):
        expected1 = net1
        expected2 = net1
        expected3 = net3
        
        # smaller largest component
        net4 = Network([['A','G1'],['B','G2'],['C','G3'],['D','G3'],['E','G4']])
        expected4 = Network([['C','G3'],['D','G3']])        
        
        self.assertEqual(net1.largestComponentToNetwork(), expected1)
        self.assertEqual(net2.largestComponentToNetwork(), expected2)
        self.assertEqual(net3.largestComponentToNetwork(), expected3) 
        self.assertEqual(net4.largestComponentToNetwork(), expected4)  
    
    def testGetLargestProportion(self):
        expected1 = [5/5, 4/4]
        expected2 = [5/7, 4/5]
        expected3 = [16/16, 8/8]
        
        # smaller largest component
        net4 = Network([['A','G1'],['B','G2'],['C','G3'],['D','G3'],['E','G4']])
        expected4 = [2/5, 1/4]      
        
        actual1 = net1.getLargestProportion()
        actual2 = net2.getLargestProportion()
        actual3 = net3.getLargestProportion()
        actual4 = net4.getLargestProportion()
        
        self.assertAlmostEqual(actual1[0], expected1[0], delta=0.00001)
        self.assertAlmostEqual(actual1[1], expected1[1], delta=0.00001)  
        
        self.assertAlmostEqual(actual2[0], expected2[0], delta=0.00001)
        self.assertAlmostEqual(actual2[1], expected2[1], delta=0.00001)  
        
        self.assertAlmostEqual(actual3[0], expected3[0], delta=0.00001)
        self.assertAlmostEqual(actual3[1], expected3[1], delta=0.00001)  
        
        self.assertAlmostEqual(actual4[0], expected4[0], delta=0.00001)
        self.assertAlmostEqual(actual4[1], expected4[1], delta=0.00001)          
        
    
    def testGetPersonToPerson(self):
        expected1 = [[4, 1, 2, 2, 3], [1, 1, 1, 0, 0], [2, 1, 2, 1, 1], [2, 0, 1, 2, 2], [3, 0, 1, 2, 3]]
        expected2 = [[4, 1, 2, 2, 3, 0, 0], [1, 1, 1, 0, 0, 0, 0], [2, 1, 2, 1, 1, 0, 0], [2, 0, 1, 2, 2, 0, 0], [3, 0, 1, 2, 3, 0, 0], [0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1, 1]]
        expected3 = [[1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 2, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 0, 0, 0, 2], [0, 1, 3, 2, 1, 0, 0, 1, 2, 1, 0, 2, 1, 0, 1, 2], [0, 0, 2, 4, 1, 2, 1, 0, 2, 2, 0, 1, 2, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 2, 0, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 1, 3, 2, 2, 1, 1, 0, 0, 2, 2, 0], [1, 2, 1, 0, 0, 0, 2, 4, 2, 2, 2, 1, 0, 1, 2, 2], [1, 1, 2, 2, 1, 1, 2, 2, 4, 0, 1, 1, 1, 1, 1, 2], [0, 1, 1, 2, 0, 1, 1, 2, 0, 4, 1, 1, 1, 1, 2, 1], [1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 2, 0, 0, 0, 1, 1], [0, 1, 2, 1, 0, 0, 0, 1, 1, 1, 0, 2, 0, 0, 1, 1], [0, 0, 1, 2, 1, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1], [0, 0, 0, 1, 0, 1, 2, 1, 1, 1, 0, 0, 0, 2, 1, 0], [1, 0, 1, 1, 0, 0, 2, 2, 1, 2, 1, 1, 0, 1, 3, 0], [0, 2, 2, 1, 1, 0, 0, 2, 2, 1, 1, 1, 1, 0, 0, 3]]
        
        self.assertEqual(net1.getPersonToPerson(), expected1)
        self.assertEqual(net2.getPersonToPerson(), expected2)
        self.assertEqual(net3.getPersonToPerson(), expected3)
    
    def testGetBinPersonToPerson(self):
        expected1 = [[1, 1, 1, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 0, 1, 1, 1]]
        expected2 = [[1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0], [1, 0, 1, 1, 1, 0, 0], [1, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1, 1]]
        expected3 = [[1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1], [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0], [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1]]
        
        self.assertEqual(net1.getBinPersonToPerson(), expected1)
        self.assertEqual(net2.getBinPersonToPerson(), expected2)
        self.assertEqual(net3.getBinPersonToPerson(), expected3)
    
    def testGetMeanCoEnrollments(self):
        expected1 = 26/5
        expected2 = 28/7
        expected3 = 182/16
        
        self.assertAlmostEqual(net1.getMeanCoEnrollments(), expected1, delta=0.00001)
        self.assertAlmostEqual(net2.getMeanCoEnrollments(), expected2, delta=0.00001)
        self.assertAlmostEqual(net3.getMeanCoEnrollments(), expected3, delta=0.00001)
    
    def testGetMeanUniqueCoEnrollments(self):
        expected1 = 16/5
        expected2 = 18/7
        expected3 = 140/16
        
        self.assertAlmostEqual(net1.getMeanUniqueCoEnrollments(), expected1, delta=0.00001)
        self.assertAlmostEqual(net2.getMeanUniqueCoEnrollments(), expected2, delta=0.00001)
        self.assertAlmostEqual(net3.getMeanUniqueCoEnrollments(), expected3, delta=0.00001)
    
    def testGetUniqueEdges(self):
        expected1 = 8
        expected2 = 9
        expected3 = 70
        
        self.assertEqual(net1.getUniqueEdges(), expected1)
        self.assertEqual(net2.getUniqueEdges(), expected2)
        self.assertEqual(net3.getUniqueEdges(), expected3)
    
    def testGetNetworkDensity(self):        
        expected1 = 8/10
        expected2 = 9/21
        expected3 = 70/120
        
        self.assertAlmostEqual(net1.getNetworkDensity(), expected1, delta=0.00001)
        self.assertAlmostEqual(net2.getNetworkDensity(), expected2, delta=0.00001)
        self.assertAlmostEqual(net3.getNetworkDensity(), expected3, delta=0.00001)
    
    def testGetAverageClusterCoeff(self):
        expected1 = 13/15
        expected2 = 13/21
        expected3 = 352741/480480
        
        self.assertAlmostEqual(net1.getAverageClusterCoeff(), expected1, delta=0.00001)
        self.assertAlmostEqual(net2.getAverageClusterCoeff(), expected2, delta=0.00001)
        self.assertAlmostEqual(net3.getAverageClusterCoeff(), expected3, delta=0.00001)        
    
    def testGetCharPathLength(self):
        expected1 = 12/10
        expected2 = -1
        expected3 = 170/120
        
        # path (larger distance)
        net4 = Network([['A','G1'],['B','G1'],['B','G2'],['C','G2'],['C','G3'],['D','G3'],['D','G4'],['E','G4'],['E','G5'],['F','G5']])
        expected4 = 35/15       
        
        self.assertAlmostEqual(net1.getCharPathLength(), expected1, delta=0.00001)
        self.assertAlmostEqual(net2.getCharPathLength(), expected2, delta=0.00001)
        self.assertAlmostEqual(net3.getCharPathLength(), expected3, delta=0.00001) 
        self.assertAlmostEqual(net4.getCharPathLength(), expected4, delta=0.00001) 
    
    def testGetNetworkDiameter(self):
        expected1 = 2
        expected2 = -1
        expected3 = 2
        
        # path (larger distance)
        net4 = Network([['A','G1'],['B','G1'],['B','G2'],['C','G2'],['C','G3'],['D','G3'],['D','G4'],['E','G4'],['E','G5'],['F','G5']])
        expected4 = 5        
        
        self.assertEqual(net1.getNetworkDiameter(), expected1)
        self.assertEqual(net2.getNetworkDiameter(), expected2)
        self.assertEqual(net3.getNetworkDiameter(), expected3)
        self.assertEqual(net4.getNetworkDiameter(), expected4)
    
    def testGetKStepReach(self):
        expected1 = [0/10, 8/10, 10/10, 10/10, 10/10]
        expected2 = [0/21, 9/21, 11/21, 11/21, 11/21]
        expected3 = [0/120, 70/120, 120/120, 120/120, 120/120]
        
        # path (larger distance)
        net4 = Network([['A','G1'],['B','G1'],['B','G2'],['C','G2'],['C','G3'],['D','G3'],['D','G4'],['E','G4'],['E','G5'],['F','G5']])
        expected4 = [0/15, 5/15, 9/15, 12/15, 14/15, 15/15]
        
        for k in range(len(expected1)):
            self.assertAlmostEqual(net1.getKStepReach(k), expected1[k], delta=0.00001, msg=("when k = %d" % (k)))
            self.assertAlmostEqual(net2.getKStepReach(k), expected2[k], delta=0.00001, msg=("when k = %d" % (k)))
            self.assertAlmostEqual(net3.getKStepReach(k), expected3[k], delta=0.00001, msg=("when k = %d" % (k)))
        
        actual4 = net4.getKStepReach(5, multiple=True)
        for k in range(len(expected4)):
            self.assertAlmostEqual(actual4[k], expected4[k], delta=0.00001, msg=("when k = %d" % (k)))
        
        
if __name__ == '__main__':
    print("\n--- Network 1 ---")
    net1.printNetworkData()    
    print("\n--- Network 2 ---")
    net2.printNetworkData()     
    print("\n--- Network 3 ---")
    net3.printNetworkData()   
    
    # path (larger distance)
    net4 = Network([['A','G1'],['B','G1'],['B','G2'],['C','G2'],['C','G3'],['D','G3'],['D','G4'],['E','G4'],['E','G5'],['F','G5']])    
    
    print("\n--- Network 4 ---")
    net4.printNetworkData()      
    
    unittest.main()
    
