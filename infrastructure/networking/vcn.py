import oci

class Vcn():
    def __init__(self, config, compartment_id):
        self.compartment_id = compartment_id
        self.config = config
        self.id = None
        self.vcn_name = None
        self.virtual_network = None
        self.gateway = None
        self.subnets = set()
    
    def create_vcn(self, cidr_block, vcn_name):
        self.virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_vcn = self.virtual_network.create_vcn(oci.core.models.CreateVcnDetails(
        cidr_block=cidr_block, display_name=vcn_name, compartment_id=self.compartment_id), 
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

        vcn_creation_response = oci.wait_until(self.virtual_network, self.virtual_network.get_vcn(created_vcn.data.id),
        'lifecycle_state', 'AVAILABLE')

        self.id = vcn_creation_response.data.id
        self.vcn_name = vcn_name
    
        print("VCN Created with name {0} and id {1}".format(vcn_name, self.id))
        return
    
    def register_gateway(self, gateway):
        self.gateway = gateway
        return
    
    def register_subnet(self, subnet):
        self.subnets.add(subnet)
        return
    




