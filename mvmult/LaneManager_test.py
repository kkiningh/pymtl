#==============================================================================
# LaneManager_test.py
#==============================================================================

from new_pymtl import *
from new_pmlib import TestVectorSimulator
from new_pymtl.translation_tools.verilator_sim import get_verilated

from LaneManager import LaneManager

#------------------------------------------------------------------------------
# test_LaneManager_OneLane
#------------------------------------------------------------------------------
def test_LaneManager_OneLane( dump_vcd, test_verilog ):

  # Select and elaborate the model under test

  model = LaneManager( 1 )
  if test_verilog:
    model = get_verilated( model )
  model.elaborate()

  data_nbits = 32

  # Define test input and output functions

  def tv_in( model, test_vector ):
    model.from_cpu.val             .value = test_vector[0]
    model.from_cpu.msg[data_nbits:].value = test_vector[1]
    model.from_cpu.msg[:data_nbits].value = test_vector[2]
    model.done[0]                  .value = test_vector[3]

  def tv_out( model, test_vector ):
    assert model.from_cpu.rdy == test_vector[4]
    assert model.go           == test_vector[5]
    assert model.size         == test_vector[6]
    assert model.r_baddr      == test_vector[7]
    assert model.v_baddr      == test_vector[8]
    assert model.d_baddr      == test_vector[9]

  # Define the test vectors
  test_vectors = [
    # Inputs---------------  Outputs------------------------------------
    # val addr data   done   rdy go sz rb    vb    db
    [ 0,  1,   0x77,  0,     1,  0, 0, 0x00, 0x00, 0x00 ],
    [ 0,  0,   0x77,  0,     1,  0, 0, 0x00, 0x00, 0x00 ],
    [ 1,  1,   0x08,  0,     1,  0, 0, 0x00, 0x00, 0x00 ],
    [ 1,  1,   0x06,  0,     1,  0, 8, 0x00, 0x00, 0x00 ],
    [ 1,  2,   0x20,  0,     1,  0, 6, 0x00, 0x00, 0x00 ],
    [ 1,  3,   0x30,  0,     1,  0, 6, 0x20, 0x00, 0x00 ],
    [ 1,  4,   0x50,  0,     1,  0, 6, 0x20, 0x30, 0x00 ],
    [ 1,  0,   0x50,  0,     1,  0, 6, 0x20, 0x30, 0x50 ],
    [ 1,  0,   0x01,  0,     1,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     0,  1, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     0,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     0,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     0,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  1,     0,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     0,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     1,  0, 6, 0x20, 0x30, 0x50 ],
    [ 0,  0,   0x01,  0,     1,  0, 6, 0x20, 0x30, 0x50 ],
  ]

  # Create the simulator and configure it
  sim = TestVectorSimulator( model, test_vectors, tv_in, tv_out )
  if dump_vcd:
    sim.dump_vcd( "LaneManagerOneLane.vcd" )

  # Run the simulator
  sim.run_test()

#------------------------------------------------------------------------------
# test_LaneManager_TwoLanes
#------------------------------------------------------------------------------
def test_LaneManager_TwoLanes( dump_vcd, test_verilog ):

  # Select and elaborate the model under test

  model = LaneManager( 2 )
  if test_verilog:
    model = get_verilated( model )
  model.elaborate()

  data_nbits = 32

  # Define test input and output functions

  def tv_in( model, test_vector ):
    model.from_cpu.val             .value = test_vector[0]
    model.from_cpu.msg[data_nbits:].value = test_vector[1]
    model.from_cpu.msg[:data_nbits].value = test_vector[2]
    model.done[0]                  .value = test_vector[3]
    model.done[1]                  .value = test_vector[4]

  def tv_out( model, test_vector ):
    assert model.from_cpu.rdy == test_vector[5]
    assert model.go           == test_vector[6]
    assert model.size         == test_vector[7]
    assert model.r_baddr      == test_vector[8]
    assert model.v_baddr      == test_vector[9]
    assert model.d_baddr      == test_vector[10]

  # Define the test vectors
  test_vectors = [
    # Inputs---------------  Outputs------------------------------------
    # val addr data   dones  rdy go sz rb    vb    db
    [ 0,  1,   0x77,  0, 0,  1,  0, 0, 0x00, 0x00, 0x00, ],
    [ 0,  0,   0x77,  0, 0,  1,  0, 0, 0x00, 0x00, 0x00, ],
    [ 1,  1,   0x08,  0, 0,  1,  0, 0, 0x00, 0x00, 0x00, ],
    [ 1,  1,   0x06,  0, 0,  1,  0, 8, 0x00, 0x00, 0x00, ],
    [ 1,  2,   0x20,  0, 0,  1,  0, 6, 0x00, 0x00, 0x00, ],
    [ 1,  3,   0x30,  0, 0,  1,  0, 6, 0x20, 0x00, 0x00, ],
    [ 1,  4,   0x50,  0, 0,  1,  0, 6, 0x20, 0x30, 0x00, ],
    [ 1,  0,   0x50,  0, 0,  1,  0, 6, 0x20, 0x30, 0x50, ],
    [ 1,  0,   0x01,  0, 0,  1,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  0,  1, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  1, 0,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 1,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 1,  0,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  1,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  1, 1,  1,  0, 6, 0x20, 0x30, 0x50, ],
    [ 0,  0,   0x01,  0, 0,  1,  0, 6, 0x20, 0x30, 0x50, ],
  ]

  # Create the simulator and configure it
  sim = TestVectorSimulator( model, test_vectors, tv_in, tv_out )
  if dump_vcd:
    sim.dump_vcd( "LaneManagerOneLane.vcd" )

  # Run the simulator
  sim.run_test()