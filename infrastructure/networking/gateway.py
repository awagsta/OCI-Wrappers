import oci
class Gateway():
    def __init__(self, config, compartment_id):
        self.config = config
        self.compartment_id = compartment_id
        self.gateway_id = None

    def create_gateway(self, vcn_id, gateway_name):
        virtual_network = oci.core.VirtualNetworkClient(self.config)
        created_gateway = virtual_network.create_internet_gateway(
            oci.core.models.CreateInternetGatewayDetails(
                display_name = gateway_name, 
                compartment_id = self.compartment_id,
                is_enabled = True, vcn_id = vcn_id
            )
        )

        gateway_creation_response = oci.wait_until(virtual_network,
        virtual_network.get_internet_gateway(created_gateway.data.id), 'lifecycle_state',
        'AVAILABLE')

        self.gateway_id = gateway_creation_response.data.id
        
        print("Internet Gateway Created with name {0} and Id {1}".format(gateway_name, self.gateway_id))
        return