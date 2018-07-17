import oci

class Subnet():
    def __init__(self, config, compartment_id, availability_domain):
        self.compartment_id = compartment_id
        self.availability_domain = availability_domain
        self.config = config
        self.subnet_id = None
    
    def create_subnet(self, cidr_block, vcn_id, subnet_name):
        virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_subnet = virtual_network.create_subnet(
            oci.core.models.CreateSubnetDetails(compartment_id = self.compartment_id,
            availability_domain = self.availability_domain, display_name = subnet_name,
            vcn_id = vcn_id, cidr_block = cidr_block)
            )
        
        subnet_creation_response = oci.wait_until(virtual_network, virtual_network.get_subnet(created_subnet.data.id),
        'lifecycle_State', 'AVAILABLE')

        self.subnet_id = subnet_creation_response.data.id
        
        print("Subnet Created with name {0} and id: {1}".format(subnet_name, self.subnet_id))
        return