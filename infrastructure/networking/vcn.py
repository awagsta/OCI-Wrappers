import oci

class Vcn():
    def __init__(self, compartment_id, vcn_name):
        self.compartment_id = compartment_id
        self.id = None
        self.vcn_name = vcn_name
    
    def create_vcn(self, network_client, cidr_block):

        created_vcn = network_client.create_vcn(oci.core.models.CreateVcnDetails(
        cidr_block=cidr_block, display_name=self.vcn_name, compartment_id=self.compartment_id), 
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

        vcn_creation_response = oci.wait_until(network_client, network_client.get_vcn(created_vcn.data.id),
        'lifecycle_state', 'AVAILABLE')

        self.id = vcn_creation_response.data.id
    
        print("VCN Created with name {0} and id {1}".format(self.vcn_name, self.id))
        return
    
    def delete_vcn(self, network_client):
        network_client.delete_vcn(self.id)
        oci.wait_until( network_client,  network_client.get_vcn(self.id),
        'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted vcn {0} with id: {1}'.format(self.vcn_name, self.id))
        self.vcn_name = None
        self.id = None
        return

    




