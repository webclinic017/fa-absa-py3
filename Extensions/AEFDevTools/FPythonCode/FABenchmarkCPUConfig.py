""" Configuration options for Front Arena multi - core benchmark

 Note: Not stored in extensions as benchamrk needs to be run without ADS connects
 
(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.
 
 """
 
# Path for output file, by default current working directory
out_path = r""

# Number of cores to test for
cores = [1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128]  

# Number of 'jobs' to use when testing. Should be larger than nbr of cores
I_default_lot_sizes = [1, 3, 10, 20, 50, 100, 500, 1000, 2000]

# Number of steps, determines how heavy test is
I_steps_add = [1]
I_steps_barrierContinuousMonteCarlo = [1, 2, 3, 5, 20]
I_steps_finiteDifferenceModel = [1, 2, 3, 4, 5, 10, 30, 60, 90]

# Config values for GC tests
gc_n_arrays = 1000
gc_array_size = 100
