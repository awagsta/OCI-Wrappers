import oci

class Vcn():
    def __init__(self, config):
        self.config = config
    
    def create_vcn(self, cidr_block, vcn_name, compartment_id):
        virtual_network = oci.core.VirtualNetworkClient(self.config)

        created_vcn = virtual_network.create_vcn(oci.core.models.CreateVcnDetails(
        cidr_block=cidr_block, display_name=vcn_name, compartment_id=compartment_id), 
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

        oci.wait_until(virtual_network, virtual_network.get_vcn(created_vcn.id),
        'lifecycle_state', 'AVAILABLE')
    
        print("VCN Created with id {}".format(created_vcn.id))
        return



