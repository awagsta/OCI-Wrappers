import oci

class Subnet_Factory():
    def __init__(self, compartment_id, availability_domain):
        self.compartment_id = compartment_id
        self.availability_domain = availability_domain
    
    def create_subnet(self, network_client, cidr_block, vcn, subnet_name):
        created_subnet = network_client.create_subnet(
            oci.core.models.CreateSubnetDetails(compartment_id = self.compartment_id,
            availability_domain = self.availability_domain, display_name = subnet_name,
            vcn_id = vcn.id, cidr_block = cidr_block)
            )
        
        subnet_creation_response = oci.wait_until(network_client, 
        network_client.get_subnet(created_subnet.data.id),
        'lifecycle_State', 'AVAILABLE')
        
        print("Subnet Created with name {0} and id: {1}".format(subnet_name, subnet_creation_response.data.id))

        #returns the subnet object
        return subnet_creation_response.data

    def delete_subnet(self, network_client, subnet):
        network_client.delete_subnet(subnet.id)

        oci.wait_until(network_client, network_client.get_subnet(subnet.id),
        'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted subnet with id: {}'.format(subnet.id))
        return