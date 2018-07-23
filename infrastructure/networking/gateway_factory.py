import oci
class Gateway_Factory():
    def __init__(self, compartment_id):
        self.compartment_id = compartment_id

    def create_gateway(self, network_client, vcn, gateway_name):
        created_gateway = network_client.create_internet_gateway(
            oci.core.models.CreateInternetGatewayDetails(
                display_name = gateway_name, 
                compartment_id = self.compartment_id,
                is_enabled = True, vcn_id = vcn.id
            )
        )

        gateway_creation_response = oci.wait_until(network_client,
        network_client.get_internet_gateway(created_gateway.data.id), 'lifecycle_state',
        'AVAILABLE')

        print("Internet Gateway Created with name {0} and Id {1}".format(gateway_name, gateway_creation_response.data.id))
        # Returns the gateway object
        return gateway_creation_response.data
    
    def delete_gateway(self, network_client, gateway):
        network_client.delete_internet_gateway(gateway.id)
        oci.wait_until(network_client, network_client.get_internet_gateway(gateway.id),
            'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted Internet Gateway with id: {}'.format(gateway.id))
        return