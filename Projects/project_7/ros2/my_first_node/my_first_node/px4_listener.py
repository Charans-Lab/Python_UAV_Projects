import rclpy
from rclpy.node import Node
# from std_msgs.msg import String
from px4_msgs.msg import VehicleLocalPosition
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy




class PX4Listener(Node):
    def __init__(self):                     
        super().__init__('PX4_listener')
        qos_profile = QoSProfile(
                 reliability=ReliabilityPolicy.BEST_EFFORT,
                durability=DurabilityPolicy.TRANSIENT_LOCAL,
                history=HistoryPolicy.KEEP_LAST,
                depth=5
            )
        self.subscription = self.create_subscription(
            VehicleLocalPosition,
            '/fmu/out/vehicle_local_position_v1',
            self.listener_callback,
            qos_profile
        )


    def listener_callback(self, msg):
        self.get_logger().info(
    f'x={msg.x:.2f} y={msg.y:.2f} z={msg.z:.2f} '
    f'vx={msg.vx:.2f} vy={msg.vy:.2f} vz={msg.vz:.2f}'
)
    
def main():
    rclpy.init()
    node = PX4Listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()