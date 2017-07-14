{
  # ======================================================================
  #  Includes
  # ======================================================================
  'includes': [
    'common_target_defaults.gypi',
  ], # include

  # ======================================================================
  #  Targets
  # ======================================================================
  'targets': [
    # ----------------------------------------------------------------------
    #  Executable Targets
    # ----------------------------------------------------------------------
    {
      'target_name': 'hello',
      'type': 'executable',
      'dependencies': [
        'shared_library_target',
        'static_library_target',
      ], # dependencies
      'sources': [
        'source/hello.cpp',
      ], # sources
    }, # hello

    # ----------------------------------------------------------------------
    #  Library Targets
    # ----------------------------------------------------------------------
    {
      'target_name': 'shared_library_target',
      'type': 'shared_library',
      'variables': {
        'public_include_dirs': [
          'source',
        ], # public_include_dirs
      }, # variables
      'all_dependent_settings': {
        'include_dirs': [
          '<@(public_include_dirs)',
        ], # include_dirs
      }, # direct_dependent_settings
      'defines': [
        'USE_SHARED_IMPLEMENTATION=1',
      ], # defines
      'include_dirs': [
        '<@(public_include_dirs)',
      ], # include_dirs
      'sources': [
        'source/shared.cpp',
      ], # sources
      'conditions': [
        ['OS=="mac"', {
          # 'mac_bundle': 1,  # If set, this creates a framework.
          # 'mac_bundle_resources': [
          # ], # mac_bundle_resources
          'xcode_settings': {
            'DYLIB_INSTALL_NAME_BASE': '@rpath',
          }, # xcode_settings
        } ], # OS="mac"
        ['OS=="win"', {
        } ], # OS="win"
      ], # conditions
    }, # shared_library_target

    # ----------------------------------------------------------------------

    {
      'target_name': 'static_library_target',
      'type': 'static_library',
      'variables': {
        'public_include_dirs': [
          'source',
        ], # public_include_dirs
      }, # variables
      'all_dependent_settings': {
        'include_dirs': [
          '<@(public_include_dirs)',
        ], # include_dirs
      }, # direct_dependent_settings
      'include_dirs': [
        '<@(public_include_dirs)',
      ], # include_dirs
      'sources': [
        'source/static.cpp',
      ], # sources
    }, # static_library_target
  ], # targets
}
