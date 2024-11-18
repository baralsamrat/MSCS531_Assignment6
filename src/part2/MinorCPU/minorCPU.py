# gem5 Configuration Script for TLP and NoC Optimization
from m5.objects import *
from m5.util import addToPath
import os

# Function to create a CPU configuration
def create_cpu(cpu_type="MinorCPU", num_cores=4):
    cpus = [cpu_type() for _ in range(num_cores)]
    for i, cpu in enumerate(cpus):
        cpu.cpu_id = i
    return cpus

# Function to configure a system with memory and NoC
def configure_system(num_cores=4, mem_size="4GB", cache=True, noC_config=None):
    system = System(
        clk_domain=SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain()),
        mem_mode="timing",  # Use timing mode for detailed simulation
        mem_ranges=[AddrRange(mem_size)]
    )
    # Add CPU
    system.cpu = create_cpu(num_cores=num_cores)
    # Add memory
    system.membus = SystemXBar()
    system.system_port = system.membus.cpu_side_ports
    system.mem_ctrl = DDR3_1600_8x8(range=system.mem_ranges[0], port=system.membus.mem_side_ports)
    # Add Cache if required
    if cache:
        system.l2cache = L2Cache(size="2MB", assoc=8)
        for cpu in system.cpu:
            cpu.icache = L1Cache(size="32kB")
            cpu.dcache = L1Cache(size="32kB")
            cpu.icache.connectCPU(cpu)
            cpu.dcache.connectCPU(cpu)
            system.l2cache.connectCPUSide(cpu.dcache)
            system.l2cache.connectMemSide(system.membus)
    # Add NoC configuration if required
    if noC_config:
        system.noc = configure_noc(noC_config)
    return system

# Function to configure NoC
def configure_noc(config):
    noc = NoC()
    noc.router_list = [Router(id=i) for i in range(config['num_routers'])]
    noc.links = [Link(width=config['link_width']) for _ in range(config['num_links'])]
    # Connect routers as per config
    for link in noc.links:
        link.src_port = noc.router_list[link.src_id].out_ports[link.src_port_id]
        link.dest_port = noc.router_list[link.dest_id].in_ports[link.dest_port_id]
    return noc

# Simulation Script
if __name__ == "__m5_main__":
    # Configure the system
    num_cores = 8
    memory_size = "16GB"
    noc_config = {
        'num_routers': 4,
        'num_links': 8,
        'link_width': 64
    }
    system = configure_system(num_cores=num_cores, mem_size=memory_size, cache=True, noC_config=noc_config)

    # Run the simulation
    root = Root(full_system=False, system=system)
    m5.instantiate()
    print("Starting simulation...")
    exit_event = m5.simulate()
    print(f"Simulation ended at tick {m5.curTick()} due to {exit_event.getCause()}")
