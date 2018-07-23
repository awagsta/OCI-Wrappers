import oci

class Subnet():
    def __init__(self, subnet_name, compartment_id, availability_domain):
        self.compartment_id = compartment_id
        self.availability_domain = availability_domain
        self.id = None
        self.subnet_name = subnet_name
    
    def create_subnet(self, network_client, cidr_block, vcn):
        created_subnet = network_client.create_subnet(
            oci.core.models.CreateSubnetDetails(compartment_id = self.compartment_id,
            availability_domain = self.availability_domain, display_name = self.subnet_name,
            vcn_id = vcn.id, cidr_block = cidr_block)
            )
        
        subnet_creation_response = oci.wait_until(network_client, 
        network_client.get_subnet(created_subnet.data.id),
        'lifecycle_State', 'AVAILABLE')

        self.id = subnet_creation_response.data.id
        
        print("Subnet Created with name {0} and id: {1}".format(self.subnet_name, self.id))
        return

    def delete_subnet(self, network_client):
        network_client.delete_subnet(self.id)

        oci.wait_until(network_client, network_client.get_subnet(self.id),
        'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted {0} subnet with id: {1}'.format(self.subnet_name, self.id))
        self.subnet_name = None
        self.id = None
        return