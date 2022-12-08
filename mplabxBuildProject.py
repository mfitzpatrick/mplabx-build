#!/usr/bin/python
import glob2 as glob # TODO: can we just use glob in python 3?
import os
import subprocess
import sys
import xml.etree.ElementTree as xml

MPLABX_BASE_DIR = "/opt/microchip/mplabx/"
MPLABX_SCRIPT_DIR = "/opt/microchip/mplabx/%s/mplab_platform/bin/prjMakefilesGenerator.sh"
PROJECT_SUFFIX = "nbproject/project.xml"
CONFIG_SUFFIX = "nbproject/configurations.xml"

def getMPLABXVersion():
  mplabx_version = os.listdir(MPLABX_BASE_DIR)[0]
  print("Detected MPLABX version: %s" % mplabx_version)
  return mplabx_version

def verifyScript(mplabx_version):
  build_script_location = MPLABX_SCRIPT_DIR % mplabx_version
  if os.path.exists(build_script_location) and os.path.isfile(build_script_location):
    print("    Got build script at location: %s" % build_script_location)
  else:
    print("    FATAL ERROR: Build script not found at location: %s" % build_script_location)
    return False
  return True

def getDependencies(project_folder):
  tree_root = xml.parse(project_folder + PROJECT_SUFFIX).getroot()
  ns = {
    'ns1': tree_root.tag.split('}')[0].strip('{'),
  }
  ns['ns2'] = tree_root.find('ns1:configuration', namespaces=ns)[0].tag.split('}')[0].strip('{')

  return [(x.text[4:] + "/") for x in list(tree_root.find('ns1:configuration', namespaces=ns).find('ns2:data', namespaces=ns).find('ns2:make-dep-projects', namespaces=ns).findall('ns2:make-dep-project', namespaces=ns))]

def getConfigurations(project_folder):
  tree_root = xml.parse(project_folder + CONFIG_SUFFIX).getroot()
  return [x.attrib["name"] for x in list(tree_root.find('confs').findall('conf'))]

def findMakefile(project_folder, config):
  print("    Searching for: " + "%s**/Makefile-%s.mk" % (project_folder, config))
  try:
    return glob.glob("%s**/Makefile-%s.mk" % (project_folder, config), recursive=True)[0]
  except IndexError:
    print("        ERROR: Could not find makefile for config %s." % config)
    return None

def generateMakefile(mplabx_version, project_folder):
  process = subprocess.Popen([MPLABX_SCRIPT_DIR % mplabx_version, project_folder])
  process.communicate()

def buildMakefile(project_folder, makefile):
  # Relocalize makefile location.
  result = makefile.find('CAT2')
  extra_cmd="MP_EXTRA_CC_PRE+="
  if result != -1:
    extra_cmd = "MP_EXTRA_CC_PRE+=-D CAT2"
  makefile_local = makefile.replace(project_folder, "./")
  nproc = subprocess.check_output(["nproc"])
  cmds = ["make", "-j", str(int(nproc)), "-f", makefile_local, extra_cmd, "VERBOSE=1", "SUBPROJECTS=", ".build-conf"]
  print("  "+" ".join(cmds)) # Print the command.
  process = subprocess.Popen(cmds, cwd=project_folder)
  process.communicate()
  rc = process.returncode
  return rc

def buildProject(mplabx_version, project_folder):
  exit_code = 0
  if False: # Dependencies are built automatically with MPLAB X v4.20 and greater
    dependencies = getDependencies(project_folder)
    if len(dependencies) > 0:
      print("Building dependencies for project %s..." % project_folder)
      for dependency in dependencies:
        # Build dependencies first!
        print("    Dependency found: %s" % dependency)
        buildProject(mplabx_version, dependency)
      print("Built dependencies for project %s." % project_folder)
  print("")
  print("Building project: %s" % project_folder)
  print("    Generating makefiles...")
  generateMakefile(mplabx_version, project_folder)
  print("    Finished generating makefile.")
  configurations = getConfigurations(project_folder)
  print("    Got configurations: %s" % ",".join(configurations))
  for config in configurations:
    print("    Building config %s..." % config)
    print("        Finding makefile for config...")
    mk = findMakefile(project_folder, config)
    if mk is not None:
      print("        Found makefile %s for config %s" % (mk, config))
      print("        Making config %s..." % (config))
      return_code = buildMakefile(project_folder, mk)
      if return_code == 0: # 0 indicates success.
        print("    Build complete.")
      else:
        print("    Build failed (%d)." % return_code)
        exit_code += 1
    else:
      print("    Build skipped (makefile error).")
      exit_code += 1
      continue
  print("    All configurations built.")
  print("Done building project.")
  return exit_code

def main():
  if len(sys.argv) > 1:
    mplabx_version = getMPLABXVersion()
    if not verifyScript(mplabx_version):
      return
    # Build an individual project, as specified in the command line
    sys.exit(buildProject(mplabx_version, sys.argv[1]))
  else:
    # No project specified.
    print("Format: %s [directory]" % sys.argv[0])
    sys.exit(1)

if __name__ == '__main__':
  main()

