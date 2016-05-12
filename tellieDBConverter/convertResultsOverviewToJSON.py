#Modified from new_channel_calibration
import json
import os
import optparse
import csv
import datetime
import pytz
import copy

def check_dir(dname):
    '''Check if directory exists, create it if it doesn't'''
    direc = os.path.dirname(dname)
    try:
        os.stat(direc)
    except:
        os.mkdir(direc)
        print 'Made directory %s....' % dname
    return dname

def get_int_from_string(string):
    '''Quick function to return integers from string
    '''
    ints = ''.join(x for x in string if x.isdigit())
    return int(ints)

def load_jsons_from_direc(path): 
    '''Load all json files from the passed directory
    :param: Path .json directory.
    :returns: List of dictionary objects representing the .jsons.
    '''
    data_list = []
    files = os.listdir(path)
    for file in files:
        with open('%s/%s' % (path, file), 'r') as json_file:
            json_data = json.load(json_file)
            data_list.append(json_data)
    return data_list

def get_channel_fit_pars(fname):
    '''Read in data from csv file containing all channels results and return a dict
    of the photonVsIPW fit parameters.
    '''
    pars_dict = {}
    results = csv.DictReader(open(fname))
    for idx, line in enumerate(results):
        pars_dict[line['channel']] = ([float(line['ipw_p0']), float(line['ipw_p1']),
                                       float(line['ipw_p2'])])
    return pars_dict

def ratify_original_calibrations(json_list, run_range, pass_no):
    '''Add run number and comment fields to original calibration files.
    these will be saved with an updated pass filed, but not version (as they're 
    essentially the same!)
    '''
    timestamp = datetime.datetime.now(pytz.timezone('US/Eastern')).isoformat()
    for json_file in json_list:
        json_file['channel'] = json_file['index']
        json_file['index'] = ''
        json_file['comment'] = ''
        json_file['run_range'] = run_range
        json_file['pass'] = pass_no
        json_file['timestamp'] = timestamp
        json_file['production'] = True
    return json_list

def update_v1_calbration(fname, json_list, run_range, pass_no):
    '''Replace old photon-IPW lookup table with parameters from fits to the
    calibrated response curves. Need to include fields for both 10Hz and 1kHz
    calibrations.
    '''
    timestamp = datetime.datetime.now(pytz.timezone('US/Eastern')).isoformat()
    pars = get_channel_fit_pars(fname)
    for json_file in json_list:
        # Channel 96 does not exist at site
        if json_file['index'] == 96:
            json_list.remove(json_file)
            continue
        else:
            # Delete old fields and update
            del json_file['photons']
            del json_file['pulse_width']
            json_file['channel'] = json_file['index']
            json_file['index'] = ''
            json_file['comment'] = ''
            json_file['run_range'] = run_range
            json_file['pass'] = pass_no
            json_file['Pars_10Hz'] = [0, 0, 0]
            json_file['Eq_10Hz'] = 'poly2'
            json_file['Pars_1kHz'] = pars['%i' % json_file['channel']]
            json_file['Eq_1kHz'] = 'poly2'
            json_file['version'] = 1
            json_file['timestamp'] = timestamp
            json_file['production'] = True
    return json_list

def create_new_json_files_and_update_old(fname, save_path, oldPath, run_range, pass_no):
    '''Create new json file for a given channel dictionary
    '''
    timestamp = datetime.datetime.now(pytz.timezone('US/Eastern')).isoformat()
    pars = get_channel_fit_pars(fname)
    old_jsons = load_jsons_from_direc(oldPath)
    for key in pars.keys():
            old_json = 0
	    for old_json_it in old_jsons:
               print old_json_it
               if old_json_it["channel"] == int(key):
                 old_json = old_json_it 
            new_json = copy.copy(old_json)
            new_json['channel'] = int(key)
            new_json['index'] = ''
            new_json['comment'] = ''
            new_json['run_range'] = run_range
            new_json['pass'] = pass_no
            new_json['Pars_10Hz'] = [0, 0, 0]
            new_json['Eq_10Hz'] = 'poly2'
            new_json['Pars_1kHz'] = pars[key]
            new_json['Eq_1kHz'] = 'poly2'
            new_json['version'] = 1
            new_json['timestamp'] = timestamp
            new_json['production'] = True
	    print old_json["run_range"]	 
            old_json["run_range"] = [old_json['run_range'][0],run_range[0]]
	    with open('%s/channels/ch%03d.js' % (save_path, int(key)), 'w+') as out_file:
	        out_file.write(json.dumps(new_json))
	        out_file.close()
	    with open('%s/channels_old/ch%03d.js' % (save_path, int(key)), 'w') as out_file:
	        out_file.write(json.dumps(old_json))
	        out_file.close()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='path',
                      default='./default_database/',
                      help='Path to ./default_database/ direc')
    parser.add_option('-c', dest='calibration',
                      help='Path to current calibration data direc')
    parser.add_option('-v', dest='version', default=1,
                      help='Version of the calibration file type to be created')
    parser.add_option('-r', dest='run_valid',
                     help='The run from which the new calibrations become valid')
    parser.add_option('-o', dest='old_dir',
                     help='The directory where the old JSON files are')
    (options,args) = parser.parse_args()
    version = int(options.version)
    pass_no = 0
    create_new_json_files_and_update_old(options.calibration,options.path,options.old_dir,[int(options.run_valid),1e6],pass_no)
