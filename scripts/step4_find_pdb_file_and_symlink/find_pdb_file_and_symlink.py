# For each Uniprot ID in given ACC list file,  reads the pdb list file that have list of corresponding PDB IDs.
# Finds the PDB file on hal cluster's share/pdb directory and create symlinks of PDB files to output/step4
# 
# run this from model_systems directory in the cluster
# usage: python scripts/step4_find_pdb_file_and_symlink/find_pdb_file_and_symlink.py your_ACC_list_file
#        python scripts/step4_find_pdb_file_and_symlink/find_pdb_file_and_symlink.py uni_acc_str_2.txt
#        python scripts/step4_find_pdb_file_and_symlink/find_pdb_file_and_symlink.py uni_acc_str_of_validation_set.txt
#                                                   this is output of step1
#                                              file must be located in input/step4

from sys import argv
import os
import gzip

#unpacking
script, filename = argv

#define input and output path
input_path ="input/step4"
pdb_path = "/cbio/jclab/share"
output_path = "output/step4"

#read the file (uni_acc_str_of_validation_set) that has the names of the xml files generated by STEP1
ACCs_file = open(os.path.join(input_path, filename))
ACCs_str= ACCs_file.read()
ACCs_list = ACCs_str.split()  #convert string to a list

for acc in ACCs_list:
    pdb_from_acc_file = open(os.path.join(input_path, "pdb_list_str_of_" + acc + ".txt"))
    pdb_list_str = pdb_from_acc_file.read()
    pdb_id_list = pdb_list_str.split()  # convert read file contents to list of pdbs
    pdb_from_acc_file.close()

    for pdb_id in pdb_id_list:
        # slice pdb id string and make it lowercase to match the directory names
        pdb_dir_name = pdb_id[1:3].lower()
        print pdb_dir_name

        #Find the pdb file and create symlink in output/step4 folder with name acc_pdbid.pdb.gz
        pdb_file_path = pdb_path + '/pdb/' + pdb_dir_name
        src = os.path.join(pdb_file_path, "pdb"+ pdb_id.lower() + ".ent.gz")
        dst = os.path.join(output_path, acc + "_" + pdb_id + '.pdb.gz')
        os.symlink(src, dst)
