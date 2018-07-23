import oci
class Gateway():
    def __init__(self, gateway_name, compartment_id):
        self.compartment_id = compartment_id
        self.id = None
        self.gateway_name = gateway_name

    def create_gateway(self, network_client, vcn):
        created_gateway = network_client.create_internet_gateway(
            oci.core.models.CreateInternetGatewayDetails(
                display_name = self.gateway_name, 
                compartment_id = self.compartment_id,
                is_enabled = True, vcn_id = vcn.id
            )
        )

        gateway_creation_response = oci.wait_until(network_client,
        network_client.get_internet_gateway(created_gateway.data.id), 'lifecycle_state',
        'AVAILABLE')

        self.id = gateway_creation_response.data.id

        print("Internet Gateway Created with name {0} and Id {1}".format(self.gateway_name, self.id))
        return
    
    def delete_gateway(self, network_client):
        network_client.delete_internet_gateway(self.id)
        oci.wait_until(network_client, network_client.get_internet_gateway(self.id),
            'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted Internet Gateway {0} with id: {1}'.format(self.gateway_name, self.id))
        self.gateway_name = None
        self.id = None
        return