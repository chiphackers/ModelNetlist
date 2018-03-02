## SimpleNetlist

This folder contains the implementation of the graph model. SimpleNetlist is the class which describes the circuit.
Circuit elements are inherited as shown below.

nlNode
  |
  +--> Pin
  |
  +--> Net
  |
  +--> Cell
        |
        +--> AND2
        |
        +--> OR2


