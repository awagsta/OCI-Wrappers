import oci

class Vcn():
    def __init__(self, config, compartment_id):
        self.compartment_id = compartment_id
        self.config = config
        self.vcn_id = None
    
    def create_vcn(self, cidr_block, vcn_name):
        virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_vcn = virtual_network.create_vcn(oci.core.models.CreateVcnDetails(
        cidr_block=cidr_block, display_name=vcn_name, compartment_id=self.compartment_id), 
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

        vcn_creation_response = oci.wait_until(virtual_network, virtual_network.get_vcn(created_vcn.data.id),
        'lifecycle_state', 'AVAILABLE')

        self.vcn_id = vcn_creation_response.data.id
    
        print("VCN Created with name {0} and id {1}".format(vcn_name, self.vcn_id))
        return



