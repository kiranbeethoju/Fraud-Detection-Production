import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import os
import sys
from preprocess import get_data
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

if not (os.path.isdir("data/preprocessed/tf_records_dir")):
    os.mkdir("data/preprocessed/tf_records_dir")
    os.mkdir("data/preprocessed/tf_records_dir/tf_records_train")
    os.mkdir("data/preprocessed/tf_records_dir/tf_records_test")
    os.mkdir("data/preprocessed/tf_records_dir/tf_records_validation_set_1")
    os.mkdir("data/preprocessed/tf_records_dir/tf_records_validation_set_2")
def float_feature(value):
    ''' Helper function that wraps float features into the tf.train.Feature class 
    
    @param value: the feature or label of type float, that we want to convert 
    '''
    
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def int64_feature(value):
    ''' Helper function that wraps integer features into the tf.train.Feature class 
    
    @param value: the feature or label of type integer, that we want to convert 
    '''
    
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def write_tf_records_file(x, y, tf_writer):
    '''This function writes a feature-label pair to a TF-Records file
    
    @param x: the feature
    @param y: the label
    @param tf_writer: the TensorFlow Records writer instance that writes the files
    '''
    
    # Convert numpy array to list, because tf.train.Feature accepts only lists
    x=x.tolist()
    #Features we want to convert to the binary format
    feature_dict={ 'features': float_feature(x),
                   'labels': float_feature(y),                         
                 }

    #Another wrapper class
    features_wrapper=tf.train.Features(feature=feature_dict) 
    # Aaaand another wrapper class lol
    example = tf.train.Example(features=features_wrapper)

    # Finally we make the files binary and write them to TF-Records file
    tf_writer.write(example.SerializeToString())



def run(tf_records_dir, data):
    '''Main function for the writing process
    
    @param tf_records_dir: path where the files should be written into
    @param data: the dataset that contains the features and labels
    '''
    
    # If the directory is not present, create one
    
      
    #Get the features and labels from the dataset
    features=data[0]
    labels=data[1]
    # Number of instances in the dataset
    n_data_instances=features.shape[0]
    # Initialize a counter for the data instances
    data_instance_counter=0
    
    # Specify the number of samples that will be saved in one TF-Records file
    samples_per_file=500
    
    # Number of all TF-Records files in the end
    n_tf_records_files=round(n_data_instances/samples_per_file)
    # Counter for the TF-Records files
    tf_records_counter=0
    
   
    #Iterate over the number of total TF-Records files
    while tf_records_counter < n_tf_records_files:

        # Give each file an unique name(full-path)
        tfrecords_file_name='%s_%i.tfrecord' % (tf_records_dir, tf_records_counter)

        #Initialize a writer for the files
        with tf.python_io.TFRecordWriter(tfrecords_file_name) as tf_writer:
            
            sample_counter=0

            #Iterate over all data samples and number of samples per TF-Records file
            while data_instance_counter<n_data_instances and sample_counter<samples_per_file:
                
                sys.stdout.write('\r>> Converting data instance %d/%d' % (data_instance_counter+1, n_data_instances))
                sys.stdout.flush()
 
                # Extract a feature instance
                x=features[data_instance_counter]
                # Extract a label instance
                y=labels[data_instance_counter]
                
                # Write feature and label to a TF-Records file
                write_tf_records_file(x,y,tf_writer)

                # Increase the counters
                data_instance_counter+=1
                sample_counter+=1
                
            tf_records_counter+=1
            
    print('\nFinished converting the dataset!')
    
    
if __name__ == "__main__":
    
    # Build the paths for the training, test, and validation TF-Records files
    tf_records_root_dir='data/preprocessed/tf_records_dir/'
    train_dir = os.path.join(tf_records_root_dir, 'tf_records_train')
    test_dir = os.path.join(tf_records_root_dir, 'tf_records_test')
    validation_dir_set_1 = os.path.join(tf_records_root_dir, 'tf_records_validation_set_1')
    validation_dir_set_2 = os.path.join(tf_records_root_dir, 'tf_records_validation_set_2')
    
    # Get the preprocessed data 
    train_data, test_data ,validation_set_1,validation_set_2=get_data()    
    #Write for each dataset TF-Records file
    run(train_dir, train_data)
    run(test_dir, test_data)
    run(validation_dir_set_1, validation_set_1)
    run(validation_dir_set_2, validation_set_2)