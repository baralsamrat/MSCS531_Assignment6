from m5.objects import *

# Define FloatSimdFU configurations
def create_float_simd_fu(op_lat, issue_lat):
    return FunctionalUnit(
        opLat=op_lat,
        issueLat=issue_lat,
        count=4  # Number of functional units
    )

# Customizing MinorDefaultFUPool
class CustomMinorDefaultFUPool(MinorDefaultFUPool):
    def __init__(self):
        super().__init__()
        # Add various FloatSimdFU configurations
        configurations = [
            (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)
        ]
        for op_lat, issue_lat in configurations:
            self.funcUnits.append(create_float_simd_fu(op_lat, issue_lat))

# Instantiate the pool
fu_pool = CustomMinorDefaultFUPool()
print(f"Configured FloatSimdFU with variations: {fu_pool}")
