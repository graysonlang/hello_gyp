{
  # ======================================================================
  #  Variables
  # ======================================================================
  'variables': {
    # Evaluate the current working directory.
    'CWD': '',
    'conditions': [
      ['OS=="mac"', {'CWD': '<!(pwd)'}],
      ['OS=="win"', {'CWD': '<!(cd)'}],
    ], # conditions

    # Note: In order to prevent gyp's pathname relativization badly mangling runpath's pseudo-path syntax,
    # variable names need to not contain: _dir(s), _file(s), or _path(s).
    'mac_ld_runpath_search': [
      '@executable_path/Frameworks',
      '@executable_path/../Frameworks',
      '@loader_path',
    ], # mac_ld_runpath_search

    'node_root_dir%': '', # The '%' suffix sets the default value. (https://gyp.gsrc.io/docs/InputFormatReference.md#Providing-Default-Values-for-Variables)
  }, # variables

  # GYP workaround to reduce "Validate Project Settings" warnings in Xcode.
  # These configuration settings get placed into project.pbxproj's top level XCBuildConfiguration block for debug configs.
  'configurations': {
    'Debug': {
      'xcode_settings' :  {
        'CLANG_WARN__DUPLICATE_METHOD_MATCH': 'YES',
        'CLANG_WARN_BOOL_CONVERSION': 'YES',
        'CLANG_WARN_CONSTANT_CONVERSION': 'YES',
        'CLANG_WARN_EMPTY_BODY': 'YES',
        'CLANG_WARN_ENUM_CONVERSION': 'YES',
        'CLANG_WARN_INFINITE_RECURSION': 'YES',
        'CLANG_WARN_INT_CONVERSION': 'YES',
        'CLANG_WARN_SUSPICIOUS_MOVE': 'YES',
        'CLANG_WARN_UNREACHABLE_CODE': 'YES',
        'ENABLE_STRICT_OBJC_MSGSEND': 'YES',
        'ENABLE_TESTABILITY': 'YES',
        'GCC_NO_COMMON_BLOCKS': 'YES',
        'GCC_WARN_64_TO_32_BIT_CONVERSION': 'YES',
        'GCC_WARN_ABOUT_RETURN_TYPE': 'YES',
        'GCC_WARN_UNDECLARED_SELECTOR': 'YES',
        'GCC_WARN_UNINITIALIZED_AUTOS': 'YES',
        'GCC_WARN_UNUSED_FUNCTION': 'YES',
        'GCC_WARN_UNUSED_VARIABLE': 'YES',
        'ONLY_ACTIVE_ARCH': 'YES',
      }, # xcode_settings
    }, # Debug
  }, # configurations

  # ======================================================================
  #  Target Defaults
  # ======================================================================
  'target_defaults': {
    'default_configuration': 'Release',

    'defines': [
      # 'CATCH_CONFIG_COUNTER', # Tells "catch.hpp" to use the preprocesser macro __COUNTER__ which avoids macro naming collisions.
      '_USE_MATH_DEFINES',
    ], # defines

    'configurations': {
      'Debug': {
        'defines': [
          'DEBUG',
          '_DEBUG',
        ], # defines
      }, # Debug
      'Release': {
        'defines': [
          'NDEBUG',
        ], # defines
      } # Release
    }, # configurations

    'target_conditions': [
      # This block will remove the node related libraries and include paths that get injected by node-gyp.
      ['_type=="executable" or _type=="shared_library" or _type=="static_library"', {
        # Check if node_root_dir is defined, if so, we're in node-gyp.
        'conditions': [
          ['node_root_dir!=""', {
            # Remove node related includes.
            'include_dirs!':[
              '<(node_root_dir)/include/node',
              '<(node_root_dir)/src',
              '<(node_root_dir)/deps/uv/include',
              '<(node_root_dir)/deps/v8/include',
            ], # include_dirs!
            'conditions': [
              ['OS=="win"', {
                "libraries!" : [
                  '-l"<(node_root_dir)/$(ConfigurationName)/<(node_lib_file)"',
                ], # libraries!
              } ], # OS=="win"
            ], # conditions
          } ] # node_root_dir!=""
        ], # conditions
      } ], # _type=="executable" or _type=="shared_library" or _type=="static_library"

      # Enable Xcode "Skip install" option for static libs so it doesn't mess up .ipa archive generation.
      ['OS=="mac" and _type=="static_library"', {
        'xcode_settings' :  {
          'SKIP_INSTALL': 'YES',
        }, # xcode_settings
      } ], # OS=="mac" and _type=="static_library"

      ['OS=="mac" and (_type=="executable" or _type=="loadable_module" or _type=="shared_library")', {
        'xcode_settings': {
          'OTHER_LDFLAGS': [
            '-stdlib=libc++', # "libc++" C++ Standard Library
            '-lobjc', # objective-c runtime (for catch.hpp)
            # '-fsanitize=safe-stack', # http://clang.llvm.org/docs/SafeStack.html
          ], # OTHER_LDFLAGS
          'LD_RUNPATH_SEARCH_PATHS': [
            '<@(mac_ld_runpath_search)',
          ], # LD_RUNPATH_SEARCH_PATHS
        }, # xcode_settings
      } ], # _type=="executable" or _type=="loadable_module" or _type=="shared_library"
    ], # target_conditions

    'conditions': [
      ['OS=="mac"', {
        'link_settings': {
          'libraries': [
            '$(SDKROOT)/System/Library/Frameworks/ApplicationServices.framework',
            '$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
          ], # libraries
        }, # link_settings

        'xcode_settings': {
          # 'ARCHS': ['x86_64'], # '$(ARCHS_STANDARD_64_BIT)'
          'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x', # -std=c++0x
          'CLANG_CXX_LIBRARY': 'libc++', # -stdlib=libc++
          'COMBINE_HIDPI_IMAGES': 'YES',
          # 'GCC_ENABLE_CPP_EXCEPTIONS': 'YES', # -fexceptions
          # 'GCC_ENABLE_CPP_RTTI': 'YES', # -frtti
          'GCC_INLINES_ARE_PRIVATE_EXTERN': 'NO', # -fvisibility-inlines-hidden
          'GCC_SYMBOLS_PRIVATE_EXTERN': 'NO', # -fvisibility=hidden
          # 'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
          # 'IPHONEOS_DEPLOYMENT_TARGET': '10.3',
          # 'MACOSX_DEPLOYMENT_TARGET': '10.8', # '10.9'
          'OTHER_CPLUSPLUSFLAGS' : [
            '-x',
            'objective-c++',
            # '-fsanitize=safe-stack', # http://clang.llvm.org/docs/SafeStack.html
            # '-march=native',
            # '-mno-avx2',
            # '-mno-avx',
          ], # OTHER_CPLUSPLUSFLAGS
          'WARNING_CFLAGS': [
            '-Wno-narrowing',
            '-Wno-unknown-pragmas',
            '-Wno-unused-value',
          ], # WARNING_CFLAGS
          'WARNING_CFLAGS!': [
            '-Wall',
          ], # WARNING_CFLAGS!
        }, # xcode_settings

        'configurations': {
          'Debug': {
            'xcode_settings': {
              'GCC_GENERATE_DEBUGGING_SYMBOLS': 'YES',
              'GCC_OPTIMIZATION_LEVEL': '0',
            }, # xcode_settings
          }, # Debug

          'Release': {
            'xcode_settings': {
              'DEAD_CODE_STRIPPING': 'YES',
              'GCC_GENERATE_DEBUGGING_SYMBOLS': 'NO',
              'GCC_INLINES_ARE_PRIVATE_EXTERN': 'YES',
              'GCC_OPTIMIZATION_LEVEL': '3',
            }, # xcode_settings
          }, # Release
        }, # configurations
      } ], # OS=="mac"

      ['OS=="win"', {
        'msvs_disabled_warnings': [
          4068, # unknown pragmas (https://msdn.microsoft.com/en-us/library/w099eeey.aspx)
          4099, # missing PDB files (https://msdn.microsoft.com/en-us/library/b7whw3f3.aspx)
        ], # msvs_disabled_warnings
        'defines': [
          'WIN32',
          'WIN64',
          '_HAS_EXCEPTIONS=1',
          'UNICODE',
          '_UNICODE',
          'NOMINMAX',
          'CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1',
          'CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES_MEMORY=1',
        ], # defines
        'CharacterSet': 'Unicode',
        'msvs_configuration_platform': 'x64',
        'msvs_settings': {
          'VCCLCompilerTool': {
            'AdditionalOptions': [
              '/bigobj', # increase number of sections in object files (https://msdn.microsoft.com/en-us/library/ms173499.aspx)
            ], # AdditionalOptions
            'DebugInformationFormat': '3', # programDatabase (/Zi) (Note: a value of 4 (i.e. editAndContiue /ZI) is only supported when building for 32 bit x86)
            'ExceptionHandling': '1', # /EHs (https://msdn.microsoft.com/en-us/library/1deeycx5.aspx)
            'MultiProcessorCompilation': 'true', # /MP
          }, # VCCLCompilerTool
          'VCLinkerTool': {
            'GenerateDebugInformation': 'true', # /DEBUG
          }, # VCLinkerTool
        }, # msvs_settings
        'win_delay_load_hook': 'false',

        'configurations': {
          'Debug': {
            'defines': [
              '_ITERATOR_DEBUG_LEVEL=2', # Supersedes and combines _SECURE_SCL and _HAS_ITERATOR_DEBUGGING (https://msdn.microsoft.com/en-us/library/hh697468.aspx)
            ], # defines
            'msvs_settings': {
              'VCCLCompilerTool': {
                'Optimization': '0', # optimizeDisabled (/Od)
                'RuntimeLibrary': 1, # static debug (/MTd)
                'RuntimeTypeInfo': 'true', # /GR (https://msdn.microsoft.com/en-us/library/2kzt1wy3.aspx)
              }, # VCCLCompilerTool
              'VCLinkerTool': {
                'LinkIncremental': '2', # /INCREMENTAL
              }, # VCLinkerTool
            } # msvs_settings
          }, # Debug
          'Release': {
            'defines': [
              '_ITERATOR_DEBUG_LEVEL=0', # Supersedes and combines _SECURE_SCL and _HAS_ITERATOR_DEBUGGING (https://msdn.microsoft.com/en-us/library/hh697468.aspx)
              '_HAS_EXCEPTIONS=1',
            ], # defines
            'msvs_settings': {
              'VCCLCompilerTool': {
                'FavorSizeOrSpeed': '1', # speed (/Ot)
                'Optimization': '2', # speed (/02)
                'RuntimeLibrary': 0, # static release (/MT)
                'RuntimeTypeInfo': 'true', # /GR (https://msdn.microsoft.com/en-us/library/2kzt1wy3.aspx)
                'BufferSecurityCheck': 'true', # /GS (https://msdn.microsoft.com/en-us/library/8dbf701c.aspx)
              }, # VCCLCompilerTool

              'VCLinkerTool': {
                'DataExecutionPrevention': '1', # /NSCOMPAT (https://msdn.microsoft.com/en-us/library/ms235442.aspx)
                'RandomizedBaseAddress': '1', # /DYNAMICBASE (https://msdn.microsoft.com/en-us/library/bb384887.aspx)
                #  Only available on x86 targets (i.e. not x64 or arm)
                # 'ImageHasSafeExceptionHandlers': '1', # /SAFESEH (https://msdn.microsoft.com/en-us/library/9a89h429.aspx)
              }, # VCLinkerTool
            }, # msvs_settings
          }, # Release
        }, # configurations
      } ], # OS=="win"
    ], # conditions
  }, # target_defaults
}
