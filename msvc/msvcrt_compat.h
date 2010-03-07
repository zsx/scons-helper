/* This file is used when compiling the source with MSVC .net or newer, but
 * linking against os supplied msvcr.dll instead of the compiler supplied one.
 */
#ifndef _MSVCRT_COMPAT_H_
#define _MSVCRT_COMPAT_H_

#ifdef _MSC_VER
#define fstat(a,b) _fstat(a,b)
#if defined(__MSVCRT_VERSION__) && __MSVCRT_VERSION__ < 0x0700
#ifdef _fstat /* will be defined to _fstat64i32 */
#undef _fstat
#endif

#ifdef _wstat /* _fstat64i32 */
#undef _wstat
#endif

#ifdef _wfindfirst
#undef _wfindfirst
#endif

#ifdef _wfindnext
#undef _wfindnext
#endif

#endif
#endif /* _MSC_VER */
#endif /* _MSVCRT_COMPAT_H_ */
