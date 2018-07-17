import oci

class Subnet():
    def __init__(self, config):
        self.config = config
    
    def create_subnet(self, cidr_block, vcn_id, compartment_id, subnet_name, availability_domain):
        virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_subnet = virtual_network.create_subnet(
            oci.core.models.CreateSubnetDetails(compartment_id = compartment_id,
            availability_domain = availability_domain, display_name = subnet_name,
            vcn_id = vcn_id, cidr_block = cidr_block)
            )
        
        oci.wait_until(virtual_network, virtual_network.get_subnet(created_subnet.data.id),
        'lifecycle_State', 'AVAILABLE')
        
        print("Subnet Created with name {0} and id: {1}".format(subnet_name, created_subnet.data.id))
        return