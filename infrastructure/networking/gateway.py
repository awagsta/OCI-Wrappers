import oci
class Gateway():
    def __init__(self, config, compartment_id):
        self.config = config
        self.compartment_id = compartment_id
        self.id = None
        self.gateway_name = None
        self.virtual_network = None

    def create_gateway(self, vcn_id, gateway_name):
        self.gateway_name = gateway_name
        self.virtual_network = oci.core.VirtualNetworkClient(self.config)
        created_gateway = self.virtual_network.create_internet_gateway(
            oci.core.models.CreateInternetGatewayDetails(
                display_name = gateway_name, 
                compartment_id = self.compartment_id,
                is_enabled = True, vcn_id = vcn_id
            )
        )

        gateway_creation_response = oci.wait_until(self.virtual_network,
        self.virtual_network.get_internet_gateway(created_gateway.data.id), 'lifecycle_state',
        'AVAILABLE')

        self.id = gateway_creation_response.data.id

        print("Internet Gateway Created with name {0} and Id {1}".format(gateway_name, self.id))
        return
    
    def delete_gateway(self):
        self.virtual_network.delete_internet_gateway(self.id)
        oci.wait_until(self.virtual_network, self.virtual_network.get_internet_gateway(self.id),
            'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted Internet Gateway {0} with id: {1}'.format(self.gateway_name, self.id))
        self.gateway_name = None
        self.id = None
        return