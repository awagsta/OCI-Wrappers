import oci

class Subnet():
    def __init__(self, config, compartment_id, availability_domain):
        self.compartment_id = compartment_id
        self.availability_domain = availability_domain
        self.config = config
        self.id = None
        self.subnet_name = None
        self.virtual_network = None
    
    def create_subnet(self, cidr_block, vcn, subnet_name):
        self.virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_subnet = self.virtual_network.create_subnet(
            oci.core.models.CreateSubnetDetails(compartment_id = self.compartment_id,
            availability_domain = self.availability_domain, display_name = subnet_name,
            vcn_id = vcn.id, cidr_block = cidr_block)
            )
        
        subnet_creation_response = oci.wait_until(self.virtual_network, 
        self.virtual_network.get_subnet(created_subnet.data.id),
        'lifecycle_State', 'AVAILABLE')

        self.id = subnet_creation_response.data.id
        self.subnet_name = subnet_name
        vcn.register_subnet(self)
        
        print("Subnet Created with name {0} and id: {1}".format(subnet_name, self.id))
        return

    def delete_subnet(self):
        self.virtual_network.delete_subnet(self.id)

        oci.wait_until(self.virtual_network, self.virtual_network.get_subnet(self.id),
        'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted {0} subnet with id {1}'.format(self.subnet_name, self.id))
        return