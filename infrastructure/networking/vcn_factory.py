import oci

class Vcn_Factory():
    def __init__(self, compartment_id):
        self.compartment_id = compartment_id
    
    def create_vcn(self, network_client, cidr_block, vcn_name):

        created_vcn = network_client.create_vcn(oci.core.models.CreateVcnDetails(
        cidr_block=cidr_block, display_name=vcn_name, compartment_id=self.compartment_id), 
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

        vcn_creation_response = oci.wait_until(network_client, network_client.get_vcn(created_vcn.data.id),
        'lifecycle_state', 'AVAILABLE')
    
        print("VCN Created with name {0} and id: {1}".format(vcn_name, vcn_creation_response.data.id))
        
        #returns the vcn response object
        return vcn_creation_response.data
    
    def delete_vcn(self, network_client, vcn):
        network_client.delete_vcn(vcn.id)
        oci.wait_until( network_client,  network_client.get_vcn(vcn.id),
        'lifecycle_state', 'TERMINATED', succeed_on_not_found=True)

        print('Deleted vcn with id: {}'.format(vcn.id))
        return

    




