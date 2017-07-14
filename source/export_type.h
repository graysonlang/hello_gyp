#pragma once
#ifndef EXPORT_TYPE_H_
#define EXPORT_TYPE_H_

#ifdef WIN32
  #ifdef USE_SHARED_IMPLEMENTATION
    #define EXPORT_TYPE __declspec(dllexport)
  #else // USE_SHARED_IMPLEMENTATION
    #define EXPORT_TYPE __declspec(dllimport)
  #endif // USE_SHARED_IMPLEMENTATION
#else // WIN32
  #ifdef USE_SHARED_IMPLEMENTATION
    #define EXPORT_TYPE __attribute__((visibility("default")))
  #else // USE_SHARED_IMPLEMENTATION
    #define EXPORT_TYPE __attribute__ ((visibility ("hidden")))
  #endif // USE_SHARED_IMPLEMENTATION
#endif // WIN32

#endif // EXPORT_TYPE_H_
