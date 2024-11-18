from m5.objects import *
from gem5.simulate import Simulation

# Define a system with multi-core MinorCPU
def create_system(num_cores, fu_pool):
    system = System(
        clk_domain=SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain()),
        mem_mode="timing",
        mem_ranges=[AddrRange("1GB")]
    )
    # Configure CPUs
    system.cpu = [MinorCPU(fuPool=fu_pool) for _ in range(num_cores)]
    # Add memory controller and interconnect
    system.membus = SystemXBar()
    system.system_port = system.membus.cpu_side_ports
    system.mem_ctrl = DDR3_1600_8x8(range=system.mem_ranges[0], port=system.membus.mem_side_ports)
    return system

if __name__ == "__main__":
    num_cores = 4
    system = create_system(num_cores, CustomMinorDefaultFUPool())
    root = Root(full_system=False, system=system)
    Simulation.run(root, "configs/example/daxpy_kernel")
