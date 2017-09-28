import os
import pwd
import datetime
import json
import pickle
from collections import OrderedDict

def get_user_and_section():
    ''' Load class list from pickle for safety do not hold txt version '''
    with open('class_list.pickle', 'rb') as in_file:
        class_list = pickle.load(in_file)

    ''' Get user name from current user '''
    user_name = pwd.getpwuid(os.getuid())[0] 
    
    ''' If user not in class exit else return relevant info '''
    if user_name not in class_list:
        print('You are not in this class')
        exit()
    else:
        return (user_name, class_list[user_name])

def confirm_user_time(section):
    ''' Load in section times from pickle '''
    with open('section_times.pickle', 'rb') as in_file:
        section_times = pickle.load(in_file)

    ''' Grab our assigned section info '''
    assigned_times = section_times[section]

    ''' Grab current time / date information '''
    current = datetime.datetime.now()
    day = convert_to_weekday_letter(current.weekday())
    hour = current.hour
    
    ''' If not in correct day kick out of script '''
    if assigned_times['day'] != day:
        print('You are trying to check out outside of your assigned section')
        exit()

    ''' If we are a pm recitation adjust time '''
    if assigned_times['pm']:
        hour -= 12

    ''' If user not in correct time kick out of script '''
    if not (hour >= int(assigned_times['start']) and hour <= int(assigned_times['end'])):
        print('You are trying to check out outside of your assigned section')
        exit()

    ''' If user is in correct time and we are less than 30 minutes in class
        return quiz '''
    if hour == int(assigned_times['start']) and current.minute <= 30:
        return 'quiz'
    else:
        return 'lab'

def parse_config():
    config = None
    with open('config.json') as config_file:
        ''' We are going to use an orderedDict which allows us to enforce
            that the sections will be at the bottom and we can break on the
            key word.  Also it allows us to take the section list and rely on
            indexes to assign repos '''
        config = json.load(config_file, object_pairs_hook=OrderedDict)
    
    ''' Grab host '''
    if 'host' in config:
        host = config['host']
    else:
        print('Please specify host in config file')
        exit()

    ''' Grab base repo path '''
    if 'base' in config:
        base = config['base']
    else:
        print('Please specify the base repo path in the config file')
        exit()

    if not base.startswith('/') or not base.endswith('/'):
        print('Please wrap base in / for easier formatting')
        exit()
    
    ''' Assure sections are in config '''
    if 'sections' in config:
        sections = config['sections']
    else:
        print('Please specify the sections in the config file')
        exit()
        
    repo_list = []
    for key in config:
        ''' Already grabbed host and base '''
        if key == 'host' or key == 'base':
            continue
        ''' We already grabbed sections and since we are ordered we can break here '''
        if key == 'sections':
            break

        ''' Assume anything else is a repo specification '''
        repo_list.append((key, config[key]))

        
    return(host, base, repo_list, sections)

def get_assigned_repos(repo_list, sections, assigned_section):
    repos = []
    for i in range(len(repo_list)):
        ''' A little confusing:
            repo_list has tuples of name : list of repos
            we grab:
                -repo_list[i][1] to get the list of repos
            Then we grab from that list the index which is
                -sections[assigned_section] to get repo index list
            Then we use the index i since we are ordered to get the
            proper repo '''
        
        repos.append(repo_list[i][1][sections[assigned_section][i]])
    
    return repos

def get_repo_index(repo_list, to_grab):

    ''' Repo List is a tup of name to repos '''
    for i in range(len(repo_list)):
        if repo_list[i][0] == to_grab:
            return i

    return -1

def git_checkout_repos(host, base, user, repos, repo_to_grab, single_repo=False):
    
    if single_repo:
        os.system('git clone ssh://{0}@{1}{2}{3} ~/'.format(user, host, base, repos[0]))
        return

    os.system('git clone ssh://{0}@{1}{2}{3} ~/'.format(user, host, base, repos[repo_to_grab]))

def import_repo_into_eclipse(repos, repo_to_grab, single_repo=False):
    
    if single_repo:
        os.system('eclipse -nosplash -application ' +                    \
                  'org.eclipse.cdt.managedbuilder.core.headlessbuild ' + \
                  '-importAll {0}'.format(repos[0]))

    os.system('eclipse -nosplash -application ' +                     \
              'org.eclipse.cdt.managedbuilder.core.headlessbuild ' +  \
              '-importAll {0}'.format(repos[repo_to_grab]))

    
def convert_to_weekday_letter(day):
    ''' Converting from python day rep to letter '''
    if day == 0:
        day = 'M'
    elif day == 1:
        day = 'T'
    elif day == 2:
        day = 'W'
    elif day == 3:
        day = 'Th'
    elif day == 4:
        day = 'F'
    elif day == 5:
        day = 'S'
    elif day == 6:
        day = 'Su'

    return day

def main():

    res_tup = get_user_and_section()

    user = res_tup[0]
    assigned_section = res_tup[1]

    repo_to_grab = confirm_user_time(assigned_section)
    base_info = parse_config()

    ''' Eval our base_info tup '''
    host = base_info[0]
    base_path = base_info[1]
    repo_list = base_info[2]
    sections = base_info[3]

    repos = get_assigned_repos(repo_list, sections, assigned_section)
    repo_to_grab = get_repo_index(repo_list, repo_to_grab)

    if repo_to_grab == -1 and len(repos) > 1:
        print('Issue in config file, repo name not found')
        exit()
    
    ''' Single repo handles the case where there may not be a quiz or lab, we just checkout
        and ignore the repo_to_grab based on our user time '''
    git_checkout_repos(host,         \
                       base_path,    \
                       user,         \
                       repos,        \
                       repo_to_grab, \
                       single_repo = False if len(repos) > 1 else True)
    
    import_repo_into_eclipse(repos,        \
                             repo_to_grab, \
                             single_repo = False if len(repos) > 1 else True)

if __name__ == '__main__':
    main()

