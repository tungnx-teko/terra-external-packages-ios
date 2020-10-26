import json
import os
import sys

class Pod(object):
    def __init__(self, id, name, version, dependencies):
        self.id = id
        self.name = name
        self.version = version
        self.dependencies = dependencies
    
class Dependency(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

def decode_dependency(object):
    return Dependency(object['name'], object['version'] if 'version' in object else None)

def decode_pod(object):
    dependencies = map(lambda dict: decode_dependency(dict), object['dependencies'])
    return Pod(object['id'], object['name'], object['version'], dependencies)

def parse_json(file_path, release_tag_name):
    print("parse_json: " + release_tag_name)
    with open(file_path) as f:
        data = json.load(f)
    pod = decode_pod(data)
    generate_podspec(pod, release_tag_name)

def generate_podspec(pod, release_tag_name):
    print("generate_podspec: " + release_tag_name)
    podspec_string  = 'Pod::Spec.new do |s|\n'
    podspec_string  = fill_pod_data(podspec_string, pod, release_tag_name)
    podspec_string  = fill_author_data(podspec_string, pod)
    podspec_string  = fill_dependencies_data(podspec_string, pod)
    podspec_string += 'end'
    save(podspec_string, pod)

def fill_pod_data(podspec_string, pod, release_tag_name):
    print("fill_pod_data: " + release_tag_name)
    podspec_string += "\ts.name                   = '" + pod.id + "'\n"
    podspec_string += "\ts.version                = '" + pod.version + "'\n"
    podspec_string += "\ts.summary                = '" + pod.name + "'\n"
    podspec_string += "\ts.homepage               = 'https://github.com/teko-vn/Specs-ios.git'\n"
    podspec_string += "\ts.license                = { :type => 'MIT', :file => 'LICENSE' }\n"
    podspec_string += "\n"
    podspec_string += "\ts.source                 = { :http => 'https://github.com/tungnx-teko/terra-external-packages-ios/releases/download/" + release_tag_name + "/" + pod.name + ".zip' }\n"
    podspec_string += "\ts.vendored_frameworks    = '" + pod.name + "'\n"
    podspec_string += "\ts.public_header_files    = '" + pod.name + "/Headers/*.h'\n"
    podspec_string += "\ts.source_files           = '" + pod.name + "/Headers/*.{h,m,swift}'\n"

    podspec_string += "\n"

    return podspec_string

def fill_author_data(podspec_string, pod):
    podspec_string += "\ts.author                 = {'Mobile Lab' => 'mobile.lab@teko.vn'}\n"
    podspec_string += "\n"

    return podspec_string

def fill_dependencies_data(podspec_string, pod):
    for dependency in pod.dependencies:
        if dependency.version == '' or dependency.version is None:
            podspec_string += "\ts.dependency '" + dependency.name + "'\n"
        else:
            podspec_string += "\ts.dependency '" + dependency.name + "', '" + dependency.version + "'\n"
    return podspec_string

def save(podspec_string, pod):
    folder_path = 'Specs/' + pod.id + '/' + pod.version
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    podspec_file = open(folder_path + '/' + pod.id + ".podspec", "w")
    podspec_file.write(podspec_string)
    podspec_file.close()

if __name__ == "__main__":
    release_tag_name = sys.argv[1]
    print(release_tag_name)
    for file in os.listdir('./build/outputs'):
        if file.endswith(".json"):
            parse_json(os.path.join('./build/outputs', file), release_tag_name)
            